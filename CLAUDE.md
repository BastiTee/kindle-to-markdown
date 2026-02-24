# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

kindle-to-markdown is a Python CLI tool that converts Kindle HTML annotation/highlight exports into Markdown. It supports multiple languages (en, de, fr, it, es) via data-driven keyword dictionaries.

## Build & Development Commands

Uses **uv** for dependency management and a **Makefile** for orchestration. Virtual env is created in-project at `.venv/`.

```shell
make              # Full pipeline: clean → venv → build (includes test, mypy, lint, format-check)
make venv         # Clean install of dependencies
make test         # Run all tests: uv run py.test tests
make lint         # Ruff linting
make lint-fix     # Ruff linting with auto-fix
make format       # Format code with Ruff
make format-check # Check code formatting with Ruff
make mypy         # Static type checking
make run-venv     # Run the CLI: uv run python -m kindle_to_markdown
```

Run a single test:
```shell
uv run py.test tests/test_code.py::TestCode::test_extract_note_heading
```

## Architecture

The project has three source files total:

- **`kindle_to_markdown/__main__.py`** — All core logic and CLI entry point. Parses Kindle HTML using BeautifulSoup (selecting elements by CSS classes like `bookTitle`, `noteHeading`, `noteText`, `sectionHeading`), detects language automatically by matching heading keywords against known dictionaries, cleans Unicode text via regex, and outputs Markdown. CLI uses Click.

- **`kindle_to_markdown/languages.py`** — `SUPPORTED_LANGUAGES` dict mapping language codes to Kindle annotation keywords (`textmark`, `note`, `bookmark`, `page`, `position`). Adding a new language only requires a new entry here.

- **`tests/test_code.py`** — All tests in a single `TestCode` class. Uses HTML fixture files in `tests/res/` (one per supported language plus one for unsupported-language error testing).

## Code Style

- **Ruff** for linting and formatting, line length 88, `quote-style = "preserve"` (single quotes preserved)
- **mypy** strict mode (`disallow_untyped_defs`, `check_untyped_defs`)
- 4-space indentation (tabs for Makefile)
