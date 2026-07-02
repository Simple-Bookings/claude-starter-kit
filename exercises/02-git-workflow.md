# Exercise 02: Git Workflow with Claude

**Goal:** Let Claude handle all git operations — you focus on what to build.

**Skills:** `/feature-branch`

**Time:** 15 minutes

---

## What You'll Learn

- Claude creates branches following conventions
- Claude writes meaningful commit messages
- You never type `git` commands manually

## Step 1: Create a Feature Branch

Say to Claude:

```
Create a worktree and feature branch called "add-readme-docs"
```

Claude will:
1. Create the worktree in `.worktrees/`
2. Create the branch from develop/main
3. Switch to it

## Step 2: Make Changes

Ask Claude:

```
Add a "Getting Started" section to README.md with:
1. Prerequisites (Node.js 18+)
2. Installation steps
3. How to run tests
```

Claude will:
1. Read the current README
2. Add the section
3. Show you the changes

## Step 3: Commit

```
Commit these changes with a good message
```

Claude writes a conventional commit:
```
docs: add Getting Started section to README

- Prerequisites for Node.js 18+
- Installation and test commands
```

## Step 4: Merge

```
Merge this branch back and clean up
```

Claude will:
1. Switch to main/develop
2. Merge the feature branch
3. Delete the branch and worktree

## The Pattern

```
You say                           Claude does
───────────────────────────────────────────────────────────────────
"Create a feature branch for X"   git worktree add, git checkout -b
"Commit this"                     git add, git commit -m "..."
"Merge and clean up"              git merge, git branch -d, cleanup
```

## Why This Works

- Branch names follow conventions automatically (`feature/`, `fix/`, `docs/`)
- Commit messages are semantic (no more "wip" or "fix stuff")
- Less context-switching between coding and git

## Verification

- [ ] Branch created by Claude
- [ ] Changes committed with good message
- [ ] Branch merged and cleaned up

## Next

[Exercise 03: TDD](03-tdd.md)
