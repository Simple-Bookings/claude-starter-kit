# CLAUDE.md — Claude Starter Kit 2.0

Guidance for AI assistants in this repo.

## Project Overview

**CSK2** is a learning framework that teaches developers how to work effectively with Claude Code. It provides skills, exercises, and workshop materials for structured AI-assisted development.

**Stack-agnostic.** Works with any language or framework.

**Primary users:** Development teams learning Claude Code workflows.

## Key Components

| Path | Purpose |
|------|---------|
| `.claude/skills/` | 15 skills that guide Claude through workflows |
| `.claude/rules/` | Coding patterns, testing discipline, workflow rules |
| `.claude/agents/` | Agent profiles for team-based development |
| `exercises/` | 10 hands-on exercises (~4 hours) |
| `workshop/` | Kompendium, slides, and handout for workshops |
| `csk/` | Python CLI for setup, verification, and testing |
| `scripts/` | Devcontainer setup and helper scripts |
| `.tool-guard/` | Git safety rules (blocks dangerous operations) |

## The Work-Loop

CSK2 teaches a 4-phase development cycle:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  /planning  │ ──▶ │ /execution  │ ──▶ │ /reviewing  │ ──▶ │/integration │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
   Analyze &           TDD with           Review against       PR, merge,
   plan tasks          Claude             acceptance criteria  close issue
```

Each phase has a dedicated skill that guides the process.

## Skills

### Core Work-Loop (4 skills)
```
/planning    → Analyze issue, create task list, define ACs
/execution   → TDD implementation with Claude
/reviewing   → Code review against acceptance criteria
/integration → PR creation, merge, close issue
```

### Supporting Skills (11 skills)
```
/onboarding      → Environment check and setup
/grill-me        → Socratic questioning for clarity
/mockup-to-story → Wireframe to user stories
/tdd             → Test-driven development guide
/feature-branch  → Git branch management
/github-issues   → Create well-structured issues
/release         → Version, tag, release
/git-worktree    → Parallel agent isolation
/security-audit  → OWASP Top 10 security review
/exercises       → Workshop exercise guide
/adopt           → Import CSK2 into existing project
```

## Key Commands

```bash
csk doctor       # Check environment is ready
csk init <name>  # Create new project with CSK2 structure
csk exercises    # Start exercise server (port 8000)
csk workshop     # Start workshop materials server (port 9123)
csk progress     # View exercise progress
csk test         # Run tests
```

## Git Safety Rules

**Tool-guard** protects against dangerous git operations. See `.tool-guard/git.config.json`.

### Blocked (deny)
- `git push main` / `git push master` — Use feature branches + PR
- `git reset --hard` — Wipes uncommitted changes; use `git revert` instead

### Warned (warn)
- `git push --force` — Can overwrite others' commits
- `git commit --no-verify` — Bypasses pre-commit hooks
- `git checkout --theirs/--ours` — Blindly resolves conflicts
- `git clean -f` — Permanently deletes untracked files

## Harness Engineering

> **AI-generated code has 1.7× more defects than human-written code.**

CSK2 teaches **Harness Engineering** — building deterministic constraints around probabilistic LLM output:

1. **Editor** — Syntax highlighting, type hints
2. **Pre-commit hooks** — Lint, format, type-check
3. **CI/CD** — Tests, security scans
4. **Human review** — Final verification

Every Claude mistake → new guardrail → that mistake becomes impossible.

## Workshop Materials

| File | Purpose |
|------|---------|
| `workshop/kompendium.html` | Full reference (46 sections) |
| `workshop/slides.html` | Presentation slides (39 slides) |
| `workshop/handout.html` | Printable quick reference |

## Development

```bash
# Install dependencies
pip install -e .

# Run CLI
csk doctor

# Serve workshop materials
csk workshop

# Run tests
pytest tests/
```

## Conventions

- **English only** — All code, docs, and UI in English
- **MIT license** — Open source, attribution required
- **Stack-agnostic** — No language-specific assumptions
- **Skills are markdown** — `.claude/skills/<name>/SKILL.md`

## Don't

- Don't push directly to main — use feature branches + PR
- Don't use `git reset --hard` — use `git revert` instead
- Don't skip pre-commit hooks with `--no-verify`
- Don't add language-specific code patterns
- Don't assume a particular tech stack
- Don't add features without exercise coverage
