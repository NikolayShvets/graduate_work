.PHONY: up down check format migration migrations migrate superuser tests build

up:
	docker compose up -d --build

down:
	docker compose down -v

check:
	poetry run ruff check src --fix

format:
	poetry run ruff format src

migration:
	PYTHONPATH=src poetry run alembic revision -m $(m)

migrations:
	PYTHONPATH=src poetry run alembic revision --autogenerate -m $(m)

migrate:
	PYTHONPATH=src poetry run alembic upgrade head

superuser:
	PYTHONPATH=src python ./src/commands/createsuperuser.py

tests:
	docker compose -f test-docker-compose.yml up -d
	docker build -t test-auth:latest --file ./src/TestDockerfile ./src
	docker run --network test-auth --env-file ./src/.test.env test-auth:latest
	docker compose -f test-docker-compose.yml down -v --remove-orphans
	docker ps -a | grep 'test-auth' | awk '{print $$1}' | xargs docker rm

build:
	docker --log-level=debug build --progress=plain --pull --file=Dockerfile --tag=ghcr.io/nikolayshvets/movies-auth:1.1 .
	docker push ghcr.io/nikolayshvets/movies-auth:1.1

.DEFAULT_GOAL := up