# E2E & Test Coverage

**Sidst opdateret:** [YYYY-MM-DD]
**Ansvarlig:** [QA/ansvarlig]
**Relateret:** [FEATURES.md](FEATURES.md) (acceptkriterier), CI-pipeline

---

## 1. Coverage-overblik

### Samlet status

| Metrik | Antal | Note |
|--------|-------|------|
| **E2E spec-filer** | [N] | I `e2e/` mappen |
| **E2E tests i alt** | [N] | |
| **Server tests (unit/integration)** | [N] | |
| **Tests der passerer** | ~[X]% | Se aktuelle CI-kørsler |
| **Flaky test rate** | ~[X]% | Mål: < 2% |

### Coverage-mål

| Mål | Target | Aktuel | Status |
|-----|--------|--------|--------|
| E2E coverage af implementerede UC | 60% | [X]% | [OK / Under target] |
| Unit test coverage | 80% | [X]% | [OK / Under target] |
| Integration tests (API endpoints) | Alle | Delvist | I gang |

---

## 2. CI-struktur

Tests kører i parallelle jobs mod test-miljøet. Smoke-tests kører som gate — fejler de, stoppes alt andet.

| Kategori | Tag | Formål | CI Job |
|----------|-----|--------|--------|
| **Smoke** (gate) | `@smoke` | Kritiske happy paths — kører altid | `e2e-smoke` |
| **[Kategori 1]** | `@e2e:[kategori]` | [Hvad tester denne kategori] | `e2e-category` |
| **[Kategori 2]** | `@e2e:[kategori]` | [Hvad tester denne kategori] | `e2e-category` |
| **[Kategori N]** | `@e2e:[kategori]` | [Hvad tester denne kategori] | `e2e-category` |

**Data-isolation:** Hver kategori bruger sit eget test-site/bruger i databasen → ingen konflikter mellem parallelle jobs.

---

## 3. Coverage-matrix

### [Kerneflow — fx Booking / Onboarding / Checkout]

| UC | Navn | E2E Spec | Integration | Coverage |
|----|------|----------|-------------|----------|
| UC001 | [Use case] | [spec-fil].spec.ts | [test-fil].test.ts | [X]% |
| UC002 | [Use case] | [spec-fil].spec.ts | — | [X]% |
| UC003 | [Use case] | ❌ mangler | [test-fil].test.ts | [X]% |

### [Auth]

| UC | Navn | E2E Spec | Integration | Coverage |
|----|------|----------|-------------|----------|
| UC010 | [Login] | auth.spec.ts | auth.test.ts | [X]% |
| UC011 | [Registrering] | auth.spec.ts | auth.test.ts | [X]% |

### [Admin / backoffice]

| UC | Navn | E2E Spec | Integration | Coverage |
|----|------|----------|-------------|----------|
| UC020 | [Admin use case] | admin.spec.ts | — | [X]% |

---

## 4. Kørselskommandoer

```bash
# Alle E2E tests
npm run test:e2e

# Enkelt spec-fil
npx playwright test e2e/[feature].spec.ts

# Med UI (headed mode — til debugging)
npx playwright test --headed

# Kun smoke tests
npx playwright test --grep @smoke

# Mod specifikt miljø
BASE_URL=https://test.[projekt].dk npx playwright test

# Debug mode
npx playwright test --debug
```

---

## 5. Fixtures og helpers

### Auth fixture — separate contexts (VIGTIGT)

```typescript
// ✅ KORREKT — hver bruger-type får sin egen browser context
const adminPage = async ({ browser }, use) => {
  const context = await browser.newContext();
  const page = await context.newPage();
  await loginAs(page, 'admin@test.dk', 'password');
  await use(page);
  await context.close();
};

// ❌ FORKERT — deler { page } → tokens overskriver hinanden
const adminPage = async ({ page }, use) => {
  await loginAs(page, 'admin@test.dk', 'password');
  await use(page); // supporterPage logger ind oven på admin
};
```

### Test-data factory

```typescript
// Opret konsistent test-data
export async function createTestUser(data?: Partial<UserInput>) {
  return prisma.user.create({
    data: { email: `test-${Date.now()}@test.dk`, ...data }
  });
}
```

---

## 6. Gotchas

### Timeouts

- **ALDRIG over 10s** — det er et performanceproblem, ikke en timing-løsning
- Brug `waitForResponse` frem for `waitForTimeout`

```typescript
// ❌ FORKERT
await page.waitForTimeout(3000);

// ✅ KORREKT
await page.waitForResponse(resp => resp.url().includes('/api/[ressource]'));
```

### Skjulte knapper (hover-reveal)

```typescript
// Knapper med opacity-0 group-hover:opacity-100 kræver hover over parent
await page.hover('[data-testid="row"]');
await page.click('[data-testid="action-button"]');
```

### Test-data isolation

```typescript
// ✅ Global deleteMany i beforeEach — ikke filtreret
beforeEach(async () => {
  await prisma.[model].deleteMany(); // IKKE: deleteMany({ where: { name: { startsWith: 'Test' } } })
});
```

### Datoer og weekender

```typescript
// ❌ FORKERT — kan ramme søndag (lukket)
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);

// ✅ KORREKT — spring weekender over
const futureDate = new Date();
do {
  futureDate.setDate(futureDate.getDate() + 1);
} while (futureDate.getDay() === 0 || futureDate.getDay() === 6);
```

---

## 7. Kendte flaky tests

| Test | Årsag | Status | Issue |
|------|-------|--------|-------|
| [Test-navn] | [Root cause] | [Åben / Løst] | #[nr] |
