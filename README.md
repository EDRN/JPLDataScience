# 💽🔭 Data Science Portal

…


## 🤓 Development

Set the `DATABASE_URL` to `postgresql://:@/datasci`?

```console
$ createdb datasci
$ ./manage.sh migrate
$ ./manage.sh createsuperuser --username root --email your@email.com
```


### 🚢 Dockerization

```console
$ docker image build --tag edrndocker/datasci --file docker/Dockerfile .
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml up
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec db dropdb --force --if-exists --username=postgres datasci
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec db createdb --username=postgres --encoding=UTF8 --owner=postgres datasci
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec portal /app/src/manage.py collectstatic
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec portal /app/src/manage.py makemigrations
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec portal /app/src/manage.py migrate
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec portal /app/src/manage.py datasci_bloom
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec portal /app/src/manage.py autopopulate_main_menus
$ env POSTGRES_PASSWORD=secret DATASCI_IMAGE_OWNER= DATASCI_DATA_DIR=/Users/kelly/Downloads/docker-data/datasci DATASCI_VERSION=latest docker compose --file docker/docker-compose.yaml exec portal /app/src/manage.py wagtail_update_index
```


#### 🌱 Environment Variables


| CERT_CN | | `edrn-docker.jpl.nasa.gov` |
| DATASCI_TLS_PORT | | `5134` |
| DATASCI_IMAGE_OWNER | | `edrndocker/` |
| DATASCI_VERSION | | `1.0.0` |
| DATASCI_DATA_DIR | | `/usr/local/labcas/datasci/docker-data` |
| POSTGRES_PASSWORD | | (unset) |


## 📀 Database Backups and Export

The content database consists of the following:

-   A PostgreSQL database whose volume is mapped to the host filesystem in `docker-data/postgresql`
-   Media files (images, PDFs, etc.) served by Nginx and referenced by Wagtail and mapped in the host filesystem in `docker-data/media`

Thus, to backup the data, you should ensure that both the PostgreSQL database and the media filesystem are copied.

    @weekly /usr/local/labcas/datasci/dev/compose.sh exec --no-TTY db pg_dump --username=postgres --encoding=UTF8 --no-password --dbname=datasci | /usr/bin/bzip2 > /usr/local/labcas/datasci/dev/backups/$(/usr/bin/date --utc '+%Y-%m-%d')-backup.sql.bz2
    @weekly cp -R /usr/local/labcas/datasci/dev/docker-data/media /usr/local/labcas/datasci/dev/backups/media-$(/usr/bin/date --utc '+%Y-%m-%d')

To import the data into a new instance:

    rsync --checksum --no-motd --recursive --delete --progress $BACKUP_HOST/backups .
    dropdb --force --if-exists datasci
    createdb datasci "Data Science"
    bzip2 --decompress --stdout backups/backup.sql.bz2 | psql --dbname=datasci --echo-errors --quiet
    rm -rf media
    mv backups/media .

