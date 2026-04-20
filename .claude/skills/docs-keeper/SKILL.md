---
name: docs-keeper
description: Hold projektdokumentation i sync. Brug når du afslutter en feature, laver arkitekturændringer, skriver release notes, eller sikrer at docs afspejler koden.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Docs Keeper

Hold projektdokumentation opdateret og i sync med koden.

## Dokumentationshierarki

Et sundt projekt har dokumentation på tre niveauer:

```text
┌──────────────────────────────────────┐
│  Vision / Mission                    │  Hvorfor projektet eksisterer
│  Roadmap / Milestones                │  Hvad der bygges og hvornår
└──────────────────────────────────────┘
                   │
┌──────────────────────────────────────┐
│  CLAUDE.md / AGENTS.md               │  Conventions, always loaded
│  Arkitektur / System design          │  Hvordan systemet er bygget
│  API-dokumentation                   │  Endpoints og kontrakter
└──────────────────────────────────────┘
                   │
┌──────────────────────────────────────┐
│  Backlog / Feature-liste             │  Hvad der skal bygges
│  Issues / Task tracking              │  Hvad der arbejdes på nu
│  Acceptance criteria                 │  Hvad "done" betyder
└──────────────────────────────────────┘
```

Tilpas filnavnene til dit projekt. Det vigtige er at hvert niveau eksisterer.

## Projektets dokumentfiler

Disse filer skal holdes i sync. Tilpas stier til dit projekt:

| Fil | Indhold | Opdateres når |
|-----|---------|---------------|
| `docs/VISION.md` | Mission, problem, brugersegmenter, roadmap | Grundlæggende retning ændres (sjældent) |
| `docs/FEATURES.md` | Use cases og acceptkriterier med status (✅/❌) | Feature implementeret eller scope ændres |
| `docs/ARCHITECTURE.md` | Systemstruktur, datamodel, ADR'er | Arkitekturbeslutning træffes |
| `docs/API.md` | Endpoint-reference med request/response-eksempler | Endpoint tilføjes, ændres eller fjernes |
| `docs/SYSTEM.md` | Miljøer, env vars, deployment, rollback | Ny service, env var eller driftsprocedure |
| `docs/E2E_TESTS.md` | E2E test-oversigt, gotchas, flaky tests | Ny E2E test tilføjes eller flaky pattern opdages |

## Hvad opdateres hvornår

| Handling | Opdatér |
|---|---|
| Feature færdig | `FEATURES.md` (markér AC ✅, link til test), issue (luk med bevis) |
| Arkitekturændring | `ARCHITECTURE.md` (ny ADR), `CLAUDE.md` (hvis conventions ændres) |
| API-ændring | `API.md` (endpoint + breaking change notice i PR) |
| Ny env var eller service | `SYSTEM.md` |
| Ny E2E test eller flaky pattern | `E2E_TESTS.md` |
| Release | Release notes i PR-beskrivelse |

## Efter en feature er færdig

```text
1. Luk issue — tilføj bevis (link til PR, testresultat)
2. Opdatér backlog — markér feature som done
3. Opdatér acceptance criteria — ❌ → ✅, link til test-fil
4. Notér nye patterns i CLAUDE.md hvis koden introducerer dem
```

## Synk-tjekliste

```text
[ ] Issue lukket med bevis
[ ] Backlog markeret done, version history opdateret
[ ] Acceptance criteria opdateret og test-filer linket
[ ] Nye arkitekturmønstre dokumenteret
[ ] PR-beskrivelse linker til issue og AC
```

## Release notes-skabelon

```markdown
## Version X.Y.Z — YYYY-MM-DD

### Nye features
- **Feature** — kort beskrivelse

### Forbedringer
- Beskrivelse

### Bugfixes
- Beskrivelse

### Breaking changes
- ⚠️ Hvad der ændrede sig og migrationsvej
```

## PR-kommunikation

### Ny feature

```markdown
## Ny feature: {Navn}

**Hvad**: Kort beskrivelse
**Hvorfor**: Brugerfordel eller problem løst
**Sådan bruges det**: Kort vejledning
```

### Breaking change

```markdown
## ⚠️ Breaking change: {Beskrivelse}

**Hvad ændrede sig**: Beskrivelse
**Hvorfor**: Begrundelse
**Migration**: Trin til at opdatere

**Før**:
\`\`\`
// gammelt mønster
\`\`\`

**Efter**:
\`\`\`
// nyt mønster
\`\`\`
```

### Bugfix

```markdown
## Bugfix: {Kort beskrivelse}

**Problem**: Hvad var galt
**Root cause**: Årsag
**Fix**: Hvordan det blev løst
```

## Workflow

Når du bliver bedt om at opdatere dokumentation:

1. Læs den nuværende tilstand af relevante docs
2. Identificér hvad der mangler baseret på ændringerne
3. Opdatér hvert dokument og bevar forbindelserne
4. Verificér at kryds-referencer er korrekte
5. Opsummér hvad der blev opdateret

## Tegn på at docs er ude af sync

- Acceptance criteria siger ❌ på en feature der er implementeret
- CLAUDE.md beskriver et mønster der ikke bruges mere
- Backlog lister features som "todo" der allerede er merged
- API-dok beskriver endpoints der ikke eksisterer eller er ændret
