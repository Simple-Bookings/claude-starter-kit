# Exercise 09: Agent Teams (Bonus)

**Goal:** Use agents for parallel and specialized work.

**Skills:** Agent spawning, work distribution

**Time:** 20 minutes

---

## What You'll Learn

- When to spawn agents vs do it yourself
- How to brief agents (they have NO context)
- Parallel work patterns

## When to Use Agents

```
Situation         Use Agent?   Why
────────────────────────────────────────────────────────────────
Review 5 files    Yes          Parallel saves time
Security audit    Yes          Specialized focus
Quick fix         No           Overhead not worth it
While CI runs     Yes          Use wait time productively
```

## The Challenge

You have 3 files to review for different concerns:
- `src/auth.ts` — security review
- `src/api.ts` — performance review  
- `src/ui.ts` — accessibility review

Doing this sequentially takes 15 minutes. With agents: 5 minutes.

## Step 1: Plan the Work

```
I need to review 3 files for different concerns.
Let's spawn 3 agents in parallel:
- Agent 1: Security review auth.ts
- Agent 2: Performance review api.ts
- Agent 3: Accessibility review ui.ts
```

## Step 2: Brief Each Agent

**Critical:** Agents don't see your conversation. Brief them fully!

```
Spawn a security-focused agent with this context:

"Review src/auth.ts for:
- SQL injection
- XSS vulnerabilities  
- Auth bypass risks
- Password handling

Report: file, line, issue, severity, fix suggestion.
No false positives — only report real issues."
```

The agent runs independently and returns results.

## Step 3: Collect Results

Each agent returns findings. You (or main Claude) synthesize:

```
Summarize all 3 agent reports.
Group by severity. What needs fixing first?
```

## Step 4: Try Specialized Agents

Create an agent profile:

```
Create a security-auditor agent profile in .claude/agents/security-auditor.md
It should focus on OWASP top 10 and always check for:
- Input validation
- Output encoding
- Authentication/authorization
```

Now use it:

```
Spawn the security-auditor agent to review the auth module.
```

## Anti-patterns

```
Don't                          Do
────────────────────────────────────────────────────────────────
"Review the code"              "Review auth.ts lines 45-80 for SQL injection"
Spawn for 2-minute tasks       Use agents for 10+ minute tasks
Forget to collect results      Always get agent summary before dismissing
```

## Verification

- [ ] Spawned at least 2 agents in parallel
- [ ] Briefed agents with full context
- [ ] Collected and synthesized results
- [ ] (Bonus) Created an agent profile

## Key Takeaway

**Agents are junior developers.** Give them clear, scoped tasks with all context. They work fast but need direction.

## Next

[Exercise 10: Custom Rules](10-custom-rules.md) (if time permits)
