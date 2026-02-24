# Kindle Annotations to Markdown

> A simple program to convert Kindle HTML annotations to a Markdown file

![](https://img.shields.io/pypi/v/kindle-to-markdown)
![](https://img.shields.io/pypi/pyversions/kindle-to-markdown)

## Features

-   Conversion of page bookmarks, text highlights, and notes to Markdown
-   Included reference positions of annotations
-   Automatic detection of annotation file's language ([currently supported](kindle_to_markdown/languages.py))

## Usage

```shell
$ kindle_to_markdown --help
Usage: python -m kindle_to_markdown [OPTIONS]

  A simple program to convert Kindle HTML annotations to a Markdown file.

Options:
  -i, --input-file PATH   Path to the Kindle annotations HTML file.
                          [required]
  -o, --output-file PATH  Path to the Markdown file.
  -p, --print-only        Only print Markdown to the console.
  -s, --suppress-pages    Suppress page references in output.
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
-   Package manager `uv` installed (see [uv installation](https://docs.astral.sh/uv/getting-started/installation/))

```shell
make
uv run python -m kindle_to_markdown --help
```
