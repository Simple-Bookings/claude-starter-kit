"""csk init — Initialize a new project with CSK2 structure."""

import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.tree import Tree

console = Console()

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


def get_template_content(name: str) -> str:
    """Get template content, falling back to embedded defaults."""
    template_path = TEMPLATE_DIR / name
    if template_path.exists():
        return template_path.read_text()
    return EMBEDDED_TEMPLATES.get(name, "")


EMBEDDED_TEMPLATES = {
    "CLAUDE.md": '''# CLAUDE.md

Guidance for AI assistants in this repo.

## Project Overview

**Project:** {project_name}

**Purpose:** [Describe what this project does]

**Primary Users:** [Who uses this solution?]

## Tech Stack

- Frontend: [e.g., React, Vue, Next.js]
- Backend: [e.g., Express, FastAPI, Rails]
- Database: [e.g., PostgreSQL, SQLite]
- Testing: [e.g., Vitest, Playwright, pytest]
- Deployment: [e.g., GitHub Actions, Docker, VPS]

## Language

- Conversation, issues, docs, commits: English
- Code, filenames, identifiers: English
- UI text: [your language]

## Git Workflow

```text
main (production) <- develop (integration/test) <- feature/*
```

- Always branch from `develop`
- PRs target `develop`
- Releases go from `develop` to `main`
- Use small commits with meaningful messages

## Key Commands

```bash
# Add your project's key commands here
npm install
npm test
npm run build
```

## Do

- Follow existing patterns before introducing new ones
- Write or update tests alongside code changes
- Make root cause clear when fixing bugs
- Keep docs and scripts in sync with implementation

## Don't

- Never commit directly to `main`
- Don't use `as any` or similar type shortcuts without strong justification
- Don't add hidden magic or hardcoded local paths
- Don't close issues with open DoD checkboxes
''',
    "VISION.md": '''# Vision

## Mission

[What problem does this project solve?]

## Target Users

[Who are you building for?]

## Core Values

1. [Value 1]
2. [Value 2]
3. [Value 3]

## Success Metrics

- [Metric 1]
- [Metric 2]
''',
    "FEATURES.md": '''# Features

## Implemented

| ID | Feature | Status | Notes |
|----|---------|--------|-------|
| F001 | [Feature name] | [Planned/In Progress/Done] | [Notes] |

## User Stories

### US001: [Story Title]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

#### Acceptance Criteria

- [ ] AC1: [Criterion]
- [ ] AC2: [Criterion]
''',
    "ARCHITECTURE.md": '''# Architecture

## System Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Server    │────▶│  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Components

| Component | Purpose | Tech |
|-----------|---------|------|
| Frontend | User interface | [React/Vue/etc.] |
| Backend | API server | [Express/FastAPI/etc.] |
| Database | Data persistence | [PostgreSQL/SQLite/etc.] |

## Data Flow

1. User interacts with frontend
2. Frontend calls API endpoints
3. Backend processes request
4. Database stores/retrieves data
5. Response flows back to user

## Key Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| [Choice] | [Why] | [When] |
''',
    "skill-onboarding.md": '''---
name: onboarding
description: Environment check and project setup verification
---

# /onboarding

Verify the development environment is properly configured.

## Checklist

1. **Git**: Check `git --version` and configured user
2. **Node/Python**: Check runtime version matches project requirements
3. **Dependencies**: Verify `npm install` or `pip install` completed
4. **Database**: Test connection if applicable
5. **Tests**: Run test suite to verify setup

## Output

Report environment status with ✅ or ❌ for each check.
Suggest fixes for any failing checks.
''',
    "skill-grill-me.md": '''---
name: grill-me
description: Socratic questioning to clarify requirements before coding
---

# /grill-me

Ask probing questions to fully understand what the user wants before writing any code.

## Process

1. **Understand the goal**: What problem are we solving?
2. **Identify users**: Who will use this feature?
3. **Define scope**: What's in/out of scope?
4. **Clarify edge cases**: What happens when X fails?
5. **Confirm constraints**: Performance, security, compatibility?

## Rules

- Ask ONE question at a time
- Wait for answer before next question
- Summarize understanding before proceeding
- Never assume — always verify
- Stop when you have enough context to write clear acceptance criteria

## Output

After questioning, produce:
- Problem statement (1-2 sentences)
- User story format (As a... I want... So that...)
- Acceptance criteria (testable checkboxes)
''',
    "skill-mockup-to-story.md": '''---
name: mockup-to-story
description: Convert wireframes (Mermaid/ASCII) to user stories with acceptance criteria
---

# /mockup-to-story

Transform wireframe mockups into structured user stories.

## Input Format

Mermaid block diagram (preferred):

```mermaid
block-beta
    columns 1
    block:header["Login"]
    end
    block:form
        columns 2
        email["Email:"] input1["[______]"]
        pass["Password:"] input2["[______]"]
    end
    login["[ Login ]"]
    forgot["Forgot password?"]
```

Or ASCII wireframe:

```
┌─────────────────────────────┐
│ Login                       │
├─────────────────────────────┤
│ Email:    [____________]    │
│ Password: [____________]    │
│      [  Login  ]            │
│ Forgot password?            │
└─────────────────────────────┘
```

## Process

1. **Identify elements**: List all UI components
2. **Map interactions**: What can users click/type/do?
3. **Define flows**: Happy path and error paths
4. **Write stories**: One per distinct user goal

## Output Format

For each user story:

```markdown
### US-001: User Login

**As a** registered user
**I want to** log in with my credentials
**So that** I can access my account

#### Acceptance Criteria

- [ ] AC1: Email field accepts valid email format
- [ ] AC2: Password field masks input
- [ ] AC3: Login button submits form
- [ ] AC4: Invalid credentials show error message
- [ ] AC5: Successful login redirects to dashboard
- [ ] AC6: "Forgot password" link navigates to reset page
```

## Tips

- One story per user goal (not per screen)
- ACs must be testable (specific, measurable)
- Include error states and edge cases
- Consider accessibility (keyboard nav, screen readers)
''',
    "skill-feature-branch.md": '''---
name: feature-branch
description: Git workflow for feature development
---

# /feature-branch

Create a properly named feature branch and set up for development.

## Branch Naming

```
feat/<short-description>   # New feature
fix/<short-description>    # Bug fix
docs/<short-description>   # Documentation
refactor/<short-description>  # Code refactoring
test/<short-description>   # Test additions
```

## Workflow

```bash
# 1. Start from latest develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feat/<description>

# 3. Make changes with small commits
git add -p  # Stage selectively
git commit -m "feat: add X"

# 4. Push and create PR
git push -u origin HEAD
gh pr create --base develop
```

## Commit Messages

Use conventional commits:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code change without feature/fix
- `test:` adding tests
- `chore:` maintenance

## PR Guidelines

- Keep PRs small (< 400 lines)
- Include tests for new code
- Update relevant documentation
- Reference issue number if applicable
''',
    "skill-tdd.md": '''---
name: tdd
description: Test-driven development workflow
---

# /tdd

Write tests first, then make them pass.

## The Cycle

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│  RED    │────▶│  GREEN  │────▶│ REFACTOR │
│ (fail)  │     │ (pass)  │     │ (clean)  │
└─────────┘     └─────────┘     └──────────┘
      ▲                               │
      └───────────────────────────────┘
```

## Steps

1. **RED**: Write a failing test for the next behavior
2. **GREEN**: Write minimal code to make test pass
3. **REFACTOR**: Clean up without changing behavior
4. Repeat

## Rules

- Never write production code without a failing test
- Write only enough test to fail
- Write only enough code to pass
- Refactor only when tests are green
- Keep tests fast (< 1 second each)

## Test Structure (AAA)

```javascript
test("should calculate total with tax", () => {
  // Arrange — set up test data
  const cart = new Cart();
  cart.addItem({ price: 100 });

  // Act — execute the behavior
  const total = cart.getTotalWithTax(0.1);

  // Assert — verify the outcome
  expect(total).toBe(110);
});
```

## Good Test Names

- `should_returnEmpty_when_cartHasNoItems`
- `should_rejectInvalidEmail_when_formatIsWrong`
- `should_calculateDiscount_when_customerIsPremium`
''',
    "skill-github-issues.md": '''---
name: github-issues
description: Create well-structured GitHub issues and bug reports
---

# /github-issues

Create clear, actionable GitHub issues.

## Issue Types

### Feature Request

```markdown
## Description
[What feature do you want?]

## User Story
As a [user type], I want [goal], so that [benefit].

## Acceptance Criteria
- [ ] AC1: [Specific, testable criterion]
- [ ] AC2: [Another criterion]

## Definition of Done
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
```

### Bug Report

```markdown
## Description
[What's broken?]

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
[What should happen?]

## Actual Behavior
[What actually happens?]

## Environment
- OS: [e.g., macOS 14.0]
- Browser: [e.g., Chrome 120]
- Version: [e.g., v1.2.3]

## Screenshots
[If applicable]
```

## Good Issue Titles

- `feat: add dark mode toggle`
- `fix: login fails with special characters`
- `docs: update API reference for v2`
- `refactor: extract validation logic`

## Labels

| Label | Purpose |
|-------|---------|
| `bug` | Something isn't working |
| `feature` | New functionality |
| `docs` | Documentation only |
| `good first issue` | Easy for newcomers |
| `help wanted` | Extra attention needed |
| `priority:high` | Needs immediate attention |

## Tips

- One issue = one problem/feature
- Include reproduction steps for bugs
- Link related issues with `#123`
- Use task lists for multi-step work
''',
    "skill-release.md": '''---
name: release
description: Version, tag, and release workflow
---

# /release

Manage versions and releases properly.

## Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes (backwards compatible)
  │     └──────── New features (backwards compatible)
  └────────────── Breaking changes
```

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

## Release Workflow

```bash
# 1. Ensure develop is ready
git checkout develop
git pull origin develop
npm test  # All tests pass

# 2. Bump version
npm version patch  # or minor/major

# 3. Merge to main
git checkout main
git pull origin main
git merge develop

# 4. Tag the release
git tag -a v1.2.3 -m "Release v1.2.3"

# 5. Push everything
git push origin main --tags
git checkout develop
git merge main
git push origin develop
```

## Changelog

Keep a `CHANGELOG.md`:

```markdown
# Changelog

## [1.2.3] - 2024-01-15

### Added
- Dark mode support (#42)

### Fixed
- Login timeout issue (#38)

### Changed
- Updated dependencies
```

## Pre-release Checklist

- [ ] All tests pass
- [ ] No console errors/warnings
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped
- [ ] PR merged and reviewed

## GitHub Releases

After pushing tags:

```bash
gh release create v1.2.3 \\
  --title "v1.2.3" \\
  --notes "See CHANGELOG.md for details"
```
''',
    "skill-planning.md": '''---
name: planning
description: Analyze issue and create detailed task list before implementation
---

# /planning

Analyze the issue, understand the codebase, write precise tasks.

**Do NOT implement anything in this phase.**

## Steps

1. **Load issue context** — read requirements and ACs
2. **Check readiness** — is it clear enough to implement?
3. **Analyze codebase** — find files to change, patterns to follow
4. **Write plan file** — `docs/plans/{issue}-plan.md`
5. **Write progress file** — `docs/plans/{issue}-progress.md`

## Task Format

Every task needs:
- **Description** — specific and unambiguous
- **File** — exact path(s)
- **Verify** — command that proves it's done

## Output

```markdown
# Plan: Issue #{number}

## Files to Change
| File | Change | Reason |

## Task List
- [ ] Task 1 — **File:** path — **Verify:** command
```
''',
    "skill-execution.md": '''---
name: execution
description: Implement plan tasks using TDD, record evidence
---

# /execution

Implement plan tasks one by one with TDD.

**Prerequisites:** Plan file exists

## TDD Loop (per task)

1. **RED** — Write failing test
2. **GREEN** — Minimal code to pass
3. **REFACTOR** — Clean up
4. **EVIDENCE** — Record commit + files
5. **COMMIT** — `feat(scope): description`

## Progress Update

```markdown
- [x] Task 1: description
  - **Commit:** abc1234
  - **Files:** path/to/file.ts
```

## Done When

- All tasks `[x]` with evidence
- `npm test` passes
- `npm run lint` clean
- Status = `READY_FOR_REVIEW`
''',
    "skill-reviewing.md": '''---
name: reviewing
description: Code review against plan and acceptance criteria
---

# /reviewing

Review implementation against plan and ACs.

**Prerequisites:** Status = `READY_FOR_REVIEW`

## Checklist

1. **ACs verified** — each has test proof
2. **Security** — no secrets, injection, XSS
3. **Quality** — small functions, no duplication
4. **Tests** — meaningful coverage
5. **Docs** — updated as needed

## Output

```markdown
## Review (Round N)

### Status: APPROVED | NEEDS_FIXES

### Findings
| # | Severity | File | Line | Issue |
```

## Decision

- **APPROVED** — proceed to `/integration`
- **NEEDS_FIXES** — back to `/execution`, then re-review
''',
    "skill-integration.md": '''---
name: integration
description: Create PR, handle feedback, merge to develop
---

# /integration

PR creation to merge completion.

**Prerequisites:** Review = `APPROVED`

## Steps

1. **Push branch** — `git push -u origin HEAD`
2. **Create PR** — `gh pr create --base develop`
3. **Handle CI** — fix failures, re-push
4. **Handle review** — address comments
5. **Merge** — `gh pr merge --squash --delete-branch`
6. **Close issue** — update progress to COMPLETE

## PR Title Format

```
type(scope): description
```

Types: feat, fix, docs, test, refactor, chore

## Done When

- PR merged to develop
- Branch deleted
- Progress = COMPLETE
''',
    "skill-git-worktree.md": '''---
name: git-worktree
description: Parallel agent isolation using Git worktrees
---

# /git-worktree

Isolated working directories for parallel agents.

## Problem

Multiple agents in one directory cause:
- Branch switching conflicts
- Git index.lock blocking
- Commits with unintended files

## Solution

Git worktrees share `.git` but have independent working dirs.

## Quick Start

```bash
# Create worktree
git worktree add .worktrees/agent1 -b feat/task origin/develop

# Work in it
cd .worktrees/agent1
# ... make changes ...

# Cleanup
cd ..
git worktree remove .worktrees/agent1
```

## Commands

| Command | Purpose |
|---------|---------|
| `git worktree add <path> -b <branch>` | Create |
| `git worktree list` | List all |
| `git worktree remove <path>` | Remove |
| `git worktree prune` | Clean stale |

## Best Practices

- One worktree per code-changing agent
- Remove worktrees when done
- Don't let worktrees accumulate
''',
    "skill-security-audit.md": r'''---
name: security-audit
description: OWASP Top 10 security review
---

# /security-audit

Systematic security review.

## When to Run

- Before releasing to production
- After major feature additions
- When adding new dependencies

## Step 1: Dependencies

```bash
npm audit --production --audit-level=high
```

## Step 2: OWASP Top 10

### A01 — Access Control

```bash
# Find routes without auth
grep -r "router\.(get|post)" --include="*.ts" src/routes/
```

### A03 — Injection

```bash
# Find raw SQL
grep -r ".query(" --include="*.ts" src/
```

## Step 3: Auth Boundary

Map all endpoints:
- **Public** — intentionally unauthenticated
- **Authenticated** — any valid user
- **Authorized** — specific role required

## Findings Format

```markdown
### Critical
- [ ] **[OWASP A0X]** — Description
  - **File:** path/to/file.ts:42
  - **Risk:** What attacker can do
  - **Fix:** Remediation
```

## Rules

- Document with evidence
- Fix in isolation (no bundled features)
- Add regression tests
''',
    "rule-testing.md": '''# Testing Rules

## When a Test Fails

1. Find root cause — no quick fixes
2. Fix the code, not the test (unless the test is wrong)
3. Verify ALL tests pass after the fix

**Never:**
- Skip or comment out failing tests
- Use `.skip` without documenting why

## Test Data

```typescript
// Always reset data in beforeEach
beforeEach(async () => {
  await db.model.deleteMany();  // Global, not filtered
  await db.model.createMany({ data: [...] });
});
```

## TDD Workflow

```
RED → GREEN → REFACTOR
```

1. Write a failing test first
2. Write minimum code to pass
3. Refactor without breaking tests
''',
    "rule-workflow.md": '''# Workflow Rules

## Git Workflow

```
main ← develop ← feature/*
```

- Branch from `develop`
- PR to `develop`
- Releases: `develop` → `main`

## Before Starting Work

1. Check for existing PRs on the same issue
2. Create a feature branch
3. Keep PRs small and focused

## Commit Messages

Use conventional commits:

```
feat: add user authentication
fix: resolve login timeout issue
docs: update API documentation
refactor: simplify payment logic
test: add unit tests for cart
```

## Code Review

Before requesting review:

1. Self-review the diff
2. Remove console.logs and debug code
3. Verify tests pass
4. Check for security issues
''',
    "rule-coding-patterns.md": '''# Coding Patterns

## General

- Follow existing patterns before introducing new ones
- Keep functions small and focused
- Name things clearly — avoid abbreviations

## Error Handling

```typescript
// Handle errors explicitly
try {
  await riskyOperation();
} catch (error) {
  console.error('Operation failed:', error);
  // Handle or rethrow
}
```

## File Operations

```bash
# Always use absolute paths
Edit /path/to/file.ts

# Check before destructive operations
if [ -d "$DIR" ] && [ "$DIR" != "/" ]; then
  rm -rf "$DIR"
fi
```

## Bash

```bash
# Use strict mode in scripts
set -euo pipefail

# local is only valid inside functions
my_function() {
  local var="value"  # OK
}
var="value"  # In main script, no local
```
''',
}


@click.command()
@click.argument("project_name")
@click.option("--force", "-f", is_flag=True, help="Overwrite existing directory")
def init(project_name: str, force: bool):
    """Initialize a new project with CSK2 structure.

    Creates a new directory with:
    - CLAUDE.md configuration
    - .claude/ directory with agents, skills, and rules
    - docs/ directory with VISION.md and FEATURES.md
    - .devcontainer/ for VS Code devcontainer support

    Example:

        csk init my-awesome-project
    """
    project_path = Path.cwd() / project_name

    if project_path.exists():
        if not force:
            console.print(f"[red]Error:[/red] Directory '{project_name}' already exists.")
            console.print("Use [cyan]--force[/cyan] to overwrite.")
            raise SystemExit(1)
        shutil.rmtree(project_path)

    console.print(f"\n[bold cyan]Creating project:[/bold cyan] {project_name}\n")

    dirs = [
        ".claude/agents",
        ".claude/skills/onboarding",
        ".claude/skills/grill-me",
        ".claude/skills/mockup-to-story",
        ".claude/skills/feature-branch",
        ".claude/skills/tdd",
        ".claude/skills/github-issues",
        ".claude/skills/release",
        ".claude/skills/planning",
        ".claude/skills/execution",
        ".claude/skills/reviewing",
        ".claude/skills/integration",
        ".claude/skills/git-worktree",
        ".claude/skills/security-audit",
        ".claude/rules",
        ".devcontainer",
        "docs",
        "docs/plans",
        "tests",
    ]

    for d in dirs:
        (project_path / d).mkdir(parents=True, exist_ok=True)

    files = {
        "CLAUDE.md": get_template_content("CLAUDE.md").format(project_name=project_name),
        "docs/VISION.md": get_template_content("VISION.md"),
        "docs/FEATURES.md": get_template_content("FEATURES.md"),
        "docs/ARCHITECTURE.md": get_template_content("ARCHITECTURE.md"),
        ".claude/skills/onboarding/SKILL.md": get_template_content("skill-onboarding.md"),
        ".claude/skills/grill-me/SKILL.md": get_template_content("skill-grill-me.md"),
        ".claude/skills/mockup-to-story/SKILL.md": get_template_content("skill-mockup-to-story.md"),
        ".claude/skills/feature-branch/SKILL.md": get_template_content("skill-feature-branch.md"),
        ".claude/skills/tdd/SKILL.md": get_template_content("skill-tdd.md"),
        ".claude/skills/github-issues/SKILL.md": get_template_content("skill-github-issues.md"),
        ".claude/skills/release/SKILL.md": get_template_content("skill-release.md"),
        ".claude/skills/planning/SKILL.md": get_template_content("skill-planning.md"),
        ".claude/skills/execution/SKILL.md": get_template_content("skill-execution.md"),
        ".claude/skills/reviewing/SKILL.md": get_template_content("skill-reviewing.md"),
        ".claude/skills/integration/SKILL.md": get_template_content("skill-integration.md"),
        ".claude/skills/git-worktree/SKILL.md": get_template_content("skill-git-worktree.md"),
        ".claude/skills/security-audit/SKILL.md": get_template_content("skill-security-audit.md"),
        ".claude/rules/testing.md": get_template_content("rule-testing.md"),
        ".claude/rules/workflow.md": get_template_content("rule-workflow.md"),
        ".claude/rules/coding-patterns.md": get_template_content("rule-coding-patterns.md"),
        ".gitignore": "node_modules/\n__pycache__/\n.env\n.csk-progress.md\n",
        "README.md": f"# {project_name}\n\nCreated with [Claude Starter Kit](https://github.com/Simple-Bookings/claude-starter-kit).\n",
    }

    for filepath, content in files.items():
        (project_path / filepath).write_text(content)

    # Copy agent files from CSK repo
    csk_agents_dir = Path(__file__).parent.parent.parent / ".claude" / "agents"
    if csk_agents_dir.exists():
        for agent_file in csk_agents_dir.glob("*.md"):
            dest = project_path / ".claude" / "agents" / agent_file.name
            shutil.copy2(agent_file, dest)

    tree = Tree(f"[bold]{project_name}[/bold]")
    claude_branch = tree.add(".claude/")
    agents_branch = claude_branch.add("agents/")
    # List copied agents
    agents_dest = project_path / ".claude" / "agents"
    for agent_file in sorted(agents_dest.glob("*.md")):
        agents_branch.add(agent_file.name)
    skills_branch = claude_branch.add("skills/")
    skills_branch.add("onboarding/")
    skills_branch.add("grill-me/")
    skills_branch.add("planning/")
    skills_branch.add("execution/")
    skills_branch.add("reviewing/")
    skills_branch.add("integration/")
    skills_branch.add("tdd/")
    skills_branch.add("feature-branch/")
    skills_branch.add("github-issues/")
    skills_branch.add("release/")
    skills_branch.add("git-worktree/")
    skills_branch.add("security-audit/")
    rules_branch = claude_branch.add("rules/")
    rules_branch.add("testing.md")
    rules_branch.add("workflow.md")
    rules_branch.add("coding-patterns.md")
    tree.add(".devcontainer/")
    docs_branch = tree.add("docs/")
    docs_branch.add("plans/")
    docs_branch.add("VISION.md")
    docs_branch.add("FEATURES.md")
    docs_branch.add("ARCHITECTURE.md")
    tree.add("tests/")
    tree.add("CLAUDE.md")
    tree.add("README.md")
    tree.add(".gitignore")

    console.print(tree)
    console.print(f"\n[bold green]Project created![/bold green]\n")
    console.print("Next steps:")
    console.print(f"  [cyan]cd {project_name}[/cyan]")
    console.print("  [cyan]git init[/cyan]")
    console.print("  [cyan]claude[/cyan]  — Start Claude Code")
    console.print("  [cyan]/onboarding[/cyan]  — Run the onboarding skill\n")
