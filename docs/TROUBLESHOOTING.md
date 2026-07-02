# CSK2 Troubleshooting Guide

Quick reference for common issues w/ Claude Code, solutions, and prevention.

---

## 1. Context Overflow

**Symptom:** Claude forgets earlier conversation, repeats itself, loses context mid-task.

**Root causes:**
- Session running 2+ hours w/ many tool calls
- Large files read repeatedly (logs, schema, AI output)
- Many parallel tool invocations w/ large outputs
- Tokens approaching limit (~200k)

**Solutions:**

```bash
# Check current context size
/status  # shows token estimate

# Clear context and restart
/clear
# Claude resets session — start fresh conversation w/ same codebase

# Compact session (archive old messages)
/compact
# Keeps only recent turns, archives old ones to memory

# Start new session
# Close Claude window, reopen fresh
```

**Prevention:**
- Close sessions after 90+ min of heavy work
- Ask Claude to summarize findings before context fills
- Use `/compact` proactively during long tasks
- Delegate heavy lifting to background agents w/ `run_in_background: true`

---

## 2. Claude Hallucinates

**Symptom:** References files/functions that don't exist, invents code patterns, claims features exist.

**Root causes:**
- Claude training data is older than codebase
- File paths changed but Claude uses old names
- Function signatures refactored but Claude uses old version
- Claude assumes standard patterns that don't apply here

**Solutions:**

```bash
# 1. Ask Claude to read the file FIRST
"Read your-project/server/src/lib/api/auth.ts and verify the AuthIdentity type"

# 2. Verify outputs before using them
# - If Claude suggests `function foo()`, grep to confirm it exists
grep -r "function foo" your-project/

# 3. Ask Claude to search instead of assume
"Search for how we handle JWT refresh tokens — don't assume, grep first"

# 4. Cross-check against actual code
# When Claude claims "the BookingDTO has a `staffId` field":
grep -A 20 "interface BookingDTO" your-project/server/src/lib/api/types.ts
```

**Prevention:**
- Always start with `/read` or search, never assume patterns
- Ask Claude: "Does this file/function exist? Check before referencing."
- Use grep/search skills proactively
- Request explicit file paths, not loose references

---

## 3. Tests Fail in CI But Not Locally

**Symptom:** All tests pass `npm test` locally, but fail in GitHub Actions.

**Root causes:**
- Environment variables missing in CI
- Database state differs (stale test data, incomplete cleanup)
- Timing issues (network latency in CI runners)
- Port conflicts or resource limits
- OS differences (Linux in CI vs macOS locally)

**Solutions:**

**A. Check environment variables:**
```bash
# 1. List all env vars used by tests
grep -r "process.env\." your-project/server/src --include="*.test.ts" | cut -d: -f2 | sort -u

# 2. Verify .env.test has all required vars
cat your-project/server/.env.test

# 3. Check CI workflow for missing exports
gh workflow view ci.yml | grep "env:" -A 20
```

**B. Check database state:**
```bash
# 1. Verify test database exists
psql "postgresql://postgres:postgres@localhost:5432/simple_bookings_test1" -c "SELECT 1"

# 2. Run migrations fresh
cd your-project/server
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/simple_bookings_test1" \
  npx prisma migrate deploy

# 3. Check for stale test data (filtered deleteMany = danger!)
# Look for beforeEach patterns:
grep -A 3 "beforeEach" your-project/server/src/test/*.test.ts | grep "deleteMany"
# ❌ DANGER: deleteMany({ where: {...} }) leaves orphaned data
# ✅ CORRECT: deleteMany({}) — global delete
```

**C. Check timing issues:**
```bash
# 1. Look for hardcoded timeouts
grep -r "waitForTimeout\|sleep" your-project/e2e-test --include="*.spec.ts"

# 2. Check for flaky date-based tests
grep -r "new Date()\|setDate" your-project/server/src --include="*.test.ts"
# Weekend tests fail on Saturday, "tomorrow" tests fail at midnight

# 3. Memory leak detector (E2E only)
python3 scripts/memory-leak-detector.py your-project/e2e-test/
```

**D. Reproduce CI environment locally:**
```bash
# 1. Use same Node version as CI
cat .github/workflows/ci.yml | grep "node-version"

# 2. Run tests w/ same environment as CI
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/simple_bookings_test2" \
NODE_ENV=test \
npm test 2>&1 | head -100

# 3. If tests hang: check for missing afterAll cleanup
grep -L "afterAll" your-project/server/src/test/*.test.ts
# Missing afterAll(async () => { await prisma.$disconnect(); }) = hang
```

**Prevention:**
- Always test locally w/ `DATABASE_URL=... npm test` BEFORE push
- Add `.env.test` to git — never skip env setup
- Use global `deleteMany()` in test setup, never filtered
- Avoid date-based assertions (use fixed past dates)
- Check for memory leaks before committing E2E tests

---

## 4. Planning Laver Forkert Plan

**Symptom:** Claude's plan doesn't match what you asked for, has wrong subtasks, skips critical steps.

**Root causes:**
- Ambiguous request — Claude interprets differently
- Claude didn't understand domain constraints
- Request missing context (which app? which feature?)
- Plan too generic (copy-paste template, not specific)

**Solutions:**

```bash
# 1. Use /grill-me first (clarify requirements)
/grill-me
# Claude asks 5-10 clarifying questions before planning

# 2. Be extremely specific in your request
# ❌ VAGUE: "Add a new API endpoint"
# ✅ SPECIFIC: "Add POST /api/bookings/:bookingId/reschedule endpoint
#    that accepts { newStart, newEnd } and returns updated Booking.
#    Must validate availability, check user auth, emit event, return 409 if conflict"

# 3. Reference existing patterns
"Create similar to how POST /api/sites works — see your-project/server/src/routes/sites.ts"

# 4. Ask Claude to break plan into tiny steps
"Give me a 10-step breakdown — I want to verify EACH step before implementation"

# 5. Verify plan against issue acceptance criteria
"Plan against issue #1234 — does every AC have a corresponding step?"
```

**Prevention:**
- Always start w/ `/grill-me` for ambiguous tasks
- Include file paths, not generic descriptions
- Copy acceptance criteria into your prompt
- Ask Claude to map plan → acceptance criteria explicitly
- Request 5-10 small steps, not 2-3 big ones

---

## 5. Claude Refuses Command

**Symptom:** "I can't do that", "I'm not able to", "That's outside my capabilities", "I cannot execute...".

**Root causes:**
- Safety policy (Claude thinks it's dangerous)
- Permission denied (tool not available in this environment)
- Ambiguous/vague request (Claude doesn't understand what you want)
- Claude misunderstood scope (thinks you're asking for something harmful)

**Solutions:**

**A. Safety policy refusal:**
```bash
# Problem: "I can't execute git push --force, that's dangerous"
# Solution: Explain why it's safe in this context

# ✅ CORRECT: Reframe as safe operation
"I need to force-push to my feature branch (not main) to rebase.
Branch is: fix/auth-token (not develop or main).
Rebase reason: squash WIP commits.
This is safe — my feature branch, my consent, not production."

# ✅ CORRECT: Ask for guidance instead of command
"How should I rebase this branch safely? Current state: 23 commits.
Goal: 3 clean commits for PR. Should I rebase or force-push?"
```

**B. Permission denied:**
```bash
# Problem: "Tool X not available" or "InputValidationError"
# Solution: Fetch the tool schema first

# Ask for tool availability
/help | grep -i "email\|slack\|browser"

# If tool appears in deferred list:
# Use ToolSearch to load schema before calling
ToolSearch(query: "select:email_send,memory_store")
```

**C. Ambiguous request:**
```bash
# Problem: "I'm not sure what you're asking, can you clarify?"
# Solution: Be extremely concrete

# ❌ VAGUE: "Fix the auth issue"
# ✅ CONCRETE: "File: your-project/server/src/lib/api/auth.ts
#              Line 42: refresh token validation fails for expired tokens
#              Expected: return 401 w/ 'token expired' message
#              Current: returns 500
#              Root cause: missing try-catch"
```

**D. Claude thinks it's unsafe:**
```bash
# Problem: "I can't modify that file, it's critical"
# Solution: Ask Claude to think through the safety

# ✅ CORRECT: Explain the safety analysis
"I'm adding a console.log to debug — not changing behavior.
File is: your-project/server/src/lib/api/auth.ts
Change: add 1 line after line 42: console.log('token:', token);
This is safe — debug-only, will remove after testing.
Proceed?"

# ✅ CORRECT: Ask Claude to review change before executing
"Read your-project/server/src/lib/api/auth.ts
Show me line 40-45 and explain whether it's safe to add logging there"
```

**Prevention:**
- Be specific: file paths, line numbers, exact change
- Explain **why** change is safe (not just "I need it")
- Ask Claude to verify before executing dangerous commands
- Use `/grill-me` to clarify ambiguous requests
- Reference precedent: "Similar to PR #XXXX which did..."

---

## 6. Slow Responses

**Symptom:** Claude takes 30+ seconds to respond, timeout errors, "still thinking..." messages.

**Root causes:**
- Large context window (200k+ tokens)
- Model overloaded (peak hours)
- Computationally expensive task (large file analysis, grep across huge repo)
- Network latency
- Opus model (slower but more capable than Sonnet)

**Solutions:**

**A. Reduce context:**
```bash
# Clear old messages
/clear

# Compact session
/compact

# Start new session (nuclear option)
# Close Claude, reopen fresh
```

**B. Switch to faster model:**
```bash
# Current: Opus (slower, more capable)
# Alternative: Sonnet (faster, 90% as capable for most tasks)

# Change model in Claude Code settings:
# Claude Code Settings → Model → select Sonnet

# Or set env var:
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**C. Simplify the request:**
```bash
# ❌ SLOW: "Search entire codebase for X, analyze patterns, summarize findings"
# ✅ FAST: "Grep for X in your-project/server/src/lib/api/"

# Narrow scope:
# - Specific file paths instead of whole apps
# - Smaller search patterns instead of globbing
# - Yes/no questions instead of open-ended analysis
```

**D. Use background agents:**
```bash
# Instead of waiting for response, spawn agent in background
Agent({
  description: "Large codebase analysis",
  prompt: "Search and analyze...",
  run_in_background: true
})

# Continue other work, get notified when done
```

**Prevention:**
- Keep sessions under 90 min, then `/compact` or `/clear`
- Use Sonnet for searches/reads, Opus for complex reasoning
- Narrow file scope before asking for analysis
- Spawn background agents for "nice to have" analysis

---

## 7. Git Conflicts

**Symptom:** Merge conflicts when rebasing, "both modified" errors, git stuck in rebase state.

**Root causes:**
- Branch diverged too far from base
- Rebase against wrong branch
- Conflicting changes to same lines
- `.prettierrc`, `schema.prisma`, or other auto-generated files changed

**Solutions:**

**A. Resolve conflicts (automated):**
```bash
# 1. Check conflict status
git status  # shows "both modified" files

# 2. Ask Claude to resolve (w/ Edit tool, one file at a time)
# Claude reads conflicted file
# Removes conflict markers
# Keeps correct version
# Uses Edit tool (not sed/sed)

# 3. Mark resolved
git add <file>
git rebase --continue
```

**B. Resolve conflicts (manual):**
```bash
# 1. View conflict
git diff <file>

# 2. Understand both sides
# <<<<<<<< HEAD = your changes
# ======== = incoming changes
# >>>>>>> branch-name

# 3. Choose which to keep (NEVER use --theirs/--ours!)
# Use Edit tool to manually remove conflict markers
# Keep the correct code, delete markers + wrong code

# 4. Add resolved file
git add <file>
git rebase --continue
```

**C. Abort and restart:**
```bash
# If conflict is too messy, abort rebase
git rebase --abort

# Rebase against develop (not main)
git fetch origin develop
git rebase origin/develop

# Or cherry-pick instead
git reset --hard <original-branch>
git checkout -b fix/new-branch
git cherry-pick <commit1> <commit2> ...
```

**Prevention:**
- Always rebase against `develop`, never `main`
- Rebase frequently (before 5+ commits drift)
- Avoid changing files that others are modifying (coordinate via GitHub labels)
- Use `.husky/pre-commit` to catch schema drift before push
- Ask about conflicts early: "Does anyone else touch `schema.prisma`?"

---

## Quick Reference: When to Use What

| Issue | First Step | If Still Stuck |
|-------|-----------|-----------------|
| Context overflow | `/clear` | Start new session |
| Hallucination | Ask to `/read` file first | Grep to verify claims |
| CI test failure | Check env vars + DB state | Reproduce w/ CI environment |
| Bad plan | `/grill-me` | Be more specific in request |
| Refusal | Explain safety | Ask to verify instead |
| Slow response | `/compact` | Switch to Sonnet model |
| Git conflict | Let Claude resolve w/ Edit | Manual resolution w/ Edit (never --theirs) |

---

## Escalation

If troubleshooting doesn't work:

1. **Check skill/docs:** `.claude/docs/`, `.claude/skills/`
2. **Ask for help:** @ mention coworker in GitHub issue
3. **Spawn specialist agent:** `Agent(subagent_type: "quinn", prompt: "...")` for security, `scott` for QA, etc.
4. **Last resort:** Ask Troels or Vera directly (rare)

---

**Last updated:** 2026-06-30
