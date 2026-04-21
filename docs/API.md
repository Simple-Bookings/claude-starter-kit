# API-dokumentation

**Sidst opdateret:** [YYYY-MM-DD]
**Vedligeholdt af:** [Team/ansvarlig]
**Relateret:** [SYSTEM.md](SYSTEM.md) (systemdokumentation), [ARCHITECTURE.md](ARCHITECTURE.md) (designbeslutninger)

---

## 1. Konventioner

### Base URL

```
Production:  https://api.[dit-projekt].dk
Test:        https://test-api.[dit-projekt].dk
Dev:         http://localhost:3000
```

Alle endpoints er monteret under `/api/`.

### Autentificering

```
Authorization: Bearer <jwt-token>
```

Endpoints markeret **Auth: Ja** kræver gyldigt token. Uautoriserede kald returnerer `401`.

### Fejlformat

```json
{ "error": "Menneskelig beskrivelse", "code": "MACHINE_READABLE_CODE" }
```

### Datoer og tidszoner

- Alle datoer gemmes i **UTC** i databasen
- API returnerer datoer som **ISO 8601 strings** i UTC: `"2024-01-15T10:30:00Z"`
- Frontend konverterer til lokal tidszone ved visning

### Status-værdier

Alle status-værdier er **UPPERCASE**:

| Model | Værdier |
|-------|---------|
| **[Model]Status** | `PENDING`, `ACTIVE`, `CANCELLED`, `COMPLETED` |
| **UserRole** | `ADMIN`, `USER` |

### Paginering

```
GET /api/[ressource]?page=1&limit=20
```

```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "limit": 20
}
```

---

## 2. Endpoint-oversigt

### Autentificering (`/api/auth`)

| Metode | Sti | Auth | Beskrivelse |
|--------|-----|------|-------------|
| `POST` | `/auth/login` | Nej | Log ind med email og adgangskode |
| `POST` | `/auth/register` | Nej | Opret ny bruger |
| `POST` | `/auth/logout` | Ja | Log ud og invalider token |
| `POST` | `/auth/refresh` | Nej | Forny access token via refresh token |
| `GET` | `/auth/me` | Ja | Hent aktuel brugers information |

### [Ressource A] (`/api/[ressource]`)

| Metode | Sti | Auth | Beskrivelse |
|--------|-----|------|-------------|
| `GET` | `/[ressource]` | Ja | Hent liste — støtter `?page` og `?limit` |
| `GET` | `/[ressource]/:id` | Ja | Hent enkelt objekt |
| `POST` | `/[ressource]` | Ja | Opret nyt objekt |
| `PATCH` | `/[ressource]/:id` | Ja | Opdatér objekt (kun ejer) |
| `DELETE` | `/[ressource]/:id` | Ja | Slet objekt (kun ejer) |

### [Ressource B] (`/api/[ressource-b]`)

| Metode | Sti | Auth | Beskrivelse |
|--------|-----|------|-------------|
| `GET` | `/[ressource-b]` | Nej | [Offentlig endpoint] |
| `POST` | `/[ressource-b]` | Ja | [Beskrivelse] |

---

## 3. Request/Response-skemaer

### Auth — POST /auth/login

**Request:**
```json
{
  "email": "bruger@eksempel.dk",
  "password": "min8tegn"
}
```

**Response 200:**
```json
{
  "token": "eyJ...",
  "refreshToken": "eyJ...",
  "user": { "id": "uuid", "email": "bruger@eksempel.dk", "role": "USER" }
}
```

**Fejl:**
| HTTP | Code | Beskrivelse |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Manglende eller ugyldigt felt |
| 401 | `INVALID_CREDENTIALS` | Forkert email eller adgangskode |
| 429 | `RATE_LIMITED` | For mange forsøg — prøv igen om `retryAfter` sekunder |

---

### [Ressource A] — GET /api/[ressource]

**Response 200:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Navn",
      "status": "ACTIVE",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 20
}
```

---

### [Ressource A] — POST /api/[ressource]

**Request:**
```json
{
  "name": "Nyt objekt",
  "description": "Valgfri beskrivelse"
}
```

**Response 201:**
```json
{
  "id": "uuid",
  "name": "Nyt objekt",
  "status": "ACTIVE",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

**Fejl:**
| HTTP | Code | Beskrivelse |
|------|------|-------------|
| 400 | `VALIDATION_ERROR` | Manglende obligatorisk felt |
| 409 | `ALREADY_EXISTS` | Objekt med dette navn eksisterer allerede |

---

## 4. TypeScript-interfaces (DTO'er)

```typescript
// [Ressource]DTO — API response (datoer som strings)
interface [Ressource]DTO {
  id: string;
  name: string;
  status: 'PENDING' | 'ACTIVE' | 'CANCELLED' | 'COMPLETED';
  createdAt: string;   // ISO 8601
  updatedAt: string;   // ISO 8601
}

// [Ressource] — Frontend model (datoer som Date-objekter)
interface [Ressource] {
  id: string;
  name: string;
  status: ResourceStatus;
  createdAt: Date;
  updatedAt: Date;
}
```

---

## 5. Breaking changes

| Dato | Endpoint | Ændring | Migration |
|------|----------|---------|-----------|
| [YYYY-MM-DD] | [Endpoint] | [Hvad ændrede sig] | [Hvordan klienter opdaterer] |
