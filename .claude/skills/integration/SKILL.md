---
name: integration
description: Integration phase — manage the PR through CI, handle review comments, rebase if needed, merge, and close the issue. Run in a loop, one task per iteration. Use after /reviewing APPROVED.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# /integration — Integration Phase

Your role: **Integration Engineer**. Execute exactly ONE integration task, mark it `[x]`, and stop. The loop calls you again for the next task.

**One task per iteration. No more.**

---

## Step 1: Find Next Task

```bash
grep -n '^\- \[ \] \[INT-' plans/{issue}-progress.md | head -1
```

If no `[INT-*]` tasks exist yet → run **Step 0: Detect Environment** first, then initialise the task list.

If all `[INT-*]` tasks are `[x]` → `INT-6` has written `MERGED` to `## Status`. Stop.

---

## Step 0: Detect Environment (only when initialising INT tasks)

Run this probe once. The results determine which INT tasks are relevant and which are N/A.

```bash
# Current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Branch type: feature branch or integration branch (main/develop/master)?
echo "$CURRENT_BRANCH" | grep -qE "^(main|master|develop)$" \
  && BRANCH_TYPE="integration" \
  || BRANCH_TYPE="feature"
echo "Branch type: $BRANCH_TYPE"

# Does a develop branch exist?
git branch -a | grep -qE "(^|\s)develop$|(^|\s)remotes/origin/develop$" \
  && HAS_DEVELOP="true" || HAS_DEVELOP="false"
echo "Has develop: $HAS_DEVELOP"

# What is the repo default branch?
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || echo "main")
echo "Default branch: $DEFAULT_BRANCH"

# Determine integration branch (where PRs should target)
if [ "$HAS_DEVELOP" = "true" ]; then
  INTEGRATION_BRANCH="develop"
else
  INTEGRATION_BRANCH="$DEFAULT_BRANCH"
fi
echo "Integration branch: $INTEGRATION_BRANCH"

# Is there already a PR for this branch?
PR_NUM=$(gh pr list --state all --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$CURRENT_BRANCH\")][0].number // empty")
echo "Existing PR: ${PR_NUM:-none}"

# What CI workflows exist?
ls .github/workflows/ 2>/dev/null \
  && grep -h "^name:" .github/workflows/*.yml 2>/dev/null \
  || echo "No CI workflows found"

# Are there required status checks on the integration branch?
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
gh api "repos/$REPO/branches/$INTEGRATION_BRANCH/protection" \
  --jq '.required_status_checks.contexts // []' 2>/dev/null \
  || echo "No branch protection / required checks"
```

**Based on the probe, initialise INT tasks — marking N/A tasks immediately:**

```bash
# Determine which tasks are N/A up front
# - INT-1 (PR): N/A if BRANCH_TYPE=integration (committed directly to main/develop)
# - INT-2 (review comments): N/A if no PR exists or BRANCH_TYPE=integration
# - INT-3 (CI): N/A if no CI workflows exist
# - INT-4 (rebase): N/A if BRANCH_TYPE=integration
# - INT-5 (merge): N/A if BRANCH_TYPE=integration
# - INT-6 (close issue): always runs

python3 << 'PYEOF'
import subprocess, re

branch = subprocess.check_output(['git','branch','--show-current']).decode().strip()
is_integration = bool(re.match(r'^(main|master|develop)$', branch))
has_develop = bool(subprocess.run(
    ['git','branch','-a'], capture_output=True, text=True
).stdout.find('develop') >= 0)
integration_branch = 'develop' if has_develop else 'main'

pr_result = subprocess.run(
    ['gh','pr','list','--state','all','--json','number,headRefName',
     '--jq', f'[.[] | select(.headRefName == "{branch}")][0].number // empty'],
    capture_output=True, text=True
).stdout.strip()
has_pr = bool(pr_result)

has_ci = bool(subprocess.run(
    ['ls','.github/workflows/'], capture_output=True
).returncode == 0)

def task(n, label, na_condition, na_reason=""):
    if na_condition:
        return f"- [x] [INT-{n}] {label} — N/A: {na_reason}"
    return f"- [ ] [INT-{n}] {label}"

tasks = [
    task(1, "Create/find PR and enable auto-merge",
         is_integration, f"commits gik direkte til {branch}"),
    task(2, "Handle all open PR review comments",
         is_integration or not has_pr, "ingen PR"),
    task(3, "Check CI status — fix failing checks (gentages til grøn)",
         not has_ci, "ingen CI workflows fundet"),
    task(4, f"Rebase branch if BEHIND {integration_branch}",
         is_integration, f"ingen feature-branch"),
    task(5, "Merge PR",
         is_integration, f"direkte på {branch}"),
    "- [ ] [INT-6] Post-merge: docs verification + DoD/AC + close issue",
]

env_block = f"""
## Environment (integration)
- **Current branch:** {branch}
- **Branch type:** {"integration — commits direkte på denne branch" if is_integration else "feature — skal merges via PR"}
- **Integration branch:** {integration_branch}
- **Has develop branch:** {has_develop}
- **Existing PR:** {pr_result if has_pr else "ingen"}
- **CI workflows:** {"ja" if has_ci else "ingen"}
"""

with open('plans/{{issue}}-progress.md') as f:
    body = f.read()

if '## Integration Tasks' not in body:
    body += env_block + "\n## Integration Tasks\n" + "\n".join(tasks) + "\n"

with open('plans/{{issue}}-progress.md', 'w') as f:
    f.write(body)

print("Environment detected and INT tasks initialised.")
print(f"Branch type: {'integration' if is_integration else 'feature'}")
print(f"Integration branch: {integration_branch}")
print(f"Tasks marked N/A: INT-1={is_integration}, INT-2={is_integration or not has_pr}, INT-3={not has_ci}, INT-4={is_integration}, INT-5={is_integration}")
PYEOF
```

After running the probe and writing the tasks, commit the progress file and **stop this iteration**:

```bash
git add plans/{issue}-progress.md
git commit -m "progress: [INT-0] environment detected, INT tasks initialised"
git push origin HEAD
```

Then schedule the next iteration via CronCreate and stop.

---

## Step 2: Execute the Task

Read `## Environment (integration)` from the progress file before executing any task.

---

### [INT-1] Create/find PR and enable auto-merge

*(Skip if marked N/A)*

```bash
BRANCH=$(git branch --show-current)
# Read integration branch from ## Environment in progress file
INTEGRATION_BRANCH="develop"  # replace with value from ## Environment

PR_NUM=$(gh pr list --state all --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number // empty")

if [ -z "$PR_NUM" ]; then
  gh pr create --base "$INTEGRATION_BRANCH" \
    --title "fix(#{issue}): <description>" \
    --body "Part of #{issue}"
  PR_NUM=$(gh pr list --state all --json number,headRefName \
    --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number")
fi

gh pr merge "$PR_NUM" --auto --squash 2>/dev/null \
  && echo "Auto-merge enabled" \
  || echo "Auto-merge ikke tilgængeligt — merger manuelt i INT-5"
```

---

### [INT-2] Handle open PR review comments

*(Skip if marked N/A)*

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
BRANCH=$(git branch --show-current)
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number")

# Inline comments
gh api "repos/$REPO/pulls/$PR_NUM/comments" \
  --jq '.[] | {id: .id, body: .body, path: .path, line: .line}'

# Reviews requesting changes
gh api "repos/$REPO/pulls/$PR_NUM/reviews" \
  --jq '.[] | select(.state == "CHANGES_REQUESTED") | {id: .id, body: .body}'
```

For each comment:

| Type | Handling |
|---|---|
| Reel bug | Fix koden, commit, svar med commit SHA |
| Lille forbedring | Fix det, commit, svar med SHA |
| Stor refaktor | Opret follow-up issue, svar med issue-link |
| False positive | Svar med forklaring |

Reply:
```bash
gh api "repos/$REPO/pulls/$PR_NUM/comments/$COMMENT_ID/replies" \
  --method POST \
  -f body="Fixed in $(git rev-parse --short HEAD): <what and why>"
```

---

### [INT-3] Check CI — fix failing checks

*(Skip if marked N/A — ingen CI workflows)*

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
HEAD_SHA=$(git rev-parse HEAD)

# Hent check-status på HEAD (fungerer både med og uden PR)
gh api "repos/$REPO/commits/$HEAD_SHA/check-runs?per_page=100" \
  --jq '.check_runs[] | {name: .name, status: .status, conclusion: .conclusion}'
```

**Hvis checks stadig kører:** stop iterationen — schedule næste INT-3 via CronCreate. Markér IKKE INT-3 done.

**Hvis failures:**
1. `gh run view $RUN_ID --log-failed 2>&1 | tail -200`
2. Find root cause
3. Er fejlen i dit blast radius? `git diff --name-only origin/main..HEAD`
4. Nej → retrigger: `git commit --allow-empty -m "ci: retrigger CI" && git push origin HEAD`
5. Ja → fix koden, commit, push

**Markér INT-3 done kun når alle checks er `success`:**
```bash
gh api "repos/$REPO/commits/$HEAD_SHA/check-runs?per_page=100" \
  --jq '[.check_runs[] | .conclusion] | all(. == "success")'
# → true = CI grøn
```

---

### [INT-4] Rebase if BEHIND

*(Skip if marked N/A)*

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
BRANCH=$(git branch --show-current)
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number")
MERGE_STATE=$(gh pr view "$PR_NUM" --json mergeStateStatus --jq '.mergeStateStatus')
# Read integration branch from ## Environment
INTEGRATION_BRANCH="develop"

if [ "$MERGE_STATE" = "BEHIND" ] || [ "$MERGE_STATE" = "DIRTY" ]; then
  git fetch origin "$INTEGRATION_BRANCH"
  git rebase "origin/$INTEGRATION_BRANCH"

  # Conflict strategy:
  # - Docs (*.md): behold integration-branch som base, tilføj branch-ændringer manuelt
  # - Source files: analysér manuelt — aldrig blind --theirs
  # - Lock files (package-lock.json, yarn.lock): --theirs + geninstallér afhængigheder

  git push origin HEAD --force-with-lease
fi
```

---

### [INT-5] Merge PR

*(Skip if marked N/A)*

```bash
BRANCH=$(git branch --show-current)
PR_NUM=$(gh pr list --state open --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number")
MERGE_STATE=$(gh pr view "$PR_NUM" --json mergeStateStatus --jq '.mergeStateStatus')

if [ "$MERGE_STATE" = "CLEAN" ]; then
  gh pr merge "$PR_NUM" --squash
else
  echo "PR ikke klar: $MERGE_STATE — kør INT-3/INT-4 igen"
  exit 0
fi
```

---

### [INT-6] Post-merge: docs + DoD/AC + close issue

```bash
# Find seneste merged PR på denne branch (hvis der er en)
BRANCH=$(git branch --show-current)
PR_NUM=$(gh pr list --state merged --json number,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0].number // empty")
```

**a) Verificér docs:**

Tjek ændrede filer mod relevante docs:
```bash
git diff --name-only HEAD~10
```

Opdatér docs direkte hvis de er ude af sync — små korrektioner kræver ikke separate tasks.

**b) Kryds DoD/AC-bokse af med evidens:**

```bash
gh issue view "$GH_ISSUE" --json body --jq '.body' > /tmp/issue_body.txt
python3 << 'EOF'
with open('/tmp/issue_body.txt') as f:
    body = f.read()
# body = body.replace('- [ ] AC text', '- [x] AC text — **Evidence:** ...')
with open('/tmp/issue_body_fixed.txt', 'w') as f:
    f.write(body)
EOF
gh issue edit "$GH_ISSUE" --body "$(cat /tmp/issue_body_fixed.txt)"
```

**c) Luk issue (kun hvis alle DoD er krydset):**

```bash
REMAINING=$(gh issue view "$GH_ISSUE" --json body --jq '.body' \
  | grep -c '^\- \[ \]' || echo 0)

if [ "$REMAINING" -eq 0 ]; then
  gh issue close "$GH_ISSUE" --comment "$(cat <<'MSG'
Implementation komplet. Alle DoD verificeret.
MSG
)"
else
  echo "$REMAINING umarkerede DoD — issue lukkes ikke"
  gh issue comment "$GH_ISSUE" --body "$REMAINING DoD-checkboxes er stadig åbne — kræver manuel verifikation."
fi
```

**d) Skriv MERGED til progress-filen:**

```bash
python3 << 'EOF'
import re
with open('plans/{issue}-progress.md') as f:
    body = f.read()
body = re.sub(r'## Status\n\w+', '## Status\nMERGED', body)
with open('plans/{issue}-progress.md', 'w') as f:
    f.write(body)
EOF
git add plans/{issue}-progress.md
git commit -m "done: issue #{issue} lukket — MERGED" || true
git push origin HEAD || true
```

---

## Step 3: Mark Task Done

```bash
python3 << 'EOF'
with open('plans/{issue}-progress.md') as f:
    body = f.read()
body = body.replace('- [ ] [INT-X]', '- [x] [INT-X]')  # erstat X med task-nummer
with open('plans/{issue}-progress.md', 'w') as f:
    f.write(body)
EOF

git add plans/{issue}-progress.md
git commit -m "progress: [INT-X] done" || true
git push origin HEAD || true
```

**Undtagelse:** INT-3 markeres kun done når CI er grøn.
**Undtagelse:** INT-6 skriver `MERGED` — det er det endelige completion-signal.

---

## Loop Setup (REQUIRED at end of every iteration)

```bash
REMAINING=$(grep -c '^\- \[ \] \[INT-' plans/{issue}-progress.md || echo 0)
STATUS=$(python3 -c "
import re
with open('plans/{issue}-progress.md') as f: body = f.read()
m = re.search(r'## Status\n([A-Z_]+)', body)
print(m.group(1) if m else '')
")
echo "Remaining INT tasks: $REMAINING, Status: $STATUS"
```

**Hvis integration IKKE er komplet (`REMAINING > 0` eller `STATUS != MERGED`):**

```
CronCreate(
  cron: "*/1 * * * *",
  prompt: "/integration — fortsæt issue #{issue}. Plan: plans/{issue}-plan.md, Progress: plans/{issue}-progress.md",
  recurring: false
)
```

**Hvis `STATUS = MERGED`:** stop — integration er komplet.

---

## Rules

- **Probe first** — læs altid `## Environment (integration)` inden du udfører noget
- **One task per iteration** — stop efter at have markeret den `[x]`
- **INT-3 gentages** til CI er grøn — markér den ikke done for tidligt
- **Aldrig blind `--theirs`** — analysér konflikter manuelt
- **Aldrig `Fixes #NNN`** i commits — brug `Part of #NNN`
- **N/A tasks tæller som done** — de blokerer ikke loop-fremgang
