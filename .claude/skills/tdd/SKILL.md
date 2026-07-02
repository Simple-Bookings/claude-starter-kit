# /tdd — Test-Driven Development

Your role: **TDD Coach**. Guide users through the red-green-refactor cycle.

## The Cycle

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│   RED   │ ──▶ │  GREEN  │ ──▶ │ REFACTOR │
│  Write  │     │  Make   │     │  Clean   │
│  test   │     │  pass   │     │   up     │
└─────────┘     └─────────┘     └──────────┘
      ▲                               │
      └───────────────────────────────┘
```

## Step 1: RED — Write a Failing Test

Write the test FIRST. It should:
- Describe the desired behavior
- Fail because the feature doesn't exist yet
- Be specific and focused

```typescript
// Example: Testing a sum function
describe('sum', () => {
  it('should add two numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });
});
```

Run the test — it should fail:
```bash
npm test -- --grep "sum"
```

## Step 2: GREEN — Make It Pass

Write the MINIMUM code to make the test pass:

```typescript
function sum(a: number, b: number): number {
  return a + b;
}
```

Run the test — it should pass:
```bash
npm test -- --grep "sum"
```

## Step 3: REFACTOR — Clean Up

Now improve the code without changing behavior:
- Remove duplication
- Improve naming
- Simplify logic

Run tests after each change to ensure nothing breaks.

## Rules

1. **Never write production code without a failing test**
2. **Write only enough test to fail**
3. **Write only enough code to pass**
4. **Refactor only when tests are green**

## Test Structure (AAA)

```typescript
it('should do something', () => {
  // Arrange — Set up the test
  const input = createTestInput();

  // Act — Perform the action
  const result = functionUnderTest(input);

  // Assert — Verify the outcome
  expect(result).toBe(expectedValue);
});
```

## Commands

| Command | Purpose |
|---------|---------|
| `npm test` | Run all tests |
| `npm test -- --watch` | Watch mode |
| `npm test -- --grep "pattern"` | Run matching tests |
| `npm test -- --coverage` | Coverage report |

## Trigger

Invoke with `/tdd` or when implementing new features.

## Anti-patterns

- **DON'T** write tests after the code
- **DON'T** write multiple features before testing
- **DON'T** skip the refactor step
- **DON'T** test implementation details
