# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-07-02

First open-source release of Claude Starter Kit 2.0.

### Added

- CLI commands: `doctor`, `init`, `exercises`, `progress`, `reset`, `test`, `upgrade`, `upgrade-project`, `workshop`
- 15 skills (4 core + 11 supporting):
  - Core: planning, execution, reviewing, integration
  - Supporting: onboarding, grill-me, mockup-to-story, tdd, feature-branch, github-issues, release, security-audit, adopt, git-worktree, exercises
- 7 agent profiles: aksel, dan, frida, pia, quinn, scott, tom
- 3 rule files: testing, workflow, coding-patterns
- 10 hands-on exercises (~4 hours), including bonus exercises for agent teams and custom rules
- Devcontainer support
- Platform setup guides: macOS, Linux, Windows/WSL2
- Full test suite

### Workshop Materials

- **slides.html** — 41 presentation slides with detailed speaker notes
- **presenter.html** — Speaker notes in a separate window, synced live with slides
- **kompendium.html** — Complete developer reference manual
- **handout.html** — Print-optimized participant handout
- **quick-reference.html** — Printable one-page cheat sheet

### CLI Features

- `csk doctor` — Environment verification
- `csk init <name>` — Project scaffolding with skills, rules, and CLAUDE.md
- `csk exercises` — Interactive exercise server
- `csk workshop` — Workshop materials server with stop/restart
- `csk progress` — Track exercise completion
- `csk upgrade` — Self-update from GitHub
- `csk upgrade-project` — Update an existing project's skills/rules from latest templates
