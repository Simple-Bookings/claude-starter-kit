# Starter-Kit — standardiseret Claude Code-flow i dit repo

Denne guide viser, hvordan du kopierer starter-kittet ind i et repo, tilpasser det til projektet og kører det første Claude Code-flow fra issue til implementering.

## Forudsætninger

- `gh` (GitHub CLI) og Claude Code installeret — se [CLAUDE_SETUP.md](CLAUDE_SETUP.md)
- `git` og `jq`

Se oversigten over tredjeparts-værktøjer i [README.md](../README.md) for en samlet liste over hvad starter-kittet bygger på.

---

## Første succes

### 1. Kopiér starter-kittet

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit && git sparse-checkout set starter-kit
cp -R starter-kit/. /path/to/dit-repo/
```

### 2. Udfyld `CLAUDE.md`

Åbn `CLAUDE.md` og udfyld de fem felter:

- **Projekt-overview** — hvad bygger I?
- **Tech stack** — frontend, backend, database, test
- **Sprog** — dansk eller engelsk i kode og docs?
- **Git workflow** — branch-navne, merge-regler
- **Key commands** — `npm install`, `npm test`, `npm run build`

Hold det kort. En ny udvikler skal kunne læse det på to minutter.

> **Git workflow:** Starter-kittet bruger `develop` som integrationsgren. Bruger dit repo `main` + feature-branches direkte, tilpas git workflow-sektionen i `CLAUDE.md`.

### 3. Commit og start Claude Code

```bash
cd /path/to/dit-repo
git add . && git commit -m "feat: tilføj Claude Code starter-kit"
claude
```

### 4. Første session

```text
/feature-branch
Opret en feature-branch fra develop til issue #<nr>
```

Derefter:

```text
/planning
Lav en konkret task-liste for issue #<nr> med fil-paths og verify-kommandoer
```

Når planen er godkendt:

```text
/execution
Implementér den første task fra planen
```

---

## Du er klar når

- [ ] `gh auth status` — logger ind som dig
- [ ] `claude --version` — viser en version
- [ ] `CLAUDE.md` er udfyldt med projekt, stack og commands
- [ ] Starter-kittet er kopieret ind i dit repo
- [ ] Første branch kan oprettes
- [ ] Første PR kan laves mod `develop`

---

## Tilpas teamet

Agentdefinitionerne ligger i `.claude/agents/`. Tilpas rollebeskrivelse og e-mailadresse til dit projekt for hver agent du vil bruge.

| Agent | Rolle |
|-------|-------|
| `pia` | Product Manager — scope og acceptkriterier |
| `tom` | Full Stack Developer — end-to-end features |
| `scott` | QA / Tester — tests og bug-hunting |
| `dan` | DevOps — CI/CD og drift |
| `aksel` | Architect — systemdesign og code review |
| `quinn` | Security — audits og OWASP |
| `frida` | UI Designer — komponenter og UX |

Start med én eller to agenter. Tilføj flere efterhånden som behovet opstår.

---

## Reference: Skills

Aktiveres ved at skrive `/skill-navn` i Claude Code.

#### Udviklingsflow

| Skill | Hvad |
|-------|------|
| `/planning` | Groomer et GitHub issue og producerer en konkret task-liste |
| `/execution` | Implementerer én task ad gangen og committer med bevis |
| `/reviewing` | Deep code review — outputter APPROVED eller NEEDS_FIXES |
| `/integration` | Håndterer PR-livscyklus: CI, rebase, merge og luk issue |

#### Git workflow

| Skill | Hvad |
|-------|------|
| `/feature-branch` | Opretter feature-branch og holder git-flowet rent |
| `/release` | Release fra develop til main med checkliste |
| `/hotfix` | Kritisk prod-bug: branch fra main, deploy, sync til develop |

#### Kodekvalitet

| Skill | Hvad |
|-------|------|
| `/tdd` | Red-green-refactor: skriv den fejlende test først |
| `/db-performance` | Finder og fikser N+1 queries og manglende indexes |
| `/validation-debugging` | Debugger schema-mangler mellem client og server |
| `/security-audit` | OWASP Top 10, npm audit, JWT-tjekliste, IDOR-check |

#### Dokumentation og issues

| Skill | Hvad |
|-------|------|
| `/github-issues` | Opretter issues med acceptkriterier og Definition of Done |
| `/docs-keeper` | Holder docs i sync med koden efter features |

#### Parallelisering

| Skill | Hvad |
|-------|------|
| `/issue-surfing` | Kører op til 5 agenter parallelt via git worktrees |
| `/git-worktree` | Isolerede arbejdsmapper til parallelle agenter |

#### Terminal

| Skill | Hvad |
|-------|------|
| `/bash-tui` | Best practices for flicker-fri terminal UI |

---

## Reference: Docs-templates

Ligger i `docs/`. Holdes i sync via `/docs-keeper`.

| Fil | Indhold |
|-----|---------|
| `VISION.md` | Mission, problem, brugersegmenter og roadmap |
| `FEATURES.md` | Use cases og acceptkriterier (✅/❌) |
| `ARCHITECTURE.md` | Systemstruktur og Architecture Decision Records |
| `API.md` | REST endpoint-reference med request/response-eksempler |
| `SYSTEM.md` | Miljøer, env vars, deployment og rollback |
| `E2E_TESTS.md` | E2E test-oversigt, gotchas og flaky tests |
