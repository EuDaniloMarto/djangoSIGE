run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

test:
	coverage run --source='djangosige' manage.py test && coverage report

format:
	black . && isort .

lint:
	flake8 . && djlint djangosige/ --lint
