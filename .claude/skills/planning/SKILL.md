---
name: planning
description: Planning phase — groom a GitHub issue, analyse the codebase, and produce a concrete task list that a fast executor can follow without ambiguity. Use before /execution.
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# /planning — Planning Phase

Your role: **Scrum Master / Planning Lead**. Analyse the issue, understand the codebase, and write a task list so precise that the executor never needs to make a design decision.

**Do NOT implement anything in this phase.**

---

## Step 1: Load Issue Context

```bash
gh issue view $GH_ISSUE --json title,body,labels,comments,assignees,state
```

Also check:
- Existing branches: `git branch -a | grep -i "$GH_ISSUE"`
- Existing PRs: `gh pr list --state open --search "#$GH_ISSUE in:body" --json number,title,headRefName,url`
- Recent main branch commits: `git log origin/main..HEAD --oneline -10`
- Referenced issues: extract `#NNN` from body/comments, check their state

If a branch or PR already exists, note it — the build phase must use it instead of creating a new one.

---

## Step 2: Issue Readiness (Definition of Ready)

| Criteria | Question |
|---|---|
| Clear description | Can a developer implement without guessing? |
| Testable ACs | Are acceptance criteria specific and verifiable? |
| DoD with evidence requirements | Are there checkboxes with concrete proof requirements? |
| No blocking dependencies | Are referenced issues closed or non-blocking? |
| Realistic scope | Can it be done in ~10 build iterations? |
| How to test | Are there concrete test steps? |

**If a criteria fails:**
- If fixable (missing ACs, vague DoD) → fix it via `gh issue edit`
- If human input is needed → add `needs:human` label, write `BLOCKED` to progress file
- If scope is too large → reduce scope, create follow-up issue

---

## Step 3: Deep Code Analysis

Before writing tasks, understand the codebase:

```bash
# Find related code
grep -r "relevantPattern" --include="*.ts" --include="*.tsx" -l

# Find related test files
find . -name "*.test.*" -o -name "*.spec.*" | xargs grep -l "relevantPattern" 2>/dev/null

# Check similar existing implementations
grep -r "similarFunction" --include="*.ts" -l
```

Identify:
1. All files that need to change
2. Cross-cutting concerns (auth, types, migrations, tests)
3. Dependencies between tasks
4. Patterns already in use that the executor should follow

---

## Step 4: Update GitHub Issue

After your analysis, update the issue with findings:

```bash
gh issue view $GH_ISSUE --json body --jq '.body' > /tmp/body.txt
python3 << 'EOF'
with open('/tmp/body.txt') as f:
    body = f.read()
# Add/improve ACs, DoD, how-to-test
body = body.replace('- [ ] Vague AC', '- [ ] Specific, testable AC')
with open('/tmp/body_fixed.txt', 'w') as f:
    f.write(body)
EOF
gh issue edit $GH_ISSUE --body "$(cat /tmp/body_fixed.txt)"
```

Add a comment with the plan summary:
```bash
gh issue comment $GH_ISSUE --body "$(cat <<'EOF'
## Plan
- Tasks: X planned
- Root cause: <brief summary>
- Files to change: <list>
- Estimated iterations: N
EOF
)"
```

---

## Step 5: Write Plan File

Write to `plans/{issue}-plan.md`:

```markdown
# Plan: Issue #$GH_ISSUE

## Context
<What the issue asks for and why>

## Files to Change
| File | Change | Reason |
|------|--------|--------|
| path/to/file.ts | Add X | Implements AC-1 |

## Task List
- [ ] Task 1: description — **File:** path — **Verify:** command
- [ ] Task 2: description — **File:** path — **Verify:** command

## DoD Verification
- [ ] AC-1 met — **Evidence:** command
- [ ] Tests pass — **Evidence:** test run command
- [ ] Build clean — **Evidence:** build command
```

---

## Step 6: Write Progress File

Write to `plans/{issue}-progress.md`:

```markdown
# Progress: Issue #$GH_ISSUE

## Status
IN_PROGRESS

## Tasks
- [ ] Task 1: description — **File:** path — **Verify:** command
- [ ] Task 2: description — **File:** path — **Verify:** command

## Notes
<discoveries, decisions, risks>
```

---

## Task Format Requirements

Every task MUST have:
1. **Description** — specific and unambiguous
2. **File** — exact file path(s)
3. **Verify** — command that proves the task is done

---

## Rules

- **Do NOT modify source files** — only plan/progress files and the GH issue
- **Do NOT create branches or PRs** — the build phase handles that
- **Search thoroughly** before assuming something is missing
- **Every task** must be completable in one build iteration
- **Order tasks** by dependency (blocking tasks first)
- Use subagents for parallel codebase exploration

## Done Criteria

You are done when:
1. ✅ Plan file written with concrete tasks
2. ✅ Progress file written
3. ✅ GitHub issue updated (ACs, DoD, how-to-test)
4. ✅ Comment posted with plan summary
