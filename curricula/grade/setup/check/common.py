from typing import Optional
from pathlib import Path

from curricula.grade.resource import Buffer
from . import CheckResult

__all__ = ("check_file_exists", "check_makefile_exists", "search_file_by_name")


def check_file_exists(*paths: Path, log: Buffer = None) -> CheckResult:
    """Check if a file is present in the directory."""

    if not any(path.exists() for path in paths):
        log and log[2](f"Can't find {paths[0].parts[-1]}!")
        return CheckResult(passed=False, error=f"can't find {paths[0].parts[-1]}")

    log and log[2](f"Found {paths[0].parts[-1]}")
    return CheckResult(passed=True)


def check_makefile_exists(path: Path, log: Buffer = None) -> CheckResult:
    """Check whether there is a makefile in a directory."""

    lower_path = path.joinpath("makefile")
    upper_path = path.joinpath("Makefile")

    if not lower_path.exists() and not upper_path.exists():
        log and log[2](f"Can't find {upper_path.parts[-1]}!")
        return CheckResult(passed=False, error=f"can't find {upper_path.parts[-1]}")

    log and log[2](f"Found {upper_path.parts[-1]}")
    return CheckResult(passed=True)


def search_file_by_name(name: str, path: Path) -> Optional[Path]:
    """Find file by name, None if none or multiple."""

    results = tuple(path.glob(f"**/{name}"))
    if len(results) == 1:
        return results[0]
    return None
