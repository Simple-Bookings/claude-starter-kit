"""CSK CLI — Main entry point."""

import click
from rich.console import Console

from csk import __version__
from csk.commands import doctor, init, exercises, progress, test, upgrade, upgrade_project, workshop

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="csk")
def main():
    """Claude Starter Kit 2.0 — Interactive learning for Claude Code workflows.

    Get started:

        csk doctor     Check your environment is ready
        csk init       Initialize a new project with CSK2 structure
        csk exercises  Start the exercise server and track progress
    """
    pass


main.add_command(doctor.doctor)
main.add_command(init.init)
main.add_command(exercises.exercises)
main.add_command(progress.progress)
main.add_command(progress.reset)
main.add_command(test.test)
main.add_command(upgrade.upgrade)
main.add_command(upgrade_project.upgrade_project)
main.add_command(workshop.workshop)


if __name__ == "__main__":
    main()
