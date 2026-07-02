# Test Discipline

**Tests are your safety net. NEVER accept failing tests.**

## When a Test Fails

1. **Find root cause** — no quick fixes or workarounds
2. **Investigate systematically:**

```text
┌─ Test fails
├─ Have acceptance criteria changed? → Check issue + implementation
├─ Is there a mismatch between AC and implementation? → RED FLAG
│  ├─ Should AC be updated? Should test be updated? Is code the problem?
│  └─ Create issue for clarification
└─ Fix issue → Verify ALL tests pass
```

**Never:**
- ❌ "Fix" the test without understanding root cause
- ❌ Comment out tests
- ❌ Use `.skip` without good reason and documentation

**Always:**
- ✅ Find stable, correct solution
- ✅ Verify ALL tests pass

---

## Definition of Done — New Functionality

When adding new functionality, ALWAYS:

```text
┌─ Code written
├─ ✅ Unit Tests — do tests cover the logic?
├─ ✅ Integration Tests — do tests cover all ACs?
├─ ✅ E2E Tests — does test cover the full user journey?
└─ ✅ Commit & PR — references issue, PR mentions ACs
```

1. Implement feature AND write tests
2. Mark DoD checkboxes with evidence
3. Verify DoD before creating PR

---

## Test Data Gotchas

### Always Reset Test Data

```typescript
// ❌ WRONG — fails if old data exists
if (count === 0) { await db.model.createMany(...) }

// ✅ CORRECT — always consistent data
await db.model.deleteMany({});
await db.model.createMany({ data: [...] });
```

### Never Filter deleteMany in beforeEach

**Never use filtered `deleteMany` in `beforeEach`/`afterEach`** — it leaves stale data that breaks unique constraints.

```typescript
// ❌ WRONG — stale data survives if filter doesn't match
beforeEach(async () => {
  await db.model.deleteMany({ where: { name: { startsWith: 'Test' } } });
});

// ✅ CORRECT — global deleteMany ensures clean slate
beforeEach(async () => {
  await db.model.deleteMany();
});
```

**Symptom:** `duplicate key value violates unique constraint` in CI, especially on 2nd+ runs.

### Dates That Depend on "Tomorrow" — FLAKY TEST

**Never use `new Date() + 1 day`** — it can hit weekends or holidays.

```typescript
// ❌ WRONG — fails on Saturday (tomorrow = Sunday = possibly closed)
const futureTime = new Date();
futureTime.setDate(futureTime.getDate() + 1);

// ✅ CORRECT — skip weekends
const futureTime = new Date();
do {
  futureTime.setDate(futureTime.getDate() + 1);
} while (futureTime.getDay() === 0 || futureTime.getDay() === 6);

// ✅ ALTERNATIVE — use fixed historical date
const pastDate = new Date('2020-01-01T10:00:00Z');
```

---

## E2E Test Timeouts

- **NEVER set timeout over 10s** — that's a BUG, not a timing solution
- Over 5s → investigate performance (N+1 queries, slow API, render loops)
- Classify the failure BEFORE you act: performance / code bug / not implemented / test data conflict
