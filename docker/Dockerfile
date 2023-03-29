# Data Science — Docker Image
# ===========================
#
# Used by "docker image build" to create a containerizable image of the data science site.


# Basis
# -----

FROM alpine:3.17


# Configurable Arguments
# ----------------------
#
# - `user_id` should be 500, which is what the world generally sues

ARG user_id=500


# Environment Variables
# ---------------------
#
# These don't need to be overridden

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=datascience.settings.production \
    STATIC_ROOT=/app/static \
    MEDIA_ROOT=/app/media

# Layering
# --------
#
# Note that this project uses Python-LDAP 3.4.0 which only supports OpenLDAP 2.4, which reached end-of-life.
# Alpine Linux smartly incldues OpenLDAP 2.5. The `echo` in the `RUN` below works around this incompatibility.
# See https://github.com/python-ldap/python-ldap/issues/432#issuecomment-974799221
#
# The `py_deps` we install as APK packages instead of as dependencies of later `pip install` in order to
# save time.
#
# 🔮 TODO: these `build_deps` and `run_deps` feel excessive.

RUN \
    : Add system group datasci &&\
    /usr/sbin/addgroup -S -g $user_id datasci &&\
    : Add system user datasci, no password, home dir datasci, group datasci, gecos info "Datasci User" &&\
    /usr/sbin/adduser -S -D -h /datasci -G datasci -u $user_id -g 'Datasci User' datasci &&\
    : Dependencies &&\
    echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories &&\
    echo '@edge https://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories &&\
    /sbin/apk update &&\
    :

RUN \
    build_deps="automake bzip2-dev cyrus-sasl-dev g++ gcc libffi-dev libjpeg-turbo-dev libwebp-dev libxml2-dev libxslt-dev make musl-dev openjpeg-dev openldap-dev openssl-dev pcre-dev python3-dev postgresql-dev su-exec tiff-dev zlib-dev " &&\
    run_deps="ca-certificates curl krb5-libs libgcc libjpeg-turbo libldap libpq libsasl libstdc++ libwebp libxml2 libxslt netcat-openbsd openjpeg python3 rsync tiff" &&\
    py_deps="py3-pillow py3-psycopg2 py3-tz py3-tzdata py3-tzlocal" &&\
    /sbin/apk update --quiet &&\
    /sbin/apk add --no-progress --quiet --virtual /datasci-build $build_deps &&\
    /sbin/apk add --no-progress --quiet $run_deps &&\
    /sbin/apk add --no-progress --quiet $py_deps &&\
    :

RUN \
    : See https://github.com/python-ldap/python-ldap/issues/432 for workaround to Python LDAP vs OpenLDAP 2.5 issue &&\
    echo 'INPUT ( libldap.so )' > /usr/lib/libldap_r.so &&\
    /usr/bin/python3 -m ensurepip --upgrade &&\
    /usr/bin/pip3 install --quiet --progress-bar off --upgrade pip setuptools wheel &&\
    /usr/bin/pip3 install gunicorn==20.1.0 &&\
    /usr/bin/install -o datasci -g datasci -d /app /app/media /app/static /app/wheels &&\
    :

COPY --chown=datasci:datasci requirements.txt /app
RUN /usr/bin/pip3 install --progress-bar off --quiet --requirement /app/requirements.txt
COPY --chown=datasci:datasci ./src /app/src/


RUN \
    cd /app &&\
    : Get the static files ready &&\
    : Although to be fair you will do this via docker-compose so your web server can serve the static files itself &&\
    /sbin/su-exec datasci /usr/bin/env SECRET_KEY=unused python3 src/manage.py collectstatic --settings datascience.settings.production --no-input --clear --link &&\
    /usr/bin/pip3 uninstall --yes --quiet pip &&\
    /sbin/apk del --quiet /datasci-build &&\
    /bin/rm -rf /app/wheels &&\
    /bin/rm -rf /var/cache/apk/* &&\
    /bin/chown -R datasci:datasci /usr/lib/python3.*/site-packages &&\
    :


# Image Morphology
# ----------------
#
# Define external shape and other miscellaneous details of the image.

EXPOSE      8000
VOLUME      ["/app/media"]
USER        datasci
WORKDIR     /app/src
# ENTRYPOINT  ["/usr/bin/python3"]
CMD         set -xe; gunicorn --bind=0.0.0.0:8000 datascience.wsgi:application
# HEALTHCHECK --interval=5m --timeout=2m --start-period=10m CMD /usr/bin/curl --fail --retry 6 --max-time 5 --retry-delay 10 --retry-max-time 60 http://127.0.0.1:8000/ || /bin/sh -c 'killall5 -TERM && (/bin/sleep 10; killall5 -KILL)'


# Metadata
# --------
#
# Note that ``org.label-schema`` is deprecated, but it's a heck of a lot easier to understand. Still, why not just
# use the Dublin Core?

LABEL "org.label-schema.name"="Data Science"
LABEL "org.label-schema.description"="Public website for Center for Data Science & Technology"
LABEL "org.label-schema.version"="6.0.0"
