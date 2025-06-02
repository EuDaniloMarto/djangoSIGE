run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

shell:
	python manage.py shell

test:
	pytest -cov

format:
	black . && isort .

bandit:
	bandit -r . -f html -o bandit_report.html --severity-level high
