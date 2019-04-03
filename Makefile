###############################################################################
# CONFIGURATION                                                               #
###############################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

PYTHON = python
PKG_MGR = pipenv


###############################################################################
# SETUP                                                                       #
###############################################################################

SUBDIR_ROOTS := docs src tests
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := *.pyc *~ *-checkpoint.ipynb
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

FLAKE8 = flake8
UNIT_TEST = pytest
TWINE = twine

ifeq ($(PKG_MGR), pipenv)
    RUN_PRE = pipenv run
    INSTALL_DEPENDENCIES = pipenv install --dev
    GENERATE_DEPENDENCIES = pipenv lock --dev -r > requirements.txt
else
    RUN_PRE =
    INSTALL_DEPENDENCIES = pip install -r requirements.txt
    GENERATE_DEPENDENCIES = pip freeze --local > requirements.txt
endif

PYTHON := $(RUN_PRE) $(PYTHON)
FLAKE8 := $(RUN_PRE) $(FLAKE8)
UNIT_TEST := $(RUN_PRE) $(UNIT_TEST)
TWINE := $(RUN_PRE) $(TWINE)

###############################################################################
# COMMANDS                                                                    #
###############################################################################
.PHONY: help \
        requirements requirements-generate \
        docs docs-clean \
        clean clean-build \
		changelog changelog-draft \
		lint coverage \
		test \
		build check-build release

.DEFAULT-GOAL := help

help: ## Displays this help message
	@printf 'Usage: make \033[36m[target]\033[0m\n'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ''

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

docs-apigen: ## Generates the API documentation files
	@cd docs/ && $(RUN_PRE) sphinx-apidoc -e -M -o api ../src/spines

# Cleaning

clean: ## Delete all compiled Python files or temp files
	@rm -rf $(GARBAGE)

clean-build: ## Clean out the compiled package files
	@rm -rf build/*.*
	@rm -rf dist/*.*

# Changes

changelog: ## Generates the new CHANGELOG.md file
	$(PYTHON) invoke release.changelog

changelog-draft: ## Generates the draft new CHANGELOG.draft.md file
	$(PYTHON) invoke release.changelog --draft

# Code

lint: ## Lint using flake8
	$(FLAKE8) src/spines/

coverage: ## Runs code coverage checks over the codebase
	$(UNIT_TEST) --cov=src/spines tests/

# Unit testing

test: ## Run the unit tests over the project
	$(UNIT_TEST) tests/

# Distribution

build: clean-build ## Builds the library package
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls dist/

check-build: ## Check the ubilt packages prior to uploading
	$(TWINE) check dist/*

upload: ## Uploads the package to the PyPI server
	$(TWINE) upload dist/*
