import os

from django.conf import settings
from django.template import Context, Engine

from fabric.api import abort, cd, lcd, local, prompt, put, run, sudo
from fabric.contrib.console import confirm


settings.configure()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# From http://stackoverflow.com/a/11958481/3762084
with lcd(BASE_DIR):
    current_branch = local(
        'git rev-parse --symbolic-full-name --abbrev-ref HEAD',
        capture=True)
if current_branch != 'master':
    if not confirm(
            'Would you like to deploy the {0} branch?'.format(current_branch),
            default=False):

        abort("Aborting deployment of non-master branch.")


ACTIVATE_ENV = '. env/bin/activate'
DB_NAME = 'djangodb'
DB_PASSWORD = prompt("Enter database password:")
DB_USER = 'django'
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


def configure_db():
    with open('templates/createdb.sql.template') as f:
        template = Engine().from_string(f.read())

    context = Context({
        'db_name': DB_NAME,
        'db_password': DB_PASSWORD,
        'db_user': DB_USER,
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
    with cd(REMOTE_PROJECT_DIR):
        sudo('cp nginx-config /etc/nginx/sites-available/chmvh-website')

    sudo('ln -fs /etc/nginx/sites-available/chmvh-website '
         '/etc/nginx/sites-enabled')

    # Remove default nginx site if it exists
    sudo('rm -f /etc/nginx/sites-available/default')

    sudo('nginx -t')
    sudo('systemctl restart nginx')


def copy_settings():
    """Copy appropriate local settings."""
    with open('templates/local_settings.py.template') as f:
        template = Engine().from_string(f.read())

    context = Context({
        'db_name': DB_NAME,
        'db_password': DB_PASSWORD,
        'db_user': DB_USER,
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
    prepare_remote()
    update_remote()
    configure_db()
    create_env()
    copy_settings()
    configure_gunicorn()
    configure_nginx()
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

        run('git checkout {0} && git pull'.format(current_branch))


def _in_env(command):
    """Run a command in the remote virtualenv."""
    with cd(REMOTE_PROJECT_DIR):
        run('{} && {}'.format(ACTIVATE_ENV, command))
