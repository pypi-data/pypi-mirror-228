PROJECT_DIR := pesapal_v3

.PHONY: format build test

format:
	yapf -rmi ${PROJECT_DIR}

build:
	@echo "Running yapf" && black ${PROJECT_DIR}
	@echo "Running isort" && isort ${PROJECT_DIR}
	@echo "Running pylint" && pylint ${PROJECT_DIR} --disable=W
	@echo "Running mypy" && mypy ${PROJECT_DIR}

test:
	@echo "Running test" && pytest tests