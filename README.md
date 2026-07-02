# Claude Starter Kit (CSK)

A complete workshop toolkit for learning [Claude Code](https://docs.anthropic.com/claude-code/) — the AI pair programmer. Includes a full-day workshop (slides, reference manual, presenter mode), 10 hands-on exercises, project templates, and a CLI.

## Quick Start

```bash
# Install the CLI from GitHub
pip install git+https://github.com/Simple-Bookings/claude-starter-kit.git

# Verify your environment
csk doctor

# Create a new project with skills, rules, and CLAUDE.md pre-configured
csk init my-project
cd my-project

# Start Claude Code
claude
```

## What's Inside

| Resource | Description |
|----------|-------------|
| `workshop/slides.html` | 41 presentation slides with speaker notes |
| `workshop/kompendium.html` | Complete reference manual |
| `workshop/presenter.html` | Speaker notes in a separate synced window |
| `workshop/quick-reference.html` | Printable one-page cheat sheet |
| `workshop/handout.html` | Print-friendly participant handout |
| `exercises/` | 10 hands-on exercises |
| `templates/` | Project templates: skills, rules, agents |
| `csk/` | Python CLI |

## The Workshop

A full-day (09:00–16:00) hands-on workshop teaching teams to work effectively with Claude Code:

- **Morning:** Introduction, Foundation (CLAUDE.md, Skills, Rules, Models), and the 4-phase Work-Loop
- **Afternoon:** Hands-on exercises, supporting skills, and advanced topics (worktrees, MCP, hooks, agent teams)

**Presenter mode:** Open `workshop/index.html`, click "Start Presenter Mode" — slides open in a popup for screen 2 while speaker notes stay on your laptop, synced live.

## Exercises

1. **Setup** — Verify environment, first conversation
2. **Git Workflow** — Let Claude handle git
3. **TDD** — RED → GREEN → REFACTOR
4. **Code Review** — PR workflow with Claude
5. **Debugging** — Systematic bug hunting
6. **Full Cycle** — Complete feature development 🎓
7. **When Claude Fails** — Handling mistakes
8. **Guardrails** — Build safety nets
9. **Agent Teams** — Parallel work (bonus)
10. **Custom Rules** — Path-activated rules (bonus)

## The Work-Loop

The core methodology taught by this kit:

```
/planning → /execution → /reviewing → /integration
    ↑                         │
    └──────── NEEDS_FIXES ←───┘
```

- **`/planning`** — Analyze and plan. No code.
- **`/execution`** — Implement with TDD (RED → GREEN → REFACTOR)
- **`/reviewing`** — Claude reviews its own work
- **`/integration`** — Branch, PR, merge

## CLI Commands

```bash
csk doctor           # Check environment
csk init <name>      # Create a new project
csk exercises        # Start the exercise server
csk progress         # Track exercise progress
csk upgrade          # Upgrade the CLI from GitHub
csk upgrade-project  # Update a project's skills/rules from latest templates
```

## Requirements

- Python 3.10+
- Git
- [Claude Code](https://docs.anthropic.com/claude-code/)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports and PRs welcome.

## License

MIT — see [LICENSE](LICENSE).
