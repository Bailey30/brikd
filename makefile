
# Use pipenv inside the backend container
SHELL := /bin/bash

dev:
	pipenv shell

up:
	docker-compose up --build

down:
	docker-compose down -v

front:
	docker-compose up frontend --build

back:
	docker-compose up backend --build

migrate:
	docker-compose exec backend pipenv run python manage.py migrate

makemigrations:
	docker-compose exec backend pipenv run python manage.py makemigrations

runserver:
	docker-compose exec backend pipenv run python manage.py runserver 0.0.0.0:8000

createsuperuser:
	docker-compose exec backend pipenv run python manage.py createsuperuser

testbackend:
	docker-compose exec backend pipenv run python manage.py test

shell: 
	docker-compose exec backend pipenv run python manage.py shell
