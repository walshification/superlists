ENV := $(shell pipenv --venv)
PYTHON := $(ENV)/bin/python
BANDIT := $(ENV)/bin/bandit
BLACK := $(ENV)/bin/black
COVERAGE := $(ENV)/bin/coverage
DJANGO := $(ENV)/bin/django-admin
FLAKE8 := $(ENV)/bin/flake8
GECKDRIVER := /usr/local/bin/geckodriver
IPYTHON := $(ENV)/bin/ipython
ISORT := $(ENV)/bin/isort
SELENIUM := $(ENV)/lib/python3.6/site-packages/selenium

RUN := pipenv run
RUN_MANAGE := $(RUN) python manage.py
RUN_COVERAGE := $(RUN) coverage

start: | $(DJANGO)
	$(RUN_MANAGE) runserver 0.0.0.0:8000

fmt: | $(AUTOFLAKE) $(BLACK) $(ISORT)
	pipenv run isort --recursive .
	pipenv run autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables .
	pipenv run black .

test: test-unit test-func

test-unit: | $(COVERAGE)
	$(RUN_COVERAGE) erase && rm -rf htmlcov
	$(RUN_COVERAGE) run manage.py test lists
	$(RUN_COVERAGE) report
	$(RUN_COVERAGE) html

test-func: | $(SELENIUM)
	$(RUN_MANAGE) test functional_tests

# test-security: | $(BANDIT)
# 	$(RUN) bandit -r .

lint: | $(AUTOFLAKE) $(BLACK) $(FLAKE8) $(ISORT)
	$(RUN) black . --check
	$(RUN) flake8
	$(RUN) isort --recursive --check-only .

$(DJANGO) $(ENV):
	pipenv install

$(COVERAGE) $(IPYTHON) $(BLACK) $(FLAKE8) $(SELENIUM): | $(ENV)
	pipenv install --dev

$(GECKODRIVER):
	brew bundle

clean:
	pipenv --rm
	find . -name "__pycache__" -type d -exec rm -r "{}" \;

