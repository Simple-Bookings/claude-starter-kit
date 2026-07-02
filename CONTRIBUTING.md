# Contributing to CSK2

Thank you for your interest in contributing to Claude Starter Kit 2.0!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/claude-starter-kit.git
   cd claude-starter-kit
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests:
   ```bash
   pytest tests/
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature
   ```

2. Make your changes

3. Run tests:
   ```bash
   pytest tests/ -v
   ```

4. Commit with conventional commits:
   ```bash
   git commit -m "feat: add new feature"
   ```

5. Push and create a PR:
   ```bash
   git push origin feat/your-feature
   ```

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation only
- `test:` — Adding or updating tests
- `refactor:` — Code change without feature/fix
- `chore:` — Maintenance tasks

## Code Style

- Python code follows PEP 8
- Use type hints where practical
- Keep functions small and focused
- Write docstrings for public functions

## Adding Skills

To add a new skill:

1. Create `.claude/skills/<skill-name>/SKILL.md`
2. Add template to `csk/commands/init.py`
3. Update `README.md` skills table
4. Add tests if applicable

## Adding Exercises

To add a new exercise:

1. Create `exercises/NN-exercise-name.md`
2. Update `csk/commands/progress.py` EXERCISES list
3. Update README exercises table

## Questions?

Open an issue for questions or suggestions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
