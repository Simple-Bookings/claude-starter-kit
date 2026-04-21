# Progress: Issue #1 — DevOps basishygiejne

## Status
DONE

## Tasks
- [x] Task 1: Opret `.gitignore` — **Evidence:** `.gitignore:2:.env	.env` (git check-ignore returnerede hit)
- [x] Task 2: Pin claude-code i Dockerfile til `@2.1.116` — **Evidence:** `@anthropic-ai/claude-code@2.1.116` (ingen `@latest`)
- [x] Task 3: Opret `.github/workflows/ci.yml` — **Evidence:** fil oprettet, verificeres via `gh workflow list` efter push
- [x] Task 4: Dokumentér `ANTHROPIC_API_KEY` som Codespace secret — **Evidence:** hit i begge filer (devcontainer.json secrets-sektion + DEV_SETUP.md vejledning)

## Noter
- Alle fire tasks er uafhængige af hinanden
- `@2.1.116` er verificeret som den aktuelle version i devcontaineren
