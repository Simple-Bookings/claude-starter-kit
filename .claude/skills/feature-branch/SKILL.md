# /feature-branch — Git Workflow

Your role: **Git Guide**. Help users follow a clean feature branch workflow.

---

## Branch Strategy

```
main (production) ← develop (integration) ← feature/* (work)
                                          ← fix/* (bugfixes)
```

**main**: Production code. Only merged from develop via release PR.
**develop**: Integration branch. All feature branches merge here.
**feature/\***: Individual feature work. Short-lived (days, not weeks).

---

## Creating a Feature Branch

```bash
# 1. Start from latest develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/add-dark-mode

# 3. Work in small commits
git add -p  # Stage interactively
git commit -m "feat: add theme context"

# 4. Push and set upstream
git push -u origin feature/add-dark-mode

# 5. Create PR when ready
gh pr create --base develop
```

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/{short-name}` | `feature/user-auth` |
| Bug fix | `fix/{issue-or-name}` | `fix/login-error` |
| Hotfix | `hotfix/{urgent}` | `hotfix/prod-crash` |
| Docs | `docs/{topic}` | `docs/api-reference` |
| Refactor | `refactor/{scope}` | `refactor/db-layer` |
| Experiment | `experiment/{name}` | `experiment/new-ui` |

**Rules:**
- Lowercase, hyphens (not underscores)
- Short but descriptive (2-4 words)
- No issue numbers alone (`fix/123` is bad, `fix/login-timeout` is good)

---

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|------|-------------|
| `feat` | New feature for users |
| `fix` | Bug fix for users |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Code restructure, no feature change |
| `test` | Adding or fixing tests |
| `chore` | Build, CI, dependencies |

### Examples

```bash
# Feature
git commit -m "feat(auth): add password reset flow"

# Bug fix
git commit -m "fix(api): handle null user in response"

# With body
git commit -m "$(cat <<'EOF'
refactor(db): extract query builder

- Move SQL generation to QueryBuilder class
- Add unit tests for complex queries
- No behavior change
EOF
)"
```

---

## Keeping Branch Up to Date

```bash
# Option 1: Rebase (cleaner history, use for personal branches)
git fetch origin
git rebase origin/develop

# Option 2: Merge (safer, use for shared branches)
git fetch origin
git merge origin/develop

# If conflicts during rebase
git status                    # See conflicting files
# Fix conflicts in editor
git add <fixed-files>
git rebase --continue

# Abort if stuck
git rebase --abort
```

---

## Pull Request Checklist

Before creating PR:

- [ ] Branch rebased/merged with latest develop
- [ ] All tests pass locally (`npm test`)
- [ ] Linting passes (`npm run lint`)
- [ ] Build succeeds (`npm run build`)
- [ ] Self-reviewed the diff
- [ ] PR description explains WHY, not just WHAT

```bash
# Create PR with good description
gh pr create --base develop --title "feat: add dark mode" --body "$(cat <<'EOF'
## Summary
- Adds dark mode toggle to header
- Persists preference in localStorage

## Test Plan
- [x] Toggle works
- [x] Preference persists after refresh

Closes #42
EOF
)"
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Create branch | `git checkout -b feature/x` |
| Stage changes | `git add -p` |
| Commit | `git commit -m "feat: ..."` |
| Push (first time) | `git push -u origin feature/x` |
| Push (subsequent) | `git push` |
| Update from develop | `git rebase origin/develop` |
| Create PR | `gh pr create --base develop` |
| View PR status | `gh pr status` |
| Merge PR | `gh pr merge --squash` |
| Delete local branch | `git branch -d feature/x` |
| Delete remote branch | `git push origin --delete feature/x` |

---

## Common Issues

### "Your branch is behind develop"

```bash
git fetch origin
git rebase origin/develop
git push --force-with-lease  # Safe force push
```

### "Merge conflict"

```bash
# 1. See what's conflicting
git status

# 2. Open file, look for conflict markers
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> origin/develop

# 3. Edit to resolve, remove markers

# 4. Mark resolved and continue
git add <file>
git rebase --continue
```

### "Accidentally committed to develop"

```bash
# Move commits to new branch
git branch feature/oops        # Create branch at current commit
git checkout develop
git reset --hard origin/develop  # Reset develop to remote
git checkout feature/oops      # Continue work on new branch
```

---

## Output

When creating a branch:

```
✅ Feature Branch Created

Branch: feature/add-dark-mode
Base: develop (up to date)
Next: Make changes, commit, push, create PR
```
