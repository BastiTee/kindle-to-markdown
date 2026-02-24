# Required executables
ifeq (, $(shell which python))
 $(error "No python on PATH.")
endif
ifeq (, $(shell which uv))
 $(error "No uv on PATH.")
endif

export LC_ALL = C
export LANG = C.UTF-8
PY_FILES := kindle_to_markdown tests

.PHONY: all clean clear-cache venv build test mypy lint lint-fix format \
	format-check outdated run-venv install update help

.DEFAULT_GOAL := all

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Bundle tasks

all: clean venv build ## Full pipeline: clean, venv, build

# Clean up and set up

clean: ## Remove generated files and caches
	find . -type d \
	-name ".venv" -o \
	-name ".tox" -o \
	-name ".ropeproject" -o \
	-name ".mypy_cache" -o \
	-name ".pytest_cache" -o \
	-name ".ruff_cache" -o \
	-name "__pycache__" -o \
	-iname "*.egg-info" -o \
	-name "build" -o \
	-name "dist" \
	|xargs rm -rfv

clear-cache: ## Clear uv cache
	uv cache clean

venv: clean ## Install dependencies into .venv
	uv sync

# Building software

build: test mypy lint format-check ## Run tests, checks, and package
	uv build

test: ## Run all test suites
	uv run py.test tests

mypy: ## Run static type checks
	uv run mypy $(PY_FILES)

lint: ## Run linting with Ruff
	uv run ruff check $(PY_FILES)

lint-fix: ## Run linting with Ruff and auto-fix
	uv run ruff check --fix $(PY_FILES)

format: ## Format code with Ruff
	uv run ruff format $(PY_FILES)

format-check: ## Check code formatting with Ruff
	uv run ruff format --check $(PY_FILES)

outdated: ## Show outdated dependencies
	uv pip list --outdated --exclude-editable

update: ## Update all dependencies
	uv sync --upgrade

# Executing

run-venv: ## Execute package in virtual environment
	uv run python -m kindle_to_markdown

install: ## Install package using activated Python env
	python -m pip install --upgrade .
