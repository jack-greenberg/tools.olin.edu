import nox
import tempfile

locations = "tools", "tests", "noxfile.py"
nox.options.sessions = "lint", "safety", "tests"


@nox.session(python=["3.7"])
def tests(session):
    args = ["-ra", "--cov", "-cpyproject.toml"]
    session.run("pytest", *args, external=True)


@nox.session(python=["3.7"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-black", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python="3.7")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python="3.7")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python="3.7")
def coverage(session):
    """Upload coverage data."""
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
