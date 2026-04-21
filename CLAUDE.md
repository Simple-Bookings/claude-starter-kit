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

## ⛔ Secrets — ABSOLUT FORBUD mod push

Filer der indeholder eller ligner secrets må **aldrig** committes eller pushes uden eksplicit tilladelse fra brugeren.

**Hvad der tæller som secrets:**
- API-nøgler, tokens, passwords, private keys
- `.env`-filer og varianter (`.env.local`, `.env.production`, osv.)
- Filer med mønstre som `SECRET`, `PASSWORD`, `API_KEY`, `PRIVATE_KEY`, `TOKEN` i værdier
- Certifikater og nøglefiler (`.pem`, `.key`, `.p12`, `.pfx`)
- Credential-filer (`credentials.json`, `serviceAccount.json`, osv.)

**Procedure ved fund:**

1. Stop — commit eller push IKKE filen
2. Tilføj filen til `.gitignore` med det samme
3. Fortæl brugeren hvad du fandt og hvorfor du ikke pusher det
4. Afvent eksplicit tilladelse før du fortsætter

```bash
# ✅ KORREKT — tilføj til .gitignore før noget andet
echo ".env.local" >> .gitignore
echo "credentials.json" >> .gitignore
```

> Hvis brugeren eksplicit beder dig committe en fil med secrets, bekræft én gang til og dokumentér tilladelsen i commit-beskeden.

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
