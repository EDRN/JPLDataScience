# encoding: utf-8

'''📀🔬 Data Science site: base settings.'''

from .ldap import *  # noqa: F401, F403
import os, dj_database_url


# Installed Applications
# ----------------------
#
# The "apps" (Python packages) enabled for Django.

INSTALLED_APPS = [
    'datascience',
    'search',
    'theme',
    'blocks',
    'content',
    'controls',
    'wagtail.contrib.table_block',
    'wagtail.contrib.typed_table_block',
    'wagtail.contrib.modeladmin',  # Needed by wagtailmenus
    'wagtail.contrib.settings',    # Needed for @register_setting, etc.
    'wagtailmenus',
    'wagtail.contrib.forms',
    'widget_tweaks',
    'wagtailcaptcha',
    'captcha',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.contrib.search_promotions',  # Promote certain search results
    'modelcluster',
    'taggit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'wagtail_blocks',
]


# Middleware
# ----------
#
# Pipeline processors on the request/response.

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]


# CSRF
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#csrf-trusted-origins

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://*.jpl.nasa.gov,https://*.jpl.nasa.gov,http://localhost,https://localhost').split(',')


# Root URL Configuration
# ----------------------
#
# Name of the module that contains URL patterns.

ROOT_URLCONF = 'datascience.urls'


# Databases
# ---------
#
# We let the magic of `dj-database-url` set this up for us. Note that `DATABASE_URL` will need to be
# provided in the environment.

DATABASES = {'default': dj_database_url.config(default='postgresql://:@/datasci', conn_max_age=120)}  # seconds


# Templates
# ---------
#
# The template engines and getting them going, etc.
#
# No regular filesystem templates here; everything comes from the "apps" (Python packages).

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtailmenus.context_processors.wagtailmenus',  # For menus
            ],
        },
    },
]

# Application for Web Services Gateway Interface
# ----------------------------------------------
#
# Full path to Python object that's the WSGI application.

WSGI_APPLICATION = 'datascience.wsgi.application'


# Type of Primary Key Field for Models
# ------------------------------------
#
# For models that don't have a primary key field, they get a default. This tells the data type
# of that field, `BigAutoField` in this case.
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password Strength
# -----------------
#
# We don't use this because users keep creds in LDAP
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# --------------------
#
# Settings for time zones, languages, locales, etc.

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True


# Static Files
# ------------
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#staticfiles-storage
# 🔗 https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#manifeststaticfilesstorage

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(os.path.abspath(os.getcwd()), 'static'))


# Media Files
# -----------

MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(os.path.abspath(os.getcwd()), 'media'))


# Site Identification
# -------------------
#
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtail-site-name

WAGTAIL_SITE_NAME = 'JPL Data Science'


# Search
# ------
#
# 🔗 https://docs.wagtail.org/en/stable/reference/settings.html#wagtailsearch-backends

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch7',
        'AUTO_UPDATE': True,
        'ATOMIC_REBUILD': True,
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'OPTIONS': {},
        'INDEX_SETTINGS': {},
        'URLS': [os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')]
    }
}

# Admin Base URL
# --------------
#
# 🔗 https://docs.wagtail.org/en/stable/reference/settings.html#wagtailadmin-base-url

WAGTAILADMIN_BASE_URL = os.getenv('BASE_URL', 'https://datascience.jpl.nasa.gov/')


# reCAPTChA
#
# 🔗 https://github.com/springload/wagtail-django-recaptcha

RECAPTCHA_PUBLIC_KEY = os.getenv('JPL_DS_RECAPTCHA_SITE_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.getenv('JPL_DS_RECAPTCHA_SECRET_KEY', '')


# Email
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#email-host

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.jpl.nasa.gov')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
