import importlib.util
import json
import sys
from typing import Dict, List, Iterable, Iterator, Tuple
from pathlib import Path
from dataclasses import dataclass

from .grader import Grader
from .report import Report
from .resource import Context
from ..mapping.shared import *
from ..mapping.models import Problem


def import_grader(tests_path: Path, grader_name: str = "grader") -> Grader:
    """Import a grader from a tests file."""

    sys.path.insert(0, str(tests_path.parent))
    spec = importlib.util.spec_from_file_location(f"{tests_path.parent}.tests", str(tests_path))
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
    grader = getattr(tests, grader_name)
    sys.path.pop(0)

    return grader


def generate_grading_schema(grading_path: Path, problems: List[Problem]) -> dict:
    """Generate a JSON schema describing the grading package.

    This method requires the grading artifact to already have been
    aggregated, as it has to access the individual problem graders to
    dump their task summaries.
    """

    result = {}
    for problem in problems:
        grader = import_grader(grading_path.joinpath(problem.short, Files.TESTS))
        result[problem.short] = dict(percentage=problem.percentage, tasks=grader.dump())
    return result


MISSED = {'amanosme', 'amalcolm', 'hern784', 'doh732', 'emanning', 'smcneely', 'ebork', 'hanjeffr', 'liu861', 'conormcc', 'zhuanzhl', 'sagartiw', 'kexinw', 'edelheal', 'daerowon', 'bmorehou', 'kakooza', 'udasgupt', 'hannaho', 'johncand', 'roycechu', 'andrewfw', 'ujwalgup', 'mitraarj', 'zhianli', 'roost', 'maryowen', 'patricjk', 'ddrain', 'binwu', 'bmrollin', 'varanasi', 'najensen', 'jliu6011', 'junyou', 'kim257', 'taylorri', 'concho'}


@dataclass
class Manager:
    """A container for multiple graders in an assignment."""

    graders: Dict[str, Grader]

    @classmethod
    def load(cls, grading_path: Path) -> "Manager":
        """Load a manager from a grading artifact in the file system."""

        with grading_path.joinpath(Files.GRADING).open() as file:
            schema = json.load(file)

        graders = {}
        for problem_short in schema:
            graders[problem_short] = import_grader(grading_path.joinpath(problem_short, Files.TESTS))

        return Manager(graders)

    def run(self, target_path: Path, **options) -> Dict[str, Report]:
        """Run all tests on a submission and return a dict of results."""

        reports = {}
        for problem_short, grader in self.graders.items():
            context = Context(target_path, **options)
            reports[problem_short] = grader.run(context=context)
        return reports

    def run_batch(self, target_paths: Iterable[Path], **options) -> Iterator[Tuple[Path, Dict[str, Report]]]:
        """Run multiple reports, map directory to report."""

        report_tree = {}
        for target_path in target_paths:
            if target_path.parts[-1] in MISSED:
                yield target_path, self.run(target_path, **options)
        return report_tree
