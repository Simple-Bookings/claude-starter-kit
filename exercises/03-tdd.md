# Exercise 03: Test-Driven Development

**Goal:** Guide Claude through RED → GREEN → REFACTOR.

**Skills:** `/tdd`

**Time:** 30 minutes

---

## What You'll Learn

- The TDD cycle with Claude as the implementer
- How to describe tests without writing them
- Claude handles the code; you handle the thinking

## The Challenge

Build a `formatDuration` function:
- Input: seconds (number)
- Output: `"Xh Ym"` format

Examples:
- `formatDuration(0)` → `"0h 0m"`
- `formatDuration(3600)` → `"1h 0m"`
- `formatDuration(5400)` → `"1h 30m"`

## Step 1: RED — Write a Failing Test

Start the TDD skill:

```
/tdd
```

Then:

```
Create a test for formatDuration that converts seconds to "Xh Ym" format.
Start with the simplest case: 0 seconds → "0h 0m".
Only write the test, don't implement yet.
```

Claude creates the test. **Run it. It fails.** That's RED.

## Step 2: GREEN — Make It Pass

```
Now implement formatDuration to make this test pass.
Write the minimum code needed — nothing fancy.
```

Claude implements. **Run it. It passes.** That's GREEN.

## Step 3: Add More Cases

```
Add tests for:
- 3600 seconds (1 hour)
- 5400 seconds (1h 30m)
- 90 seconds (0h 1m)

Run them.
```

Some may fail. Tell Claude to fix them one at a time.

## Step 4: REFACTOR

Once all tests pass:

```
Refactor the implementation for clarity.
Extract magic numbers as constants.
Keep tests green.
```

Claude improves the code while tests protect against regressions.

## The TDD Rhythm

```
Phase      You say                 Claude does
─────────────────────────────────────────────────────────────
RED        "Write a test for X"    Creates failing test
GREEN      "Make it pass"          Writes minimum implementation
REFACTOR   "Clean it up"           Improves code, tests stay green
```

## Why This Works

- You think about WHAT to test
- Claude handles HOW to implement
- Tests document behavior
- Refactoring is safe

## Verification

- [ ] First test failed (RED)
- [ ] Implementation made it pass (GREEN)
- [ ] Multiple edge cases added
- [ ] Code refactored while tests stayed green

## Next

[Exercise 04: Code Review](04-code-review.md)
