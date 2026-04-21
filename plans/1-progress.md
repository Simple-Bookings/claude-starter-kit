# Progress: Issue #1 — DevOps basishygiejne

## Status
DONE

## Tasks
- [x] Task 1: Opret `.gitignore` — **Evidence:** `.gitignore:2:.env	.env` (git check-ignore returnerede hit)
- [x] Task 2: Pin claude-code i Dockerfile til `@2.1.116` — **Evidence:** `@anthropic-ai/claude-code@2.1.116` (ingen `@latest`)
- [x] Task 3: Opret `.github/workflows/ci.yml` — **Evidence:** fil oprettet, verificeres via `gh workflow list` efter push
- [x] Task 4: Dokumentér `ANTHROPIC_API_KEY` som Codespace secret — **Evidence:** hit i begge filer (devcontainer.json secrets-sektion + DEV_SETUP.md vejledning)

## Review
- **Verdict**: APPROVED
- **Verificeret:**
  - AC-1: `.gitignore` fanger `.env`, `.env.*`, `.env.production`, `.env.local`, `credentials.json`, `*.pem` — alle wildcards testet
  - AC-2: Dockerfile pinner `@2.1.116`, ingen `@latest`
  - AC-3: CI grøn på begge push-commits, workflow registreret som `active` på GitHub
  - AC-4: `secrets`-sektion i devcontainer.json + vejledning i DEV_SETUP.md
  - CI `grep -qE '^\.env'`-mønster fanger alle `.env`-varianter korrekt
  - `actions/checkout@v4` er den aktuelle major version
- **Ingen findings**

## Status
APPROVED

## Noter
- Alle fire tasks er uafhængige af hinanden
- `@2.1.116` er verificeret som den aktuelle version i devcontaineren
