import os

from django.conf import settings as django_settings
from django.template import Context, Engine

from fabric.api import (
    cd, env, local, prefix, prompt, put, run, sudo)
from fabric.contrib.console import confirm

import yaml


django_settings.configure()


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CREDENTIAL_MAP = {
    'db_name': 'database name',
    'db_password': 'database password',
    'db_user': 'database user',
    'secret_key': 'Django secret key',
    'sendgrid_password': 'SendGrid password',
    'sendgrid_user': 'SendGrid username',
    'sudo_password': 'sudo password',
}
REMOTE_PROJECT_DIR = '/home/chathan/chmvh-website'
REPOSITORY_URL = 'https://github.com/cdriehuys/chmvh-website'


required_packages = (
    'git',
    'letsencrypt',
    'libjpeg-dev',
    'libpq-dev',
    'postgresql', 'postgresql-contrib',
    'nginx',
    'python3-dev', 'python3-pip',
    'zlib1g-dev',
)


class Credentials:
    FILE_PATH = os.path.join(BASE_PATH, 'secure-config.yml')

    credentials = None

    @classmethod
    def get(cls, name):
        if cls.credentials is None:
            cls.load_credentials()

        host_credentials = cls.credentials.get(env.host, {})

        existing = host_credentials.get(name, None)

        # If that credential is already stored, return it
        if existing is not None:
            return existing

        # Credential doesn't exist, so prompt for it and then save it
        message = 'Enter {0} for {1}:'.format(CREDENTIAL_MAP[name], env.host)
        host_credentials[name] = prompt(message)

        cls.credentials[env.host] = host_credentials
        cls._save_credentials()

        return host_credentials[name]

    @classmethod
    def load_credentials(cls):
        if os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'r') as f:
                cls.credentials = yaml.load(f)
        else:
            cls.credentials = {}

    @classmethod
    def _save_credentials(cls):
        with open(cls.FILE_PATH, 'w') as f:
            yaml.dump(cls.credentials, f)


def prepare_local():
    """Prepare local machine for deployment"""
    # From http://stackoverflow.com/a/11958481/3762084
    env.current_branch = local(
        'git rev-parse --symbolic-full-name --abbrev-ref HEAD',
        capture=True)

    if env.current_branch != 'master':
        if not confirm("You are trying to deploy from the '{0}' branch. "
                       "Is this what you want?".format(env.current_branch),
                       default=False):
            env.current_branch = prompt(
                "Enter branch to deploy from:",
                default='master')


def remote_setup():
    """Set up the remote machine"""
    sudo('apt-get update -y')

    # Install required packages
    sudo('apt-get install -y {0}'.format(' '.join(required_packages)))

    # Set up the database
    _configure_database()

    # Set up webserver
    _configure_gunicorn()
    _configure_nginx()
    _configure_ssl()


def update_remote():
    """Update the code on the remote machine."""
    with cd('/home/chathan'):
        run('if ! test -d chmvh-website; then git clone {0}; fi'.format(
            REPOSITORY_URL))

    with cd(REMOTE_PROJECT_DIR):
        run('git pull && git checkout {0} && git pull'.format(
            env.current_branch))

    _configure_env()

    # Clear out static files
    with cd(REMOTE_PROJECT_DIR):
        run('rm -rf chmvh_websites/staticfiles')

    # Run migrations and collect static files
    with cd(REMOTE_PROJECT_DIR), prefix('source env/bin/activate'):
        run('chmvh_website/manage.py migrate')
        run('chmvh_website/manage.py compilescss')
        run('chmvh_website/manage.py collectstatic -i *.scss --noinput')


def post_update():
    """Runs after the remote machine has updated its codebase"""
    # Upload local settings
    context = Context({
        'db_name': Credentials.get('db_name'),
        'db_password': Credentials.get('db_password'),
        'db_user': Credentials.get('db_user'),
        'domain_name': env.host,
        'secret_key': Credentials.get('secret_key'),
        'sendgrid_password': Credentials.get('sendgrid_password'),
        'sendgrid_user': Credentials.get('sendgrid_user'),
    })
    _upload_template(
        'templates/local_settings.py.template',
        '{}/chmvh_website/chmvh_website/local_settings.py'.format(
            REMOTE_PROJECT_DIR),
        context)

    # Restart gunicorn to reflect app changes
    sudo('systemctl restart gunicorn')


def deploy():
    if not env.sudo_password:
        env.sudo_password = Credentials.get('sudo_password')

    prepare_local()
    remote_setup()
    update_remote()
    post_update()


def _configure_database():
    """Create the database for the application."""
    context = {
        'db_name': Credentials.get('db_name'),
        'db_password': Credentials.get('db_password'),
        'db_user': Credentials.get('db_user'),
    }
    _upload_template(
        'templates/createdb.sql.template',
        '/tmp/createdb.sql',
        context)
    sudo('sudo -u postgres psql -f /tmp/createdb.sql')


def _configure_env():
    """Configure the virtualenv for the application"""
    with cd(REMOTE_PROJECT_DIR):
        run('if ! test -d env; then virtualenv --python=python3 env; fi')

        with prefix('source env/bin/activate'):
            run('pip install -r requirements.txt')


def _configure_gunicorn():
    """Set up gunicorn service."""
    _upload_template(
        'templates/gunicorn.service',
        '/etc/systemd/system/gunicorn.service',
        use_sudo=True)

    sudo('systemctl daemon-reload')
    sudo('systemctl start gunicorn')
    sudo('systemctl enable gunicorn')


def _configure_nginx():
    """Set up nginx."""
    context = {
        'domain_name': env.host,
    }
    _upload_template(
        'templates/chmvh-website-basic.conf.template',
        '/etc/nginx/sites-available/chmvh-website',
        context,
        use_sudo=True)

    sudo('ln -fs /etc/nginx/sites-available/chmvh-website '
         '/etc/nginx/sites-enabled')

    # Remove default nginx site if it exists
    sudo('rm -f /etc/nginx/sites-available/default '
         '/etc/nginx/sites-enabled/default')

    # Test basic config
    sudo('nginx -t')
    sudo('systemctl restart nginx')


def _configure_ssl():
    """Configure SSL with letsencrypt"""
    configured = sudo(('if sudo test -d /etc/letsencrypt/live/{0}; then echo '
                       'exists; fi').format(env.host))

    if configured == 'exists':
        _renew_ssl()
    else:
        _set_up_ssl()

    # Configure nginx to use the certificate
    context = {
        'domain_name': env.host,
    }

    _upload_template(
        'templates/chmvh-website.conf.template',
        '/etc/nginx/sites-available/chmvh-website',
        context)
    _upload_template(
        'templates/ssl-domain.conf.template',
        '/etc/nginx/snippets/ssl-{0}.conf'.format(env.host),
        context,
        use_sudo=True)
    put('templates/ssl-params.conf',
        '/etc/nginx/snippets/ssl-params.conf',
        use_sudo=True)

    # Test nginx and restart
    sudo('nginx -t')
    sudo('systemctl restart nginx')

    # Set up cron job for certificate renewal
    with cd('/tmp'):
        run('echo "30 2 * * 1 /usr/bin/letsencrypt renew >> '
            '/var/log/le-renew.log" > newcron')
        run('echo "35 2 * * 1 /bin/systemctl reload nginx" >> newcron')
        run('crontab newcron')
        run('rm newcron')


def _renew_ssl():
    sudo('letsencrypt renew')


def _set_up_ssl():
    # Create web-root if doesn't exist
    sudo('if ! test -d /var/www/chmvh-website/html; then mkdir -p '
         '/var/www/chmvh-website/html && chown -R www-data:www-data '
         '/var/www/chmvh-website; fi')

    create_cert_cmd = ' '.join((
        'letsencrypt certonly',
        '-a webroot',
        '--agree-tos',
        '-d {0}'.format(env.host),
        '--email cdriehuys@gmail.com',
        '--webroot-path=/var/www/chmvh-website/html',
    ))

    sudo(create_cert_cmd)

    # Generate Strong Diffie-Hellman Group
    sudo('openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048')


def _upload_template(template_path, remote_dest, context={}, out_path=None,
                     **kwargs):
    """Process and upload a template to the remote machine."""
    with open(template_path) as f:
        template = Engine().from_string(f.read())

    output = template.render(Context(context))

    out_file = os.path.basename(template_path).replace('.template', '')
    out_path = out_path or os.path.join('/', 'tmp', 'chmvh-website', out_file)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        f.write(output)

    put(out_path, remote_dest, **kwargs)

    os.remove(out_path)
