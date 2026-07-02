# Exercise 07: When Claude Fails

**Goal:** Learn to identify and fix Claude's mistakes.

**Skills:** `/grill-me`

**Time:** 25 minutes

---

## What You'll Learn

- Claude is not perfect
- How to spot common mistakes
- Verification is essential

## Important Truth

Claude will:
- Hallucinate imports that don't exist
- Write tests that pass for wrong reasons
- Make incorrect assumptions
- Use outdated patterns

Your job: catch these before they ship.

## Scenario 1: Hallucinated Import (10 min)

### Create the Problem

```
Create a utility that uses the built-in formatCurrency helper from our utils folder to format prices.
```

Claude will likely import a function that doesn't exist.

### Identify It

```
Read the utils folder and list all exported functions.
Does formatCurrency actually exist?
```

Claude will admit it doesn't.

### Fix It

```
formatCurrency doesn't exist.
Either create it, or use a different approach.
Explain your choice.
```

## Scenario 2: Incomplete Test (10 min)

### Create the Problem

```
Write a test for a function that validates email addresses.
Make the test pass.
```

### Challenge It

```
Does this test actually verify email validation?
What happens if I pass "not-an-email"?
Run the test with invalid input.
```

### Fix It

```
The test is incomplete. Add cases for:
- Missing @ symbol
- Missing domain
- Empty string
- Valid email

Each case must be tested.
```

## Common Mistakes

```
Mistake              How to Spot              How to Fix
────────────────────────────────────────────────────────────────
Hallucinated imports "Read the file first"    Verify before using
Incomplete tests     "What if X?"             Add edge cases
Wrong assumptions    Review the plan          Be more specific
Outdated patterns    Check current docs       Point to docs
```

## The Golden Rule

**Trust but verify.**

1. Read Claude's output
2. Question assumptions
3. Test edge cases
4. Run the code

Don't assume it works because it compiles.

## Verification

- [ ] Found a hallucinated import
- [ ] Found an incomplete test
- [ ] Fixed both with Claude's help
- [ ] Understood WHY Claude made the mistake

## Key Takeaway

Claude is powerful but probabilistic. Your job is to catch mistakes before production — not to blame Claude when they slip through.

## Next

[Exercise 08: Harness Engineering](08-guardrails.md)
