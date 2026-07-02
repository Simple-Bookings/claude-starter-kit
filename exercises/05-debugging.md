# Exercise 05: Debugging with Claude

**Goal:** Use Claude to trace execution and find root causes.

**Skills:** `/execution`

**Time:** 20 minutes

---

## What You'll Learn

- How to describe bugs effectively
- Claude traces execution step by step
- Understanding > quick fixes

## The Setup

We'll create a buggy function and debug it systematically.

## Step 1: Create a Bug

```
Create a parseTime function that converts "2h 30m" to seconds.
Make it buggy — it should fail when minutes are 0, like "2h 0m".
Put it in src/parseTime.ts
```

Claude creates something like:

```typescript
export function parseTime(timeStr: string): number {
  const [hours, minutes] = timeStr.split('h ');
  return parseInt(hours) * 3600 + parseInt(minutes) * 60;
}
```

## Step 2: Write a Failing Test

```
Write a test: parseTime("2h 0m") should return 7200.
Run it.
```

The test fails — probably returns `NaN` instead of `7200`.

## Step 3: The Wrong Way

**Don't say:** "Fix it"

That gives you a fix without understanding. You learn nothing.

## Step 4: The Right Way

```
I have a failing test. parseTime("2h 0m") returns NaN instead of 7200.

Please:
1. Read the implementation
2. Trace through what happens with "2h 0m" step by step
3. Identify exactly where it breaks
4. Explain the root cause BEFORE suggesting a fix
```

Claude traces:
1. `"2h 0m".split('h ')` → `["2", "0m"]`
2. `hours` = `"2"`, `minutes` = `"0m"`
3. `parseInt("0m")` = `0` (works!)
4. Wait... but we're missing the 'm'...

Claude explains WHY before fixing.

## Step 5: Apply the Fix

Once you understand:

```
Good analysis. Now fix it using a regex approach that handles all formats.
Add tests for edge cases.
```

## Good vs Bad Prompts

```
Bad                   Good
────────────────────────────────────────────────────────────────
"Fix this test"       "Trace execution and explain what's wrong"
"It doesn't work"     "Expected X, got Y, with input Z"
"Make it pass"        "Find root cause, then fix"
```

## Why This Works

If you ask "just fix it", you:
- Don't understand your codebase
- Can't recognize similar bugs later
- Miss systemic issues

If you ask for explanation, you:
- Learn patterns in your code
- Catch root causes, not symptoms
- Build intuition

## Verification

- [ ] Bug created intentionally
- [ ] Test showed the failure
- [ ] Claude traced execution step by step
- [ ] You understood root cause before fixing

## Next

[Exercise 06: Full Cycle](06-full-cycle.md)
