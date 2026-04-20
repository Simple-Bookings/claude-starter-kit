---
name: integrate
description: Integration phase — manage the PR through CI, handle review comments, rebase if needed, merge, and close the issue. Run in a loop, one task per iteration. Use after /review APPROVED.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# /integrate — Integration Phase

Your role: **Integration Engineer**. Execute exactly ONE integration task, mark it `[x]`, and stop. The loop calls you again for the next task.

**One task per iteration. No more.**

---

## Step 1: Find Next Task

```bash
grep -n '^\- \[ \] \[INT-' plans/{issue}-progress.md | head -1
```

If no `[INT-*]` tasks exist yet, initialise the list:

```bash
cat >> plans/{issue}-progress.md << 'TASKS'

## Integration Tasks
- [ ] [INT-1] Create/find PR and enable auto-merge
- [ ] [INT-2] Handle all open PR review comments
- [ ] [INT-3] Check CI status — fix failing checks (repeated until green)
- [ ] [INT-4] Rebase branch if BEHIND develop
- [ ] [INT-5] Merge PR
- [ ] [INT-6] Post-merge: docs verification + DoD/AC + close issue
TASKS
```

If all `[INT-*]` tasks are `[x]` → write `MERGED` to status and stop.

---

## Step 2: Execute the Task

### [INT-1] Create/find PR and enable auto-merge

```bash
BRANCH=$(git branch --show-current)

PR_NUM=$(gh pr list --state all --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number // empty")

if [ -z "$PR_NUM" ]; then
  gh pr create --base develop \
    --title "fix(#{issue}): <description>" \
    --body "Part of #{issue}"
  PR_NUM=$(gh pr list --state all --json number,headRefName \
    --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number")
fi

gh pr merge "$PR_NUM" --auto --squash 2>/dev/null \
  && echo "Auto-merge enabled" \
  || echo "Auto-merge not available — will merge manually in INT-5"
```

---

### [INT-2] Handle open PR review comments

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$(git branch --show-current)\")][0].number")

# Inline comments
gh api "repos/$REPO/pulls/$PR_NUM/comments" \
  --jq '.[] | {id: .id, body: .body, path: .path, line: .line}'

# Reviews requesting changes
gh api "repos/$REPO/pulls/$PR_NUM/reviews" \
  --jq '.[] | select(.state == "CHANGES_REQUESTED") | {id: .id, body: .body}'
```

For each comment:

| Type | Action |
|---|---|
| Real bug | Fix the code, commit, reply with commit SHA |
| Small improvement | Fix it, commit, reply with SHA |
| Large refactor | Create follow-up issue, reply with issue link |
| False positive | Reply with explanation |

Reply to a comment:
```bash
gh api "repos/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies" \
  --method POST \
  -f body="Fixed in $(git rev-parse --short HEAD): <what and why>"
```

---

### [INT-3] Check CI — fix failing checks

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$(git branch --show-current)\")][0].number")
HEAD_SHA=$(gh pr view "$PR_NUM" --json headRefOid --jq '.headRefOid')
PR_STATE=$(gh pr view "$PR_NUM" --json state --jq '.state')

if [ "$PR_STATE" = "MERGED" ]; then
  echo "PR already merged — skip to INT-6"
  exit 0
fi

# Check failing runs
gh api "repos/$REPO/commits/$HEAD_SHA/check-runs?per_page=100" \
  --jq '.check_runs[] | select(.conclusion == "failure") | {name: .name}'
```

**If checks are still running:**

Do not use `sleep`. Do NOT mark INT-3 done. Stop this iteration — the general loop at the end of this skill will schedule the next check via CronCreate.

**If failures exist:**
1. Get logs: `gh run view $RUN_ID --log-failed 2>&1 | tail -200`
2. Identify root cause
3. Check if failure is in your blast radius:
   ```bash
   git diff --name-only origin/develop..HEAD
   ```
4. If NOT in blast radius → retrigger CI with an empty commit:
   ```bash
   git commit --allow-empty -m "ci: retrigger CI"
   git push origin HEAD
   ```
5. If YES in blast radius → fix the code, commit, push

**Only mark INT-3 done** when all required checks are `success`:
```bash
gh api "repos/$REPO/commits/$HEAD_SHA/check-runs?per_page=100" \
  --jq '[.check_runs[] | select(.name | test("gate|required")) | .conclusion] | all(. == "success")'
# → true = CI green
```

---

### [INT-4] Rebase if BEHIND

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$(git branch --show-current)\")][0].number")
MERGE_STATE=$(gh pr view "$PR_NUM" --json mergeStateStatus --jq '.mergeStateStatus')

if [ "$MERGE_STATE" = "BEHIND" ] || [ "$MERGE_STATE" = "DIRTY" ]; then
  git fetch origin develop
  git rebase origin/develop

  # Conflict strategy:
  # - Docs (*.md): keep develop as base, add branch changes manually
  # - Source files: analyse manually — never blind --theirs
  # - Lock files (package-lock.json, yarn.lock): --theirs + reinstall dependencies

  git push origin HEAD --force-with-lease
fi
```

---

### [INT-5] Merge PR

```bash
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$(git branch --show-current)\")][0].number")
MERGE_STATE=$(gh pr view "$PR_NUM" --json mergeStateStatus --jq '.mergeStateStatus')

if [ "$MERGE_STATE" = "CLEAN" ]; then
  gh pr merge "$PR_NUM" --squash
else
  echo "PR not ready: $MERGE_STATE — re-run INT-3/INT-4 first"
  exit 0
fi
```

---

### [INT-6] Post-merge: docs + DoD/AC + close issue

```bash
PR_NUM=$(gh pr list --state merged --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$(git branch --show-current)\")][0].number")
```

**a) Verify docs are up to date:**
```bash
gh pr view "$PR_NUM" --json files --jq '.files[].path'
```

Check relevant project docs against the changed files. Update any that are out of sync.

**b) Cross DoD/AC checkboxes with evidence:**
```bash
gh issue view "$GH_ISSUE" --json body --jq '.body' > /tmp/issue_body.txt

COMMIT_SHAS=$(gh pr view "$PR_NUM" --json commits \
  --jq '[.commits[].oid[:8]] | join(", ")')

python3 << 'EOF'
with open('/tmp/issue_body.txt') as f:
    body = f.read()
# body = body.replace('- [ ] AC text', '- [x] AC text — **Evidence:** PR #... commits: ...')
with open('/tmp/issue_body_fixed.txt', 'w') as f:
    f.write(body)
EOF
gh issue edit "$GH_ISSUE" --body "$(cat /tmp/issue_body_fixed.txt)"
```

**c) Close issue (only if all DoD are checked):**
```bash
REMAINING=$(gh issue view "$GH_ISSUE" --json body --jq '.body' \
  | grep -c '^\- \[ \]' || echo 0)

if [ "$REMAINING" -eq 0 ]; then
  gh issue close "$GH_ISSUE" --comment "Implementation complete. PR merged to develop. All DoD verified."
else
  echo "$REMAINING unchecked DoD items — issue not closed"
  gh issue comment "$GH_ISSUE" --body "$REMAINING DoD checkboxes still open — needs manual verification."
fi
```

Write final status (update `## Status` section, don't just append):
```bash
python3 << 'EOF'
with open('plans/{issue}-progress.md') as f:
    body = f.read()
if '## Status' in body:
    body = body.replace('## Status\nIN_PROGRESS', '## Status\nMERGED')
else:
    body += '\n## Status\nMERGED\n'
with open('plans/{issue}-progress.md', 'w') as f:
    f.write(body)
EOF
git add plans/{issue}-progress.md
git commit -m "done: issue #{issue} closed — MERGED" || true
git push origin HEAD || true
```

---

## Step 3: Mark Task Done

```bash
python3 << 'EOF'
with open('plans/{issue}-progress.md') as f:
    body = f.read()
body = body.replace('- [ ] [INT-X]', '- [x] [INT-X]')  # replace X with task number
with open('plans/{issue}-progress.md', 'w') as f:
    f.write(body)
EOF

git add plans/{issue}-progress.md
git commit -m "progress: [INT-X] done" || true
git push origin HEAD || true
```

**Exception:** INT-3 is only marked done when CI is green (it repeats).
**Exception:** INT-6 writes `MERGED` — this is the final completion signal.

---

## Loop Setup (REQUIRED at end of every iteration)

After marking the task done, check if integration is complete:

```bash
REMAINING=$(grep -c '^\- \[ \] \[INT-' plans/{issue}-progress.md || echo 0)
STATUS=$(python3 - << 'EOF'
import re
with open('plans/{issue}-progress.md') as f:
    body = f.read()
m = re.search(r'## Status\n([A-Z_]+)', body)
print(m.group(1) if m else '')
EOF
)
echo "Remaining INT tasks: $REMAINING, Status: $STATUS"
```

**If integration is NOT complete (`REMAINING > 0` or `STATUS != MERGED`):**

Schedule the next integration iteration using CronCreate:

```
CronCreate(
  cron: "*/1 * * * *",
  prompt: "/integrate — continue issue #{issue}. Plan: plans/{issue}-plan.md, Progress: plans/{issue}-progress.md",
  recurring: false
)
```

**If `STATUS = MERGED`:**

Do not schedule another iteration. Integration is complete.

---

## Rules

- **One task per iteration** — stop after marking it `[x]`
- **INT-3 repeats** until CI is green — don't mark it done prematurely
- **Never skip tests** — fix the root cause
- **Never blind `--theirs`** — analyse conflicts manually
- **Never use `Fixes #NNN`** in commits — use `Part of #NNN`
