PYTHON = $(shell which python3.4)
ENV = $(CURDIR)/env
PROJECT = lists
COVERAGE = $(ENV)/bin/coverage
COVERAGE_OPTS = --rcfile=coverage.cfg
TEST = $(MANAGE) test
UNIT = $(TEST) lists
FUNCTIONAL = $(TEST) functional_tests
MANAGE = ./manage.py

virtual-env:
    virtualenv --python=$(PYTHON) env

env: virtual-env
	env/bin/pip3 install -r requirements.txt

clean:
	rm -rf env
	find . -iname '*.pyc' -exec rm {} \;

nose2 coverage:
	$(ENV)/bin/pip3 install -r requirements.txt

test: nose2
	$(ENV)/bin/python3 $(TEST)

unit: nose2
	$(ENV)/bin/python3 $(UNIT)

func: nose2
	$(ENV)/bin/python3 $(FUNCTIONAL)

test-coverage: coverage
	$(COVERAGE) erase
	. $(ENV)/bin/activate; $(COVERAGE) run $(COVERAGE_OPTS) -L $(TEST)
	$(COVERAGE) report -m $(COVERAGE_OPTS)

coverage-html: test-coverage
	$(COVERAGE) html $(COVERAGE_OPTS)

coverage-xml: test-coverage
	$(COVERAGE) xml $(COVERAGE_OPTS)

migrate:
	env/bin/python3 manage.py makemigrations $(PROJECT)
	env/bin/python3 manage.py migrate $(PROJECT)

run:
	env/bin/python3 manage.py runserver 0.0.0.0:8000

requirements:
	env/bin/pip3 freeze > requirements.txt
