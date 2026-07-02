# Workflow Rules

## Git Workflow

```
main ← develop ← feature/*
```

- Branch from `develop`
- PR to `develop`
- Releases: `develop` → `main`

## Before Starting Work

1. Check for existing PRs on the same issue
2. Create a feature branch
3. Keep PRs small and focused

## Commit Messages

Use conventional commits:

```
feat: add user authentication
fix: resolve login timeout issue
docs: update API documentation
refactor: simplify payment logic
test: add unit tests for cart
```

## Code Review

Before requesting review:

1. Self-review the diff
2. Remove console.logs and debug code
3. Verify tests pass
4. Check for security issues
