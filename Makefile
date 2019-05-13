.SILENT:

.PHONY: dev
setup:
	pipenv install --python 3.7 --dev

.PHONY: run
test:
	PYTHONPATH=$(CURDIR) pipenv run py.test
