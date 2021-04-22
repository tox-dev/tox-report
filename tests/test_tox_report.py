"""Tests for tox-report."""
import types


def test_import() -> None:
    """Validated that we can import."""
    # pylint: disable=import-outside-toplevel
    from tox_report.hooks import tox_cleanup

    assert isinstance(tox_cleanup, types.FunctionType)
