import sys
import shutil
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent.parent))
from grade.shortcuts import *
from grade.library import valgrind
from grade.library import process

grader = Grader()
root = Path(__file__).absolute().parent


def overwrite_directory(path: Path):
    if path.exists():
        shutil.rmtree(str(path))
    path.mkdir()


@grader.check(required=True)
def check_program(context: Context, log: Logger):
    """Check if the program has been submitted."""

    if not context.target.joinpath("program.cpp").exists():
        return CheckResult(False, error="missing file test.cpp")
    log[2]("Found program.cpp")
    return CheckResult(True)


@grader.build(required=True)
def build_program(context: Context, log: Logger):
    """Compile program with GCC."""

    source = context.target.joinpath("program.cpp")
    build = root.joinpath("build")
    overwrite_directory(build)
    executable = build.joinpath("program")

    runtime = process.run("g++", "-Wall", "-o", str(executable), str(source), timeout=5)
    if runtime.code != 0:
        return BuildResult(False, error="failed to build program")

    log[2]("Successfully built program")
    return BuildResult(True, Executable(str(executable)), inject="program")


@grader.test()
def test_memory(program: Executable):
    """Check memory leakage."""

    return MemoryResult.from_valgrind_report(valgrind.run(program.args[0], timeout=2))


if __name__ == "__main__":
    from grade.shell import main
    main(grader)
