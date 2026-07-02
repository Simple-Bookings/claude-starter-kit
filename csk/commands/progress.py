"""csk progress — View and manage exercise progress."""

from pathlib import Path

import click
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

PROGRESS_FILE = Path.cwd() / ".csk-progress.md"

EXERCISES = [
    {
        "id": "01",
        "title": "Setup & First Conversation",
        "goal": "Verify environment, talk to Claude",
        "skills": ["onboarding"],
    },
    {
        "id": "02",
        "title": "Git Workflow",
        "goal": "Let Claude handle git for you",
        "skills": ["feature-branch"],
    },
    {
        "id": "03",
        "title": "TDD",
        "goal": "RED → GREEN → REFACTOR with Claude",
        "skills": ["tdd"],
    },
    {
        "id": "04",
        "title": "Code Review",
        "goal": "Claude creates PR and reviews code",
        "skills": ["reviewing"],
    },
    {
        "id": "05",
        "title": "Debugging",
        "goal": "Claude traces execution to find bugs",
        "skills": ["execution"],
    },
    {
        "id": "06",
        "title": "Full Cycle",
        "goal": "Complete feature: plan → code → review → merge",
        "skills": ["planning", "execution", "reviewing", "integration"],
    },
    {
        "id": "07",
        "title": "When Claude Fails",
        "goal": "Identify and fix Claude's mistakes",
        "skills": ["grill-me"],
    },
    {
        "id": "08",
        "title": "Harness Engineering",
        "goal": "Build guardrails around Claude output",
        "skills": ["security-audit"],
    },
    {
        "id": "09",
        "title": "Agent Teams (Bonus)",
        "goal": "Parallel work with specialized agents",
        "skills": [],
    },
    {
        "id": "10",
        "title": "Custom Rules (Bonus)",
        "goal": "Create path-activated rules for your team",
        "skills": [],
    },
]


def load_progress() -> dict:
    """Load progress from .csk-progress.md file."""
    if not PROGRESS_FILE.exists():
        return {}

    content = PROGRESS_FILE.read_text()
    progress = {}

    for line in content.split("\n"):
        if line.startswith("- [x]"):
            ex_id = line.split("]")[1].strip().split(":")[0].strip()
            progress[ex_id] = "completed"
        elif line.startswith("- [ ]"):
            ex_id = line.split("]")[1].strip().split(":")[0].strip()
            if ex_id not in progress:
                progress[ex_id] = "not_started"
        elif line.startswith("- [~]"):
            ex_id = line.split("]")[1].strip().split(":")[0].strip()
            progress[ex_id] = "in_progress"

    return progress


def save_progress(progress: dict):
    """Save progress to .csk-progress.md file."""
    lines = ["# CSK Exercise Progress\n"]

    for ex in EXERCISES:
        status = progress.get(ex["id"], "not_started")
        checkbox = {"completed": "[x]", "in_progress": "[~]", "not_started": "[ ]"}.get(
            status, "[ ]"
        )
        lines.append(f"- {checkbox} {ex['id']}: {ex['title']}")

    lines.append("")
    PROGRESS_FILE.write_text("\n".join(lines))


@click.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def progress(as_json: bool):
    """Show your exercise progress.

    Reads from .csk-progress.md in the current directory.

    Example:

        csk progress         # Show progress table
        csk progress --json  # Output as JSON
    """
    prog = load_progress()

    if as_json:
        import json

        click.echo(json.dumps(prog, indent=2))
        return

    console.print("\n[bold cyan]CSK Exercise Progress[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Exercise", width=30)
    table.add_column("Status", width=15)
    table.add_column("Skills", width=20)

    completed = 0
    for ex in EXERCISES:
        status = prog.get(ex["id"], "not_started")
        if status == "completed":
            completed += 1
            status_display = "[green]Completed[/green]"
        elif status == "in_progress":
            status_display = "[yellow]In Progress[/yellow]"
        else:
            status_display = "[dim]Not Started[/dim]"

        skills = ", ".join(ex["skills"]) if ex["skills"] else "-"
        table.add_row(f"{ex['id']}: {ex['title']}", status_display, skills)

    console.print(table)

    total = len(EXERCISES)
    pct = int((completed / total) * 100) if total > 0 else 0
    console.print(f"\n[bold]Progress:[/bold] {completed}/{total} ({pct}%)\n")


@click.command()
@click.option("--confirm", "-y", is_flag=True, help="Skip confirmation")
def reset(confirm: bool):
    """Reset all exercise progress.

    Deletes .csk-progress.md and starts fresh.

    Example:

        csk reset      # Reset with confirmation
        csk reset -y   # Reset without confirmation
    """
    if not PROGRESS_FILE.exists():
        console.print("[dim]No progress file found. Nothing to reset.[/dim]")
        return

    if not confirm:
        if not click.confirm("Reset all exercise progress?"):
            console.print("[dim]Cancelled.[/dim]")
            return

    PROGRESS_FILE.unlink()
    console.print("[green]Progress reset![/green] Start fresh with [cyan]csk exercises[/cyan].")
