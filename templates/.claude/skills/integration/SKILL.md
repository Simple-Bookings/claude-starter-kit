# /integration — Integration Phase

Create PR, handle review feedback, merge to develop.

**Prerequisites:** Review status = `APPROVED`

## Step 0: Verify Ready State

```bash
# Check review approved
grep "APPROVED" docs/plans/{issue}-progress.md

# Check all tests pass
npm test && npm run lint && npm run build
```

## Step 1: Push Branch

```bash
git push -u origin feature/{issue}-{desc}
```

## Step 2: Create Pull Request

```bash
gh pr create \
  --base develop \
  --title "feat({scope}): {description}" \
  --body "$(cat <<'EOF'
## Summary
Brief description of changes.

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Manual testing done

## Acceptance Criteria
- [x] AC-1: description
- [x] AC-2: description

Addresses #{issue}
EOF
)"
```

## Step 3: Record PR

Update `progress.md`:
```markdown
## Integration

**PR:** #{pr-number}
**Status:** OPEN

### Checklist
- [x] PR created
- [ ] CI passes
- [ ] Review approved
- [ ] Merged
```

## Step 4: Handle CI

Wait for CI checks. If they fail:
1. Read the error logs
2. Fix the issue
3. Push fix
4. Wait for CI again

## Step 5: Handle Review Feedback

If reviewer requests changes:
1. Address each comment
2. Push fixes
3. Request re-review
4. Update progress with round number

## Step 6: Merge

When approved and CI green:
```bash
gh pr merge {number} --squash --delete-branch
```

## Step 7: Close Issue

```bash
# Update progress
echo "## Status: COMPLETE" >> docs/plans/{issue}-progress.md

# Close issue if applicable
gh issue close {number} --comment "Completed in PR #{pr}"
```

## PR Title Format

```
type(scope): description

Types: feat, fix, docs, test, refactor, chore
Scope: component or area affected
Description: imperative mood, lowercase
```

Examples:
- `feat(auth): add password reset flow`
- `fix(booking): handle timezone edge case`
- `docs(readme): update installation steps`

## Done Criteria

Integration is complete when:
1. ✅ PR created with proper description
2. ✅ CI passes
3. ✅ Review approved
4. ✅ PR merged to develop
5. ✅ Branch deleted
6. ✅ Progress updated to COMPLETE
