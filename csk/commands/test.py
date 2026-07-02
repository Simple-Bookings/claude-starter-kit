"""csk test — Run E2E tests for CSK2."""

import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--coverage", is_flag=True, help="Run with coverage report")
def test(verbose: bool, coverage: bool):
    """Run E2E tests for CSK2.

    Tests verify that all CSK2 commands work correctly:
    - csk doctor
    - csk init
    - csk exercises
    - csk progress

    Example:

        csk test              # Run all tests
        csk test -v           # Verbose output
        csk test --coverage   # With coverage report
    """
    console.print("\n[bold cyan]Running CSK2 Tests[/bold cyan]\n")

    tests_dir = Path(__file__).parent.parent.parent / "tests"

    if not tests_dir.exists():
        console.print(f"[red]Error:[/red] Tests directory not found: {tests_dir}")
        raise SystemExit(1)

    cmd = [sys.executable, "-m", "pytest", str(tests_dir)]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=csk", "--cov-report=term-missing"])

    console.print(f"[dim]Running: {' '.join(cmd)}[/dim]\n")

    result = subprocess.run(cmd)
    raise SystemExit(result.returncode)
