import os
import sys
from continue.settings import PROJECT_DIR

APP_PATH = os.path.join(PROJECT_DIR, 'app',).replace('\\', '/'),

sys.path.append(APP_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()