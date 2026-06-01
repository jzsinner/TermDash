"""Basic package tests for TermDash."""

import importlib


def test_package_imports() -> None:
    """The termdash package should import successfully."""
    module = importlib.import_module("termdash")
    assert module is not None


def test_cli_module_imports() -> None:
    """The CLI module should import successfully."""
    module = importlib.import_module("termdash.cli")
    assert module is not None


def test_package_has_version() -> None:
    """The package should expose a version string."""
    module = importlib.import_module("termdash")
    assert hasattr(module, "__version__")
    assert isinstance(module.__version__, str)
    assert module.__version__