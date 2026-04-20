---
name: build
description: Build phase — implement ONE task from the plan, validate it, commit and push. Run in a loop until all tasks are done. Use after /plan.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, Agent
---

# /build — Build Phase

Your role: **Executor**. Implement exactly ONE task from the task list, verify it, commit, and stop. The loop calls you again for the next task.

**One task per iteration. No more.**

---

## Step 0: Orient Yourself

```bash
# Confirm you are on the right branch
git rev-parse --abbrev-ref HEAD

# Read the plan
cat plans/{issue}-plan.md

# Read the progress file
cat plans/{issue}-progress.md
```

---

## Step 1: Select ONE Task

Pick the highest-priority uncompleted task (`- [ ]`).

Before implementing, verify the task is not already done:
```bash
grep -r "functionName" --include="*.ts" -l
```

---

## Step 2: Implement

Make the necessary code changes:
- Follow existing patterns in the codebase
- Keep changes focused and minimal
- Do not change files unrelated to the task

**Run type checks on changed files only — never the full project:**
```bash
# Example for TypeScript — adjust to your build tool
npx tsc --noEmit 2>&1 | grep "filename.ts" | grep "error"
```

**Do NOT run the full test suite locally** — CI handles that. Run only the test file for the code you changed:
```bash
# Run only the relevant test file
npx vitest run --bail 1 path/to/specific.test.ts
# or: jest path/to/specific.test.ts
# or: your-test-runner specific-test-file
```

**Never mark a task [x] without running its Verify command.**

---

## Step 3: Update Progress File

```markdown
## Tasks
- [x] Task 1: completed — **Evidence:** <command output>
- [ ] Task 2: next up
```

Add notes about anything discovered.

---

## Step 4: Commit and Push

**Every iteration MUST produce a commit.**

```bash
# Stage ONLY the files you changed + the progress file
git add path/to/changed/file.ts plans/{issue}-progress.md

git commit -m "feat(#{issue}): descriptive message

Part of #{issue}"

git push origin HEAD
```

Rules:
- **Never `git add -A` or `git add .`** — only stage what you changed
- **Always push after commit** — unpushed work is invisible
- **Never use `Fixes #NNN` or `Closes #NNN`** in commit messages — use `Part of #NNN`
- Include the progress file in every commit

Even if no source files changed (verification-only task), commit the updated progress file.

---

## Step 5: Check Completion

Count tasks:
- How many total? How many `[x]`? How many `[ ]`?
- If ANY task is still `[ ]` → keep Status as `IN_PROGRESS`
- Only signal completion when ALL tasks are `[x]` AND DoD verification passes

**When all tasks are complete:**

```bash
# Run DoD verification from the plan file
# All checks must pass before signaling done
```

Update Status in the progress file:
```markdown
## Status
DONE
```

Commit the final progress file:
```bash
git add plans/{issue}-progress.md
git commit -m "done: all tasks complete

Part of #{issue}"
git push origin HEAD
```

**Do NOT schedule another /build iteration** — all tasks are done. Run `/review` next.

---

## Loop Setup (REQUIRED at end of every iteration)

After committing, check if there are remaining tasks:

```bash
REMAINING=$(grep -c '^\- \[ \]' plans/{issue}-progress.md || echo 0)
echo "Remaining tasks: $REMAINING"
```

**If tasks remain (Status is IN_PROGRESS):**

Schedule the next build iteration using CronCreate:

```
CronCreate(
  cron: "*/1 * * * *",
  prompt: "/build — continue issue #{issue}. Plan: plans/{issue}-plan.md, Progress: plans/{issue}-progress.md",
  recurring: false
)
```

**If no tasks remain (Status is DONE):**

Do not schedule another build. Tell the user to run `/review`.

---

## Rules

- **One task per iteration**
- **Search before implementing** — verify the code doesn't already exist
- **Run the Verify command** — never claim done without proof
- **Commit with progress file** — every commit includes the updated progress
- **Push every commit** — lost work is unpushed work
- **Never `as any`** — fix the type correctly
- **If blocked** — add a note, move to the next task, keep Status as IN_PROGRESS

---

## Progress File Format

```markdown
# Progress: Issue #{issue}

## Status
IN_PROGRESS

## Tasks
- [x] Task 1: done — **Evidence:** 0 errors
- [x] Task 2: done — **Evidence:** test passed
- [ ] Task 3: next

## Completed This Iteration
- Task 2: added validation to X, fixed type in Y

## Notes
<discoveries, side-effects, risks>
```
