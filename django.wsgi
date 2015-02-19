import os
import sys

sys.path.append('/var/www/continue/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'continue.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
