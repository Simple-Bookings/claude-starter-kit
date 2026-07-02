# /integration — PR and Merge

Your role: **Release Engineer**. Create PR, handle feedback, merge to main branch.

**Goal: Code merged and issue closed.**

---

## Prerequisites

Before integration:
1. Review status: APPROVED
2. All tests passing
3. Branch up to date with target

---

## Steps

### Step 1: Update Branch

Ensure branch is up to date:

```bash
git fetch origin
git rebase origin/main  # or origin/develop
```

Resolve any conflicts. Run tests again after rebase.

### Step 2: Push Branch

```bash
git push -u origin HEAD
```

### Step 3: Create Pull Request

```bash
gh pr create --title "feat: add dark mode toggle" --body "$(cat <<'EOF'
## Summary
- Adds theme toggle button to header
- Persists preference in localStorage
- Respects system preference on first visit

## Acceptance Criteria
- [x] AC1: Toggle button in header
- [x] AC2: Persists across sessions
- [x] AC3: Respects system preference

## Test Plan
- [x] Unit tests for useTheme hook
- [x] Component tests for ThemeToggle
- [x] Manual test in browser

## Screenshots
(Add if UI changes)

Closes #123
EOF
)"
```

### Step 4: Wait for CI

Monitor CI status:

```bash
gh pr checks
```

If CI fails:
1. Read the error
2. Fix locally
3. Push fix
4. Wait for CI again

### Step 5: Handle Review Feedback

If reviewer requests changes:

```bash
# Make changes locally
git add -A
git commit -m "fix: address review feedback"
git push
```

Respond to each comment:
- "Fixed in abc123"
- "Good point, updated"
- "Discussed — keeping as-is because..."

### Step 6: Merge

Once approved and CI green:

```bash
# Squash merge (recommended)
gh pr merge --squash --delete-branch

# Or regular merge
gh pr merge --merge --delete-branch
```

### Step 7: Verify Deployment

If auto-deploy is configured:

```bash
# Check deployment status
gh run list --limit 3

# Verify in production
curl https://app.example.com/api/health
```

### Step 8: Close Issue

If not auto-closed:

```bash
gh issue close 123 --comment "Implemented in PR #456"
```

### Step 9: Clean Up

```bash
# Switch back to main
git checkout main
git pull

# Delete local branch
git branch -d feature/dark-mode

# Clean up plan files (optional)
rm docs/plans/dark-mode-*.md
```

---

## Output

```
✅ Integration Complete

PR: #456 (merged)
Issue: #123 (closed)
Commits: 5 squashed to 1
Branch: feature/dark-mode (deleted)

🎉 Feature shipped!
```

---

## PR Description Template

```markdown
## Summary
[1-2 sentences describing what this PR does]

## Changes
- [Bullet list of main changes]

## Acceptance Criteria
- [x] AC1: [criterion]
- [x] AC2: [criterion]

## Test Plan
- [x] Unit tests
- [x] Integration tests
- [ ] Manual testing (describe steps)

## Screenshots
[If UI changes, add before/after]

## Breaking Changes
[List any breaking changes, or "None"]

## Related Issues
Closes #123
```

---

## Rules

- **CI must pass** — Never merge with failing checks
- **Review required** — At least one approval (if team policy)
- **Squash commits** — Clean history with one commit per feature
- **Delete branch** — Clean up after merge
- **Close issues** — Link PRs to issues with "Closes #X"

---

## Handling CI Failures

### Test Failure

```bash
# Download CI logs
gh run view --log-failed

# Find the failing test
grep -A 10 "FAIL" ci-log.txt

# Fix and push
npm test -- failing-test
git add -A && git commit -m "fix: correct test assertion"
git push
```

### Lint/Type Error

```bash
# Run locally
npm run lint
npm run typecheck

# Fix and push
git add -A && git commit -m "fix: resolve lint errors"
git push
```

### Build Failure

```bash
# Run build locally
npm run build

# Check for missing dependencies
npm install

# Fix and push
```

---

## Merge Strategies

| Strategy | When to Use |
|----------|-------------|
| **Squash** | Feature branches — one clean commit |
| **Merge** | Long-running branches — preserve history |
| **Rebase** | Personal preference — linear history |

Default: **Squash merge** for feature branches.

---

## Done!

The feature is now:
- ✅ Merged to main/develop
- ✅ Issue closed
- ✅ Branch cleaned up
- ✅ Ready for release

Next: Start the next feature with `/planning`!
