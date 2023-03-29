# encoding: utf-8

'''Data Science: Lightweight Directory Access Protocol settings'''

from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType
import ldap, os


# Wagtail Specific Settings
# -------------------------
#
# This ensures that Wagtail stays out of the way of LDAP
#
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtail-password-management-enabled
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtail-password-reset-enabled
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtailusers-password-enabled

WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
WAGTAIL_PASSWORD_RESET_ENABLED      = False
WAGTAILUSERS_PASSWORD_ENABLED       = False


# Backends to Authenticate Against
# --------------------------------
#
# This says to try LDAP first, then the local site database.
#
# 🔗 https://docs.djangoproject.com/en/latest/ref/settings/#authentication-backends

AUTHENTICATION_BACKENDS = ['django_auth_ldap.backend.LDAPBackend', 'django.contrib.auth.backends.ModelBackend']


# Server
# ------
#
# The timeout is in seconds. The weird server URL is explained by
# https://jpl.slack.com/archives/C01DXUKQ69L/p1680102577455989?thread_ts=1680100505.489409&cid=C01DXUKQ69L
#
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/authentication.html#server-config
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-cache-timeout

AUTH_LDAP_SERVER_URI = os.getenv('LDAP_URI', 'ldaps://ldap-202007.jpl.nasa.gov')
AUTH_LDAP_CACHE_TIMEOUT = int(os.getenv('LDAP_CACHE_TIMEOUT', '3600'))


# How to Find Users
# -----------------
#
# Normally we'd use AUTH_LDAP_USER_DN_TEMPLATE which is more efficient than binding with a manager
# DN and searching, but I cannot get the AUTH_LDAP_USER_DN_TEMPLATE to work with our LDAP server.
# So we're stuck going binding (and getting the credential) from the environment.
#
# Regardless, we keep AUTH_LDAP_ALWAYS_UPDATE_USER True so that LDAP values update Django `User`
# values.
#
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-always-update-user
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-dn-template
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-bind-dn
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-bind-password
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-search

AUTH_LDAP_ALWAYS_UPDATE_USER = False
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=personnel,dc=dir,dc=jpl,dc=nasa,dc=gov'
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True


# Groups
# ------
#
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-group-search
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-group-type
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-find-group-perms
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-mirror-groups

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    'ou=personnel,dc=dir,dc=jpl,dc=nasa,dc=gov', ldap.SCOPE_ONELEVEL, '(objectClass=groupOfUniqueNames)'
)
AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType(name_attr='cn')
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_MIRROR_GROUPS = True


# Mapping User Attributes
# -----------------------
#
# This mapping is from Django user attribute name to LDAP attribute name.
#
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-attr-map

AUTH_LDAP_USER_ATTR_MAP = {
    'email':      'mail',
    'first_name': 'givenName',
    'last_name':  'sn',
    'username':   'uid',
}


# Special Groups
# --------------
#
# These groups get special treatment in Django.
#
# 🔗 https://django-auth-ldap.readthedocs.io/en/latest/reference.html#auth-ldap-user-flags-by-group

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_active':    'cn=all.personnel,ou=personnel,dc=dir,dc=jpl,dc=nasa,dc=gov',
    'is_staff':     'cn=datasystechoffice,ou=personnel,dc=dir,dc=jpl,dc=nasa,dc=gov',
    'is_superuser': 'cn=datasystechoffice,ou=personnel,dc=dir,dc=jpl,dc=nasa,dc=gov',
}
