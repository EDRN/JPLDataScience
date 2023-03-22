# encoding: utf-8

'''Data Science: development mode site.'''

from .base import *  # noqa: F401, F403

# Debug Mode
# ----------
#
# In development we want debug mode of course.
#
# 🚨 This must never be True in production.
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#debug

DEBUG = True


# Email Backend
# -------------
#
# How to send email while in debug mode: don't! Write emails to stdout.

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Allowed Hosts
# -------------
#
# 🚨 This must never be `*` in production.
#
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts

ALLOWED_HOSTS = ["*"]


# Site Identification
# -------------------
#
# Override the site name so we obviously see this is a debug mode site.
#
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtail-site-name

WAGTAIL_SITE_NAME = 'JPL Data Science (🔧 dev)'


# Debugging & Development Tools
# -----------------------------

INSTALLED_APPS += [  # noqa
    'wagtail.contrib.styleguide',
]
MIDDLEWARE = [
] + globals().get('MIDDLEWARE', [])
