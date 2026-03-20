.PHONY: up down build logs migrate makemigrations shell up-d

include .env

export UID=${shell id -u}

export

up:
	docker compose up --build

up-d:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

migrate:
	docker compose exec backend alembic upgrade head

makemigrations:
	docker compose exec backend alembic revision --autogenerate -m "migration"

shell:
	docker compose exec backend sh

clean:
	docker compose down -v --remove-orphans

clear-all:
	@read -p "Это удалит всё (волюмы/образы/контейнеры). Точно ли сделать это ? [y/n]: " confirm && \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker compose down -v --rmi all --remove-orphans; \
	else \
		echo "Отмена"; \
	fi

