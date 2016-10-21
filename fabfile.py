from fabric.api import cd, run

ACTIVATE_ENV = '. env/bin/activate'
REMOTE_PROJECT_DIR = '/home/chathan/chmvh-website'


def deploy():
    update_remote()
    generate_static()
    restart_services()


def generate_static():
    """Generate static files on the remote server."""
    with cd(REMOTE_PROJECT_DIR):
        _in_env('chmvh_website/manage.py compilescss')
        _in_env('chmvh_website/manage.py collectstatic -i *.scss --noinput')


def restart_services():
    """Restart services on remote server."""
    run('sudo systemctl restart gunicorn nginx')


def update_remote():
    """Pull code onto remote machine."""
    with cd(REMOTE_PROJECT_DIR):
        run('git pull')


def _in_env(command):
    """Run a command in the remote virtualenv."""
    with cd(REMOTE_PROJECT_DIR):
        run('{} && {}'.format(ACTIVATE_ENV, command))
