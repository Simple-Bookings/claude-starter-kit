"""Locate CSK data directories in both repo and pip-installed layouts.

When running from a git clone (or `pip install -e .`), data directories
(templates/, workshop/, exercises/, .claude/agents/) live at the repo root.

When installed from a wheel, they are bundled inside the package at
csk/_data/ (see [tool.hatch.build.targets.wheel.force-include] in
pyproject.toml).
"""

from pathlib import Path

_PACKAGE_DIR = Path(__file__).parent
_REPO_ROOT = _PACKAGE_DIR.parent
_BUNDLED_DATA = _PACKAGE_DIR / "_data"


def find_data_dir(name: str) -> Path | None:
    """Return the path to a data directory, or None if not found.

    Checks the repo layout first (git clone / editable install),
    then the bundled package data (wheel install).
    """
    repo_path = _REPO_ROOT / name
    if repo_path.is_dir():
        return repo_path

    bundled_path = _BUNDLED_DATA / name
    if bundled_path.is_dir():
        return bundled_path

    return None


def templates_dir() -> Path | None:
    """Project templates (skills, rules, CLAUDE.md, etc.)."""
    return find_data_dir("templates")


def workshop_dir() -> Path | None:
    """Workshop materials (slides, kompendium, presenter, handout)."""
    return find_data_dir("workshop")


def exercises_dir() -> Path | None:
    """Hands-on exercise markdown files."""
    return find_data_dir("exercises")


def agents_dir() -> Path | None:
    """Agent profile markdown files."""
    repo_path = _REPO_ROOT / ".claude" / "agents"
    if repo_path.is_dir():
        return repo_path

    bundled_path = _BUNDLED_DATA / "agents"
    if bundled_path.is_dir():
        return bundled_path

    return None
