---
name: hotfix
description: Hotfix workflow — branch from main, test with production data in test environment, deploy to production, then sync back to develop. Use only for critical production incidents.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# /hotfix — Hotfix Workflow

Use this workflow **only** for critical production bugs that cannot wait for a normal release cycle.

## When to Use Hotfix

| Criterion | Example |
|-----------|---------|
| System down | Core user flow completely broken |
| Data loss risk | Corrupted or deleted user data |
| Security vulnerability | Actively exploited or high-severity |
| Economic impact | Revenue-blocking bug |

**Default:** Use the normal develop → release workflow unless the bug meets one of these criteria. Requires team lead approval to activate.

---

## Step 1: Backup Production Data

Before any changes, create a backup snapshot.

```bash
# Database backup (adapt to your stack)
pg_dump $DATABASE_URL > /tmp/backup-$(date +%Y%m%d-%H%M%S).sql

# Or trigger your cloud backup mechanism
# aws rds create-db-snapshot --db-instance-identifier prod-db --db-snapshot-identifier hotfix-backup-$(date +%Y%m%d)
```

Verify backup succeeded before continuing.

---

## Step 2: Branch from Main

```bash
git fetch origin
git checkout main
git pull origin main

git checkout -b hotfix/short-description
```

**Critical:** Hotfix branches from `main`, NOT `develop`. The fix must match production exactly.

Implement the minimal fix. Do not add unrelated changes.

```bash
# Run type checks on changed files
npx tsc --noEmit 2>&1 | grep "filename.ts"

# Run only the test file for changed code
npx vitest run --bail 1 path/to/specific.test.ts
```

---

## Step 3: Test with Production Data in Test Environment

Hotfixes are uniquely dangerous — use production-like data.

```bash
# Deploy hotfix branch to test environment
git push origin hotfix/short-description

# Trigger test environment deploy (adapt to your CI/CD)
gh workflow run deploy-test.yml --ref hotfix/short-description

# Wait for deploy
gh run watch
```

Verify the fix with production data:
- Use a production database dump in the test environment
- Test the exact scenario that was broken
- Check for regressions in adjacent functionality

**Do not proceed to production if test fails.**

---

## Step 4: Create PR to Main

```bash
gh pr create \
  --base main \
  --head hotfix/short-description \
  --title "hotfix: short description of fix" \
  --body "$(cat <<'EOF'
## Hotfix

**Problem:** [describe the production incident]
**Root cause:** [measurable root cause — e.g. "missing null check in X causes 500 on Y"]
**Fix:** [what was changed]
**Tested:** [how it was verified in test environment]

## Checklist
- [ ] Production backup created
- [ ] Fix verified in test environment with production-like data
- [ ] No unrelated changes included
- [ ] Tests added/updated for the fixed scenario
EOF
)"
```

Get review approval, then merge to main:

```bash
gh pr merge $PR_NUM --squash
```

---

## Step 5: Deploy to Production

```bash
# Monitor production deploy
gh run list --branch main --limit 3
gh run watch

# Verify production health after deploy
curl -s https://your-app.com/api/health | jq
```

Confirm the incident is resolved in production before continuing.

---

## Step 6: Sync Back to Develop

The hotfix must be synced to `develop` so it is not lost in the next release.

```bash
git fetch origin
git checkout develop
git pull origin develop

# Cherry-pick the hotfix commit (not merge — keep history clean)
HOTFIX_SHA=$(git log origin/main --oneline -1 | cut -d' ' -f1)
git cherry-pick $HOTFIX_SHA

# Or cherry-pick the range if multiple commits
git cherry-pick main~3..main
```

Resolve any conflicts manually. Never use `--theirs` blindly — analyse each conflict.

```bash
git push origin develop
```

Create a PR if your workflow requires review for develop merges:

```bash
gh pr create \
  --base develop \
  --head hotfix/short-description-sync \
  --title "sync: hotfix short-description to develop" \
  --body "Part of hotfix/short-description — syncs fix back to develop"
```

---

## Step 7: Add Regression Test

After the incident is resolved, add an E2E or integration test that would have caught this bug.

```bash
# Write the regression test
# Run it to confirm it passes
npx vitest run --bail 1 path/to/regression.test.ts
```

Commit to develop:

```bash
git add path/to/regression.test.ts
git commit -m "test: add regression test for [incident description]"
git push origin develop
```

---

## Rollback

If the hotfix makes things worse:

```bash
# Find the merge commit
git log --oneline -5 origin/main

# Revert
git checkout main && git pull
git revert -m 1 <merge-commit-sha>
git push

# Restore database from backup if needed
psql $DATABASE_URL < /tmp/backup-YYYYMMDD-HHMMSS.sql
```

---

## Rules

- **Branch from main** — never from develop
- **Minimal fix** — one problem, one fix
- **Test with production data** — test environment must match production
- **Add regression test** — in develop after the incident
- **Document the incident** — root cause, fix, timeline
