#!/bin/sh -e
#
#
# Run django-admin locally with this convenience script

. ${HOME}/.secrets/passwords.sh

export DJANGO_SETTINGS_MODULE=datascience.settings.production

if [ ! -d "src" -o ! -d "docker" ]; then
    echo "🚨 Run this from the checked-out JPLDataScience source directory" 1>&2
    echo "You should have these subdirs in the current directory: src docker" 1>&2
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "⚠️ Local Python virtual environment missing; attempting to re-create it" 1>&2
    python3.10 -m venv .venv
    venv/bin/pip install --quiet --upgrade setuptools pip wheel build
    venv/bin/pip install --requirement requirements.txt
fi

. .venv/bin/activate

command=$1
shift
exec /usr/bin/env \
    DATABASE_URL="postgresql://:@/datasci" \
    "src/manage.py" $command --settings local --pythonpath . "$@"
