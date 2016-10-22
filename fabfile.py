import os

from django.conf import settings as django_settings
from django.template import Context, Engine

from fabric.api import (
    abort, cd, env, lcd, local, prompt, put, run, sudo)
from fabric.contrib.console import confirm

import yaml


django_settings.configure()


BASE_PATH = os.path.dirname(os.path.abspath(__file__))


# From http://stackoverflow.com/a/11958481/3762084
with lcd(BASE_PATH):
    current_branch = local(
        'git rev-parse --symbolic-full-name --abbrev-ref HEAD',
        capture=True)
if current_branch != 'master':
    if not confirm(
            'Would you like to deploy the {0} branch?'.format(current_branch),
            default=False):
        if not confirm(
                'Would you like to deploy the master branch instead?'):
            abort("Aborting deployment of non-master branch.")
        else:
            current_branch = 'master'


ACTIVATE_ENV = '. /home/chathan/chmvh-website/env/bin/activate'
CREDENTIAL_MAP = {
    'db_name': 'database name',
    'db_password': 'database password',
    'db_user': 'database user',
    'sudo_password': 'sudo password',
}
REMOTE_PROJECT_DIR = '/home/chathan/chmvh-website'


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


def configure_db():
    with open('templates/createdb.sql.template') as f:
        template = Engine().from_string(f.read())

    context = Context({
        'db_name': Credentials.get('db_name'),
        'db_password': Credentials.get('db_password'),
        'db_user': Credentials.get('db_user'),
    })

    output = template.render(context)

    out_name = '/tmp/chmvh-website/createdb.sql'
    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    with open(out_name, 'w') as f:
        f.write(output)

    # Upload SQL script to remote
    put(out_name, '/tmp')

    # Run script on remote
    sudo('sudo -u postgres psql -f /tmp/createdb.sql')


def configure_gunicorn():
    """Set up gunicorn service."""
    with cd(REMOTE_PROJECT_DIR):
        sudo('cp gunicorn.service /etc/systemd/system')

    sudo('systemctl start gunicorn && sudo systemctl daemon-reload')
    sudo('systemctl enable gunicorn')


def configure_nginx():
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


def configure_ssl():
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
    put(
        'templates/ssl-params.conf',
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


def copy_settings():
    """Copy appropriate local settings."""
    with open('templates/local_settings.py.template') as f:
        template = Engine().from_string(f.read())

    context = Context({
        'db_name': Credentials.get('db_name'),
        'db_password': Credentials.get('db_password'),
        'db_user': Credentials.get('db_user'),
    })

    output = template.render(context)

    out_name = '/tmp/chmvh-website/local_settings.py'
    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    with open(out_name, 'w') as f:
        f.write(output)

    with cd(REMOTE_PROJECT_DIR):
        put(out_name, 'chmvh_website/chmvh_website')


def create_env():
    """Create a virtualenv if it doesn't exist"""
    with cd(REMOTE_PROJECT_DIR):
        run('test -d env || virtualenv --python=python3 env')
        _in_env('pip install -r requirements.txt')


def deploy():
    if not env.sudo_password:
        env.sudo_password = Credentials.get('sudo_password')

    prepare_remote()
    update_remote()
    configure_db()
    create_env()
    copy_settings()
    configure_gunicorn()
    configure_nginx()
    configure_ssl()
    generate_static()
    restart_services()


def generate_static():
    """Generate static files on the remote server."""
    with cd(REMOTE_PROJECT_DIR):
        _in_env('chmvh_website/manage.py migrate')
        _in_env('chmvh_website/manage.py compilescss')
        _in_env('chmvh_website/manage.py collectstatic -i *.scss --noinput')


def prepare_remote():
    """Install required packages."""
    sudo('apt-get update -y && sudo apt-get install -y {}'.format(
        ' '.join(required_packages)))

    run('pip3 install virtualenv')


def restart_services():
    """Restart services on remote server."""
    sudo('systemctl restart gunicorn nginx')


def update_remote():
    """Pull code onto remote machine."""
    with cd('/home/chathan'):
        run('if ! test -d chmvh-website; '
            'then git clone https://github.com/cdriehuys/chmvh-website; fi')

    with cd(REMOTE_PROJECT_DIR):
        run('git pull && git checkout {0}'.format(current_branch))


def _in_env(command):
    """Run a command in the remote virtualenv."""
    with cd(REMOTE_PROJECT_DIR):
        run('{} && {}'.format(ACTIVATE_ENV, command))


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
