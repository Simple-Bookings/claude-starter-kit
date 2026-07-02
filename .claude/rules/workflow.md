# Workflow & Delegation

**Every team member owns a domain.** Ownership means: informed about changes, involved in decisions, assigned relevant issues.

---

## Delegation — Never Just "Say It Out Loud"

> Mentioning a task in conversation is NOT enough. It disappears in the context window and never gets done.

**Use at least one of these methods:**

| Method | When | How |
|--------|------|-----|
| **GitHub Issue + Label** | Bugs, features, tech debt | Create issue with `owner:{name}` label |
| **Email** | Important info, decisions, handover | Send to `{name}@your-project.com` |
| **Agent Spawn** | Urgent, needs to happen NOW | `Agent(subagent_type: "{name}", prompt: "...")` |
| **GitHub Issue Comment** | Add context to existing issue | `gh issue comment {nr} --body "..."` |

---

## Handover Protocol

When you encounter something outside your area of responsibility:

1. **Identify the owner** — check team profiles or ask
2. **Create a trackable artifact** — issue, email, or comment (NEVER just verbal)
3. **Include context** — what you found, why it's relevant, what needs to be done
4. **Mention it briefly** in conversation — "I've created #XXXX and assigned [name]"

```bash
# ✅ CORRECT — trackable and actionable
gh issue create \
  --title "fix: brief description" \
  --label "owner:dan,P1-high,type:bug" \
  --body "Description of the problem and what needs to be done."

# ❌ WRONG — disappears in context window
"This is probably something for Dan."
```

---

## Issue Claiming

**Before starting work on an issue — claim it.**

1. Check if issue already has `status:in-progress` label
2. Check if there are open PRs for the issue
3. Add `status:in-progress` label
4. THEN create branch and start work

```bash
# Check for existing work
gh pr list --state open --search "#123"

# Claim the issue
gh issue edit 123 --add-label "status:in-progress"

# Now start working
git checkout -b fix/issue-123
```

---

## Parallel Work Coordination

When multiple people might work on the same codebase:

1. **Communicate** what you're working on
2. **Claim issues** before starting
3. **Use feature branches** — never work directly on develop/main
4. **Keep PRs small** — easier to merge, fewer conflicts
5. **Merge frequently** — don't let branches diverge too far
