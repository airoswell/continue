import os
import sys


PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

ACTIVATE_THIS = PROJECT_DIR + '/env-continue/bin/activate_this.py'
activate_env=os.path.expanduser(ACTIVATE_THIS)
execfile(activate_env, dict(__file__=activate_env))


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()