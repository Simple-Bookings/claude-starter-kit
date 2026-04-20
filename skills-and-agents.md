# Kom i gang med starter-kittet

Denne guide er lavet til at få et nyt repo i gang med et mini AI-team på under 30 minutter.

## Forudsætninger

- `git`
- `gh` (GitHub CLI)
- `bash`
- `jq` (anbefalet, især til helper-scripts)
- Claude Code installeret — se [`cli-setup.md`](./cli-setup.md)

## Trin 1: Kopiér starter-kittet ind i dit repo

Kopiér indholdet af `starter-kit/` til roden af dit nye repo:

```bash
cp -R starter-kit/. /path/to/dit-repo/
```

Når kopien er på plads, bør du mindst have:

- `CLAUDE.md`
- `.claude/agents/`
- `.claude/skills/`

## Hvad er med i starter-kittet

### Skills

Aktiveres automatisk når du skriver `/skill-navn` i Claude Code.

#### Udviklingsflow

De fire skills der driver AH-flowet fra issue til merged PR. Kør dem i rækkefølge.

| Skill | Hvem | Hvad | Hvorfor |
|-------|------|------|---------|
| `/plan` | pia, tom | Groomer et GitHub issue og producerer en konkret task-liste med fil-paths og verify-kommandoer | Sikrer at ingen implementerer før scope og tasks er klare — eliminerer design-beslutninger under implementering |
| `/build` | tom | Implementerer én task ad gangen, kører verify-kommando og committer — sætter selv næste iteration op via CronCreate | Tvinger fokus på én ting ad gangen og giver sporbar progress med bevis ved hvert trin |
| `/review` | aksel, tom | Deep code review: pattern-konsistens, arkitektur, blast-radius tests — outputter APPROVED eller NEEDS_FIXES | Finder hvad en hurtig executor overser: manglende mapper, inkonsistente typer, test-huller |
| `/integrate` | tom, dan | Håndterer hele PR-livscyklussen: CI, review-kommentarer, rebase, merge og luk issue | Ingen manuel opfølgning — looper automatisk til PR er merged og issue er lukket |

#### Git workflow

| Skill | Hvem | Hvad | Hvorfor |
|-------|------|------|---------|
| `/feature-branch` | tom, frida | Opretter feature-branch fra develop og holder git-flowet rent | Forhindrer at kode lander direkte på main — håndhæver PR-processen |
| `/release` | dan | Release fra develop til main med checkliste og TEST-verifikation | Struktureret release-flow der sikrer at intet shipper uden at være testet |
| `/hotfix` | dan, tom | Brancher fra main, tester med prod-data, deployer og syncer tilbage til develop | Til kritiske produktionsbug der ikke kan vente på normal release-cyklus |

#### Kodekvalitet

| Skill | Hvem | Hvad | Hvorfor |
|-------|------|------|---------|
| `/tdd` | tom, scott | Red-green-refactor: skriv den fejlende test først, implementer, refaktorer | Sikrer at tests afspejler kravene — ikke implementationen |
| `/db-performance` | tom, aksel | Finder og fikser N+1 queries, manglende indexes og slow database-kald | API-responstider over 500ms skyldes næsten altid databasen — dette skill finder årsagen |
| `/validation-debugging` | tom, scott | Debugger Zod middleware stripping, DTO-mapper-mangler og ORM select-huller | Felter der "forsvinder" mellem client og server er næsten altid et schema-mismatch |
| `/security-audit` | quinn | OWASP Top 10 gennemgang, npm audit, JWT-tjekliste, IDOR-check — producerer findings-rapport | Systematisk sikkerhedsreview der finder hvad ad-hoc review overser |

#### Dokumentation og issues

| Skill | Hvem | Hvad | Hvorfor |
|-------|------|------|---------|
| `/github-issues` | pia | Opretter issues med tydelig task list, acceptkriterier og Definition of Done | Issues uden AC og DoD er ikke klar til implementering — dette skill håndhæver standarden |
| `/docs-keeper` | pia, frida | Holder dokumentation i sync med koden efter features og arkitekturændringer | Docs der ikke opdateres ved release bliver løgn — dette skill gør det til en del af done |

#### Parallelisering

| Skill | Hvem | Hvad | Hvorfor |
|-------|------|------|---------|
| `/surfing` | pia, tom | Kører op til 5 agenter parallelt via TeamCreate og git worktrees | Reducerer calendar time markant for opgaver der kan splittes i uafhængige spor |
| `/git-worktree` | tom, dan | Isolerede arbejdsmapper til parallelle agenter uden git-konflikter | Nødvendig infrastruktur for `/surfing` — hver agent arbejder i sin egen branch uden at forstyrre andre |

#### Terminaler og scripts

| Skill | Hvem | Hvad | Hvorfor |
|-------|------|------|---------|
| `/bash-tui` | dan | Best practices for flicker-fri terminal UI med cursor-styring og farver | Bash-TUI'er flimrer og crasher uden de rigtige teknikker — dette skill samler dem ét sted |

### Rules

Indlæses automatisk af Claude Code som kontekst. Ligger i `.claude/rules/`.

| Fil | Indhold |
|-----|---------|
| `coding-patterns.md` | CronCreate vs sleep, bash `local`-gotcha, GitHub CLI patterns |
| `testing.md` | Test-disciplin, test data gotchas, DoD-tjekliste, E2E timeouts |
| `workflow.md` | Delegering og handover-protokol for AI-team coworkers |

### Agents

Agentdefinitioner til Claude Code. Ligger i `.claude/agents/`. Hver fil indeholder YAML frontmatter og rollebeskrivelse — det er alt hvad Claude Code behøver for at spawne agenten som `subagent_type`.

| Fil | Rolle |
|-----|-------|
| `pia.md` | Product Manager — scope, acceptkriterier, prioritering |
| `tom.md` | Full Stack Developer — end-to-end features på tværs af stacken |
| `scott.md` | QA / Tester — tests, bug-hunting og verificering af DoD |
| `dan.md` | DevOps Engineer — CI/CD, scripts og drift |
| `aksel.md` | Architect — systemdesign, code review og designbeslutninger |
| `quinn.md` | Security Engineer — audits, auth-review og OWASP |
| `frida.md` | UI Designer — komponenter, UX og accessibility |

Tilpas rollebeskrivelser og e-mailadresser til dit projekt. Brug dem sådan:

```text
Agent(subagent_type: "tom", prompt: "Implementér feature X fra issue #42")
Agent(subagent_type: "quinn", prompt: "Review auth-koden i src/middleware/")
```

### Docs

Dokumentations-templates med eksempler. Ligger i `docs/`. Holdes i sync via `/docs-keeper`.

| Fil | Indhold |
|-----|---------|
| `docs/VISION.md` | Mission, problem, brugersegmenter og overordnet roadmap |
| `docs/FEATURES.md` | Use cases og acceptkriterier med implementeringsstatus (✅/❌) |
| `docs/ARCHITECTURE.md` | Systemstruktur, datamodel og Architecture Decision Records |
| `docs/API.md` | REST endpoint-reference med request/response-eksempler |
| `docs/SYSTEM.md` | Miljøer, environment variables, deployment og rollback |
| `docs/E2E_TESTS.md` | E2E test-oversigt, gotchas og kendte flaky tests |

---

## Trin 2: Tilpas `CLAUDE.md`

Udfyld de fem vigtigste felter først:

1. Projekt-overview
2. Tech stack
3. Sprog-regler
4. Git workflow
5. Key commands

Hold filen kort. Starter-kittet virker bedst når nye udviklere kan læse det vigtigste på få minutter.

## Trin 3: Aktivér mini-teamet

Teamet består af 7 coworkers (se oversigten ovenfor). Start med dem der er relevante for din første opgave — du behøver ikke alle med det samme.

Tilpas `.claude/agents/{navn}.md` hvis rollerne eller tonen skal passe bedre til projektet. Opdatér e-mailadresserne til dit domæne.

## Trin 4: Kør din første session med `/feature-branch`

Et godt første flow er:

```text
/feature-branch
```

Målet er at:

1. branch'e fra `develop`
2. implementere en lille opgave
3. køre testsuiten
4. bygge projektet
5. oprette en PR til `develop`

## Tips til at holde pakken minimal

- Start med de coworkers der er relevante for din første opgave
- Tilføj først flere skills når et konkret behov opstår
- Hold driftsspecifikke URL'er og hemmeligheder ude af starterpakken
- Gør alle lokale paths relative, ikke maskinspecifikke

## Fejlfinding

### `jq` mangler

Installer `jq`, eller brug `python3 -m json.tool` som alternativ.

---

## Næste skridt

Du er klar. Start Claude Code i dit projekt og kør `/feature-branch` for at tage det første flow i brug.
