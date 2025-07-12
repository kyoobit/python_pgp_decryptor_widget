# Makefile for Python dearmor widget
# https://www.gnu.org/software/make/manual/make.html
SHELL := /bin/sh
VENV = .venv
VENV_BIN = ./$(VENV)/bin

install: requirements-ci.txt ## Install the application requirements
	# Install `uv' 
	uv --version || curl -LsSf https://astral.sh/uv/install.sh | sh
	# Install the Python requirements using uv in a virtual environment
	# CI requirements-ci.txt file includes dependencies for format, lint, and test
	uv add --upgrade --requirements requirements-ci.txt --dev

format: ## (Re)Format the application files
	uv run black *.py

lint: ## Lint the application files
	# Lint the application files
	# Ignore anti-pattern E266 too many leading '#' because, just because
	# Ignore [anti-]pattern W503 Line break occurred before a binary operator, trust black
	# Ignore [anti-]pattern W293 blank line contains whitespace, part of the content
	uv run flake8 --max-line-length 127 *.py --ignore=E266,W503,W293
	uv run ruff check *.py

test: ## Test the application
	# Test the application (PGP_KEY_PASSPHRASE needed in environment variables)
	uv run coverage run -m pytest -v test_dearmor.py
	# Report code coverage
	uv run coverage report -m

depcheck: ## Dependency check for known vulnarbilities
	# Perform a scan of dependancies backed by the OSS Index
	uv run jake --warn-only ddt

secscan: ## Run a source code security analyzer
	# Analyze the application files
	# Ignore B101 Use of assert detected, due to laziness of putting tests in the same file
	uv run bandit --recursive *.py --skip B101

all: install lint test depcheck secscan

# Actions that don't require target files
.PHONY: clean
.PHONY: help

help: ## Print a list of make options available
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' ${MAKEFILE_LIST} | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

clean: ## Clean up files used locally when needed
	# Remove the Python cache files
	rm -rf ./__pycache__
	rm -rf ./tests/__pycache__
	# Remove the Python pytest files
	rm -rf ./.pytest_cache
	# Remove the Python the virtual environment
	rm -rf ./$(VENV)
