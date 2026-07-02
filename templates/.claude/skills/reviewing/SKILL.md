# /reviewing — Code Review Phase

Review the implementation against the plan and acceptance criteria.

**Prerequisites:** Progress status = `READY_FOR_REVIEW`

## Step 0: Load Context

```bash
cat docs/plans/{issue}-plan.md
cat docs/plans/{issue}-progress.md
git diff develop...HEAD --stat
```

## Step 1: Verify Acceptance Criteria

For each AC in the plan:
- [ ] Is it implemented?
- [ ] Is there a test that proves it?
- [ ] Does the test actually verify the AC?

## Step 2: Code Quality Review

Check each changed file for:

### Security
- [ ] No hardcoded secrets
- [ ] No SQL injection
- [ ] No XSS vulnerabilities
- [ ] Input validation present

### Code Quality
- [ ] Functions are small and focused
- [ ] No code duplication
- [ ] Clear naming
- [ ] No `any` types (TypeScript)

### Tests
- [ ] Tests exist for new code
- [ ] Tests are meaningful (not just coverage)
- [ ] Edge cases covered

### Documentation
- [ ] Complex logic has comments
- [ ] Public APIs are documented
- [ ] README updated if needed

## Step 3: Run Verification

```bash
npm test
npm run lint
npm run build
```

## Step 4: Record Findings

Update `progress.md` with review section:

```markdown
## Review (Round 1)

### Status: APPROVED | NEEDS_FIXES

### Findings
| # | Severity | File | Line | Issue | Fix |
|---|----------|------|------|-------|-----|
| 1 | HIGH | path.ts | 42 | Missing null check | Add guard |

### Summary
- Security: ✅ No issues
- Quality: ⚠️ 2 minor issues
- Tests: ✅ Good coverage
- Docs: ✅ Updated
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| HIGH | Security/data loss risk | Must fix before merge |
| MEDIUM | Bug or bad practice | Should fix |
| LOW | Style or preference | Optional |

## Decision Outputs

### APPROVED
All checks pass. Ready for `/integration`.

### NEEDS_FIXES
Issues found. Return to `/execution` to fix.

After fixes, run `/reviewing` again (Round 2, 3, ...).

## Done Criteria

Review is complete when:
1. ✅ All ACs verified
2. ✅ Code quality checked
3. ✅ Findings recorded
4. ✅ Decision made (APPROVED or NEEDS_FIXES)
