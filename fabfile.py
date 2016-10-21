from fabric.api import cd, run

ACTIVATE_ENV = '. env/bin/activate'
REMOTE_PROJECT_DIR = '/home/chathan/chmvh-website'


required_packages = (
    'git',
    'libjpeg-dev',
    'libpq-dev',
    'postgresql', 'postgresql-contrib',
    'nginx',
    'python3-dev', 'python3-pip',
    'zlib1g-dev',
)


def configure_gunicorn():
    """Set up gunicorn service."""
    with cd(REMOTE_PROJECT_DIR):
        run('sudo mv gunicorn.service /etc/systemd/system')

    run('sudo systemctl start gunicorn')
    run('sudo systemctl enable gunicorn')


def configure_nginx():
    """Set up nginx."""
    with cd(REMOTE_PROJECT_DIR):
        run('sudo mv nginx-config /etc/nginx/sites-available/chmvh-website')

    run('sudo ln -s /etc/nginx/sites-available/chmvh-website '
        '/etc/nginx/sites-enabled')
    run('sudo nginx -t')
    run('sudo systemctl restart nginx')


def create_env():
    """Create a virtualenv if it doesn't exist"""
    with cd(REMOTE_PROJECT_DIR):
        run('test -d env || virtualenv --python=python3 env')
        _in_env('pip install -r requirements.txt')


def deploy():
    prepare_remote()
    update_remote()
    create_env()
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
    run('sudo apt-get update -y && sudo apt-get install -y {}'.format(
        ' '.join(required_packages)))

    run('pip3 install virtualenv')


def restart_services():
    """Restart services on remote server."""
    run('sudo systemctl restart gunicorn nginx')


def update_remote():
    """Pull code onto remote machine."""
    with cd('/home/chathan'):
        run('if test -d chmvh-website; then cd chmvh-website && git pull; '
            'else git clone https://github.com/cdriehuys/chmvh-website; fi')

    with cd(REMOTE_PROJECT_DIR):
        run('git checkout auto-deploy && git pull')


def _in_env(command):
    """Run a command in the remote virtualenv."""
    with cd(REMOTE_PROJECT_DIR):
        run('{} && {}'.format(ACTIVATE_ENV, command))
