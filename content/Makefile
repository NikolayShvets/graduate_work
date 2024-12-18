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

.DEFAULT_GOAL := up
