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
$ docker image build --tag datasci --file docker/Dockerfile .
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
| DATASCI_IMAGE_OWNER | | `nutjob4life/` |
| DATASCI_VERSION | | `1.0.0` |
| DATASCI_DATA_DIR | | `/usr/local/labcas/datasci/docker-data` |
| POSTGRES_PASSWORD | | (unset) |

