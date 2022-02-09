SHELL=/bin/bash

.PHONY: check-links
check-links:
	./.ci/check-links.sh $$(pwd)

.PHONY: install
install:
	pip install --upgrade black[jupyter] flake8 nbqa requests jsonschema 

.PHONY: templates.json
templates.json:
	python .ci/generate-templates.py

.PHONY: format
format:
	black .

.PHONY: validate
validate:
	python .ci/validate-examples.py --examples-dir $$(pwd)/examples --skip-image-check

.PHONY: lint
lint:
	black --check --diff .
	flake8 --count .
	nbqa flake8 .

.PHONY: test
test: lint
