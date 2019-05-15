.SILENT:

.PHONY: clean
clean:
	find . \( -iname "*.pyc" -o -iname "__pycache__" \) -print0 | xargs -0 rm -rf
	-rm -rf .eggs *.egg-info/ .coverage build/ .cache

.PHONY: setup
setup:
	pipenv install --python 3.7 --dev

.PHONY: run
test:
	PYTHONPATH=$(CURDIR) pipenv run py.test
