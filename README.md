<div align="center">

# Ask Service

community-supported service that allows users to ask questions and get answers to them

</div>

> [!IMPORTANT]  
> Currently, only local launch is possible. 

## Contents

* [Requirements](#requirements)
* [Getting Started](#getting-started)
  * [MacOS & Linux](#macos-linux)
    * [Local](#local-steps)
    * [Docker](#docker-steps)
* [Commands](#commands)
  * [Local](#local-commands)
  * [Docker](#docker-commands)
* [Benchmarks](#benchmarks)

## Requirements <a name="requirements"></a>

* [docker](https://docs.docker.com/)
* [docker compose](https://docs.docker.com/compose/)
* [make](https://www.gnu.org/software/make/manual/make.html)
* [centrifugo](https://centrifugal.dev/)

> [!IMPORTANT]  
> The project supports docker compose v2 by default, but if you want to use v1, then you need to add the `DOCKER_COMPOSE = docker-compose` line in the `Makefile.local`.

## Getting Started <a name="getting-started"></a>

### MacOS & Linux <a name="macos-linux"></a>

#### Local <a name="local-steps"></a>

1. Setup virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start postgres database

3. Apply migrations:

```shell
make migrate
```

4. Fill db with generated data:

```shell
make fill-db ratio=100
```

5. Run centrifugo server (available on `127.0.0.1:8001`):

```shell
make cent
```

6. Run project:

```shell
make run
```

7. Open the `127.0.0.1:8000` path in the browser

#### Docker <a name="docker-steps"></a>

1. Set the `IN_DOCKER` variable in `app/core/local_settings.py` to `True`

```python
...
IN_DOCKER = True
...
```

2. Build the container:

```shell
make docker-build
```

3. Apply migrations:

```shell
make docker-migrate
```

4. Fill db with generated data:

```shell
make docker-fill-db ratio=100
```

5. Run project:

```shell
make docker-run
```

> [!IMPORTANT]  
> If you see in the logs that the database does not accept requests, it means that the database container started later than the application container. In this case, you need to run the command again or manually launch the database container first (`docker start postgres-service-container`).

5. Open the `127.0.0.1:8000` path in the browser

6. Stop and remove docker containers:

```shell
make clear-docker
```

## Commands <a name="commands"></a>

### Local <a name="local-commands"></a>

* `make docker-migrations` - create migrations
* `make docker-migrate` - apply migrations
* `make docker-fill-db ratio=<ratio>` - fill database with generated data
* `make docker-run` - start gunicorn server
* `make docker-superuser` - create superuser
* `make docker-clear-db` - remove data from database
* `make docker-clear-db-schema` - remove database schema and data in it
* `make clear-docker` - stop and remove containers

### Docker <a name="docker-commands"></a>

* `make migrations` - create migrations
* `make migrate` - apply migrations
* `make fill-db ratio=<ratio>` - fill database with generated data
* `make cent` - start centrifugo server
* `make run` - start gunicorn server
* `make superuser` - create superuser
* `make clear-db` - remove data from database
* `make clear-db-schema` - remove database schema and data in it

## Benchmarks <a name="benchmarks"></a>

The results of the service's benchmarks are [here](docs/benchmarks.md).
