---
name: reviewing
description: Review phase — deep code analysis, blast-radius testing, and quality gate. Finds what a fast executor misses. Outputs APPROVED or NEEDS_FIXES. Use after /execution.
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# /reviewing — Review Phase

Your role: **Senior Architect Reviewer**. Your job is NOT just "does it compile" — you do deep analysis that a fast executor misses. You are the quality gate.

**Do NOT implement fixes yourself** — add tasks to the progress file and let the executor fix them.

---

## Step 0: Load Context

Read the plan file and progress file:
- What was the original goal?
- What tasks were planned?
- What does the executor claim to have done?

```bash
cat plans/{issue}-plan.md
cat plans/{issue}-progress.md
```

---

## Step 0.5: Probe the Environment

Before reviewing anything, understand the repo's actual setup. Run all commands, then record findings in the progress file under `## Environment`.

```bash
# Which branches exist locally and remotely?
git branch -a

# What is the current branch?
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Does a develop branch exist?
git branch -a | grep -q "develop" && echo "HAS_DEVELOP=true" || echo "HAS_DEVELOP=false"

# Is the current branch a feature branch or an integration branch (main/develop)?
echo "$CURRENT_BRANCH" | grep -qE "^(main|master|develop)$" \
  && echo "BRANCH_TYPE=integration" \
  || echo "BRANCH_TYPE=feature"

# What CI workflows exist?
ls .github/workflows/ 2>/dev/null && cat .github/workflows/*.yml 2>/dev/null | grep -E "^name:|^\s+name:" | head -20 \
  || echo "NO_CI_WORKFLOWS"

# What test runner does the project use?
if [ -f package.json ]; then
  cat package.json | python3 -c "import sys,json; p=json.load(sys.stdin); print(p.get('scripts',{}))"
fi
ls vitest.config.* jest.config.* pytest.ini setup.cfg pyproject.toml 2>/dev/null || echo "no test config found"

# What is the default/target branch for PRs?
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null || echo "unknown"
```

**Classify the environment and write it to the progress file:**

```bash
python3 << 'EOF'
with open('plans/{issue}-progress.md') as f:
    body = f.read()

if '## Environment' not in body:
    env_block = """
## Environment
- **Branch type:** [feature | integration] — [branch name]
- **Integration branch:** [develop | main | master]
- **Has develop branch:** [yes | no]
- **CI workflows:** [list workflow names, or "none"]
- **Required CI checks:** [list check names from workflow, or "none"]
- **Test runner:** [vitest | jest | pytest | none detected]
- **PR needed:** [yes — commits on feature branch | no — commits directly on integration branch]
"""
    body = body + env_block

with open('plans/{issue}-progress.md', 'w') as f:
    f.write(body)
EOF
```

Fill in the values from the probe commands above before continuing.

---

## Step 1: Deep Code Analysis

The executor can write code and run tests. It lacks the ability to see **broad patterns across the codebase**. Find what it missed:

### a) Pattern consistency

```bash
# Find similar patterns that may also need updating
grep -r "changedPattern" --include="*.ts" --include="*.tsx" -l

# Check for callers/consumers of changed functions
grep -r "changedFunctionName" --include="*.ts" -l
```

Ask:
- Did the executor change a DTO but not the mapper?
- Did it change an API but not the E2E test?
- Are there other files following the same pattern that also need updating?

### b) Architectural impact

- Does the change break existing abstractions?
- Is error handling consistent with the rest of the codebase?
- Are there callers that need updating?

### c) Cross-cutting concerns

- **Security**: Is auth/authorization handled correctly? Any IDOR risks?
- **Types**: Are TypeScript types consistent? Any implicit `any`?
- **Migrations**: If schema changed, is the migration reversible? Is there a rollback?
- **Tests**: Does every new behaviour have a test?

### d) Mock coverage audit (for test files)

For each new test file, verify mocks match the implementation:

```bash
# Count DB calls in the implementation
grep -c "db\.\w*\.\(findMany\|findFirst\|update\|create\|delete\)" path/to/service.ts

# Count mock calls in the test
grep -c "mockResolvedValue\|mockRejectedValue" path/to/service.test.ts
```

If a function calls `findMany` twice, the test must mock it twice with `mockResolvedValueOnce`.

---

## Step 2: GitHub Issue Audit

```bash
gh issue view $GH_ISSUE --json body,labels,state
```

For each AC and DoD checkbox in the issue:
- Find the concrete code that satisfies it
- Verify with evidence (test output, grep, file exists)
- Cross the checkbox with proof if evidence exists
- Note as a finding if evidence is missing

Update issue via Python str.replace() (not sed):

```bash
gh issue view $GH_ISSUE --json body --jq '.body' > /tmp/body.txt
python3 << 'EOF'
with open('/tmp/body.txt') as f:
    body = f.read()
body = body.replace('- [ ] AC text', '- [x] AC text — **Evidence:** command output')
with open('/tmp/body_fixed.txt', 'w') as f:
    f.write(body)
EOF
gh issue edit $GH_ISSUE --body "$(cat /tmp/body_fixed.txt)"
```

---

## Step 3: Documentation Check

Find changed files:
```bash
git diff --name-only HEAD~10 | grep -E "\.(ts|tsx|js|jsx|py)$"
```

For each relevant doc in your project, check if the changes require an update:
- API documentation (new/changed endpoints)
- Architecture docs (new services, env vars, patterns)
- Feature/acceptance criteria docs
- Test coverage docs

Update directly if needed — small doc corrections don't need separate tasks.

---

## Step 4: Blast-Radius Tests

**First check the detected test runner from `## Environment`.** Skip this step entirely if no test runner was detected.

```bash
# Step 1: Find changed files
CHANGED=$(git diff --name-only HEAD~5 | grep -E "\.(ts|tsx|js|jsx|py)$" | grep -v node_modules)

# Step 2: Find their test files
for f in $CHANGED; do
  base=$(basename "$f" | sed 's/\.[tj]sx\?$//;s/\.py$//')
  find "$(dirname "$f")" -maxdepth 3 \
    \( -name "${base}.test.*" -o -name "${base}.spec.*" -o -name "test_${base}.py" \) 2>/dev/null
done | sort -u > /tmp/blast-radius-tests.txt

# Step 3: Run only those tests — adapt command to detected test runner
if [ -s /tmp/blast-radius-tests.txt ]; then
  TEST_FILES=$(cat /tmp/blast-radius-tests.txt | tr '\n' ' ')
  # vitest:
  npx vitest run --bail 1 $TEST_FILES
  # jest:   jest $TEST_FILES
  # pytest: python -m pytest $TEST_FILES -x
fi
```

If no test files exist for changed code, note it as an observation (not necessarily a finding unless the change introduces new behaviour).

---

## Step 5: PR Status

**Read `## Environment` from the progress file first.**

- If `PR needed: no` (commits directly on integration branch) → skip PR creation, note "no PR — committed directly to [branch]"
- If `PR needed: yes` (feature branch) → check if PR exists:

```bash
BRANCH=$(git branch --show-current)
gh pr list --state all --json number,title,headRefName \
  --jq "[.[] | select(.headRefName == \"$BRANCH\")][0]"
```

Create if missing, targeting the detected integration branch:

```bash
# Use integration branch from ## Environment (develop or main)
INTEGRATION_BRANCH="develop"  # or "main" if no develop branch

gh pr create --base "$INTEGRATION_BRANCH" \
  --title "feat(#{issue}): <description>" \
  --body "Part of #{issue}"
```

Post inline review comments for each finding:
```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
gh api "repos/$REPO/pulls/$PR_NUM/comments" \
  --method POST \
  -f body="**Finding:** description" \
  -f path="path/to/file.ts" \
  -f line=42 \
  -f side=RIGHT
```

---

## Step 6: Verdict

Choose ONE:

### APPROVED

All tasks verified, tests pass, issue requirements met.

If a PR exists:
```bash
gh pr review $PR_NUM --approve --body "$(cat <<'EOF'
## Review

**Verdict:** APPROVED
**Tests:** all passed
**Summary:** <brief>
EOF
)"
```

Update progress file:
```markdown
## Review
- **Verdict**: APPROVED
- **Verified**: <list of checks>

## Status
APPROVED
```

### NEEDS_FIXES

Issues found. DO NOT write APPROVED.

If a PR exists:
```bash
gh pr review $PR_NUM --request-changes --body "$(cat <<'EOF'
## Review

**Verdict:** NEEDS_FIXES

### Issues
1. <specific issue with evidence>
2. <specific issue with evidence>
EOF
)"
```

Add new tasks to the progress file for each issue:
```markdown
## Review
- **Verdict**: NEEDS_FIXES
- **Issues found**: 2
- **New tasks added**: 2

## Status
IN_PROGRESS

## Tasks
...existing tasks...
- [ ] Fix: description — **File:** path — **Verify:** command
- [ ] Fix: description — **File:** path — **Verify:** command
```

---

## Rules

- **Probe first** — never assume branch strategy or CI setup
- **Be specific** — "test fails" is not enough. Which test? What error?
- **Be fair** — don't nitpick style if the work is correct
- **Every new task needs File + Verify** — no vague tasks
- **Never remove completed tasks** — only add new ones
- **Never implement yourself** — that's the executor's job
- **Review actual code changes**, not just what the progress file claims
- **Commit your progress file** after writing verdict

```bash
git add plans/{issue}-progress.md
git commit -m "review: [APPROVED|NEEDS_FIXES] — cycle {N}"
git push origin HEAD
```

---

## Loop Setup (REQUIRED after verdict)

**If verdict is NEEDS_FIXES:**

Schedule a new `/execution` loop to fix the issues:

```
CronCreate(
  cron: "*/1 * * * *",
  prompt: "/execution — fix review findings for issue #{issue}. Plan: plans/{issue}-plan.md, Progress: plans/{issue}-progress.md",
  recurring: false
)
```

**If verdict is APPROVED:**

Do not schedule anything. Tell the user to run `/integration`.
