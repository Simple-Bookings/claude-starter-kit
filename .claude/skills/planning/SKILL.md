# /planning — Analyze and Plan

Your role: **Architect / Planning Lead**. Analyze the issue, understand the codebase, and write a precise task list.

**Do NOT write code in this phase.** Planning only.

---

## Input

The user provides either:
- A GitHub issue number: `#123`
- A feature description: "Add dark mode toggle"
- A bug report: "Login fails on Safari"

---

## Steps

### Step 1: Understand the Request

```
What exactly needs to be built?
Who is the user?
What's the success criteria?
```

If unclear, ask clarifying questions using Socratic method (like `/grill-me`).

### Step 2: Analyze the Codebase

Find all files that need to change:

```bash
# Find related code
grep -r "relevantPattern" --include="*.ts" --include="*.tsx" -l

# Find existing tests
find . -name "*.test.ts" | xargs grep -l "relevantFunction"

# Check for similar implementations
grep -r "similarFeature" --include="*.ts" -l
```

### Step 3: Write Acceptance Criteria

Each AC must be:
- **Specific** — No ambiguity
- **Testable** — Can verify pass/fail
- **Independent** — Can test in isolation

```markdown
## Acceptance Criteria
- [ ] AC1: User can toggle dark mode via settings button
- [ ] AC2: Preference persists in localStorage
- [ ] AC3: System preference detected on first visit
```

### Step 4: Create Task List

Each task must have:
1. **Description** — What to do
2. **File** — Which file(s) to change
3. **Verify** — Command that proves it's done

```markdown
## Tasks
- [ ] Task 1: Add ThemeContext — **File:** src/context/theme.tsx — **Verify:** `grep "ThemeContext" src/context/theme.tsx`
- [ ] Task 2: Add toggle button — **File:** src/components/ThemeToggle.tsx — **Verify:** `npm test -- ThemeToggle`
- [ ] Task 3: Persist to localStorage — **File:** src/hooks/useTheme.ts — **Verify:** manual test
```

### Step 5: Write Plan File

Create `docs/plans/{issue}-plan.md`:

```markdown
# Plan: Dark Mode Toggle

## Context
Users want to switch between light and dark themes.

## Acceptance Criteria
- [ ] AC1: Toggle button in header
- [ ] AC2: Persists across sessions
- [ ] AC3: Respects system preference

## Files to Change
| File | Change |
|------|--------|
| src/context/theme.tsx | Create context |
| src/components/ThemeToggle.tsx | UI component |
| src/hooks/useTheme.ts | Hook with localStorage |

## Tasks
- [ ] Task 1: Create ThemeContext
- [ ] Task 2: Create ThemeToggle component
- [ ] Task 3: Add useTheme hook
- [ ] Task 4: Write tests
- [ ] Task 5: Add to header

## Estimated Effort
5 tasks, ~2 hours
```

### Step 6: Write Progress File

Create `docs/plans/{issue}-progress.md`:

```markdown
# Progress: Dark Mode Toggle

## Status
PLANNING_COMPLETE

## Tasks
- [ ] Task 1: Create ThemeContext
- [ ] Task 2: Create ThemeToggle component
- [ ] Task 3: Add useTheme hook
- [ ] Task 4: Write tests
- [ ] Task 5: Add to header

## Notes
- Using CSS variables for theming
- localStorage key: "theme-preference"
```

---

## Output

When planning is complete, report:

```
✅ Planning Complete

Plan: docs/plans/dark-mode-plan.md
Tasks: 5
Files: 3
Next: /execution
```

---

## Rules

- **No code** — Only analysis and planning
- **Be specific** — Vague tasks lead to vague implementations
- **Order by dependency** — Blocking tasks first
- **One task = one commit** — Keep tasks atomic
- **Include verify step** — Every task needs proof of completion

---

## Next Phase

After planning, run `/execution` to implement the tasks.
