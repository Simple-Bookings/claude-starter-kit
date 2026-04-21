---
name: db-performance
description: Detect and fix N+1 queries, missing indexes, and slow database calls. Use when API responses are slow, when adding new queries, or when reviewing code that fetches related data in loops.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# DB Performance — N+1 og slow queries

## Hvad er et N+1-problem?

Et N+1-problem opstår når kode henter en liste (1 query) og derefter laver et separat opslag per element (N queries):

```typescript
// ❌ N+1 — 1 query for bookings + 1 query per booking for customer
const bookings = await db.booking.findMany();
for (const booking of bookings) {
  const customer = await db.customer.findUnique({ where: { id: booking.customerId } });
  console.log(customer.name);
}

// ✅ 1 query — hent relationer med det samme
const bookings = await db.booking.findMany({
  include: { customer: true },
});
```

Symptom: API-endpoint tager 2-6 sekunder. Antallet af queries svarer til antallet af rækker i resultatet.

---

## Diagnose

### Tæl queries i udvikling

**Prisma:**

```typescript
// Tilføj til din Prisma-instans midlertidigt
const prisma = new PrismaClient({
  log: [{ level: 'query', emit: 'event' }],
});

let queryCount = 0;
prisma.$on('query', () => { queryCount++; });

// Efter kaldet:
console.log(`Queries: ${queryCount}`);
```

**Generelt (PostgreSQL):**

```sql
-- Aktiver query-logging i PostgreSQL (lokal dev)
SET log_min_duration_statement = 0;
-- Kig derefter i postgres-loggen
```

### Mål responstid

```bash
# Simpel baseline
curl -s -o /dev/null -w "%{time_total}s\n" http://localhost:3000/api/ressource

# Med jq for at se payload-størrelse
curl -s http://localhost:3000/api/ressource | wc -c
```

**Tommelfingerregler:**

| Responstid | Vurdering |
|---|---|
| < 200ms | God |
| 200ms–1s | Acceptabel |
| 1–3s | Undersøg |
| > 3s | Bug — fix før deploy |

---

## Løsninger

### 1. Eager loading med `include`

```typescript
// Hent relationer i samme query
const orders = await db.order.findMany({
  include: {
    customer: true,
    items: {
      include: { product: true },
    },
  },
});
```

### 2. Vælg kun de felter du bruger (`select`)

```typescript
// ❌ Henter alle kolonner — dyrt ved brede tabeller
const users = await db.user.findMany();

// ✅ Kun det nødvendige
const users = await db.user.findMany({
  select: { id: true, name: true, email: true },
});
```

### 3. Flyt beregninger til databasen

```typescript
// ❌ Tæl i JavaScript
const bookings = await db.booking.findMany();
const confirmed = bookings.filter(b => b.status === 'CONFIRMED').length;

// ✅ Tæl i databasen
const confirmed = await db.booking.count({
  where: { status: 'CONFIRMED' },
});
```

### 4. Batch-opslag med `findMany` + `in`

```typescript
// ❌ Et opslag per ID
const results = await Promise.all(
  ids.map(id => db.product.findUnique({ where: { id } }))
);

// ✅ Et samlet opslag
const results = await db.product.findMany({
  where: { id: { in: ids } },
});
```

### 5. Pagination — aldrig hent alt

```typescript
// ❌ Kan returnere tusindvis af rækker
const all = await db.booking.findMany();

// ✅ Begræns altid
const page = await db.booking.findMany({
  take: 50,
  skip: offset,
  orderBy: { createdAt: 'desc' },
});
```

---

## Indexes

Manglende indexes er den næsthyppigste årsag til slow queries efter N+1.

### Hvornår skal du tilføje et index?

- Kolonner brugt i `WHERE`-betingelser der kører ofte
- Kolonner brugt i `ORDER BY` på store tabeller
- Foreign keys (de fleste ORM'er tilføjer ikke automatisk)
- Kolonner brugt i `JOIN`-betingelser

### Prisma-eksempel

```prisma
model Booking {
  id        String   @id
  status    String
  siteId    String
  createdAt DateTime

  @@index([siteId])           // Hent bookinger per site
  @@index([status, siteId])   // Filtrer på status + site
  @@index([createdAt])        // Sortering på dato
}
```

### Tjek om et index bruges (PostgreSQL)

```sql
EXPLAIN ANALYZE
SELECT * FROM "Booking" WHERE "siteId" = 'abc' ORDER BY "createdAt" DESC LIMIT 50;
```

Kig efter `Index Scan` i output. `Seq Scan` på store tabeller er et tegn på manglende index.

---

## Code review-tjekliste

Kig efter disse mønstre når du reviewer kode der rammer databasen:

```text
[ ] findMany() efterfulgt af loop med findUnique/findFirst → N+1
[ ] findMany() uden take/limit på endpoints der kan vokse → unbounded query
[ ] Filtrering i JavaScript på data der allerede er hentet → flyt til WHERE
[ ] Manglende index på foreign keys og hyppigt filtrerede kolonner
[ ] select(*) / ingen select på brede tabeller med mange kolonner
[ ] Nested loops med db-kald → batch med findMany({ where: { id: { in: ids } } })
```

---

## Tommelfingerregler

- **Max 5 queries per API-request** som udgangspunkt
- **Max 10 queries** ved komplekse aggregeringer
- Hvis du ser > 20 queries: der er altid et N+1-problem
- Mål FØR og EFTER en fix — tal, ikke mavefornemmelse
