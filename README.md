# Kindle Annotations to Markdown

> A simple program to convert Kindle HTML annotations to a Markdown file

## Features

-   Conversion of page bookmarks, text highlights, and notes to Markdown
-   Included reference positions of annotations
-   Automatic detection of annotation file's language (currently supported: en, de)

## Usage

```shell
$ kindle_to_markdown --help
Usage: kindle_to_markdown [OPTIONS]

  A simple program to convert Kindle HTML annotations to a Markdown file.

Options:
  -i, --input-file PATH   Path to the Kindle annotations HTML file.
                          [required]
  -o, --output-file PATH  Path to the Markdown file.
  -p, --print-only        Only print Markdown to the console.
  --help                  Show this message and exit.
```

## Installation

### From PyPi

```shell
pip install kindle-to-markdown
```

### From Source

Prerequisites:

-   `python` in a [supported version](pyproject.toml) available on your path.
-   Package manager `poetry` installed (e.g., `python -m pip install poetry`)

```shell
make
poetry run python -m kindle_to_markdown --help
```
