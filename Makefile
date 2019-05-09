#!make

###############################################################################
# CONFIGURATION                                                               #
###############################################################################


###############################################################################
# SETUP                                                                       #
###############################################################################

-include .env

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

ifndef MODE
	MODE = dev
endif

ifndef PYTHON
	PYTHON = python
endif

ifndef PKG_MGR
	PKG_MGR = pipenv
endif

ifndef TODO_CMD
	TODO_CMD = todo.sh
endif

ifndef PYTEST_CORES
	PYTEST_CORES = auto
endif

SUBDIR_ROOTS := docs src tests
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := *.pyc *~ *-checkpoint.ipynb *.egg-info __pycache__/
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

ifeq (, $(shell which direnv))
	DIRENV = direnv
else
	DIRENV =
endif

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

    INSTALL_DEPENDENCIES = pipenv install
	INSTALL_DEPENDENCIES_DEV := $(INSTALL_DEPENDENCIES) --dev
	UPDATE_DEPENDENCIES = pipenv update
	UPDATE_DEPENDENCIES_DEV := $(UPDATE_DEPENDENCIES) --dev
    GENERATE_DEPENDENCIES = pipenv lock -r > requirements.txt
	GENERATE_DEPENDENCIES_DEV := $(GENERATE_DEPENDENCIES) && pipenv lock -r --dev > requirements-dev.txt
else
    RUN_PRE =
	VENV_DIR = env

	CREATE_VENV := virtualenv $(VENV_DIR)/
	REMOVE_VENV := rm -rf $(VENV_DIR)

    INSTALL_DEPENDENCIES = pip install -r requirements.txt
	INSTALL_DEPENDENCIES_DEV = pip install -r requirements-dev.txt
	UPDATE_DEPENDENCIES =
	UPDATE_DEPENDENCIES_DEV =
    GENERATE_DEPENDENCIES = pip freeze --local > requirements.txt
	GENERATE_DEPENDENCIES_DEV := $(GENERATE_DEPENDENCIES) > requirements-dev.txt
endif

ACTIVATE_VENV := source $(VENV_DIR)/bin/activate
DEACTIVATE_VENV = deactivate

ifeq ($(MODE), dev)
	INSTALL_DEPS := $(INSTALL_DEPENDENCIES_DEV)
	UPDATE_DEPS := $(UPDATE_DEPENDENCIES_DEV)
	GENERATE_DEPS = $(GENERATE_DEPENDENCIES_DEV)
else
	INSTALL_DEPS := $(INSTALL_DEPENDENCIES)
	UPDATE_DEPS := $(UPDATE_DEPENDENCIES)
	GENERATE_DEPS := $(GENERATE_DEPENDENCIES)
endif

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
        requirements generate-requirements update-requirements \
		-update-requirements-actual \
        docs clean-docs generate-docs \
        clean clean-build \
		authors authors-draft changes changes-draft changelog changelog-draft \
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

clean: ## Delete all compiled Python files or temp files
	@rm -rf $(GARBAGE)

setup: venv-create requirements ## Sets up the environment
	$(if $(DIRENV),$(DIRENV) allow,)

teardown: venv-remove ## Removes the environment
	$(if $(DIRENV),$(DIRENV) deny,)

# Virtual environment

venv-create:
	$(CREATE_VENV)

venv-remove:
	$(REMOVE_VENV)

# Requirements

requirements: ## Installs Python dependencies
	(export PIP_USE_PEP517=false; $(INSTALL_DEPS))

update-requirements: -update-requirements-actual generate-requirements ## Updates the project's dependencies

-update-requirements-actual:
	(export PIP_USE_PEP517=false; $(UPDATE_DEPS))

generate-requirements:
	$(GENERATE_DEPS)

# Documentation

docs: ## Generates the sphinx HTML documentation
	@cd docs/ && $(RUN_PRE) make html

clean-docs: ## Cleans the generated documentation
	@cd docs/ && $(RUN_PRE) make clean

generate-docs: ## Generates the documentation files from the source files
	@cd docs/ && $(RUN_PRE) sphinx-apidoc -e -M -o api ../src/spines
	$(INVOKE) docs.generate-make

# Changes

authors: ## Generates the AUTHORS file
	$(INVOKE) generate.authors

authors-draft: ## Generates the draft AUTHORS file
	$(INVOKE) generate.authors --draft

changes: ## Generates the changes files from the todo files
	$(INVOKE) generate.todos

changes-draft: ## Generates the draft changes from the todo files
	$(INVOKE) generate.todos --draft

changelog: ## Generates the new CHANGELOG.md file
	$(INVOKE) generate.changelog

changelog-draft: ## Generates the draft new CHANGELOG.draft.md file
	$(INVOKE) generate.changelog --draft

# Code

lint: ## Lint using flake8
	$(FLAKE8) src/spines/

coverage: ## Runs code coverage checks over the codebase
	$(PYTEST) --cov=src/spines -n $(PYTEST_CORES)

# Unit testing

test: ## Run the unit tests over the project
	$(PYTEST) -n $(PYTEST_CORES)

test-tox: ## Run the tox unit tests over the project
	$(TOX)

test-watch: ## Run pytest-watch to run tests on project changes
	$(PYTEST) -f -q -n $(PYTEST_CORES)

tox-rebuild: clean ## Rebuilds the tox environments
	$(TOX) --recreate --notest

# Distribution

build: clean-build ## Builds the library package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

check-build: ## Check the built packages prior to uploading
	$(TWINE) check dist/*

clean-build: ## Clean out the compiled package files
	@rm -rf build/*
	@rm -rf dist/*

upload: ## Uploads the package to the PyPI server
	$(TWINE) upload dist/*
