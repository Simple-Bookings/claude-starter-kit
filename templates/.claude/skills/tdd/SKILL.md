# /tdd — Test-Driven Development

Write the test first, then implement the minimum code to pass.

## The Cycle

```
🔴 RED     → Write a failing test
🟢 GREEN   → Write minimum code to pass
🔵 REFACTOR → Improve without breaking tests
```

## Rules

1. **Never write code without a failing test first**
2. **Write the smallest possible failing test**
3. **Write only enough code to make it pass**
4. **Run tests after every change**
5. **Refactor only when tests are green**

## Step-by-step

### 1. RED — Write failing test

```typescript
describe('add', () => {
  it('should add two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

Run: `npm test` → FAIL (function doesn't exist)

### 2. GREEN — Minimum implementation

```typescript
function add(a, b) {
  return a + b;
}
```

Run: `npm test` → PASS

### 3. REFACTOR — Improve code

Add types, documentation, handle edge cases — but keep tests green.

## Anti-patterns

- ❌ Writing implementation before tests
- ❌ Writing multiple tests before implementing
- ❌ Refactoring with failing tests
- ❌ Skipping the refactor phase

## Output

Working code with comprehensive test coverage, built incrementally.
