# Ask Service

## Requirements

* [docker](https://docs.docker.com/)
* [docker compose](https://docs.docker.com/compose/)
* [make](https://www.gnu.org/software/make/manual/make.html)

> [!IMPORTANT]  
> The project supports docker compose v2 by default, but if you want to use v1, then you need to change the `DOCKER_COMPOSE ?= docker compose` line in the `Makefile` to `DOCKER_COMPOSE ?= docker-compose`.

## Getting Started

### MacOS & Linux

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

> [!NOTE]  
> If you see in the logs that the database does not accept requests, it means that the database container started later than the application container. In this case, you need to run the command again or manually launch the database container first (`docker start postgres-service-container`).

5. Open the `0.0.0.0:8000` path in the browser