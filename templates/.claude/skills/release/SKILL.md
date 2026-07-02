# /release — Version and Release

Create releases following semantic versioning.

## Semantic Versioning

`MAJOR.MINOR.PATCH`

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking change | MAJOR | 1.0.0 → 2.0.0 |
| New feature | MINOR | 1.0.0 → 1.1.0 |
| Bug fix | PATCH | 1.0.0 → 1.0.1 |

## Pre-release checklist

- [ ] All PRs merged to develop
- [ ] Tests pass on develop
- [ ] Version number updated
- [ ] CHANGELOG updated
- [ ] No known critical bugs

## Release workflow

### 1. Update develop
```bash
git checkout develop
git pull origin develop
```

### 2. Merge to main
```bash
git checkout main
git pull origin main
git merge develop --no-ff -m "release: v1.2.0"
```

### 3. Tag the release
```bash
git tag -a v1.2.0 -m "Release v1.2.0"
```

### 4. Push everything
```bash
git push origin main --tags
```

### 5. Create GitHub release
```bash
gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes "## What's New
- Feature: User authentication
- Fix: Login timeout issue
- Docs: Updated API reference"
```

## Rules

- Never push directly to main
- Tag every release
- Write release notes
- Keep releases small and frequent
