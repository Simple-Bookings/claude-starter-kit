# Testing Rules

## When a Test Fails

1. Find root cause — no quick fixes
2. Fix the code, not the test (unless the test is wrong)
3. Verify ALL tests pass after the fix

**Never:**
- Skip or comment out failing tests
- Use `.skip` without documenting why

## Test Data

```typescript
// Always reset data in beforeEach
beforeEach(async () => {
  await db.model.deleteMany();  // Global, not filtered
  await db.model.createMany({ data: [...] });
});
```

## TDD Workflow

```
RED → GREEN → REFACTOR
```

1. Write a failing test first
2. Write minimum code to pass
3. Refactor without breaking tests
