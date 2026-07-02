# /git-worktree — Parallel Agent Isolation

Provides isolated working directories for parallel agents to avoid git conflicts.

---

## Problem

When multiple agents run in parallel in the same working directory:
- Branch switching affects all agents
- Git index.lock blocks operations
- Commits include unintended files
- One agent's changes can conflict with another's

## Solution

Git worktrees create separate working directories that share the same `.git` folder but have independent:
- Working directory
- Index (staging area)
- HEAD (current branch)

---

## Quick Start

```bash
# Create worktree for agent
git worktree add .worktrees/agent1 -b feature/task-name origin/develop

# Work in the worktree
cd .worktrees/agent1
# ... make changes, commit, push ...

# Cleanup when done
cd ..
git worktree remove .worktrees/agent1
git branch -d feature/task-name  # if merged
```

---

## Directory Structure

```
my-project/
├── .git/                       # Shared git data
├── src/                        # Main working directory
└── .worktrees/                 # Agent worktrees
    ├── agent1/                 # Agent 1's isolated workspace
    │   └── src/                # Full copy of working tree
    ├── agent2/                 # Agent 2's isolated workspace
    └── ...
```

---

## Worktree Commands

### Create Worktree

```bash
# Create with new branch from develop
git worktree add .worktrees/<name> -b <branch> origin/develop

# Create with existing branch
git worktree add .worktrees/<name> <existing-branch>

# Examples
git worktree add .worktrees/tom -b fix/login-bug origin/develop
git worktree add .worktrees/dan -b feat/deploy-pipeline origin/develop
```

### List Worktrees

```bash
git worktree list

# Output:
# /path/to/project         abc1234 [develop]
# /path/to/project/.worktrees/tom  def5678 [fix/login-bug]
```

### Remove Worktree

```bash
# Remove worktree (keeps branch)
git worktree remove .worktrees/<name>

# Force remove if uncommitted changes
git worktree remove --force .worktrees/<name>

# Cleanup stale entries
git worktree prune
```

---

## Integration with Parallel Agents

When spawning parallel agents:

```javascript
// 1. Create worktrees for each agent
Bash({ command: "git worktree add .worktrees/agent1 -b feat/task-1 origin/develop" })
Bash({ command: "git worktree add .worktrees/agent2 -b feat/task-2 origin/develop" })

// 2. Spawn agents with worktree paths
Agent({
  run_in_background: true,
  prompt: `Work in: /path/to/project/.worktrees/agent1
  
  IMPORTANT: All work must happen in this directory.
  cd /path/to/project/.worktrees/agent1 FIRST.
  
  Task: Implement feature X...`
})

// 3. Cleanup when done
Bash({ command: "git worktree remove .worktrees/agent1" })
Bash({ command: "git worktree remove .worktrees/agent2" })
```

---

## Branch Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/{agent}-{task}` | `feat/tom-user-auth` |
| Bug fix | `fix/{agent}-{task}` | `fix/dan-login-error` |
| Test | `test/{agent}-{task}` | `test/scott-e2e-coverage` |
| Docs | `docs/{agent}-{task}` | `docs/simone-api-guide` |

---

## Best Practices

### 1. One Worktree Per Code-Changing Agent

Agents that modify source code need their own worktree to avoid conflicts.

### 2. Shared Directory OK for Docs-Only

Agents that only write to non-code files (docs, configs) can sometimes share, but worktrees are safer.

### 3. Always Cleanup After Parallel Session

```bash
# List all worktrees
git worktree list

# Remove each agent worktree
git worktree remove .worktrees/agent1
git worktree remove .worktrees/agent2

# Prune stale entries
git worktree prune
```

### 4. Avoid Long-Lived Worktrees

Create worktrees for specific tasks, remove when done. Don't let them accumulate.

---

## Troubleshooting

### "fatal: 'feature/x' is already checked out"

The branch is in use in another worktree:

```bash
# Find which worktree
git worktree list

# Remove it
git worktree remove .worktrees/<name>
```

### "Cannot create worktree"

Check if directory exists:

```bash
rm -rf .worktrees/<name>
git worktree prune
git worktree add .worktrees/<name> -b <branch> origin/develop
```

### Stale Worktree Data

```bash
git worktree prune
```

### Branch Merge Conflicts

When merging back to develop:

```bash
cd .worktrees/<name>
git fetch origin develop
git rebase origin/develop
# resolve conflicts if any
git push --force-with-lease origin <branch>
```

---

## Limitations

1. **Disk Space**: Each worktree uses ~50MB (working directory only, git data is shared)
2. **Branch Locking**: A branch can only be checked out in ONE worktree
3. **Submodules**: May need manual initialization in each worktree

---

## Related Skills

- `/feature-branch` — Branch naming and PR workflow
- `/integration` — Merging and PR creation
