# Features & Acceptkriterier

**Sidst opdateret:** [YYYY-MM-DD]
**Vedligeholdt af:** [Team/ansvarlig]
**Relateret:** [SYSTEM.md](SYSTEM.md) (implementering), [E2E_TESTS.md](E2E_TESTS.md) (teststatus)

---

## Legende

| Symbol | Betydning |
|--------|-----------|
| ✅ | Implementeret og testet |
| ⏳ | Delvist implementeret eller testet |
| ❌ | Ikke implementeret / mangler test |
| — | Ikke relevant |

**AC-tabel kolonner:**
- **E2E** — er acceptkriteriet dækket af en E2E test?
- **Integration** — er det dækket af en integration test?
- **Issue** — GitHub issue-nummer hvis der mangler test eller er en known bug

---

## UC001: [Bruger kan [gøre noget]]

**Beskrivelse:** [Hvad use casen handler om — ét flow fra brugerens perspektiv]
**Missionskontekst:** *[Hvordan dette hænger sammen med produktets mission]*

| AC | Kriterium | E2E | Integration | Issue |
|----|-----------|-----|-------------|-------|
| AC001 | [Specifikt, testbart kriterie — fx "Bruger ser bekræftelsesbesked efter handling"] | ✅ | — | - |
| AC002 | [Specifikt, testbart kriterie] | ✅ | ✅ | - |
| AC003 | [Fejlscenarie — fx "Ugyldigt input viser fejlbesked"] | ❌ | — | #123 |

**E2E:** `e2e/[feature].spec.ts`
**Integration:** `src/[feature]/[feature].test.ts`

---

## UC002: [Bruger kan [gøre noget andet]]

**Beskrivelse:** [Beskrivelse]
**Missionskontekst:** *[Missionskontekst]*

| AC | Kriterium | E2E | Integration | Issue |
|----|-----------|-----|-------------|-------|
| AC004 | [Kriterie] | ✅ | ✅ | - |
| AC005 | [Kriterie] | ❌ | ❌ | - |

**E2E:** `e2e/[feature].spec.ts`

---

## UC003: [Tilføj ny use case her]

**Beskrivelse:** [Beskrivelse]
**Missionskontekst:** *[Missionskontekst]*

| AC | Kriterium | E2E | Integration | Issue |
|----|-----------|-----|-------------|-------|
| AC006 | [Kriterie] | ❌ | ❌ | - |

---

## Coverage-oversigt

Opdateres løbende. Detaljeret coverage: se `docs/E2E_TESTS.md`.

| UC-gruppe | Use Cases | E2E-dækning | Integrationsdækning |
|-----------|-----------|-------------|---------------------|
| [Kerneflow] | UC001–UC005 | ~80% | ~60% |
| [Auth] | UC006–UC008 | ~50% | ~90% |
| [Admin] | UC009–UC015 | ~30% | ~70% |
| **Total** | | **~55%** | **~70%** |

**Mål:** E2E-dækning > 60% på implementerede use cases.
