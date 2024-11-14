PHONY := up local down

up:
	docker compose up -d --build

local:
	docker compose -f local-docker-compose.yml up

down:
	docker compose down -v

.DEFAULT_GOAL := up