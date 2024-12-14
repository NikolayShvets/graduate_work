.PHONY: help up down check format

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

build:
	docker --log-level=debug build --progress=plain --pull --file=Dockerfile --tag=ghcr.io/nikolayshvets/movies-billing:1.1 .
	docker push ghcr.io/nikolayshvets/movies-billing:1.1

.DEFAULT_GOAL := up
