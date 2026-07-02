# /exercises — Workshop Exercise Guide

Shows exercise progress and guides you through the CSK2 workshop exercises.

---

## Usage

```
/exercises          # Show progress overview
/exercises 3        # Start exercise 3
/exercises check 3  # Check completion for exercise 3
```

---

## Exercise Overview

| # | Name | Skill | Time | Description |
|---|------|-------|------|-------------|
| 01 | Setup | `/onboarding` | 10m | Verify environment |
| 02 | Git Workflow | `/feature-branch` | 15m | Branch, commit, merge |
| 03 | TDD | `/tdd` | 30m | Red-green-refactor |
| 04 | Code Review | `/reviewing` | 20m | PR workflow |
| 05 | Debugging | `/execution` | 20m | Systematic debugging |
| 06 | Full Cycle | All 4 phases | 45m | End-to-end feature |

Total time: ~2.5 hours

---

## Progress Tracking

Progress is stored in `.csk-progress.md`:

```markdown
- [x] 01: Setup
- [x] 02: Git Workflow
- [ ] 03: TDD
- [ ] 04: Code Review
- [ ] 05: Debugging
- [ ] 06: Full Cycle
```

---

## Completion Criteria

### Exercise 01: Setup
- [ ] `csk doctor` shows all green
- [ ] Project has `.claude/` directory
- [ ] Claude Code starts

### Exercise 02: Git Workflow
- [ ] develop branch created
- [ ] Feature branch created
- [ ] Commit made with conventional message
- [ ] Merged to develop

### Exercise 03: TDD
- [ ] Failing test written first (RED)
- [ ] Implementation makes test pass (GREEN)
- [ ] Code refactored (REFACTOR)

### Exercise 04: Code Review
- [ ] PR created with description
- [ ] Self-reviewed
- [ ] Feedback received
- [ ] PR merged

### Exercise 05: Debugging
- [ ] Buggy function created
- [ ] Failing test written
- [ ] Root cause identified
- [ ] Bug fixed

### Exercise 06: Full Cycle
- [ ] Plan file created (`/planning`)
- [ ] TDD implementation (`/execution`)
- [ ] Review passed (`/reviewing`)
- [ ] PR merged (`/integration`)

---

## Commands

### Show Progress

```
> /exercises

📊 Exercise Progress

✅ 01 Setup
✅ 02 Git Workflow
🔄 03 TDD (in progress)
⬜ 04 Code Review
⬜ 05 Debugging
⬜ 06 Full Cycle

Progress: 2/6 complete
Next: Exercise 03 — TDD
```

### Start Exercise

```
> /exercises 3

📝 Exercise 03: TDD

Skill: /tdd
Time: 30 minutes

Goal: Practice test-driven development with red-green-refactor.

Steps:
1. Write a failing test (RED)
2. Write minimum code to pass (GREEN)
3. Refactor without breaking tests

Let's begin!
```

### Check Completion

```
> /exercises check 3

Checking Exercise 03...

✅ Wrote failing test
✅ Made test pass
✅ Refactored safely

🎉 Exercise 03 Complete!

Progress updated. Next: Exercise 04 — Code Review
```

---

## Tips

- Complete exercises in order — they build on each other
- Don't rush — understanding matters more than speed
- Ask for help if stuck — Claude can guide you
