DOCKER_COMPOSE ?= docker compose
PYTHON ?= python

# use Makefile.local for customization
-include Makefile.local

.PHONY: docker-build
docker-build:
	$(DOCKER_COMPOSE) build

.PHONY: docker-run
docker-run:
	$(DOCKER_COMPOSE) up

.PHONY: migrate
migrate:
	$(PYTHON) app/manage.py migrate

.PHONY: migrations
migrations:
	$(PYTHON) app/manage.py makemigrations

.PHONY: superuser
superuser:
	$(PYTHON) app/manage.py createsuperuser

.PHONY: fill-db
fill-db:
	$(PYTHON) app/manage.py fill_db $(ratio)

.PHONY: clear-db
clear-db:
	$(PYTHON) app/manage.py clear_db

.PHONY: clear-db-schema
clear-db-schema:
	$(PYTHON) app/manage.py clear_db_schema

.PHONY: docker-migrate docker-migrations docker-superuser docker-fill-db docker-clear-db docker-clear-db-schema
docker-migrate docker-migrations docker-superuser docker-fill-db docker-clear-db docker-clear-db-schema: docker-%:
	$(DOCKER_COMPOSE) run -e ratio=$(ratio) --rm askme-service make $*

.PHONY: clear-docker
clear-docker:
	$(DOCKER_COMPOSE) down -v