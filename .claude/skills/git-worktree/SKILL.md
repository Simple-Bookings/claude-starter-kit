# Git Worktree Support for Parallel Agents

Provides isolated working directories for parallel agents to avoid git conflicts.

## Problem

When multiple agents run in parallel in the same working directory:
- Branch switching affects all agents
- Git index.lock blocks operations
- Commits include unintended files
- Lintering reverts changes from other agents

## Solution

Git worktrees create separate working directories that share the same .git folder but have independent:
- Working directory
- Index (staging area)
- HEAD (current branch)

## Usage

### Setup Worktree for Agent

```bash
# Create worktree for a specific agent/coworker
./scripts/worktree-create.sh maya feature/billing-emails

# This creates:
# /workspaces/agent-worktrees/maya/ with branch feature/billing-emails
```

### List Active Worktrees

```bash
./scripts/worktree-list.sh
# Shows all active worktrees with their branches
```

### Cleanup Worktree

```bash
./scripts/worktree-remove.sh maya
# Removes the worktree after agent completes
```

### Cleanup All Worktrees

```bash
./scripts/worktree-cleanup.sh
# Removes all agent worktrees (use after parallel session)
```

## Integration with spawn-team

When spawning coworkers for parallel work:

```javascript
// 1. Create worktree first
Bash({
  command: "./scripts/worktree-create.sh aksel feature/aksel-task"
})

// 2. Spawn agent with worktree path
Task({
  subagent_type: "general-purpose",
  run_in_background: true,
  prompt: `Du er Aksel...

  **VIGTIGT: Arbejd i worktree**
  cd /workspaces/agent-worktrees/aksel

  Al dit arbejde skal ske i denne mappe.
  Git operationer er isolerede fra andre agenter.`
})

// 3. Cleanup when done
Bash({
  command: "./scripts/worktree-remove.sh aksel"
})
```

## Worktree Directory Structure

```
/workspaces/
├── simple-bookings/                    # Main repo (orchestrator)
│   └── .git/                           # Shared git data
└── simple-bookings-worktrees/          # Agent worktrees
    ├── tom/                            # Tom's isolated workspace
    ├── dan/                            # Dan's isolated workspace
    ├── frida/                          # Frida's isolated workspace
    └── ...
```

## Best Practices

### 1. One Worktree Per Code-Changing Agent

Agents that modify code need their own worktree:
- Tom, Ada, Dan (developers)
- Scott (tests)
- Frida (frontend)

### 2. Shared Directory OK for Docs-Only Agents

Agents that only write to `.claude/` can share:
- Simone (content)
- Pia (product docs)
- Nora (compliance docs)
- Mark (research)

### 3. Branch Naming Convention

```bash
# Pattern: feature/{coworker}-{task}
feature/maya-billing-emails
feature/dan-stripe-infra
test/scott-e2e-coverage
docs/nora-compliance
```

### 4. Always Cleanup

After parallel session:
```bash
./scripts/worktree-cleanup.sh
```

## Limitations

1. **Disk Space**: Each worktree uses ~50MB (working directory only, git data is shared)
2. **Branch Locking**: A branch can only be checked out in ONE worktree
3. **Submodules**: Not fully supported in worktrees

## Troubleshooting

### "fatal: 'feature/x' is already checked out"

The branch is in use in another worktree:
```bash
git worktree list  # Find which worktree
./scripts/worktree-remove.sh <name>  # Remove it
```

### "Cannot create worktree"

Check if worktree directory exists:
```bash
rm -rf /workspaces/agent-worktrees/<name>
git worktree prune
./scripts/worktree-create.sh <name> <branch>
```

### Stale Worktree Data

```bash
git worktree prune  # Clean up stale entries
```

## Related Skills

- **spawn-team**: Uses worktrees for parallel coworker agents
- **spawn-agent**: Can use worktrees for isolated tasks
- **feature-branch**: Branch creation follows worktree conventions
