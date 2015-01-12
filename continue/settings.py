"""
Django settings for continue project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# ====================================================================
# ======================== Path settings =============================
# Build paths inside the project like this: os.path.join(PROJECT_DIR, ...)
import os

# /Users/Lelouch/projects/continue/continue
SETTINGS_DIR = os.path.dirname(__file__)
# /Users/Lelouch/projects/continue
PROJECT_DIR = os.path.dirname(SETTINGS_DIR)
# Set up absolute locations of the template files
TEMPLATE_DIRS = {
    os.path.join(
        PROJECT_DIR,
        'app/templates',
    ).replace('\\', '/'),
    os.path.join(
        PROJECT_DIR,
        'app/templates/pages',
    ).replace('\\', '/'),
    os.path.join(
        PROJECT_DIR,
        'app/templates/pages/components',
    ).replace('\\', '/'),
    os.path.join(
        PROJECT_DIR,
        '',
    ).replace('\\', '/'),
}
print(TEMPLATE_DIRS)
STATIC_ROOT = os.path.join(PROJECT_DIR, 'app/static/')
# STATIC_ROOT = os.path.join(PROJECT_DIR, 'public/static/')
STATIC_PRECOMPILER_OUTPUT_DIR = "../static/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ais*fe=ql^do8g3z=qao_549f*q*w$n91)(l$a91f5s@qjn7se'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ROOT_URLCONF = 'continue.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# This is the URL, not the absolute path in the machine
STATIC_URL = '/static/'

# ====================== Path settings END ===========================

import socket
if socket.gethostname().startswith('FBI-SVL-666.home'):
    LIVEHOST = False
else:
    LIVEHOST = True



# =====================
# Django core settings
# ====================
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'haystack',
    # ================================
    # ==== Django Rest Framework ====#
    'rest_framework',
    "static_precompiler",
    # =====================================
    # ==== django-allauth components ==== #
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.weibo',
    'postman',      # mailing app
    'markdown_deux',
    'compressor',
    'app',          # the app name
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

WSGI_APPLICATION = 'continue.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if LIVEHOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_continue',
            'USER': 'airoswell',
            'PASSWORD': '299792458',
            'HOST': '104.237.144.150',
            'PORT': '3306',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
APPEND_SLASH = True


# =====================
# Django REST framework
# =====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # ======== uncomment if want to disable browsable API view
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )
}


# ==============
# Django-allauth
# ==============
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# The id of the working URL in the Sites table
# Currently the URL is http://localhost:8000/
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'user_photos', "publish_actions"],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.2'
    }
}

# The email backend for allauth
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by allauth template tags
    "django.core.context_processors.request",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'django.contrib.auth.context_processors.auth',
    'postman.context_processors.inbox',     # Django-postman
)

LOGIN_REDIRECT_URL = "/app/"
ROOT_URL = '/app/'

# ====================
# Django-Coffee script
# ====================
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'static_precompiler.finders.StaticPrecompilerFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_PRECOMPILER_COMPILERS = (
    'static_precompiler.compilers.CoffeeScript',
)


# ===============
# Django Haystack
# ===============
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# ==============
# Django-postman
# ==============
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_QUICKREPLY_QUOTE_BODY = True
POSTMAN_NOTIFIER_APP = 'notification'
POSTMAN_DISABLE_USER_EMAILING = False
POSTMAN_AUTO_MODERATE_AS = True
# =================
# Django-compressor
# =================
COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]
