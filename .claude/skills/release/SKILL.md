# /release — Release Workflow

Your role: **Release Manager**. Guide users through merging develop to main.

## Release Flow

```
develop (tested) ──▶ main (production)
```

## Pre-release Checklist

- [ ] All PRs merged to develop
- [ ] CI pipeline green on develop
- [ ] Version bumped (if applicable)
- [ ] Changelog updated
- [ ] No blocking issues

## Creating a Release

### 1. Ensure develop is ready

```bash
git checkout develop
git pull origin develop

# Verify tests pass
npm test
npm run build
```

### 2. Create release branch (optional)

For larger releases:

```bash
git checkout -b release/v1.2.0
# Make final adjustments
git push -u origin release/v1.2.0
```

### 3. Merge to main

```bash
# Fast-forward merge (clean history)
git checkout main
git pull origin main
git merge develop --ff-only
git push origin main

# Or create a merge commit
git merge develop --no-ff -m "release: v1.2.0"
git push origin main
```

### 4. Tag the release

```bash
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

### 5. Create GitHub release

```bash
gh release create v1.2.0 \
  --title "v1.2.0" \
  --notes "## Changes\n- Feature 1\n- Fix 2"
```

## Hotfix Flow

For urgent production fixes:

```bash
# Branch from main
git checkout main
git checkout -b hotfix/critical-fix

# Fix, test, commit
git commit -m "fix: critical issue"

# Merge to main AND develop
git checkout main
git merge hotfix/critical-fix
git push origin main

git checkout develop
git merge hotfix/critical-fix
git push origin develop
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
  │      │     └── Bug fixes
  │      └──────── New features (backwards compatible)
  └─────────────── Breaking changes
```

## Commands

| Command | Purpose |
|---------|---------|
| `gh release list` | List releases |
| `gh release create` | Create release |
| `git tag -a v1.0.0` | Create tag |
| `git push origin --tags` | Push all tags |

## Trigger

Invoke with `/release` when ready to deploy to production.
