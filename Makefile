SHELL := /bin/bash
.PHONY: help docs mypy test test-coverage publish

help:
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

docs: ## Generate documents
	cp README.md docs/index.md
	poetry run mkdocs build
	rm docs/index.md

mypy: ## Static type checking
#   Skipping other directories, such as init_script
	poetry run mypy octopus_sensing

test: ## Runs tests
	poetry run pytest --full-trace --showlocals

test-coverage: ## Runs tests and reports coverage
	poetry run coverage run -m pytest --full-trace --showlocals
	poetry run coverage report

# TODO: PyPi publish
#publish: ## Publishes to PyPi
#publish: mypy test
#	update version
#   commit
#	tag
#	push tag
#	poetry publish
