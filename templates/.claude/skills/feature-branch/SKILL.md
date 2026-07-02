# /feature-branch — Git Branch Workflow

Create and manage feature branches with consistent naming.

## Branch naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<description>` | `feature/user-auth` |
| Bug fix | `fix/<description>` | `fix/login-timeout` |
| Refactor | `refactor/<description>` | `refactor/db-queries` |
| Docs | `docs/<description>` | `docs/api-reference` |

## Workflow

### 1. Update develop
```bash
git checkout develop
git pull origin develop
```

### 2. Create branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make changes and commit
```bash
git add .
git commit -m "feat: add user authentication"
```

### 4. Push and create PR
```bash
git push -u origin feature/your-feature-name
gh pr create --base develop
```

### 5. After merge, cleanup
```bash
git checkout develop
git pull
git branch -d feature/your-feature-name
```

## Commit message format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## Rules

- Always branch from `develop`, never from `main`
- One feature per branch
- Keep branches short-lived (hours to days, not weeks)
- Delete branch after merge
