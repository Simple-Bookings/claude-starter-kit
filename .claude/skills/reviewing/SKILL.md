# /reviewing — Code Review

Your role: **Code Reviewer**. Verify implementation against acceptance criteria.

**Decision: APPROVED or NEEDS_FIXES**

---

## Prerequisites

Before reviewing:
1. All tasks marked complete in progress.md
2. All tests passing
3. Build succeeds

---

## Review Checklist

### 1. Acceptance Criteria (Required)

For each AC in the plan:

```markdown
| AC | Status | Evidence |
|----|--------|----------|
| AC1: Toggle button works | ✅ | Test: ThemeToggle.test.ts:12 |
| AC2: Persists to localStorage | ✅ | Test: useTheme.test.ts:8 |
| AC3: System preference detected | ❌ | Missing test |
```

**Every AC must have test evidence.**

### 2. Code Quality

Check for:

- [ ] **No dead code** — Remove unused imports, variables
- [ ] **No console.log** — Remove debug statements
- [ ] **No hardcoded values** — Use constants/config
- [ ] **Clear naming** — Variables describe their purpose
- [ ] **Small functions** — Each does one thing
- [ ] **No duplication** — DRY principle

### 3. Test Quality

Check for:

- [ ] **Happy path covered** — Main use case works
- [ ] **Edge cases covered** — Empty, null, boundary values
- [ ] **Error cases covered** — What happens when things fail
- [ ] **Tests are readable** — Clear arrange/act/assert

### 4. Security (Critical)

Check for:

- [ ] **No secrets in code** — API keys, passwords
- [ ] **No SQL injection** — Parameterized queries
- [ ] **No XSS** — Sanitized user input
- [ ] **No sensitive data in logs** — PII, tokens

### 5. Performance

Check for:

- [ ] **No N+1 queries** — Batch database calls
- [ ] **No memory leaks** — Clean up subscriptions
- [ ] **No blocking operations** — Async where needed

---

## Review Process

### Step 1: Read the Plan

```bash
cat docs/plans/*-plan.md
```

Understand what was supposed to be built.

### Step 2: Check Each AC

For each acceptance criterion:

1. Find the test that verifies it
2. Read the test
3. Run the test
4. Mark as verified or failed

### Step 3: Review the Diff

```bash
git diff main..HEAD --stat
git diff main..HEAD
```

Look for:
- Files that shouldn't be changed
- Unexpected changes
- Missing files

### Step 4: Run All Checks

```bash
npm test
npm run build
npm run lint
npm run typecheck  # if TypeScript
```

All must pass.

### Step 5: Write Review

Update progress.md with findings:

```markdown
## Review

**Status:** NEEDS_FIXES

### Findings

1. **AC3 not verified** — No test for system preference detection
2. **Security issue** — API key visible in ThemeContext.tsx:15
3. **Code quality** — Duplicate logic in useTheme.ts:20-35

### Required Changes
- [ ] Add test for system preference
- [ ] Move API key to environment variable
- [ ] Extract duplicate logic to helper function
```

---

## Decision

### APPROVED

All criteria met:
- ✅ All ACs verified with tests
- ✅ No security issues
- ✅ Code quality acceptable
- ✅ All checks pass

```
✅ Review: APPROVED

ACs: 3/3 verified
Security: Clear
Quality: Good
Next: /integration
```

### NEEDS_FIXES

Issues found:

```
❌ Review: NEEDS_FIXES

Findings:
1. AC3 missing test coverage
2. Hardcoded API key in ThemeContext.tsx

Required: Fix issues and re-run /reviewing
```

---

## Output Format

```markdown
## Review Summary

**Status:** APPROVED | NEEDS_FIXES

### Acceptance Criteria
| AC | Status | Evidence |
|----|--------|----------|
| AC1 | ✅ | test.ts:12 |
| AC2 | ✅ | test.ts:20 |

### Security
✅ No issues found

### Code Quality
- Small functions: ✅
- No duplication: ✅
- Clear naming: ✅

### Findings
(List any issues)

### Decision
APPROVED — Ready for /integration
```

---

## Rules

- **Evidence required** — Every AC needs test proof
- **Security is non-negotiable** — Any security issue = NEEDS_FIXES
- **Be constructive** — Explain why, not just what
- **One pass only** — Don't nitpick after approval

---

## Next Phase

If APPROVED, run `/integration` to create PR and merge.
If NEEDS_FIXES, run `/execution` to fix issues.
