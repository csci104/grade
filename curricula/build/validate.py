import json
import jsonschema
import sys
from pathlib import Path

from .models import Assignment
from ..shared import *
from ..log import log

root = Path(__file__).absolute().parent

with root.joinpath("schema", "assignment.schema.json").open() as _file:
    ASSIGNMENT_SCHEMA = json.load(_file)
with root.joinpath("schema", "problem.schema.json").open() as _file:
    PROBLEM_SCHEMA = json.load(_file)


def validate_json(path: Path, schema: dict):
    """Run actual validation."""

    with path.open() as file:
        problem_json = json.load(file)

    try:
        jsonschema.validate(problem_json, schema)
    except jsonschema.ValidationError as e:
        log.error(f"invalid schema in {path}")
        print(e, file=sys.stderr)
        raise


def validate_problem_json(problem_path: Path):
    """Validate with jsonschema."""

    validate_json(problem_path.joinpath(Files.PROBLEM), PROBLEM_SCHEMA)


def validate_assignment_json(assignment_path: Path):
    """Validate with jsonschema."""

    validate_json(assignment_path.joinpath(Files.ASSIGNMENT), ASSIGNMENT_SCHEMA)

    assignment = Assignment.load(assignment_path)
    for problem in assignment.problems:
        validate_problem_json(problem.path)


def validate_assignment(assignment_path: Path):
    """Validators per assignment."""

    validate_assignment_json(assignment_path)


def validate(assignment_path: Path):
    """Do a bunch of checks """

    validate_assignment(assignment_path)
