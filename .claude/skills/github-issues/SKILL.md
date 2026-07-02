# /github-issues — Create Effective Issues

Your role: **Issue Architect**. Help create clear, actionable, trackable issues.

**A good issue = someone can implement it without asking questions.**

---

## Issue Templates

### Feature Request

```markdown
## Description
[One sentence: what does this feature do?]

## User Story
As a [role], I want [capability], so that [benefit].

## Acceptance Criteria
- [ ] AC1: [Specific, testable criterion]
- [ ] AC2: [Another measurable criterion]
- [ ] AC3: [Edge case handled]

## Technical Notes
[Implementation hints, relevant files, dependencies]

## Definition of Done
- [ ] Code implemented and tested
- [ ] Unit tests written
- [ ] Documentation updated if needed
- [ ] PR reviewed and approved
- [ ] Merged to develop
```

### Bug Report

```markdown
## Bug Description
[One sentence: what's broken?]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [See error]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 14.0]
- Browser: [e.g., Chrome 120]
- Version: [e.g., v1.2.3]

## Possible Cause
[If known, suggest where the bug might be]

## Definition of Done
- [ ] Bug reproduced
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Test added to prevent regression
- [ ] PR merged
```

---

## Writing Good Acceptance Criteria

Each AC must be:
- **Specific** — No ambiguity
- **Measurable** — Can verify pass/fail
- **Testable** — Can write a test for it

### Examples

| ❌ Bad | ✅ Good |
|--------|---------|
| "Page should load fast" | "Page loads in <2s on 3G" |
| "User can login" | "User can login with email + password" |
| "Handle errors" | "Show error toast when API returns 4xx" |
| "Works on mobile" | "Layout responsive at 320px-768px widths" |

---

## Labels

| Label | Meaning |
|-------|---------|
| `bug` | Something isn't working |
| `feature` | New functionality |
| `enhancement` | Improvement to existing feature |
| `documentation` | Docs only |
| `good first issue` | Good for newcomers |
| `P0-critical` | Must fix immediately |
| `P1-high` | Important, this sprint |
| `P2-medium` | Nice to have |

---

## Commands

```bash
# Create issue
gh issue create --title "feat: add search" --body "..."

# Create with template
gh issue create --template feature_request.md

# List issues
gh issue list --state open
gh issue list --label bug

# View issue
gh issue view 123

# Close with comment
gh issue close 123 --comment "Fixed in PR #456"

# Add label
gh issue edit 123 --add-label "P1-high"
```

---

## Linking Issues and PRs

```markdown
# In PR description:
Closes #123          # Auto-closes issue when merged
Fixes #123           # Same as Closes
Part of #100         # Links without auto-close
Addresses #123       # Links without auto-close
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Vague title | Can't search for it | Be specific: "Login fails on Safari" |
| No ACs | Don't know when done | Add 2-3 testable criteria |
| Too big | Can't estimate time | Split into smaller issues |
| No context | Others can't help | Add background, links |
| Missing labels | Gets lost | Add priority + type |

---

## Issue Hygiene

- **Close stale issues** — >60 days inactive = probably won't be done
- **Link related issues** — Use "Related to #X" in description
- **Update status** — Comment when starting work, blocked, or done
- **One issue = one thing** — Don't bundle unrelated work

---

## Output

When creating an issue:

```
✅ Issue Created

#123: feat: add dark mode toggle
Labels: feature, P2-medium
ACs: 3 defined
Next: Add to sprint or backlog
```
