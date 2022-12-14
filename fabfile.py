from __future__ import with_statement
from fabric.api import local, settings, run, cd, lcd, prefix, env, abort
from fabric.contrib.console import confirm
from fabric.contrib import project
from contextlib import contextmanager
from os import path

# Assumptions
# - virtual environment name identical to app name MYAPP
# - this file (fabfile.py) is located next to manage.py
# - production settings can be found in myapp_project.settings_prod
# - gunicorn conf files are in etc/gunicorn.prod.py and etc/gunicorn.dev.py
# - pop requirements are in requirements.txt (local and server)

# Build local directories like this: path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(__file__)

USER = 'rmoor'
HOST = 'mdrexl.webfactional.com'

# App name, same as the name of the virtualenvironment both, in development and production area
MYAPP = 'guwen'

# Project package name "myapp_project"
DJANGO_BASE_DIR = 'django_base'
env.hosts = ['{}@{}'.format(USER, HOST)]

# Where the static files get collected locally
# has to be identical to STATIC_ROOT in settings.py for collectstatic to function locally
LOCAL_STATIC_ROOT = path.join(BASE_DIR, 'static_root/')

# production area file paths
REMOTE_STATIC_ROOT = '/home/{}/webapps/{}_nginx/static'.format(USER, MYAPP)
PROD_DIR = '/home/{}/webapps/{}_django'.format(USER, MYAPP)

# production settings file
SETTINGS_NAME = 'settings_prod'

# supervisor app name
SUPERVISOR_NAME = MYAPP

# workaround because local invokes /bin/sh on my local machine, thus neither local nor prefix works with local
def mylocal(command):
  return local('/bin/bash -l -c "source /usr/local/bin/virtualenvwrapper.sh && workon {} && {}"'.format(MYAPP, command))

# only for remote
@contextmanager
def venv():
  with prefix('workon {}'.format(MYAPP)):
    yield

@contextmanager
def remote_dir():
  with cd(PROD_DIR), venv():
    yield

@contextmanager
def local_dir():
  with lcd(BASE_DIR):
    yield


# Deploy static files
def deploy_static_files():
  with local_dir():
    mylocal('python manage.py collectstatic --noinput')
    project.rsync_project(
      remote_dir=REMOTE_STATIC_ROOT,
      local_dir=LOCAL_STATIC_ROOT,
      delete=True,
      )

# Deploying
def prepare():
  with local_dir():
    with settings(warn_only=True):
      result = mylocal('python manage.py schemamigration {} --auto'.format(MYAPP))
    if result.failed and not confirm('Continue anyway?'):
      abort('Aborting.')
    mylocal('python manage.py migrate {}'.format(MYAPP))
    mylocal('pip freeze > requirements.txt')
    mylocal('git add --all')
    with settings(warn_only=True):
      mylocal('git commit -a')
    mylocal('git push origin')

def deploy(branch='master'):
  with remote_dir():
    # get new branches
    run('git pull')
    run('git checkout {}'.format(branch))
    # update selected branch    
    run('git pull origin {}'.format(branch))
    run('pip install -r requirements.txt -q')
    if confirm('Applying migrations of branch {} with settings {}. Is that correct? ("No" to skip migration)'.format(branch, SETTINGS_NAME)):
      run('python manage.py migrate --settings={}.{}'.format(DJANGO_BASE_DIR, SETTINGS_NAME))
  deploy_static_files()
  run('supervisorctl restart {}'.format(SUPERVISOR_NAME))

def clearsessions():
  with remote_dir():
    run('python manage.py clearsessions --settings={}.{}'.format(DJANGO_BASE_DIR, SETTINGS_NAME))

def local_update():
  with local_dir():
    with settings(warn_only=True):
      mylocal('python manage.py schemamigration {} --auto'.format(MYAPP))
    mylocal('python manage.py migrate')
    if path.exists('gunicorn.pid'):
      mylocal('kill -HUP `cat gunicorn.pid`')
    else:
      mylocal('gunicorn {}.wsgi -c etc/gunicorn.dev.py -D -p gunicorn.pid'.format(DJANGO_BASE_DIR))