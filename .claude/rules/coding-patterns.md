---
name: coding-patterns
description: Claude Code gotchas — CronCreate vs sleep, bash local, GitHub CLI patterns
type: rule
---

# Coding Patterns & Gotchas

## ⛔ ALDRIG brug `sleep N && kommando` — brug CronCreate i stedet

`sleep N && kommando` blokerer hele Claude-sessionen og forhindrer brugeren i at kommunikere med Claude i ventetiden.

**Brug CronCreate med `recurring: false`:**

```text
CronCreate(
  cron: "*/1 * * * *",
  prompt: "tjek CI status på PR #1234: gh pr view 1234 --json statusCheckRollup",
  recurring: false
)
```

| Sleep | Cron expression |
|-------|----------------|
| `sleep 60` | `*/1 * * * *` |
| `sleep 120` | `*/2 * * * *` |
| `sleep 300` | `*/5 * * * *` |

## Bash: `local` kun i funktioner

`local` kan KUN bruges inde i funktioner. Brug i main-loop crasher scriptet.

```bash
# ❌ FORKERT — crasher
while true; do
  case "$key" in
    s) local max=$(( ${#ITEMS[@]} - 1 )) ;;  # CRASH!
  esac
done

# ✅ KORREKT
while true; do
  case "$key" in
    s) max=$(( ${#ITEMS[@]} - 1 )) ;;
  esac
done
```

## GitHub Issue Body — Erstat tekst med Python, ikke sed/bash

GitHub issue bodies indeholder escaped backticks i JSON. `sed` og bash-erstatning håndterer dem forkert.

```bash
# ❌ FORKERT — sed matcher ikke escaped backticks
sed 's/- \[ \] Foo/- [x] Foo/' body.txt

# ✅ KORREKT — Python str.replace() på fil
gh issue view 1234 --json body --jq '.body' > /tmp/body.txt
python3 << 'EOF'
with open('/tmp/body.txt') as f:
    body = f.read()
body = body.replace('- [ ] Foo', '- [x] Foo — **Bevis:** ...')
with open('/tmp/body_fixed.txt', 'w') as f:
    f.write(body)
EOF
gh issue edit 1234 --body "$(cat /tmp/body_fixed.txt)"
```

## GitHub Issue/PR Kommentarer — Brug altid HEREDOC

`gh issue comment --body "tekst med \n linjeskift"` fortolker **ikke** `\n` som linjeskift.

```bash
# ❌ FORKERT — \n bliver bogstavelig tekst
gh issue comment 1234 --body "Linje 1\nLinje 2"

# ✅ KORREKT — HEREDOC med $() bevarer linjeskift
gh issue comment 1234 --body "$(cat <<'EOF'
Linje 1
Linje 2
EOF
)"
```

Samme regel gælder `git commit -m` — brug altid HEREDOC ved linjeskift.

## CI retrigger via workflow_dispatch

Når seneste commit har `[skip ci]` eller kun matcher dokumentationsfiler, trigger CI eksplicit:

```bash
# ✅ Trigger CI uden fil-ændringer
gh workflow run ci.yml --ref <branch-name>

# Verificer at run startede
gh run list --branch <branch-name> --limit 3
```

**Fallback** hvis workflow_dispatch ikke virker:
```bash
echo "# CI retrigger: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> scripts/.ci-retrigger
git add scripts/.ci-retrigger
git commit -m "ci: retrigger CI"
git push origin <branch-name>
```
