# Coding Patterns & Gotchas

Common patterns and mistakes to avoid.

---

## Don't Use sleep — Use Scheduling

`sleep N && command` blocks the entire Claude session.

```bash
# ❌ WRONG — blocks session
sleep 60 && check_status

# ✅ CORRECT — use CronCreate (if available)
CronCreate(
  cron: "*/1 * * * *",
  prompt: "check CI status",
  recurring: false
)

# ✅ ALTERNATIVE — run in background and check later
check_status &
```

---

## Bash: `local` Only Inside Functions

`local` can ONLY be used inside functions. Using it in main loop crashes the script.

```bash
# ❌ WRONG — crashes
while true; do
  case "$key" in
    s) local max=$(( ${#ITEMS[@]} - 1 )) ;;  # CRASH!
  esac
done

# ✅ CORRECT
while true; do
  case "$key" in
    s) max=$(( ${#ITEMS[@]} - 1 )) ;;
  esac
done
```

---

## GitHub Issue Body — Use Python, Not sed

GitHub issue bodies contain escaped backticks in JSON. `sed` handles them incorrectly.

```bash
# ❌ WRONG — sed doesn't match escaped backticks
sed 's/- \[ \] Foo/- [x] Foo/' body.txt

# ✅ CORRECT — Python str.replace() on file
gh issue view 1234 --json body --jq '.body' > /tmp/body.txt
python3 << 'EOF'
with open('/tmp/body.txt') as f:
    body = f.read()
body = body.replace('- [ ] Foo', '- [x] Foo — **Evidence:** ...')
with open('/tmp/body_fixed.txt', 'w') as f:
    f.write(body)
EOF
gh issue edit 1234 --body "$(cat /tmp/body_fixed.txt)"
```

---

## GitHub Comments — Use HEREDOC

`gh issue comment --body "text with \n"` does NOT interpret `\n` as newline.

```bash
# ❌ WRONG — \n becomes literal text
gh issue comment 1234 --body "Line 1\nLine 2"

# ✅ CORRECT — HEREDOC preserves newlines
gh issue comment 1234 --body "$(cat <<'EOF'
Line 1
Line 2
EOF
)"
```

Same rule applies to `git commit -m` — always use HEREDOC for multi-line messages.

---

## Git: Don't Use --theirs or --ours Blindly

**Never use `git checkout --theirs` or `--ours`** without understanding what you're accepting.

```bash
# ❌ DANGEROUS — blind merge
git checkout --theirs file.txt

# ✅ CORRECT — inspect conflicts manually
git diff --check  # See conflict markers
# Edit file manually to resolve
git add file.txt
git rebase --continue
```

**Why:** `--theirs` during rebase means "their" branch (often develop), which can overwrite your work.

---

## Error Handling

### Don't Swallow Errors

```bash
# ❌ WRONG — hides errors
command 2>/dev/null || true

# ✅ CORRECT — handle errors explicitly
if ! command; then
  echo "Command failed, handling..."
  # actual error handling
fi
```

### Exit on Failure in Scripts

```bash
#!/bin/bash
set -e  # Exit on any error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure
```

---

## File Operations

### Check Before Destructive Operations

```bash
# ❌ DANGEROUS — no verification
rm -rf $DIR

# ✅ SAFER — verify first
if [ -d "$DIR" ] && [ "$DIR" != "/" ] && [ "$DIR" != "$HOME" ]; then
  rm -rf "$DIR"
fi
```

### Use Absolute Paths

```bash
# ❌ FRAGILE — depends on current directory
Edit file.txt

# ✅ ROBUST — explicit path
Edit /path/to/project/file.txt
```
