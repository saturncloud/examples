SHELL=/bin/bash

.PHONY: check-links
check-links:
	./.ci/check-links.sh $$(pwd)

.PHONY: format
format:
	black .

.PHONY: validate
validate:
	python .ci/validate-examples.py --examples-dir $$(pwd)/examples

.PHONY: lint
lint: validate
	black --check --diff .
	flake8 --count .
	nbqa flake8 .

.PHONY: test
test: lint
