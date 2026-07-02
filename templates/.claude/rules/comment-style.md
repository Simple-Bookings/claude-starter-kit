# Comment Style — Issues & PRs

Rules for comments on issues, pull requests, and code reviews.

## Language

Match your team's convention. Most open source projects use English.

## Structure: Problem → Solution

Every reply or status comment has two parts:

1. **Problem** — One sentence restating the issue. Proves you understood it.
2. **Solution** — Concrete change + commit SHA. Proves the action.

```markdown
**Problem:** The function silently swallows errors instead of logging them.

**Solution:** Added error logging with stack trace. Commit `a1b2c3d`.
```

If disagreeing:

```markdown
**Problem:** Reviewer suggests using a different pattern.

**Disagree** — The suggested pattern would require refactoring 12 files.
Keeping current implementation because it's isolated to this module.
```

## Markdown is mandatory

- Bold labels (`**Problem:**`, `**Solution:**`)
- Blank lines between sections
- `code spans` for identifiers and SHAs
- Fenced code blocks for code examples
- Bullet lists for multi-point answers

## Include relevant code

If the reply addresses a code change, include the new code as a fenced block:

```markdown
**Solution:** Refactored to use early return. Commit `d44ad52`.

```python
def process(data):
    if not data:
        return None
    return transform(data)
```
```

## Hard bans

- ❌ Sycophancy: "Good point", "Great catch", "Thanks for the feedback"
- ❌ Filler: "I think", "Maybe we could", "It seems"
- ❌ Skipping problem restatement — jumping straight to "Fixed in `<sha>`"
- ❌ Wall-of-text — break sections with blank lines
- ❌ Meta-notes about tooling or AI process
- ❌ Explanation of process: "I will now…", "After investigating…"

## Examples

✅ **Good:**

```markdown
**Problem:** Every wrapper has to remember to call `init()`.

**Solution:** Moved initialization into property getter for auto-init.
Commit `d44ad52`.

```python
@property
def service(self):
    if not self._initialized:
        self._initialize()
    return self._service
```
```

❌ **Bad:**

```markdown
Good point! I noticed the same issue and have now fixed it.
After investigating, I refactored the engine to use a property-based
init pattern. Thanks for catching this!
```
