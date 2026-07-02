# Exercise 04: Code Review & PRs

**Goal:** Use Claude to create PRs and review code systematically.

**Skills:** `/reviewing`

**Time:** 20 minutes

---

## What You'll Learn

- Claude writes PR descriptions
- Claude reviews code for common issues
- The review-fix-verify cycle

## Step 1: Create a PR

Ask Claude:

```
Create a PR for the formatDuration feature.
Base it on develop.
Write a description that explains what it does and how to test it.
```

Claude will:
1. Push the branch
2. Create the PR with title and description
3. Return the PR URL

## Step 2: Self-Review

Before requesting review from others:

```
Review the code in this PR. Look for:
- Code quality issues
- Missing test cases
- Any console.logs or TODOs left
- Edge cases not covered
```

Claude analyzes the diff and reports findings.

## Step 3: Fix Issues

If Claude found problems:

```
Fix the issues you found and push the changes.
```

Claude will:
1. Make the changes
2. Commit: `refactor: address review feedback`
3. Push to update the PR

## Step 4: Final Review Checklist

```
/reviewing

Run through the review checklist for this PR.
```

Claude verifies:
- [ ] Tests pass
- [ ] No debug code
- [ ] Follows code conventions
- [ ] No security issues
- [ ] Build succeeds

## Step 5: Merge

```
Merge the PR and clean up.
```

Claude squash-merges and deletes the branch.

## The Review Pattern

```
Stage    You say                 Claude does
────────────────────────────────────────────────────────────────
Create   "Create a PR for X"     Pushes, writes description
Review   "Review for issues"     Analyzes diff, reports problems
Fix      "Fix those"             Commits fixes, updates PR
Merge    "Merge and clean up"    Squash merge, delete branch
```

## Why This Works

- Self-review catches obvious issues before wasting others' time
- Consistent checklists prevent recurring problems
- Automated cleanup keeps repo tidy

## Verification

- [ ] PR created with good description
- [ ] Claude found at least one issue
- [ ] Issue was fixed
- [ ] PR merged

## Next

[Exercise 05: Debugging](05-debugging.md)
