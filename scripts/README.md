# Scripts

Helper scripts for CSK2 development environment.

## devcontainer-setup.sh

Runs automatically when the devcontainer is created (`postCreateCommand`).

- Ensures `~/.local/bin` is on PATH
- Installs CSK2 CLI (`pip install -e .`)
- Runs `csk doctor` to verify environment

**Manual run:**
```bash
bash scripts/devcontainer-setup.sh
```

## Tool Guard

The `.tool-guard/` directory contains safety rules for git commands. These rules:

- **Block** dangerous operations (push to main, reset --hard)
- **Warn** about risky operations (force push, --no-verify, checkout --theirs)

Rules are applied when running under Claude Code (`claude_only: true` for some rules).

See `.tool-guard/git.config.json` for the full policy.
