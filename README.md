<div align="center">

# Ask Service

community-supported service that allows users to ask questions and get answers to them

</div>

## Contents

* [Requirements](#requirements)
* [Getting Started](#getting-started)
  * [MacOS & Linux](#macos-linux)
* [Commands](#commands)

## Requirements <a name="requirements"></a>

* [docker](https://docs.docker.com/)
* [docker compose](https://docs.docker.com/compose/)
* [make](https://www.gnu.org/software/make/manual/make.html)

> [!IMPORTANT]  
> The project supports docker compose v2 by default, but if you want to use v1, then you need to add the `DOCKER_COMPOSE = docker-compose` line in the `Makefile.local`.

## Getting Started <a name="getting-started"></a>

### MacOS & Linux <a name="macos-linux"></a>

1. Build the container:

```shell
make docker-build
```

2. Apply migrations:

```shell
make docker-migrate
```

3. Fill db with generated data:

```shell
make docker-fill-db ratio=100
```

4. Run project:

```shell
make docker-run
```

> [!IMPORTANT]  
> If you see in the logs that the database does not accept requests, it means that the database container started later than the application container. In this case, you need to run the command again or manually launch the database container first (`docker start postgres-service-container`).

5. Open the `localhost:8000` path in the browser

6. Stop and remove docker containers:

```shell
make clear-docker
```

## Commands <a name="commands"></a>

* `make docker-build` - build containers
* `make docker-migrations` - create migrations
* `make docker-migrate` - apply migrations
* `make docker-fill-db ratio=<ratio>` - fill database with generated data
* `make superuser` - create superuser
* `make docker-clear-db` - remove data from database
* `make docker-clear-db-schema` - remove database schema and data in it
* `make clear-docker` - stop and remove containers