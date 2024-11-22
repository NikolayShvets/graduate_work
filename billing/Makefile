.PHONY: help up down check format

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up:
	docker compose up -d --build

down:
	docker compose down -v

check:
	poetry run ruff check src --fix

format:
	poetry run ruff format src

migrations:
	PYTHONPATH=src poetry run alembic revision --autogenerate -m $(m)

migrate:
	PYTHONPATH=src poetry run alembic upgrade head

build:
	docker --log-level=debug build --progress=plain --pull --file=Dockerfile --tag=ghcr.io/nikolayshvets/movies-billing:1.1 .
	docker push ghcr.io/nikolayshvets/movies-billing:1.1

.DEFAULT_GOAL := up
