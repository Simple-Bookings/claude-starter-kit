# Claude Code Starter-Kit

Et mini AI-team til dit repo — klar til brug på under 30 minutter.

Kittet giver dig 7 AI-coworkers, 16 skills og et komplet workflow fra GitHub issue til merged PR, baseret på [Claude Code](https://claude.ai/code).

---

## Guides

| Fil | Indhold |
|-----|---------|
| [getting-started.md](getting-started.md) | Overblik over kittet — skills, agents, rules og docs |
| [cli-setup.md](cli-setup.md) | Installer gh, Copilot CLI, Claude Code og Heimsense |
| [local-devcontainer.md](local-devcontainer.md) | Opsæt lokal devcontainer med VSCode |

---

## Kom i gang

### 1. Kopiér starter-kittet ind i dit repo

```bash
git clone https://github.com/Simple-Bookings/claude-starter-kit.git

cp -R claude-starter-kit/starter-kit/. /path/to/dit-repo/
```

Når kopien er på plads, har du:

```
dit-repo/
├── CLAUDE.md                   ← tilpas til dit projekt
├── .claude/
│   ├── agents/                 ← 7 AI-coworker definitioner
│   ├── skills/                 ← 16 aktiverbare skills
│   └── rules/                  ← koderegler auto-indlæst af Claude
└── docs/
    ├── VISION.md
    ├── FEATURES.md
    ├── ARCHITECTURE.md
    ├── API.md
    ├── SYSTEM.md
    └── E2E_TESTS.md
```

### 2. Tilpas `CLAUDE.md`

Udfyld de fem vigtigste felter: projekt-overview, tech stack, sprog-regler, git workflow og key commands.

### 3. Start Claude Code

```bash
cd dit-repo
claude
```

Kør `/feature-branch` for at starte dit første flow.

---

## Hvad er med

### Skills

Aktiveres ved at skrive `/skill-navn` i Claude Code.

#### Udviklingsflow

| Skill | Hvem | Hvad |
|-------|------|------|
| `/plan` | pia, tom | Groomer et GitHub issue og producerer en konkret task-liste |
| `/build` | tom | Implementerer én task ad gangen og committer med bevis |
| `/review` | aksel, tom | Deep code review — outputter APPROVED eller NEEDS_FIXES |
| `/integrate` | tom, dan | Håndterer PR-livscyklus: CI, rebase, merge og luk issue |

#### Git workflow

| Skill | Hvem | Hvad |
|-------|------|------|
| `/feature-branch` | tom, frida | Opretter feature-branch og holder git-flowet rent |
| `/release` | dan | Release fra develop til main med checkliste |
| `/hotfix` | dan, tom | Kritisk prod-bug: branch fra main, deploy, sync til develop |

#### Kodekvalitet

| Skill | Hvem | Hvad |
|-------|------|------|
| `/tdd` | tom, scott | Red-green-refactor: skriv den fejlende test først |
| `/db-performance` | tom, aksel | Finder og fikser N+1 queries og manglende indexes |
| `/validation-debugging` | tom, scott | Debugger Zod/DTO-mangler og ORM select-huller |
| `/security-audit` | quinn | OWASP Top 10, npm audit, JWT-tjekliste, IDOR-check |

#### Dokumentation og issues

| Skill | Hvem | Hvad |
|-------|------|------|
| `/github-issues` | pia | Opretter issues med AC og Definition of Done |
| `/docs-keeper` | pia, frida | Holder docs i sync med koden efter features |

#### Parallelisering

| Skill | Hvem | Hvad |
|-------|------|------|
| `/surfing` | pia, tom | Kører op til 5 agenter parallelt via git worktrees |
| `/git-worktree` | tom, dan | Isolerede arbejdsmapper til parallelle agenter |

#### Terminal

| Skill | Hvem | Hvad |
|-------|------|------|
| `/bash-tui` | dan | Best practices for flicker-fri terminal UI |

---

### Agents

7 AI-coworkers i `starter-kit/.claude/agents/`:

| Agent | Rolle |
|-------|-------|
| `pia` | Product Manager — scope, acceptkriterier, prioritering |
| `tom` | Full Stack Developer — end-to-end features |
| `scott` | QA / Tester — tests, bug-hunting, DoD |
| `dan` | DevOps Engineer — CI/CD, scripts, drift |
| `aksel` | Architect — systemdesign, code review |
| `quinn` | Security Engineer — audits, auth-review, OWASP |
| `frida` | UI Designer — komponenter, UX, accessibility |

### Rules

3 filer i `starter-kit/.claude/rules/` — indlæses automatisk som kontekst:

| Fil | Indhold |
|-----|---------|
| [`coding-patterns.md`](starter-kit/.claude/rules/coding-patterns.md) | CronCreate vs sleep, bash `local`-gotcha, GitHub CLI patterns |
| [`testing.md`](starter-kit/.claude/rules/testing.md) | Test-disciplin, test data gotchas, DoD, E2E timeouts |
| [`workflow.md`](starter-kit/.claude/rules/workflow.md) | Delegering og handover-protokol |

### Docs

6 templates i `starter-kit/docs/`:

| Fil | Indhold |
|-----|---------|
| [`VISION.md`](starter-kit/docs/VISION.md) | Mission, problem, brugersegmenter og roadmap |
| [`FEATURES.md`](starter-kit/docs/FEATURES.md) | Use cases og acceptkriterier (✅/❌) |
| [`ARCHITECTURE.md`](starter-kit/docs/ARCHITECTURE.md) | Systemstruktur og Architecture Decision Records |
| [`API.md`](starter-kit/docs/API.md) | REST endpoint-reference med request/response-eksempler |
| [`SYSTEM.md`](starter-kit/docs/SYSTEM.md) | Miljøer, env vars, deployment og rollback |
| [`E2E_TESTS.md`](starter-kit/docs/E2E_TESTS.md) | E2E test-oversigt, gotchas og flaky tests |

---

## Forudsætninger

- [Claude Code](https://claude.ai/code)
- `git` og `gh` (GitHub CLI)
- `jq` (anbefalet)

---

## Licens

MIT
