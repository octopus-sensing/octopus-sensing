SHELL := /bin/bash
.PHONY: help docs mypy test test-coverage publish

# Extract optional device dependencies from pyproject.toml via Poetry environment
DEVICES_DEPENDENCIES := $(shell poetry run python scripts/get_devices_dependencies.py)

help:
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

mypy: ## Static type checking
#   Skipping other directories, such as init_script
	poetry run mypy octopus_sensing

test: ## Runs tests
# Integration test mocks lots of modules which intefer with other tests. So, we're running it separately.
	poetry run pytest --full-trace --showlocals octopus_sensing/
	poetry run pytest --full-trace --showlocals octopus_sensing/tests/integration.py

test-coverage: ## Runs tests and reports coverage
# See 'test' comment for why we're running two commands.
	poetry run coverage run -m pytest --full-trace --showlocals octopus_sensing/
	poetry run coverage run --append -m pytest --full-trace --showlocals octopus_sensing/tests/integration.py
	poetry run coverage xml
	poetry run coverage report

install: ## Installs all dependencies, including optional device dependencies
	poetry sync --all-groups
	poetry run pip install ".[$(DEVICES_DEPENDENCIES)]"

build: ## Builds the package
	poetry check
	poetry build

# TODO: Automate this.
# For now, see the development.rst file for instructions.
#publish: ## Publishes to PyPi

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs_build

docs: ## Build the documents. Output will be './docs_build'
docs: install
	poetry run $(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

docs-latex: ## Build the documents in LaTeX format.
docs-latex: install
	poetry run $(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
