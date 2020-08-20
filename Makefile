.PHONY: format
format:
	black --line-length 100 .

.PHONY: lint
lint:
	flake8 --count --max-line-length 100 .
	black --check --diff --line-length 100 .

.PHONY: validate
validate:
	python .ci/validate-examples.py --examples-dir $$(pwd)/examples

.PHONY: test
test: format lint validate
