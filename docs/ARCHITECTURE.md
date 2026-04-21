# Design Decisions

**Sidst opdateret:** [YYYY-MM-DD]
**Vedligeholdt af:** [Team/ansvarlig]
**Relateret:** [SYSTEM.md](SYSTEM.md) (systemdokumentation), [API.md](API.md) (endpoint-reference)

Dokumenterer de vigtigste arkitekturbeslutninger med rationale. Reference dette dokument når du implementerer nye features for at holde konsistens.

---

## Arkitektur

### Repo-struktur

```text
[projekt]/
├── src/          # Frontend
├── server/       # Backend
└── docs/         # Dokumentation
```

**Beslutning:** [Monorepo / polyrepo / andet]

**Rationale:** [Hvorfor denne struktur — hvad forenkler den, hvad giver den op?]

### Tech Stack

| Lag | Teknologi | Rationale |
|-----|-----------|-----------|
| Frontend | [fx React 18 + TypeScript] | [Kort begrundelse] |
| UI | [fx shadcn/ui + Tailwind] | [Kort begrundelse] |
| State | [fx Zustand + React Query] | [Kort begrundelse] |
| Backend | [fx Express + TypeScript] | [Kort begrundelse] |
| Database | [fx PostgreSQL + Prisma] | [Kort begrundelse] |
| Auth | [fx JWT + OAuth2] | [Kort begrundelse] |
| Infrastruktur | [fx Docker + VPS] | [Kort begrundelse] |

---

## Datamodel

### Overordnet struktur

```text
[Model A] ──< [Junction] >── [Model B]
                                │
                                ├── [Model C]
                                └── [Model D]
```

**Beslutning:** [Beskriv den overordnede struktur]

**Rationale:** [Hvorfor denne struktur]

### Vigtige modelvalg

**[Valg 1: fx Soft delete frem for hard delete]**

Beslutning: [Hvad blev valgt]

Rationale:
- [Årsag 1]
- [Årsag 2]

**[Valg 2: fx Denormalisering af bestemte felter]**

Beslutning: [Hvad blev valgt]

Rationale:
- [Årsag 1 — fx historisk nøjagtighed]
- [Årsag 2 — fx query performance]

---

## API Design

### Konventioner

```text
GET    /api/[ressource]          → liste
GET    /api/[ressource]/:id      → enkelt
POST   /api/[ressource]          → opret
PATCH  /api/[ressource]/:id      → opdatér
DELETE /api/[ressource]/:id      → slet
```

**Beslutning:** REST over JSON. Alle endpoints under `/api/`.

**Rationale:** [Hvorfor REST frem for GraphQL / gRPC / etc.]

### Fejlformat

```json
{ "error": "Beskrivelse", "code": "ERROR_CODE" }
```

**Beslutning:** Konsistent fejlformat med menneskelig besked og maskinlæsbar kode.

**Rationale:** Frontend kan vise brugervenlig tekst og logge koden til fejlfinding.

---

## Autentificering

**Beslutning:** [JWT / session / OAuth2 / magic link — beskriv hvad I bruger]

**Rationale:** [Hvorfor dette valg]

```text
Client                    Server
  │─── POST /auth/login ─►│── Validér credentials
  │                        │── Udsted JWT (kort levetid)
  │◄── { token } ──────────│
  │                        │
  │─── GET /api/ressource ►│── Validér JWT
  │    Authorization: Bearer│
  │◄── { data } ───────────│
```

**Token-strategi:**
- Access token: [fx 15 min]
- Refresh token: [fx 7 dage]
- Rotation: [fx ja/nej]

---

## Multi-tenancy (hvis relevant)

**Beslutning:** [Single-tenant / multi-tenant / hybrid]

**Rationale:** [Hvorfor]

**Data-isolation-strategi:** [Row-level security / separate schemas / separate databases]

---

## Kendte tekniske kompromisser

Ting vi ved er suboptimale, men har valgt bevidst:

| Kompromis | Årsag | Fremtidig løsning |
|-----------|-------|-------------------|
| [fx Manglende indeksering på X] | [fx Tidspres ved MVP] | [fx Tilføj index når query-analyse viser behov] |
| [fx Duplikeret logik i A og B] | [fx Opstod organisk] | [fx Refaktorer til delt service] |
