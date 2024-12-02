.PHONY: up down check format migration migrations migrate filldb build

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

filldb:
	PYTHONPATH=src python src/commands/fill_database.py

build:
	docker --log-level=debug build --progress=plain --pull --file=Dockerfile --tag=ghcr.io/nikolayshvets/movies-auth:1.1 .
	docker push ghcr.io/nikolayshvets/movies-auth:1.1

.DEFAULT_GOAL := build
