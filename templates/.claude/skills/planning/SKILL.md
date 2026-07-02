# /planning — Planning Phase

Analyze the issue, understand the codebase, and write a task list so precise that the executor never needs to make a design decision.

**Do NOT implement anything in this phase.**

## Step 1: Load Issue Context

Read the issue/ticket and understand:
- What is being asked
- Why it matters
- What acceptance criteria exist

## Step 2: Issue Readiness Check

| Criteria | Question |
|---|---|
| Clear description | Can a developer implement without guessing? |
| Testable ACs | Are acceptance criteria specific and verifiable? |
| Realistic scope | Can it be done in ~10 iterations? |

If criteria fail → ask for clarification before proceeding.

## Step 3: Deep Code Analysis

Before writing tasks, understand the codebase:

```bash
# Find related code
grep -r "relevantPattern" --include="*.ts" -l

# Find related tests
find . -name "*.test.ts" | xargs grep -l "relevantPattern"
```

Identify:
1. All files that need to change
2. Dependencies between tasks
3. Existing patterns to follow
4. Tests that will need updating

## Step 4: Write Plan File

Create `docs/plans/{issue}-plan.md`:

```markdown
# Plan: Issue #{number}

## Context
What the issue asks for and why.

## Files to Change
| File | Change | Reason |
|------|--------|--------|
| path/to/file.ts | Add X | Implements AC-1 |

## Task List
- [ ] Task 1: description — **File:** path — **Verify:** command
- [ ] Task 2: description — **File:** path — **Verify:** command

## DoD Verification
- [ ] AC-1 met — **Evidence:** command
- [ ] Tests pass — **Evidence:** `npm test`
```

## Step 5: Write Progress File

Create `docs/plans/{issue}-progress.md`:

```markdown
# Progress: Issue #{number}

## Status
PLANNED

## Tasks
(Copy from plan file)

## Notes
(Discoveries, decisions, risks)
```

## Task Format

Every task MUST have:
1. **Description** — specific and unambiguous
2. **File** — exact file path(s)
3. **Verify** — command that proves the task is done

## Done Criteria

You are done when:
1. ✅ Plan file written with concrete tasks
2. ✅ Progress file written
3. ✅ Issue updated with findings (if needed)
