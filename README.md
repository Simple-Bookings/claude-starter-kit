# Claude Code Starter-Kit

Standardiseret udviklingsflow og onboarding til Claude Code — fra GitHub issue til merged PR uden manuel opfølgning.

---

## Tredjeparts-værktøjer

Starter-kittet bygger på disse eksterne værktøjer og tjenester:

| Værktøj | Rolle | Obligatorisk |
|---------|-------|-------------|
| [Claude Code](https://claude.ai/code) | Kører skills og workflowet i repoet | Ja |
| [GitHub CLI (`gh`)](https://cli.github.com) | Issues, PR'er og GitHub-automation fra terminalen | Ja |
| [Heimsense](https://github.com/fajarhide/heimsense) | Proxy der lader Claude Code bruge Copilot API i stedet for direkte Anthropic API | Ja (hvis Copilot-licens) |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli) | Copilot i terminalen — bruges til auth-flow med Heimsense | Ja (hvis Copilot-licens) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop) | Kører lokal devcontainer | Nej (kun lokal dev) |
| [VSCode + Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) | Lokal udvikling i reproducerbart container-miljø | Nej (kun lokal dev) |

Se [`CLAUDE_SETUP.md`](starter-kit/CLAUDE_SETUP.md) for installation af CLI-værktøjer og Heimsense. Se [`DEV_SETUP.md`](starter-kit/DEV_SETUP.md) for lokal devcontainer-opsætning.

---

## Hurtigste vej

Brug "Hurtigste vej" hvis du allerede har `gh` og Claude Code. Brug "Fuld opsætning" hvis du starter fra nul.

Har du `gh` og Claude Code installeret? Så er du i gang på 5 minutter:

```bash
# Klon starter-kittet
git clone --depth 1 https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit

# Kopiér alt til dit repo (erstat /path/to/dit-repo)
bash scripts/import-to-repo.sh /path/to/dit-repo
```

Scriptet håndterer konflikter, tager backup af eksisterende filer og merger `.gitignore` automatisk. Kør derefter `/adopt` i Claude Code for at udfylde `CLAUDE.md` interaktivt.

> Se **[STARTER_KIT.md](starter-kit/STARTER_KIT.md)** for det komplette første-session-flow.

---

## Fuld opsætning

Har du ikke gh og Claude Code endnu, følg disse trin i rækkefølge:

| Dokument | Indhold |
|----------|---------|
| [DEV_SETUP.md](starter-kit/DEV_SETUP.md) | Lokal devcontainer og VSCode-setup |
| [CLAUDE_SETUP.md](starter-kit/CLAUDE_SETUP.md) | CLI-værktøjer og Heimsense |
| [STARTER_KIT.md](starter-kit/STARTER_KIT.md) | Kopiering af starter-kit og første Claude Code-flow |

### Trin 1 — Udviklingsmiljø

Installer Docker og VSCode devcontainer:

→ **[DEV_SETUP.md](starter-kit/DEV_SETUP.md)**

### Trin 2 — CLI-værktøjer

Installer gh, Copilot CLI, Claude Code og Heimsense:

→ **[CLAUDE_SETUP.md](starter-kit/CLAUDE_SETUP.md)**

### Trin 3 — AI-teamet

Kopiér starter-kittet og konfigurér teamet:

→ **[STARTER_KIT.md](starter-kit/STARTER_KIT.md)**

---

## Indhold

Dette kopieres til dit repo via `import-to-repo.sh`:

```
dit-repo/
├── CLAUDE.md                  ← tilpas til dit projekt
├── .claude/
│   ├── agents/                ← 7 AI-coworkers
│   ├── skills/                ← 18 aktiverbare skills
│   ├── rules/                 ← auto-indlæst kontekst
│   └── settings.json          ← kopieres kun hvis den mangler
├── .devcontainer/             ← Dockerfile og devcontainer.json
├── scripts/                   ← heimsense og devcontainer-scripts
├── docs/                      ← dokumentations-templates
├── .github/
│   ├── dependabot.yml
│   └── workflows/shellcheck.yml
└── .gitignore                 ← manglende linjer tilføjes
```

Setup-guides (kopieres til `starter-kit/` til reference):

```
starter-kit/
├── DEV_SETUP.md               ← lokal devcontainer-opsætning
├── CLAUDE_SETUP.md            ← CLI-værktøjer og Heimsense
└── STARTER_KIT.md             ← første-session-flow
```

---

## Licens

MIT
