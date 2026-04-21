---
name: release
description: Lav en release fra develop til main med en kort, målbar checkliste.
allowed-tools: Bash, Read
---

# Release

## Workflow

```text
feature/* -> develop -> main
```

## Før release

```bash
git fetch origin
git log origin/main..origin/develop --oneline
npm test
npm run build
```

## Release PR

```bash
gh pr create --base main --head develop --title "Release: YYYY-MM-DD"
gh pr merge --auto --merge
```

## Release-gates

- Testmiljø verificeret
- Seneste CI på `develop` er grøn
- Ingen kendte showstoppers
- Rollback-plan kendt på forhånd
