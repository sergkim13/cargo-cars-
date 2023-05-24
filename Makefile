install:
	poetry install

dev:
	poetry run uvicorn cars_app.main:app --reload

hooks:
	poetry run pre-commit run --all-files

test:
	poetry run pytest -vv

test-cov:
	poetry run pytest --cov-report term-missing --cov=cars_app --cov-report xml

compose:
	docker compose up -d

stop:
	docker compose down

compose-test:
	docker compose -f docker-compose.test.yaml -p testing up -d

stop-test:
	docker compose -f docker-compose.test.yaml -p testing down

migrate:
	alembic upgrade head
