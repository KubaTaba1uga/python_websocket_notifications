venv_name := .venv
sources := notifications_service message_store db test

help:
	@echo "lint - check style with ruff and mypy"
	@echo "format - format style with black and isort"
	@echo "tests - run tests quickly with pytest"
	@echo "venv - creates virtual environment"
	@echo "install - install requirements"
	@echo "install-dev - install dev requirements"
	@echo "install-test - install test requirements"	
	@echo "clean - remove venv"	
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-git - remove ignored and not ignored files"

lint:
	python -m ruff $(sources)
	python -m mypy $(sources)

format:
	python -m black $(sources)
	python -m isort $(sources)

unit-test:
	export `cat .test.env | xargs` && python -m pytest notifications_service/test/ message_store/test/ -vv $(arguments)

integration-test:
	export `cat .test.env | xargs` && python -m pytest test/ -vv $(arguments)


venv:
	python3 -m virtualenv $(venv_name)

install: 
	pip install -r notifications_service/requirements.txt

install-test: 
	pip install -r test-requirements.txt

clean: 
	rm -rf $(venv_name)
	rm -rf db/.data

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-git:
	git clean -fxd

.PHONY: help lint format test venv install install-dev install-test clean clean-pyc clean-git 
