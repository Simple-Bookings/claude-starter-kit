"""csk doctor — Check environment readiness."""

import shutil
import subprocess
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


def check_command(cmd: str, version_flag: str = "--version") -> tuple[bool, str]:
    """Check if a command exists and get its version."""
    path = shutil.which(cmd)
    if not path:
        return False, "not found"
    try:
        result = subprocess.run(
            [cmd, version_flag],
            capture_output=True,
            text=True,
            timeout=5,
        )
        version = result.stdout.strip() or result.stderr.strip()
        version = version.split("\n")[0][:50]
        return True, version
    except Exception as e:
        return True, f"found at {path}"


def check_claude_config() -> tuple[bool, str]:
    """Check if Claude Code is configured."""
    claude_dir = Path.home() / ".claude"
    if not claude_dir.exists():
        return False, "~/.claude not found"
    settings = claude_dir / "settings.json"
    if settings.exists():
        return True, "configured"
    return True, "directory exists"


@click.command()
def doctor():
    """Check that your environment is ready for CSK2.

    Verifies:
    - Required CLI tools (git, claude, python)
    - Claude Code configuration
    """
    console.print("\n[bold cyan]CSK2 Environment Check[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Check", style="dim", width=20)
    table.add_column("Status", width=10)
    table.add_column("Details", width=40)

    # Required checks
    required_checks = [
        ("git", *check_command("git")),
        ("claude", *check_command("claude")),
        ("python", *check_command("python3")),
        ("Claude config", *check_claude_config()),
    ]

    all_ok = True
    for name, ok, details in required_checks:
        status = "[green]OK[/green]" if ok else "[red]FAIL[/red]"
        if not ok:
            all_ok = False
        table.add_row(name, status, details)

    console.print(table)

    if all_ok:
        console.print("\n[bold green]All required checks passed![/bold green] You're ready to use CSK2.\n")
        console.print("Next steps:")
        console.print("  [cyan]csk init my-project[/cyan]  — Create a new project")
        console.print("  [cyan]csk exercises[/cyan]        — Start the learning exercises\n")
        raise SystemExit(0)
    else:
        console.print("\n[bold red]Some required checks failed.[/bold red] Please fix the issues above.\n")
        console.print("Installation guides:")
        console.print("  Git:    https://git-scm.com/downloads")
        console.print("  Claude: https://docs.anthropic.com/claude-code/getting-started\n")
        raise SystemExit(1)
