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
	@echo Executed default build pipeline

# Clean up and set up

clean: ## Remove generated files and caches
	@echo Clean project base
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
	@echo Clear uv cache
	uv cache clean

venv: clean ## Install dependencies into .venv
	@echo Initialize virtualenv, i.e., install required packages etc.
	uv sync

# Building software

build: test mypy lint format-check ## Run tests, checks, and package
	@echo Run build process to package application
	uv build

test: ## Run all test suites
	@echo Run all tests suites
	uv run py.test tests

mypy: ## Run static type checks
	@echo Run static code checks against source code base
	uv run mypy $(PY_FILES)

lint: ## Run linting with Ruff
	@echo Run linting checks against source code base
	uv run ruff check $(PY_FILES)

lint-fix: ## Run linting with Ruff and auto-fix
	@echo Run linting checks and fix issues
	uv run ruff check --fix $(PY_FILES)

format: ## Format code with Ruff
	@echo Format code with Ruff
	uv run ruff format $(PY_FILES)

format-check: ## Check code formatting with Ruff
	@echo Check code formatting with Ruff
	uv run ruff format --check $(PY_FILES)

outdated: ## Show outdated dependencies
	@echo Show outdated dependencies
	uv pip list --outdated --exclude-editable

update: ## Update all dependencies
	@echo Update all dependencies
	uv sync --upgrade

# Executing

run-venv: ## Execute package in virtual environment
	@echo Execute package directly in virtual environment
	uv run python -m kindle_to_markdown

install: ## Install package using activated Python env
	@echo Install package using the activated Python env
	python -m pip install --upgrade .
