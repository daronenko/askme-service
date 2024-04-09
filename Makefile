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

.PHONY: fill-db
fill-db:
	$(PYTHON) app/manage.py fill_db $(ratio)

.PHONY: clean-db
clean-db:
	$(PYTHON) app/manage.py clean_db

.PHONY: docker-migrate docker-migrations docker-fill-db docker-clean-db
docker-migrate docker-migrations docker-fill-db docker-clean-db: docker-%:
	$(DOCKER_COMPOSE) run -e ratio=$(ratio) --rm askme-service make $*

.PHONY: clean-docker
clean-docker:
	$(DOCKER_COMPOSE) down -v