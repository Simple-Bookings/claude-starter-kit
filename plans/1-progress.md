# Progress: Issue #1 — DevOps basishygiejne

## Status
IN_PROGRESS

## Tasks
- [x] Task 1: Opret `.gitignore` — **Evidence:** `.gitignore:2:.env	.env` (git check-ignore returnerede hit)
- [x] Task 2: Pin claude-code i Dockerfile til `@2.1.116` — **Evidence:** `@anthropic-ai/claude-code@2.1.116` (ingen `@latest`)
- [x] Task 3: Opret `.github/workflows/ci.yml` — **Evidence:** fil oprettet, verificeres via `gh workflow list` efter push
- [ ] Task 4: Dokumentér `ANTHROPIC_API_KEY` som Codespace secret — **Fil:** `.devcontainer/devcontainer.json`, `starter-kit/DEV_SETUP.md` — **Verify:** `grep -i "ANTHROPIC_API_KEY" .devcontainer/devcontainer.json starter-kit/DEV_SETUP.md`

## Noter
- Alle fire tasks er uafhængige af hinanden
- `@2.1.116` er verificeret som den aktuelle version i devcontaineren
