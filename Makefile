.SILENT:
.DEFAULT_GOAL := help

.PHONY: help
help:
	$(info Available targets:)
	$(info | help  Show this help message)
	$(info | setup Install the prod and test dependencies)
	$(info | clean Clean build, cache and coverage files)
	$(info | test  Run the tests)

.PHONY: clean
clean:
	find . \( -iname "*.pyc" -o -iname "__pycache__" -o -iname ".hypothesis" \) -print0 | xargs -0 rm -rf
	-rm -rf .eggs *.egg-info/ .coverage build/ .cache .pytest_cache

.PHONY: setup
setup:
	pipenv install --python 3.7 --dev

.PHONY: run
test:
	PYTHONPATH=$(CURDIR) pipenv run py.test

%:
	echo "Target not found!"
	make help
