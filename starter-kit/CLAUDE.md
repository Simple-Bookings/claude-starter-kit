# CLAUDE.md

Guidance for AI assistants i dette repo.

## Projekt-overview

**Projekt:** [Skriv projektnavn]

**Formål:** [Beskriv kort hvad produktet eller systemet gør]

**Primære brugere:** [Hvem bruger løsningen?]

## Tech stack

- Frontend: [fx React, Vue eller Next.js]
- Backend: [fx Express, FastAPI eller Rails]
- Database: [fx PostgreSQL eller SQLite]
- Test: [fx Vitest, Playwright, pytest]
- Deployment: [fx GitHub Actions, Docker, VPS]

> **Bemærk:** Starter-kittets skills og rules er optimeret til GitHub-baserede workflows med JavaScript/TypeScript-lignende kodebaser. De kan bruges med andre stacks, men eksempler og kommandoer (fx `npm test`) skal tilpasses i Key commands nedenfor.

## Sprog

- Samtale, issues, docs og commits: dansk
- Kode, filnavne og identifiers: engelsk
- UI-tekster: dansk, med mindre produktet er engelsksproget

## Git workflow

```text
main (produktion) <- develop (integration/test) <- feature/*
```

- Branch altid fra `develop`
- PRs går til `develop`
- Releases går fra `develop` til `main`
- Brug små commits med meningsfulde beskeder

## Key commands

```bash
npm install
npm test
npm run build
```

Tilpas kommandoerne ovenfor til projektet, og hold dem korte nok til at en ny udvikler kan komme i gang hurtigt.

## Do

- Følg eksisterende patterns før du introducerer nye
- Skriv eller opdatér tests sammen med koden
- Gør root cause tydelig ved bugs
- Hold docs og scripts på linje med implementationen

## Don't

- Commit aldrig direkte til `main`
- Brug ikke `as any` eller tilsvarende genveje uden stærk grund
- Tilføj ikke skjult magi eller hardcodede lokale paths
- Luk ikke issues med åbne DoD-checkboxes

## Dokumentation

Projektdokumentation ligger i `docs/`. Holdes i sync med koden via `/docs-keeper`.

| Fil | Indhold |
|-----|---------|
| `docs/VISION.md` | Mission, problem, brugersegmenter og overordnet roadmap |
| `docs/FEATURES.md` | Use cases og acceptkriterier med implementeringsstatus |
| `docs/ARCHITECTURE.md` | Systemstruktur, datamodel og Architecture Decision Records |
| `docs/API.md` | REST endpoint-reference med request/response-eksempler |
| `docs/SYSTEM.md` | Miljøer, environment variables, deployment og rollback |
| `docs/E2E_TESTS.md` | E2E test-oversigt, gotchas og kendte flaky tests |

## Regler

Detaljerede regler og gotchas ligger i `.claude/rules/`:

| Fil | Indhold |
|-----|---------|
| `coding-patterns.md` | CronCreate vs sleep, bash `local`, GitHub CLI patterns |
| `testing.md` | Test-disciplin, test data gotchas, DoD |
| `workflow.md` | Delegering, handover-protokol, ansvarsområder |
