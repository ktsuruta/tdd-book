import random, os
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
env.key_filename='~/.ssh/LightsailDefaultPrivateKey-ap-northeast-1.pem'
REPO_URL = 'https://github.com/ktsuruta/tdd-book.git'
if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
        env.use_ssh_config = True
def deploy():
    site_folder = '/home/' + env.user + '/sites/production'
    print(site_folder + "will be used")
    run('mkdir -p ' + site_folder)
    print('2')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run('git clone ' + REPO_URL + ' .')
    current_commit = local("git log -n 1 --format=%H", capture=True)

    #run('git reset --hard ' + current_commit)

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run('python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    insert_line = 'SITENAME=production'
    append('.env', insert_line)
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = 'm349v2o235v'
        insert_line = 'DJANGO_SECRET_KEY='+new_secret
        append('.env',insert_line)

def _update_static_files():
    run('./virtualenv/bin/python3.6 manage.py collectstatic --noinput')

def _update_database():
    run('./virtualenv/bin/python3.6 manage.py migrate --noinput')

