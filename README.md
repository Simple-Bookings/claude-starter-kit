# Claude Code Starter-Kit

Standardiseret udviklingsflow og onboarding til Claude Code — fra GitHub issue til merged PR uden manuel opfølgning.

---

## Tredjeparts-værktøjer

Starter-kittet bygger på disse eksterne værktøjer og tjenester:

| Værktøj | Rolle | Obligatorisk |
|---------|-------|-------------|
| [Claude Code](https://claude.ai/code) | Kører skills og workflowet i repoet | Ja |
| [GitHub CLI (`gh`)](https://cli.github.com) | Issues, PR'er og GitHub-automation fra terminalen | Ja |
| [Heimsense](https://github.com/strowk/heimsense) | Proxy der lader Claude Code bruge Copilot API i stedet for direkte Anthropic API | Ja (hvis Copilot-licens) |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli) | Copilot i terminalen — bruges til auth-flow med Heimsense | Ja (hvis Copilot-licens) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop) | Kører lokal devcontainer | Nej (kun lokal dev) |
| [VSCode + Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) | Lokal udvikling i reproducerbart container-miljø | Nej (kun lokal dev) |

Se [`CLAUDE_SETUP.md`](CLAUDE_SETUP.md) for installation af CLI-værktøjer og Heimsense. Se [`DEV_SETUP.md`](DEV_SETUP.md) for lokal devcontainer-opsætning.

---

## Hurtigste vej

Brug "Hurtigste vej" hvis du allerede har `gh` og Claude Code. Brug "Fuld opsætning" hvis du starter fra nul.

Har du `gh` og Claude Code installeret? Så er du i gang på 5 minutter:

```bash
# Hent starter-kittet
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit && git sparse-checkout set starter-kit
cp -R starter-kit/. /path/to/dit-repo/
```

Starter-kittet kopierer `CLAUDE.md`, agents, skills, rules og docs-templates ind i dit repo, så Claude Code kan arbejde efter et fast workflow.

Udfyld `CLAUDE.md` med projekt-navn, tech stack og key commands. Start derefter Claude Code:

```bash
cd /path/to/dit-repo
claude
```

Første session:

```text
/feature-branch
Opret en feature-branch fra develop til issue #<nr>
```

```text
/plan
Lav en konkret task-liste for issue #<nr> med fil-paths og verify-kommandoer
```

---

## Fuld opsætning

Har du ikke gh og Claude Code endnu, følg disse trin i rækkefølge:

| Dokument | Indhold |
|----------|---------|
| [DEV_SETUP.md](DEV_SETUP.md) | Lokal devcontainer og VSCode-setup |
| [CLAUDE_SETUP.md](CLAUDE_SETUP.md) | CLI-værktøjer og Heimsense |
| [STARTER_KIT.md](STARTER_KIT.md) | Kopiering af starter-kit og første Claude Code-flow |

### Trin 1 — Udviklingsmiljø

Installer Docker og VSCode devcontainer:

→ **[DEV_SETUP.md](DEV_SETUP.md)**

### Trin 2 — CLI-værktøjer

Installer gh, Copilot CLI, Claude Code og Heimsense:

→ **[CLAUDE_SETUP.md](CLAUDE_SETUP.md)**

### Trin 3 — AI-teamet

Kopiér starter-kittet og konfigurér teamet:

→ **[STARTER_KIT.md](STARTER_KIT.md)**

---

## Indhold

```
starter-kit/
├── CLAUDE.md             ← tilpas til dit projekt
├── .claude/
│   ├── agents/           ← 7 AI-coworkers
│   ├── skills/           ← 16 aktiverbare skills
│   └── rules/            ← auto-indlæst kontekst
└── docs/                 ← dokumentations-templates
```

---

## Licens

MIT
