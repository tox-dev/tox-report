"""Tests for tox-report."""

import os
import subprocess
import sys
import types
from pathlib import Path

import pytest


def test_import() -> None:
    """Validated that we can import."""
    # pylint: disable=import-outside-toplevel
    from tox_report.hooks import tox_cleanup

    assert isinstance(tox_cleanup, types.FunctionType)


@pytest.mark.parametrize(
    "filename",
    [
        pytest.param("report.html", id="ascii"),
        pytest.param("résumé.html", id="unicode"),
    ],
)
def test_html_report(tmp_path: Path, filename: str) -> None:
    """Keep report generation working with non-ASCII paths and output."""
    config = tmp_path / "tox.ini"
    config.write_text(
        "[tox]\nskipsdist = true\nenvlist = report\n[testenv]\nskip_install = true\n"
        "commands = python -c \"print('café')\"\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "-m", "tox", "-c", str(config), "--html", filename],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )
    assert (
        f"Report generated to {os.path.abspath(tmp_path / filename)}" in result.stdout
    )
    assert "café" in (tmp_path / filename).read_text(encoding="utf-8")
