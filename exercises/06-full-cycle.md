# Exercise 06: Full Feature Cycle

**Goal:** Complete a feature using all 4 phases.

**Skills:** `/planning` → `/execution` → `/reviewing` → `/integration`

**Time:** 45 minutes

---

## What You'll Learn

- The complete development workflow
- How phases connect
- From idea to merged code

## The Challenge

Build a **Weekly Summary** feature:

> Given an array of daily time entries, return total seconds, most active day, and formatted output.

## Phase 1: Planning (10 min)

```
/planning
```

```
I want a Weekly Summary feature that:
- Takes an array of { day: string, seconds: number }
- Returns total seconds for the week
- Finds the most active day
- Formats output nicely

Create a plan with concrete tasks.
```

Claude creates `docs/plans/weekly-summary-plan.md`:
- Task list with checkboxes
- Files to create
- Verification steps

**Review the plan.** Agree before proceeding.

## Phase 2: Execution (20 min)

```
/execution
```

Work through each task:

```
Start Task 1: Write tests for generateWeeklySummary
```

For each task, Claude:
1. Writes the test (RED)
2. Implements the code (GREEN)
3. Updates progress

Guide Claude through tasks:

```
Good. Task 2: Implement the function.
```

```
Task 3: Add findMostActiveDay function.
```

```
Task 4: Add formatting.
```

## Phase 3: Reviewing (5 min)

```
/reviewing
```

Claude checks:
- [ ] All tests pass
- [ ] No console.logs
- [ ] Code follows conventions
- [ ] No security issues
- [ ] Build succeeds

If issues found:

```
Fix those and review again.
```

## Phase 4: Integration (10 min)

```
/integration
```

```
Create a PR with a good description.
```

Claude:
1. Creates feature branch (if needed)
2. Commits all changes
3. Pushes to remote
4. Creates PR with description

After CI passes:

```
Merge and clean up.
```

## The Flow

```
/planning → docs/plans/X-plan.md
    ↓
/execution → TDD for each task
    ↓
/reviewing → quality checks
    ↓ (loop if issues)
/integration → PR → merge
```

## Verification

- [ ] Plan file created
- [ ] All tasks completed with TDD
- [ ] Review passed
- [ ] PR merged

## You Did It!

You now know:

1. **Claude codes** — you think
2. **4 phases** keep you organized
3. **TDD is built in** — tests first
4. **Git is automatic** — Claude handles it

## What's Next?

- Apply to real projects — start small
- Customize skills for your team
- Practice daily — becomes natural in a week

## Next

[Exercise 07: When Claude Fails](07-when-claude-fails.md)
