"""csk upgrade-project — Update project skills and rules from latest templates."""

import shutil
from datetime import datetime
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Get templates from the installed package
# Templates are at package root (../.. from commands/), not inside csk/
TEMPLATE_DIR = Path(__file__).parent.parent.parent / "templates"


def get_template_files() -> dict[str, Path]:
    """Get all template files that can be upgraded."""
    files = {}

    # Skills
    skills_dir = TEMPLATE_DIR / ".claude" / "skills"
    if skills_dir.exists():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    files[f".claude/skills/{skill_dir.name}/SKILL.md"] = skill_file

    # Rules
    rules_dir = TEMPLATE_DIR / ".claude" / "rules"
    if rules_dir.exists():
        for rule_file in rules_dir.glob("*.md"):
            files[f".claude/rules/{rule_file.name}"] = rule_file

    # Agents
    agents_dir = TEMPLATE_DIR / ".claude" / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            files[f".claude/agents/{agent_file.name}"] = agent_file

    return files


def file_differs(local: Path, template: Path) -> bool:
    """Check if local file differs from template."""
    if not local.exists():
        return True
    return local.read_text() != template.read_text()


def backup_file(path: Path) -> Path:
    """Create a backup of a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = path.with_suffix(f".backup_{timestamp}.md")
    shutil.copy2(path, backup_path)
    return backup_path


@click.command("upgrade-project")
@click.option("--check", is_flag=True, help="Only check for updates, don't apply")
@click.option("--force", "-f", is_flag=True, help="Overwrite without asking")
@click.option("--backup/--no-backup", default=True, help="Create backups before overwriting")
@click.option("--skill", "-s", multiple=True, help="Only upgrade specific skill(s)")
def upgrade_project(check: bool, force: bool, backup: bool, skill: tuple) -> None:
    """Update project skills and rules from latest CSK2 templates.

    This updates skills, rules, and agents in your project from the latest
    CSK2 templates. User customizations in CLAUDE.md are NOT touched.

    Examples:
        csk upgrade-project           # Interactive upgrade
        csk upgrade-project --check   # Only check what would change
        csk upgrade-project -f        # Force overwrite all
        csk upgrade-project -s onboarding -s tdd  # Only specific skills
    """
    project_root = Path.cwd()

    # Check if this is a CSK2 project
    if not (project_root / ".claude").exists():
        console.print("[red]Error:[/red] No .claude directory found.")
        console.print("Run this command from a CSK2 project root.")
        return

    console.print()
    console.print(Panel.fit("[bold cyan]CSK2 Project Upgrade[/]", border_style="cyan"))
    console.print()

    template_files = get_template_files()

    # Filter to specific skills if requested
    if skill:
        filtered = {}
        for key, path in template_files.items():
            for s in skill:
                if f"skills/{s}/" in key:
                    filtered[key] = path
                    break
        template_files = filtered
        if not template_files:
            console.print(f"[yellow]No matching skills found for: {', '.join(skill)}[/]")
            return

    # Check each file
    updates = []
    new_files = []
    unchanged = []

    for rel_path, template_path in template_files.items():
        local_path = project_root / rel_path

        if not local_path.exists():
            new_files.append((rel_path, template_path, local_path))
        elif file_differs(local_path, template_path):
            updates.append((rel_path, template_path, local_path))
        else:
            unchanged.append(rel_path)

    # Show status table
    table = Table(title="Project Files")
    table.add_column("File", style="cyan")
    table.add_column("Status")

    for rel_path in unchanged:
        table.add_row(rel_path, "[green]✅ Up to date[/]")

    for rel_path, _, _ in new_files:
        table.add_row(rel_path, "[blue]🆕 New (will be added)[/]")

    for rel_path, _, _ in updates:
        table.add_row(rel_path, "[yellow]📝 Update available[/]")

    console.print(table)
    console.print()

    # Summary
    total_changes = len(new_files) + len(updates)
    if total_changes == 0:
        console.print("[green]✅ All files are up to date![/]")
        console.print()
        return

    console.print(f"  [cyan]{len(new_files)}[/] new files")
    console.print(f"  [yellow]{len(updates)}[/] files with updates")
    console.print(f"  [green]{len(unchanged)}[/] unchanged")
    console.print()

    if check:
        console.print("[dim]Run without --check to apply updates.[/]")
        console.print()
        return

    # Confirm
    if not force:
        if not click.confirm("Apply updates?"):
            console.print("[dim]Upgrade cancelled.[/]")
            return

    console.print()

    # Apply new files
    for rel_path, template_path, local_path in new_files:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template_path, local_path)
        console.print(f"  [blue]Added:[/] {rel_path}")

    # Apply updates
    for rel_path, template_path, local_path in updates:
        if backup:
            backup_path = backup_file(local_path)
            console.print(f"  [dim]Backup:[/] {backup_path.name}")
        shutil.copy2(template_path, local_path)
        console.print(f"  [yellow]Updated:[/] {rel_path}")

    console.print()
    console.print(f"[green]✅ Upgraded {total_changes} files![/]")

    if backup and updates:
        console.print()
        console.print("[dim]Backups created with .backup_TIMESTAMP.md suffix.[/]")
        console.print("[dim]Review changes and delete backups when satisfied.[/]")

    console.print()
