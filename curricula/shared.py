from pathlib import Path
from typing import Iterator

__all__ = ("version", "Paths", "Files")


version = "0.1.0"


class Paths:
    ASSIGNMENT = Path("assignment")
    PROBLEM = Path("problem")
    ARTIFACTS = Path("artifacts")
    INSTRUCTIONS = Path("instructions")
    RESOURCES = Path("resources")
    SOLUTION = Path("solution")
    GRADING = Path("grading")
    ASSETS = Path("assets")

    @classmethod
    def glob_assignments(cls, material_path: Path) -> Iterator[Path]:
        """Provide a unified search for assignments."""

        for path in material_path.joinpath(cls.ASSIGNMENT).glob("*/"):
            if path.is_dir():
                yield path


class Files:
    README = "README.md"
    ASSIGNMENT = "assignment.json"
    PROBLEM = "problem.json"
    GRADING = "grading.json"
    TESTS = "tests.py"
