"""Tox hook implementations."""

import io
import os
from typing import TYPE_CHECKING

from rich.console import Console
from tox import hookimpl

if TYPE_CHECKING:
    from tox.config import Parser
    from tox.session import Session
    from tox.venv import VirtualEnv

console = Console(record=True, file=io.StringIO())
console.print("Recording started", style="bold red")


@hookimpl
def tox_addoption(parser: "Parser") -> None:
    """Add --html option."""
    parser.add_argument(
        "--html",
        dest="html_report",
        default="report.html",
        help="Path towards where it should save the HTML report of the execution",
    )


@hookimpl
def tox_configure() -> None:
    """Configure hook."""
    console.print("Reporting mode enabled", style="bold red")


@hookimpl
def tox_runtest_post(venv: "VirtualEnv") -> None:
    """runtest hook."""
    collect_data(venv)


@hookimpl
def tox_cleanup(session: "Session") -> None:
    """cleanup hook."""
    console.print("Recording stopped", style="bold red")

    html = console.export_html(inline_styles=True)
    filename = session.config.option.html_report
    if filename:
        with open(filename, "w", encoding="utf-8") as report_handler:
            report_handler.write(html)
            print(f"Report generated to {os.path.abspath(report_handler.name)}")


def collect_data(current_venv: "VirtualEnv") -> None:
    """Record data for the report."""
    console.print(current_venv.env_log.reportlog.dict)


__all__ = ["tox_addoption", "tox_cleanup", "tox_configure", "tox_runtest_post"]
