"""CSK upgrade command — check for and install updates from GitHub."""

import json
import subprocess
import sys
import urllib.request
from importlib.metadata import version

import click
from rich.console import Console
from rich.panel import Panel

console = Console()

GITHUB_REPO = "Simple-Bookings/claude-starter-kit"
GIT_INSTALL_URL = f"git+https://github.com/{GITHUB_REPO}.git"


def get_current_version() -> str:
    """Get the currently installed version."""
    try:
        return version("claude-starter-kit")
    except Exception:
        return "0.0.0"


def get_latest_version() -> str | None:
    """Check GitHub for the latest released version."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            tag = data.get("tag_name", "")
            return tag.lstrip("v") if tag else None
    except Exception:
        return None


def upgrade_package() -> bool:
    """Upgrade the package from GitHub using pip."""
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                GIT_INSTALL_URL,
                "--quiet",
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        return result.returncode == 0
    except Exception:
        return False


@click.command()
@click.option("--check", is_flag=True, help="Only check for updates, don't install")
@click.option("-y", "--yes", is_flag=True, help="Skip confirmation prompt")
def upgrade(check: bool, yes: bool) -> None:
    """Check for and install CSK updates from GitHub.

    Examples:
        csk upgrade          # Check and upgrade
        csk upgrade --check  # Only check
        csk upgrade -y       # Upgrade without confirmation
    """
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]CSK Upgrade Check[/]",
            border_style="cyan",
        )
    )
    console.print()

    current = get_current_version()
    console.print(f"  Current version: [cyan]{current}[/]")

    with console.status("[dim]Checking GitHub for updates...[/]"):
        latest = get_latest_version()

    if latest is None:
        console.print(
            "  [yellow]Could not check for updates.[/]"
        )
        console.print(
            "  [dim]No releases published yet, or network unavailable.[/]"
        )
        console.print()

        if not check:
            console.print("  [dim]To upgrade manually:[/]")
            console.print(f"  [cyan]pip install --upgrade {GIT_INSTALL_URL}[/]")
        console.print()
        return

    console.print(f"  Latest version:  [green]{latest}[/]")
    console.print()

    if current == latest:
        console.print("  [green]✅ You're running the latest version![/]")
        console.print()
        return

    if check:
        console.print(f"  [yellow]Update available: {current} → {latest}[/]")
        console.print("  [dim]Run 'csk upgrade' to install.[/]")
        console.print()
        return

    # Confirm upgrade
    if not yes:
        if not click.confirm(f"  Upgrade from {current} to {latest}?"):
            console.print("  [dim]Upgrade cancelled.[/]")
            console.print()
            return

    console.print()
    with console.status("[dim]Upgrading from GitHub...[/]"):
        success = upgrade_package()

    if success:
        new_version = get_current_version()
        console.print(f"  [green]✅ Upgraded to {new_version}[/]")
    else:
        console.print("  [red]❌ Upgrade failed.[/]")
        console.print(f"  [dim]Try manually: pip install --upgrade {GIT_INSTALL_URL}[/]")

    console.print()
