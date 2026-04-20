---
name: validation-debugging
description: Debug validation failures caused by schema/middleware mismatches — Zod schemas stripping fields, middleware not forwarding data, DTO shape mismatches. Systematic diagnosis and fix pattern.
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# /validation-debugging — Validation Failure Diagnosis

Use when a field is sent from the client but arrives as `undefined` on the server, or when data is saved to the database but not returned in API responses.

---

## The Core Problem

Validation middleware often strips fields that are not declared in the schema. If a field is added to the code but not to the schema, it silently disappears.

```
Client sends: { name: "Alice", newField: "value" }
         ↓
Zod middleware validates against schema
         ↓ newField not in schema → stripped silently
Server receives: { name: "Alice" }  ← newField gone
```

This is the most common root cause of "field is sent but undefined on server" bugs.

---

## Step 1: Reproduce with a Minimal Test

Before investigating, write a failing test that demonstrates the problem:

```typescript
it('should preserve newField through the API', async () => {
  const response = await request(app)
    .post('/api/resource')
    .send({ name: 'Test', newField: 'value' })
    .expect(200);

  expect(response.body.newField).toBe('value');
});
```

Run it to confirm it fails. This is your baseline.

---

## Step 2: Trace the Data Flow

Map the full path from request to database and back:

```
Request body
    ↓ validation middleware (Zod schema)
    ↓ route handler
    ↓ service layer
    ↓ database (ORM)
    ↓ return value
    ↓ response serialisation
Response body
```

At each step, check if the field exists.

### Add temporary logging

```typescript
// In the route handler
console.log('Request body:', JSON.stringify(req.body));
console.log('After validation:', JSON.stringify(req.validatedBody)); // if middleware adds this
console.log('Service input:', JSON.stringify(serviceInput));
console.log('DB result:', JSON.stringify(dbResult));
console.log('Response:', JSON.stringify(response));
```

Identify the exact step where the field disappears.

---

## Step 3: Find All Schemas for This Route

The same endpoint may have validation at multiple layers:

```bash
# Find Zod schemas for this route/resource
grep -r "z\.object" --include="*.ts" -l | xargs grep -l "resourceName\|routeName"

# Find middleware applied to this route
grep -r "validate\|schema\|middleware" path/to/router.ts

# Find DTO types
grep -r "interface.*DTO\|type.*DTO\|ResourceDTO" --include="*.ts" -l
```

Check every schema in the chain:

```typescript
// Common pattern: middleware applies schema before route handler
app.post('/api/resource',
  validate(resourceSchema),  // ← this schema may strip fields
  resourceController.create
);
```

---

## Step 4: Check the Schema Definition

Open the schema file and look for missing fields:

```typescript
// ❌ Schema missing newField — middleware strips it
const resourceSchema = z.object({
  name: z.string(),
  // newField is not here
});

// ✅ Add the field
const resourceSchema = z.object({
  name: z.string(),
  newField: z.string().optional(),
});
```

**Also check:**

```typescript
// strict() rejects unknown fields with an error
const schema = z.object({ name: z.string() }).strict();

// passthrough() forwards unknown fields without stripping
const schema = z.object({ name: z.string() }).passthrough();

// Default (no modifier): strips unknown fields silently ← most common culprit
const schema = z.object({ name: z.string() });
```

---

## Step 5: Check the Return Path

The field may be saved correctly but stripped on the way back:

```bash
# Check DTO type (response shape)
grep -r "ResourceDTO\|ResponseDTO" --include="*.ts" src/

# Check if the controller maps the DB result to a DTO
grep -r "toDTO\|mapToDTO\|mapResponse" --include="*.ts" src/
```

If a mapper function creates the response object manually:

```typescript
// ❌ Mapper missing newField
function toDTO(resource: Resource): ResourceDTO {
  return {
    id: resource.id,
    name: resource.name,
    // newField not mapped
  };
}

// ✅ Add newField to mapper
function toDTO(resource: Resource): ResourceDTO {
  return {
    id: resource.id,
    name: resource.name,
    newField: resource.newField,
  };
}
```

---

## Step 6: Check the ORM Select/Include

If using Prisma or similar ORMs, verify the field is selected:

```typescript
// ❌ Field not included in select
const resource = await prisma.resource.findUnique({
  where: { id },
  select: {
    id: true,
    name: true,
    // newField not selected
  }
});

// ✅ Add to select
const resource = await prisma.resource.findUnique({
  where: { id },
  select: {
    id: true,
    name: true,
    newField: true,
  }
});

// Or omit select entirely to get all fields
const resource = await prisma.resource.findUnique({
  where: { id },
});
```

---

## Step 7: Check the Database Migration

If the field was recently added:

```bash
# Check migration history
ls -la prisma/migrations/ | tail -10

# Verify the column exists
npx prisma db pull  # syncs schema from DB

# Or check directly
psql $DATABASE_URL -c "\d resource_table"
```

If the migration was not run:

```bash
npx prisma migrate dev  # development
npx prisma migrate deploy  # production
```

---

## Step 8: Check TypeScript Types

Ensure the TypeScript interface includes the field:

```typescript
// ❌ Interface missing newField
interface Resource {
  id: string;
  name: string;
}

// ✅ Add newField
interface Resource {
  id: string;
  name: string;
  newField?: string;
}
```

Run type checks to catch cascading type errors:

```bash
npx tsc --noEmit 2>&1 | grep "newField\|resourceFile.ts"
```

---

## Checklist for a Complete Fix

When adding a new field end-to-end:

- [ ] Database migration (if new column)
- [ ] ORM schema / model updated
- [ ] Validation schema updated (request body)
- [ ] TypeScript interface/type updated
- [ ] ORM query includes field in select (if using explicit select)
- [ ] Mapper/DTO includes field in response
- [ ] Response TypeScript type includes field
- [ ] Tests cover the full round-trip (sent → persisted → returned)

---

## Common Patterns

### Pattern 1: Zod middleware strips on input

**Symptom:** Field in request body, `undefined` in handler.
**Fix:** Add field to Zod schema for the route.

### Pattern 2: Mapper omits on output

**Symptom:** Field in database, missing from API response.
**Fix:** Add field to DTO mapper function.

### Pattern 3: Prisma select omits field

**Symptom:** Field in database, `undefined` in service return value.
**Fix:** Add field to Prisma `select`, or remove explicit select to get all fields.

### Pattern 4: Migration not run

**Symptom:** Field in schema.prisma, `column does not exist` database error.
**Fix:** Run `prisma migrate deploy`.

### Pattern 5: TypeScript type mismatch

**Symptom:** Type error cascades from one missing field.
**Fix:** Update interface, then fix all downstream usages.
