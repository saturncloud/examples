SHELL=/bin/bash

.PHONY: check-links
check-links:
	./.ci/check-links.sh $$(pwd)

.PHONY: format
format:
	black .
	nbqa black . --nbqa-mutate

.PHONY: validate
validate:
	python .ci/validate-examples.py --examples-dir $$(pwd)/examples

.PHONY: lint
lint: validate
	black --check --diff .
	diff_lines=$$(nbqa black --nbqa-diff . | wc -l); \
	if [ $${diff_lines} -gt 0 ]; then \
		echo "Some notebooks would be reformatted by black. Run 'make format' and try again."; \
		exit 1; \
	fi
	flake8 --count .
	nbqa flake8 .

.PHONY: test
test: lint
