ENV = $(shell pipenv --venv)
GECKODRIVER := /usr/local/bin/geckodriver
DJANGO_ADMIN := $(ENV)/bin/django-admin
PYTEST := $(ENV)/bin/pytest
BLACK := $(ENV)/bin/black
FLAKE8 := $(ENV)/bin/flake8
IPYTHON := $(ENV)/bin/ipython
BANDIT := $(ENV)/bin/bandit
SELENIUM := $(ENV)/lib/python3.6/site-packages/selenium

test: test-unit lint test-func test-security

test-unit: | $(PYTEST)
	pipenv run pytest --cov
	pipenv run coverage html

test-func: | $(SELENIUM) $(GECKODRIVER)
	pipenv run python functional_tests.py

lint: | $(BLACK) $(FLAKE8)
	pipenv run black . --check
	pipenv run flake8
	pipenv run isort --recursive --check-only .

test-security: | $(BANDIT)
	pipenv bandit -r .

fmt: | $(BLACK)
	pipenv run isort --recursive .
	pipenv run autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables .
	pipenv run black .

start: | $(DJANGO_ADMIN)
	pipenv run python manage.py runserver

shell: | $(DJANGO_ADMIN) $(IPYTHON)
	pipenv run python manage.py shell

$(ENV) init: | $(GECKODRIVER)
	pipenv install --dev

$(GECKODRIVER):
	brew bundle

ci-env:
	pip install pip --upgrade
	pip install pipenv
	pipenv install --dev --system

ci-test:
	python functional_tests.py

$(IPYTHON) $(PYTEST) $(BLACK) $(FLAKE8) $(SELENIUM): | $(ENV)
	pipenv install --dev

clean:
	pipenv --rm
