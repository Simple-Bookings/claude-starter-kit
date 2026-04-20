---
name: review
description: Review phase — deep code analysis, blast-radius testing, and quality gate. Finds what a fast executor misses. Outputs APPROVED or NEEDS_FIXES. Use after /build.
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# /review — Review Phase

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

Run ONLY tests for changed files — **never the full test suite**.

```bash
# Step 1: Find changed files
CHANGED=$(git diff --name-only HEAD~5 | grep -E "\.(ts|tsx)$" | grep -v node_modules)

# Step 2: Find their test files
for f in $CHANGED; do
  base=$(basename "$f" | sed 's/\.[tj]sx\?$//')
  find "$(dirname "$f")" -maxdepth 3 \
    \( -name "${base}.test.*" -o -name "${base}.spec.*" \) 2>/dev/null
done | sort -u > /tmp/blast-radius-tests.txt

# Step 3: Run only those tests
if [ -s /tmp/blast-radius-tests.txt ]; then
  TEST_FILES=$(cat /tmp/blast-radius-tests.txt | tr '\n' ' ')
  # Replace with your test runner:
  npx vitest run --bail 1 $TEST_FILES
  # or: jest $TEST_FILES
fi
```

---

## Step 5: PR Management

Check if PR exists:
```bash
gh pr list --state all --json number,title,headRefName \
  --jq "[.[] | select(.headRefName == \"$(git branch --show-current)\")][0]"
```

Create if missing:
```bash
gh pr create --base develop \
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

Schedule a new `/build` loop to fix the issues:

```
CronCreate(
  cron: "*/1 * * * *",
  prompt: "/build — fix review findings for issue #{issue}. Plan: plans/{issue}-plan.md, Progress: plans/{issue}-progress.md",
  recurring: false
)
```

**If verdict is APPROVED:**

Do not schedule anything. Tell the user to run `/integrate`.
