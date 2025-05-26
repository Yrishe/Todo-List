# Makefile for Flask Todo App

# Python executable
PYTHON := python

# Virtual environment activation
VENV := . venv/bin/activate

# Flask settings
FLASK_APP := run.py
FLASK_ENV := development

# Default target
.PHONY: help
help:
	@echo "make run        # Run the Flask app"
	@echo "make test       # Run unit tests with pytest"
	@echo "make freeze     # Export dependencies to requirements.txt"
	@echo "make format     # Format code with black"
	@echo "make clean      # Remove __pycache__ and .pyc files"

.PHONY: run
run:
	$(VENV) && FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run

.PHONY: test
test:
	$(VENV) && $(PYTHON) -m pytest -v --tb=short tests/

.PHONY: freeze
freeze:
	$(VENV) && pip freeze > requirements.txt

.PHONY: format
format:
	$(VENV) && black app/ tests/

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +;
	find . -type f -name "*.pyc" -delete
