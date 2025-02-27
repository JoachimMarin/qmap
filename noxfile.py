from __future__ import annotations

import os

import nox
from nox.sessions import Session

nox.options.sessions = ["lint", "tests"]

PYTHON_ALL_VERSIONS = ["3.8", "3.9", "3.10", "3.11"]

if os.environ.get("CI", None):
    nox.options.error_on_missing_interpreters = True


@nox.session(python=PYTHON_ALL_VERSIONS)
def tests(session: Session) -> None:
    """
    Run the test suite.
    Simply execute `nox -rs tests` to run all tests.
    Run as `nox -rs tests -- skip-install` to skip installing the package and its dependencies.
    """
    run_install = True
    if session.posargs and "skip-install" in session.posargs:
        run_install = False
        session.posargs.remove("skip-install")
    if run_install:
        session.install("-e", ".[test]")
    session.run("pytest", *session.posargs)


@nox.session(python=PYTHON_ALL_VERSIONS)
def coverage(session: Session) -> None:
    """
    Run the test suite and generate a coverage report.
    Simply execute `nox -rs coverage -- --cov-report=html` to generate a HTML report.
    Run as `nox -rs coverage -- skip-install` to skip installing the package and its dependencies.
    """
    run_install = True
    if session.posargs and "skip-install" in session.posargs:
        run_install = False
        session.posargs.remove("skip-install")
    if run_install:
        session.install("-e", ".[coverage]")
    session.run("pytest", "--cov", *session.posargs)


@nox.session()
def min_qiskit_version(session: Session) -> None:
    """
    Installs the minimum supported version of Qiskit, runs the test suite and collects the coverage.
    """
    session.install("qiskit-terra~=0.20.2")
    session.install("-e", ".[coverage]")
    session.run("pip", "show", "qiskit-terra")
    session.run("pytest", "--cov", *session.posargs)


@nox.session
def lint(session: Session) -> None:
    """
    Lint the Python part of the codebase using pre-commit.
    Simply execute `nox -rs lint` to run all configured hooks.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session
def pylint(session: Session) -> None:
    """
    Run pylint.
    Simply execute `nox -rs pylint` to run pylint.
    Run as `nox -rs pylint -- skip-install` to skip installing the package and its dependencies.
    """
    session.install("pylint")
    run_install = True
    if session.posargs and "skip-install" in session.posargs:
        run_install = False
        session.posargs.remove("skip-install")
    if run_install:
        session.install("-e", ".")
    session.run("pylint", "mqt.qmap", "--extension-pkg-allow-list=mqt.qmap.pyqmap", *session.posargs)


@nox.session
def mypy(session: Session) -> None:
    """
    Run mypy.
    Simply execute `nox -rs mypy` to run mypy.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "mypy", "--all-files", *session.posargs)


@nox.session
def docs(session: Session) -> None:
    """
    Build the documentation.
    Simply execute `nox -rs docs -- serve` to locally build and serve the docs.
    Run as `nox -rs docs -- skip-install` to skip installing the package and its dependencies.
    """
    run_install = True
    if session.posargs and "skip-install" in session.posargs:
        run_install = False
        session.posargs.remove("skip-install")
    if run_install:
        session.install("-e", ".[docs]")
    session.chdir("docs")
    session.run("sphinx-build", "-M", "html", "source", "_build")

    if session.posargs:
        if "serve" in session.posargs:
            print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
            session.run("python", "-m", "http.server", "8000", "-d", "_build/html")
        else:
            print("Unsupported argument to docs")
