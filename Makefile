#!make

###############################################################################
# CONFIGURATION                                                               #
###############################################################################


###############################################################################
# SETUP                                                                       #
###############################################################################

-include .env

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

ifndef PYTHON
	PYTHON = python
endif

ifndef PKG_MGR
	PKG_MGR = pipenv
endif

ifndef TODO_CMD
	TODO_CMD = todo
endif

ifndef PYTEST_CORES
	PYTEST_CORES = auto
endif

SUBDIR_ROOTS := docs src tests
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := *.pyc *~ *-checkpoint.ipynb
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

FLAKE8 = flake8
INVOKE = invoke
PYTEST = pytest
TOX = tox
TWINE = twine

ifeq ($(PKG_MGR), pipenv)
    RUN_PRE = pipenv run
	VENV_DIR := $(pipenv --venv)

	CREATE_VENV =
	REMOVE_VENV = pipenv --rm
    INSTALL_DEPENDENCIES = pipenv install --dev
    GENERATE_DEPENDENCIES = pipenv lock --dev -r > requirements.txt
else
    RUN_PRE =
	VENV_DIR = env

	CREATE_VENV := virtualenv $(VENV_DIR)/
	REMOVE_VENV := rm -rf $(VENV_DIR)
    INSTALL_DEPENDENCIES = pip install -r requirements.txt
    GENERATE_DEPENDENCIES = pip freeze --local > requirements.txt
endif

ACTIVATE_VENV := source $(VENV_DIR)/bin/activate
DEACTIVATE_VENV = deactivate

PYTHON := $(RUN_PRE) $(PYTHON)

FLAKE8 := $(RUN_PRE) $(FLAKE8)
INVOKE := $(RUN_PRE) $(INVOKE)
PYTEST := $(RUN_PRE) $(PYTEST)
TOX := $(RUN_PRE) $(TOX)
TWINE := $(RUN_PRE) $(TWINE)

###############################################################################
# COMMANDS                                                                    #
###############################################################################
.PHONY: help setup teardown \
		venv-create venv-remove \
        requirements requirements-generate \
        docs docs-clean docs-del-api docs-gen-api docs-makegen \
        clean clean-build \
		changes changes-draft changelog changelog-draft \
		ipykernel-install ipykernel-uninstall \
		lint coverage \
		test test-watch test-tox \
		build check-build release

.DEFAULT-GOAL := help

help: ## Displays this help message
	@printf 'Usage: make \033[36m[target]\033[0m\n'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ''

setup: venv-create requirements ipykernel-install ## Sets up the environment for development

teardown: ipykernel-uninstall venv-remove ## Removes the environment for development

# Virtual environment

venv-create: ## Creates the virtual environment for this project
	$(CREATE_VENV)

venv-remove: ## Removes the virtual environment for this project
	$(REMOVE_VENV)

# Requirements

requirements: ## Installs Python dependencies
	$(INSTALL_DEPENDENCIES)

requirements-generate: ## Generates the project's requirements.txt file
	$(GENERATE_DEPENDENCIES)

# Documentation

docs: ## Generates the sphinx HTML documentation
	@cd docs/ && $(RUN_PRE) make html

docs-clean: ## Cleans the generated documentation
	@cd docs/ && $(RUN_PRE) make clean

docs-del-api: ## Removes the auto-generated API documentation files
	@rm -f docs/api/*

docs-gen-api: docs-del-apidocs ## Generates the API documentation files
	@cd docs/ && $(RUN_PRE) sphinx-apidoc -e -M -o api ../src/spines

docs-makegen: ## Generates the API documentation for this Makefile
	$(INVOKE) docs.generate-make

# Cleaning

clean: ## Delete all compiled Python files or temp files
	@rm -rf $(GARBAGE)

clean-build: ## Clean out the compiled package files
	@rm -rf build/*
	@rm -rf dist/*

# Changes

changes: ## Generates the changes files from the todo files
	$(INVOKE) develop.todos

changes-draft: ## Genereates the draft changes from the todo files
	$(INVOKE) develop.todos --draft

changelog: ## Generates the new CHANGELOG.md file
	$(INVOKE) release.changelog

changelog-draft: ## Generates the draft new CHANGELOG.draft.md file
	$(INVOKE) release.changelog --draft

# IPyKernel

ipykernel-install:  ## Installs the IPyKernel for this environment
	$(INVOKE) install.ipykernel

ipykernel-uninstall: ## Uninstalls the IPyKernel for this environment
	$(INVOKE) uninstall.ipykernel

# Code

lint: ## Lint using flake8
	$(FLAKE8) src/spines/

coverage: ## Runs code coverage checks over the codebase
	$(PYTEST) --cov=src/spines tests/

# Unit testing

test: ## Run the unit tests over the project
	$(PYTEST) tests/

test-tox: ## Run the tox unit tests over the project
	$(TOX)

test-watch: ## Run pytest-watch to run tests on project changes
	$(PYTEST) -f -n $(PYTEST_CORES) tests/

# Distribution

build: clean-build ## Builds the library package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

check-build: ## Check the built packages prior to uploading
	$(TWINE) check dist/*

upload: ## Uploads the package to the PyPI server
	$(TWINE) upload dist/*
