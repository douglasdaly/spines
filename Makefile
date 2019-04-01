###############################################################################
# CONFIGURATION                                                               #
###############################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

PYTHON = python
PKG_MGR = pipenv


###############################################################################
# SETUP                                                                       #
###############################################################################

SUBDIR_ROOTS := docs spines tests
DIRS := . $(shell find $(SUBDIR_ROOTS) -type d)
GARBAGE_PATTERNS := *.pyc *~ *-checkpoint.ipynb
GARBAGE := $(foreach DIR,$(DIRS),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

FLAKE8 = flake8
UNIT_TEST = pytest

ifeq ($(PKG_MGR), pipenv)
    RUN_PRE = pipenv run
    INSTALL_DEPENDENCIES = pipenv install
    GENERATE_DEPENDENCIES = pipenv lock -r > requirements.txt
else
    RUN_PRE =
    INSTALL_DEPENDENCIES = pip install -r requirements.txt
    GENERATE_DEPENDENCIES = pip freeze --local > requirements.txt
endif

PYTHON := $(RUN_PRE) $(PYTHON)
FLAKE8 := $(RUN_PRE) $(FLAKE8)
UNIT_TEST := $(RUN_PRE) $(UNIT_TEST)

###############################################################################
# COMMANDS                                                                    #
###############################################################################
.PHONY: help \
        requirements requirements-generate \
        docs docs-clean \
        clean lint test

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
	@cd docs/ && $(RUN_PRE) sphinx-apidoc -e -M -o api ../spines

# Code

clean: ## Delete all compiled Python files or temp files
	@rm -rf $(GARBAGE)

lint: ## Lint using flake8
	$(FLAKE8) spines/

coverage: ## Runs code coverage checks over the codebase
	$(UNIT_TEST) --cov=spines tests/

test: ## Run the unit tests over the project
	$(UNIT_TEST) tests/
