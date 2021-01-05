.PHONY: format
format:
	black --line-length 100 .
	python .ci/format-notebooks.py

.PHONY: validate
validate:
	python .ci/validate-examples.py --examples-dir $$(pwd)/examples

.PHONY: lint
lint: validate
	flake8 --count --max-line-length 100 .
	black --check --diff --line-length 100 .

.PHONY: test
test: lint
