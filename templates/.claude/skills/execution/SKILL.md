# /execution — Execution Phase

Implement the plan task by task. Each task gets evidence.

**Prerequisites:** Plan file exists at `docs/plans/{issue}-plan.md`

## Step 0: Load Plan

```bash
cat docs/plans/{issue}-plan.md
cat docs/plans/{issue}-progress.md
```

Update progress status to `IN_PROGRESS`.

## Step 1: Create Feature Branch

```bash
git checkout develop && git pull
git checkout -b feature/{issue}-{short-desc}
```

## Step 2: Execute Tasks (TDD Loop)

For each unchecked task in the plan:

### 2.1 Write Failing Test (RED)
```bash
# Create test that exercises the expected behavior
npm test -- path/to/test.ts
# Should FAIL — proves the feature doesn't exist yet
```

### 2.2 Implement (GREEN)
```bash
# Write minimal code to make test pass
npm test -- path/to/test.ts
# Should PASS
```

### 2.3 Refactor (BLUE)
- Clean up code
- Ensure no duplication
- Run full test suite: `npm test`

### 2.4 Record Evidence

Update `progress.md`:
```markdown
- [x] Task 1: description
  - **Commit:** abc1234
  - **Files:** path/to/file.ts
  - **Evidence:** `npm test` passes
```

### 2.5 Commit
```bash
git add -p
git commit -m "feat({scope}): implement {task description}"
```

## Step 3: Verify All Tasks Complete

```bash
# Check all tasks are [x]
grep -c "\- \[ \]" docs/plans/{issue}-progress.md
# Should return 0
```

## Step 4: Run Full Test Suite

```bash
npm test
npm run lint
npm run build
```

All must pass before proceeding to /reviewing.

## Step 5: Update Progress

```markdown
## Status
READY_FOR_REVIEW

## Summary
- Tasks completed: N/N
- Files changed: (list)
- Tests added: (count)
```

## Evidence Format

Each completed task needs:
- **Commit SHA** — which commit implemented it
- **Files changed** — what was modified
- **Verification** — how to prove it works

## Done Criteria

Execution is complete when:
1. ✅ All plan tasks are `[x]`
2. ✅ Each task has evidence recorded
3. ✅ Tests pass (`npm test`)
4. ✅ Lint clean (`npm run lint`)
5. ✅ Build succeeds (`npm run build`)
6. ✅ Progress status = `READY_FOR_REVIEW`
