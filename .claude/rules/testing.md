---
name: testing
description: Test-disciplin, test data patterns og Definition of Done for ny funktionalitet
type: rule
---

# Test Discipline

**Tests er vores redningsline. Acceptér ALDRIG fejlende tests.**

## Når en test fejler

1. **Find root cause** — ikke quick fixes eller workarounds
2. **Undersøg systematisk:**

```text
┌─ Test fejler
├─ Er acceptkriterierne ændret? → Check GitHub issue + implementation
├─ Er der forskel mellem AC og implementation? → RØD FLAG
│  ├─ Skal AC opdateres? Skal testen opdateres? Er koden problemet?
│  └─ Opret issue til afklaring
└─ Fix issue → Verify ALL tests pass
```

**Aldrig:**
- ❌ "Fixe" testen uden at forstå root cause
- ❌ Kommentere tests ud
- ❌ Bruge `.skip` uden god grund og dokumentation

**Altid:**
- ✅ Find stabil, korrekt løsning
- ✅ Verificer at ALLE tests passerer

## Definition of Done — Ny Funktionalitet

Når vi tilføjer ny funktionalitet, ALTID:

```text
┌─ Kode skrevet
├─ ✅ Integration Tests — dækker tests alle ACs?
├─ ✅ E2E Tests — dækker den fulde user journey?
└─ ✅ Commit & PR — refererer til issue, PR nævner ACs
```

1. Implementer feature OG skriv tests
2. Marker DoD checkboxes med bevis
3. Verificer DoD før PR oprettes

## Test Data Gotchas

```typescript
// ❌ FORKERT — fejler hvis gammel data eksisterer
if (count === 0) { await db.model.createMany(...) }

// ✅ KORREKT — altid konsistent data
await db.model.deleteMany({});
await db.model.createMany({ data: [...] });
```

## ⛔ Filtered deleteMany i beforeEach — KRITISK FEJL

**Brug ALDRIG filtreret `deleteMany` i `beforeEach`/`afterEach`** — det efterlader stale data som bryder unique constraints i efterfølgende runs.

```typescript
// ❌ FORKERT — stale data overlever hvis where-filter ikke matcher
beforeEach(async () => {
  await db.model.deleteMany({ where: { name: { startsWith: 'Test' } } });
});

// ✅ KORREKT — global deleteMany sikrer rent slate
beforeEach(async () => {
  await db.model.deleteMany();
});
```

**Symptom:** `duplicate key value violates unique constraint` i CI, specielt på 2. og efterfølgende runs.
**Root cause:** Integration test creates data → filtered delete misser noget → næste run finder stale data → constraint violation.

## ⛔ Datoer der afhænger af "i morgen" — FLAKY TEST

**Brug ALDRIG `new Date() + 1 dag`** — det kan ramme weekend eller helligdag og give uventet adfærd.

```typescript
// ❌ FORKERT — fejler lørdag (i morgen = søndag = evt. lukket)
const futureTime = new Date();
futureTime.setDate(futureTime.getDate() + 1);

// ✅ KORREKT — spring weekender over
const futureTime = new Date();
do {
  futureTime.setDate(futureTime.getDate() + 1);
} while (futureTime.getDay() === 0 || futureTime.getDay() === 6);

// ✅ ALTERNATIVT — fast historisk dato (til "er-i-fortiden" tests)
const pastDate = new Date('2020-01-01T10:00:00Z');
```

## E2E Test Timeouts

- **ALDRIG sæt timeout over 10s** — det er en BUG, ikke en timing-løsning
- Over 5s → undersøg performance (N+1 queries, slow API, render loop)
- Klassificér fejlen FØR du gør noget: performance / kode-bug / ikke implementeret / test-data konflikt
