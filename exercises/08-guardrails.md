# Exercise 08: Harness Engineering

**Goal:** Build guardrails around Claude's probabilistic output.

**Skills:** `/security-audit`

**Time:** 25 minutes

---

## Why This Matters

> "Harness design is the primary performance lever, not model capability."  
> — LangChain case study (harness-only changes: rank 30 → top 5)

Industry data: AI-generated code has **1.7× more defects**. The solution isn't better prompts — it's **guardrails**.

## What You'll Learn

- Claude's output varies — this is expected
- Every mistake is a guardrail you haven't built
- The cycle: mistake → detection → guardrail → immunity

## Experiment: See the Variance (5 min)

Ask Claude the same thing 3 times (use `/clear` between):

```
Create a simple function that formats a phone number into (XXX) XXX-XXXX format.
```

Notice:
- Different function names
- Different implementations (regex? slicing?)
- Different edge case handling

Each is valid. None are identical.

## The Problem (5 min)

Ask Claude to add debugging:

```
Add console.log to debug the phone formatter. Log input and output.
```

Claude adds:

```typescript
console.log('Input:', phoneNumber);
console.log('Output:', formatted);
```

**The issue:** This is fine locally. In production:
- Logs clutter monitoring
- Phone numbers leak to logs (PII!)
- Performance hit
- Looks unprofessional

## The Guardrail (10 min)

Build a pre-commit hook:

```
Create a pre-commit hook that:
1. Checks all staged .ts and .tsx files
2. Fails if ANY contains console.log/warn/error
3. Shows the file and line number
4. Can be bypassed with --no-verify if necessary
```

Claude creates something like:

```bash
#!/bin/sh
STAGED_FILES=$(git diff --cached --name-only | grep -E '\.(ts|tsx)$')
if [ -z "$STAGED_FILES" ]; then exit 0; fi

CONSOLE=$(git diff --cached $STAGED_FILES | grep -E '^\+.*console\.(log|warn|error)')
if [ -n "$CONSOLE" ]; then
  echo "❌ console.* found in staged files:"
  echo "$CONSOLE"
  exit 1
fi
```

## Test It

```bash
# Create bad file
echo 'console.log("test");' > test-bad.ts
git add test-bad.ts
git commit -m "test"
# Should FAIL

# Remove the console.log, commit again
# Should PASS
```

## The Pattern

```
Claude outputs something bad
    ↓
You catch it (review, testing, prod incident)
    ↓
You build a guardrail
    ↓
That mistake becomes IMPOSSIBLE to commit
```

## Brainstorm More Guardrails (5 min)

```
Suggest 3 guardrails we should add:
1. A pattern to prevent
2. How to detect it (grep? lint rule? test?)
3. When to check (pre-commit? CI? runtime?)
```

Examples of guardrails to consider:

```
Pattern                    Detection                         When
─────────────────────────────────────────────────────────────────────
Hardcoded secrets          Grep for password=, apiKey=       Pre-commit
`as any` type assertions   ESLint rule                       Pre-commit
.skip on tests             Grep for test.skip                CI gate
Missing error handling     ESLint no-floating-promises       Pre-commit
```

## Verification

- [ ] Saw Claude produce different outputs
- [ ] Created console.log problem
- [ ] Built pre-commit hook
- [ ] Hook blocked bad code
- [ ] Brainstormed 3 more guardrails

## Key Takeaway

**Every Claude mistake is a guardrail you haven't built yet.**

Claude will generate mediocre code. Your job: make it impossible to ship.

- Code review catches quality issues
- Tests catch bugs
- Guardrails catch bad patterns
- Security linters catch vulnerabilities

Build enough guardrails that even if Claude messes up, the code never leaves your repo.

## Core Exercises Complete!

You've learned:
1. How to work WITH Claude, not against it
2. The 4-phase workflow
3. TDD with Claude
4. How to catch and prevent mistakes

**Bonus exercises available** if you have time!

## Next

[Exercise 09: Agent Teams](09-agents-parallel.md) (bonus)
