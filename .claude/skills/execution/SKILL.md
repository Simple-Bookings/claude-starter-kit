# /execution — Implement with TDD

Your role: **Developer**. Implement tasks from the plan using Test-Driven Development.

**Every task: RED → GREEN → REFACTOR**

---

## Prerequisites

Before starting:
1. Plan file exists: `docs/plans/{issue}-plan.md`
2. Progress file exists: `docs/plans/{issue}-progress.md`
3. Feature branch created (if not, create one)

---

## Steps

### Step 1: Load the Plan

Read the plan and progress files:

```bash
cat docs/plans/*-plan.md
cat docs/plans/*-progress.md
```

Identify the next uncompleted task.

### Step 2: Create Feature Branch (if needed)

```bash
git checkout -b feature/dark-mode
```

### Step 3: TDD Loop for Each Task

For every task, follow RED → GREEN → REFACTOR:

#### 🔴 RED: Write Failing Test First

```typescript
// src/hooks/useTheme.test.ts
describe('useTheme', () => {
  it('should default to system preference', () => {
    const { result } = renderHook(() => useTheme());
    expect(result.current.theme).toBe('system');
  });

  it('should persist theme to localStorage', () => {
    const { result } = renderHook(() => useTheme());
    act(() => result.current.setTheme('dark'));
    expect(localStorage.getItem('theme')).toBe('dark');
  });
});
```

Run test — it should FAIL:
```bash
npm test -- useTheme
```

#### 🟢 GREEN: Minimum Code to Pass

Write the simplest code that makes the test pass:

```typescript
// src/hooks/useTheme.ts
export function useTheme() {
  const [theme, setThemeState] = useState('system');
  
  const setTheme = (newTheme: string) => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);
  };
  
  return { theme, setTheme };
}
```

Run test — it should PASS:
```bash
npm test -- useTheme
```

#### 🔵 REFACTOR: Improve Without Breaking

Clean up the code. Tests must still pass:

```typescript
// Add types, improve naming
type Theme = 'light' | 'dark' | 'system';

export function useTheme(): { theme: Theme; setTheme: (t: Theme) => void } {
  // ... cleaner implementation
}
```

```bash
npm test -- useTheme  # Still green!
```

### Step 4: Commit with Evidence

After each task passes:

```bash
git add -A
git commit -m "feat: add useTheme hook with localStorage persistence"
```

### Step 5: Update Progress

Mark task complete in `docs/plans/{issue}-progress.md`:

```markdown
## Tasks
- [x] Task 1: Create ThemeContext — **Commit:** abc123
- [x] Task 2: Create ThemeToggle — **Commit:** def456
- [ ] Task 3: Add useTheme hook  ← Currently working
```

### Step 6: Repeat for All Tasks

Continue until all tasks are complete.

### Step 7: Final Verification

Run full test suite:

```bash
npm test
npm run build
npm run lint
```

All must pass before moving to review.

---

## Output

After each task:

```
✅ Task 3 Complete

Test: useTheme.test.ts — 2 passing
Commit: abc1234
Files: src/hooks/useTheme.ts, src/hooks/useTheme.test.ts

Next task: Task 4 — Write integration tests
```

After all tasks:

```
✅ Execution Complete

Tasks: 5/5 complete
Tests: 12 passing
Build: Clean
Next: /reviewing
```

---

## Rules

- **Test first** — Never write implementation before test
- **One task at a time** — Complete and commit before next
- **Small commits** — One logical change per commit
- **Evidence required** — Record commit SHA in progress.md
- **All tests pass** — Never commit with failing tests

---

## Common Patterns

### Testing React Components

```typescript
import { render, screen, fireEvent } from '@testing-library/react';

test('ThemeToggle switches theme on click', () => {
  render(<ThemeToggle />);
  fireEvent.click(screen.getByRole('button'));
  expect(screen.getByText('Dark')).toBeInTheDocument();
});
```

### Testing Hooks

```typescript
import { renderHook, act } from '@testing-library/react';

test('useCounter increments', () => {
  const { result } = renderHook(() => useCounter());
  act(() => result.current.increment());
  expect(result.current.count).toBe(1);
});
```

### Testing API Calls

```typescript
import { vi } from 'vitest';

vi.mock('../api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ name: 'Test' })
}));

test('loads user data', async () => {
  render(<UserProfile id="1" />);
  expect(await screen.findByText('Test')).toBeInTheDocument();
});
```

---

## Next Phase

After execution, run `/reviewing` to verify all acceptance criteria.
