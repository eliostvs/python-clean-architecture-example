ifeq ($(origin .RECIPEPREFIX), undefined)
	$(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif

.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.ONESHELL:
.SHELLFLAGS   := -eu -o pipefail -c
.SILENT:
MAKEFLAGS     += --no-builtin-rules
MAKEFLAGS     += --warn-undefined-variables
SHELL         = bash

.PHONY: help
help:
	$(info Available targets:)
	$(info | help    Show this help message)
	$(info | setup   Install the prod and test dependencies)
	$(info | clean   Clean build, cache and coverage files)
	$(info | format  Format files using black)
	$(info | test    Run tests)

.PHONY: setup
setup:
	poetry install

.PHONY: clean
clean:
	find . \( -iname "__pycache__" -o -iname ".hypothesis" \) -print0 | xargs -0 rm -rf
	-rm -rf .eggs *.egg-info/ .coverage build/ .cache .pytest_cache

.PHONY: format
format:
	poetry run black example tests

.PHONY: test
test:
	PYTHONPATH=$(CURDIR) poetry run py.test

%:
	echo "Target not found!"
	make help
