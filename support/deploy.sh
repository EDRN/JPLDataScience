#!/bin/sh -e
#
# Deploy onto edrn-docker.
#
# Expect to run this in either /usr/local/labcas/datasci/dev or in
# /usr/local/labcas/datasci/ops.

if [ ! -f "docker-compose.yaml" -o ! -f ".env" ]; then
    echo "🚨 Run this from the either the dev or ops directories on edrn-docker for Data Science" 1>&2
    echo "You should have docker-compose.yaml and .env files in the current directory" 1>&2
    exit 1
fi

project_name=datasci-`basename ${PWD}`
echo "📽️ Using project name ${project_name}" 1>&2

compose() {
    docker compose --project-name ${project_name} "$@"
}

echo "🛑 Stopping and removing any existing containers and services"
compose down --remove-orphans --volumes

compose run --rm --volume ${PWD}/docker-data:/mnt --no-TTY --entrypoint /bin/rm db -rf /mnt/postgresql || :
[ -d docker-data ] || mkdir docker-data
for sub in media static postgresql; do
    rm -rf docker-data/$sub
    mkdir docker-data/$sub
done

echo "🪢 Pulling latest images"
compose pull --quiet

echo "🚢 Creating containers and starting composition in detached mode" 1>&2
compose up --detach --quiet-pull --remove-orphans

echo "⏱️ Waiting a ½ minute for things to stabilize…" 1>&2
sleep 30

echo "❌ Destroying any existing datasci database" 1>&2
compose exec db dropdb --force --if-exists --username=postgres datasci
echo "🫄 Creating a new empty datasci database"
compose exec db createdb --username=postgres --encoding=UTF8 --owner=postgres datasci
echo "📺 Collecting static assets from the application"
compose exec portal /app/src/manage.py collectstatic
echo "🐣 Making missing database migrations"
compose exec portal /app/src/manage.py makemigrations
echo "🦆 Migrating"
compose exec portal /app/src/manage.py migrate
echo "🌸 Blooming initial content and settings"
compose exec portal /app/src/manage.py datasci_bloom
echo "🍱 Populating main menus"
compose exec portal /app/src/manage.py autopopulate_main_menus
echo "🗂️ Updating search index"
compose exec portal /app/src/manage.py wagtail_update_index

echo "🎉 Done!"
exit 0
