# Release Process

This document describes the release process for TermDash.

TermDash is currently early alpha. Releases should be created only after tests and linting pass.

## Versioning

TermDash uses semantic versioning.

Current version values are stored in:

```text
pyproject.toml
termdash/__init__.py
```

Before creating a release, confirm both files use the same version.

```bash
grep -n "version" pyproject.toml
grep -n "__version__" termdash/__init__.py
```

## Pre-release checklist

Run the full validation suite:

```bash
python3 -m py_compile termdash/cli.py termdash/config.py
ruff check .
pytest
python3 -m build
```

The build command should create:

```text
dist/*.tar.gz
dist/*.whl
```

## Validate package contents

After building, inspect the generated files:

```bash
ls -lh dist
tar -tzf dist/*.tar.gz | head -50
python3 -m zipfile -l dist/*.whl | head -50
```

## Local install validation

Test installing the built wheel in a temporary virtual environment:

```bash
python3 -m venv /tmp/termdash-release-test
source /tmp/termdash-release-test/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install dist/*.whl
termdash
deactivate
rm -rf /tmp/termdash-release-test
```

## GitHub release checklist

1. Update `CHANGELOG.md`.
2. Confirm tests and linting pass.
3. Confirm package build succeeds.
4. Commit version and changelog updates.
5. Create an annotated git tag.
6. Push the tag.
7. Draft and publish a GitHub release.

Example:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

## PyPI publishing status

TermDash is not ready to publish to PyPI yet.

Before publishing, confirm:

- Package metadata is complete
- The package name is available or an alternate name is selected
- Source distribution and wheel builds are valid
- README renders correctly on PyPI
- The CLI works after installing from the built wheel
- Release process is documented
- The project is stable enough for external users

## Name availability

Before publishing, check whether the desired package name is available:

```bash
python3 -m pip index versions termdash
```

If the name is already taken or unsuitable, choose an alternate package name before publishing.
