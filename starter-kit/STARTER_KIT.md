# Starter-Kit — standardiseret Claude Code-flow i dit repo

Denne guide viser, hvordan du sætter starter-kittet op — enten i et **nyt tomt repo** eller i et **eksisterende repo med kode**.

## Forudsætninger

- `gh` (GitHub CLI) og Claude Code installeret — se [CLAUDE_SETUP.md](CLAUDE_SETUP.md)
- `git` og `bash`

Se oversigten over tredjeparts-værktøjer i [README.md](../README.md) for en samlet liste over hvad starter-kittet bygger på.

---

## Scenarie A — Nyt tomt repo

Du starter fra bunden og vil bruge dette repo som udgangspunkt.

### 1. Fork eller klon

**Fork** (anbefalet — du får dit eget repo på GitHub):

Gå til [github.com/Simple-Bookings/claude-starter-kit](https://github.com/Simple-Bookings/claude-starter-kit) og klik **Fork**. Klon derefter dit fork:

```bash
gh repo clone DIT-BRUGERNAVN/claude-starter-kit mit-projekt
cd mit-projekt
```

**Eller klon direkte** (uden fork):

```bash
git clone https://github.com/Simple-Bookings/claude-starter-kit.git mit-projekt
cd mit-projekt
# Skift remote til dit eget repo
git remote set-url origin https://github.com/DIT-BRUGERNAVN/mit-projekt.git
```

### 2. Udfyld `CLAUDE.md`

> **Dette trin er ikke valgfrit.** Alle `[Skriv ...]`-felter skal udfyldes inden Claude Code startes.

Åbn `CLAUDE.md` og udfyld:
- **Projektnavn og formål**
- **Tech stack** — frontend, backend, database, test
- **Key commands** — `npm install`, `npm test`, `npm run build`

### 3. Åbn i devcontainer og start Claude Code

Åbn mappen i VSCode og vælg **"Reopen in Container"**. Devcontaineren installerer heimsense og starter PM2 automatisk.

```bash
claude
/onboarding
```

---

## Scenarie B — Eksisterende repo med kode

Du har allerede et repo med kode og vil tilføje starter-kittet til det.

### 1. Klon starter-kittet lokalt

```bash
git clone https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit
```

### 2. Kør import-scriptet

```bash
bash scripts/import-to-repo.sh /sti/til/dit-eksisterende-repo
```

Scriptet kopierer følgende ind i dit repo:

| Hvad | Håndtering ved konflikt |
|------|------------------------|
| `.claude/` (agents, skills, rules) | Overskrives |
| `.devcontainer/` | Backup tages (`.bak`) |
| `scripts/` (heimsense + devcontainer) | Backup tages pr. fil |
| `docs/` templates | Springer over filer med reelt indhold |
| `.github/` (dependabot, shellcheck) | Overskrives |
| `CLAUDE.md` | Backup tages |
| `.gitignore` | Merger — tilføjer kun manglende linjer |
| `starter-kit/` (setup-guides) | Overskrives |

**Alternativt: brug `/adopt`-skillsen** inde fra Claude Code — den guider dig interaktivt og udfylder CLAUDE.md automatisk:

```bash
cd dit-eksisterende-repo
claude
/adopt
```

### 3. Udfyld `CLAUDE.md`

Åbn den kopierede `CLAUDE.md` og tilpas til dit projekt. Er du i Claude Code, kan `/adopt`-skillsen hjælpe med at scanne dit repo og foreslå de rigtige værdier.

### 4. Commit og åbn devcontainer

```bash
cd dit-eksisterende-repo
git add .
git commit -m "feat: tilføj Claude Code starter-kit"
```

Åbn i VSCode → **"Reopen in Container"**.

### 5. Start Claude Code

```bash
claude
/onboarding
```

---

## Du er klar når

- [ ] `gh auth status` — logger ind som dig
- [ ] `claude --version` — viser en version
- [ ] `CLAUDE.md` er udfyldt med projekt, stack og commands
- [ ] Starter-kittet er i dit repo
- [ ] Devcontaineren kører (heimsense starter automatisk)
- [ ] `/onboarding` viser grøn status

---

## Første session

Start med `/onboarding` — det scanner repo-tilstanden, husker din fremgang på tværs af sessioner og guider dig til næste trin:

```
/onboarding
```

Derefter, når onboarding er grøn:

```
/planning
Jeg vil gerne bygge <beskriv hvad du vil implementere>
```

`/planning` opretter automatisk et GitHub issue, udfylder acceptkriterier og producerer en konkret task-liste. Derefter:

```
/execution
```

`/execution` opretter automatisk en feature-branch og implementerer én task ad gangen indtil alt er done.

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

#### Opsætning

| Skill | Hvad |
|-------|------|
| `/adopt` | Importér starter-kit til eksisterende repo — interaktiv guide |
| `/onboarding` | Repo-coach — scanner status og guider til næste trin |

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
