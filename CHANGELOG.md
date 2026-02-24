# Changelog

## 0.1.0

- Modernize build tooling: Poetry to uv, flake8/black/isort to Ruff
- Drop Python 3.9 support (EOL)
- Add PEP 561 py.typed marker
- Add Dependabot configuration
- Update CI to use astral-sh/setup-uv

## 0.0.3

- Add project metadata for better accessiblity on PyPi.org

## 0.0.2

- Added languages fr, es, it
- Improved language detection

## 0.0.1

- Initial release

## How to release a new version

- Finish development on branch and merge to main
- Update this changelog, bump version number in `pyproject.toml` and commit
- Run

```shell
VERSION=$( grep '^version' pyproject.toml | head -1 | sed 's/.*"\(.*\)"/\1/' ) &&\
echo "Release: ${VERSION}" &&\
git tag -a ${VERSION} -m "Version ${VERSION}" &&\
git push --tags
```

- Create a new release under <https://github.com/BastiTee/kindle-to-markdown/releases>
- Push to PyPi

```shell
uv publish
```
