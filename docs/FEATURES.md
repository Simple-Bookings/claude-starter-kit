# Features & Acceptance Criteria

**Last updated:** [YYYY-MM-DD]
**Maintained by:** [Team/owner]

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Implemented and tested |
| ⏳ | Partially implemented or tested |
| ❌ | Not implemented / missing test |
| — | Not applicable |

**AC table columns:**
- **E2E** — is this acceptance criterion covered by an E2E test?
- **Unit** — is it covered by a unit/integration test?
- **Issue** — GitHub issue number if test is missing or there's a known bug

---

## UC001: [User can do something]

**Description:** [What this use case is about — one flow from the user's perspective]
**Mission context:** *[How this connects to the product's mission]*

| AC | Criterion | E2E | Unit | Issue |
|----|-----------|-----|------|-------|
| AC001 | [Specific, testable criterion — e.g., "User sees confirmation after action"] | ✅ | — | - |
| AC002 | [Specific, testable criterion] | ✅ | ✅ | - |
| AC003 | [Error scenario — e.g., "Invalid input shows error message"] | ❌ | — | #123 |

**E2E:** `e2e/[feature].spec.ts`
**Unit:** `src/[feature]/[feature].test.ts`

---

## UC002: [User can do something else]

**Description:** [Description]
**Mission context:** *[Mission context]*

| AC | Criterion | E2E | Unit | Issue |
|----|-----------|-----|------|-------|
| AC004 | [Criterion] | ✅ | ✅ | - |
| AC005 | [Criterion] | ❌ | ❌ | - |

**E2E:** `e2e/[feature].spec.ts`

---

## UC003: [Add new use case here]

**Description:** [Description]
**Mission context:** *[Mission context]*

| AC | Criterion | E2E | Unit | Issue |
|----|-----------|-----|------|-------|
| AC006 | [Criterion] | ❌ | ❌ | - |

---

## Writing Good Acceptance Criteria

Each AC must be:
- **Specific** — No ambiguity
- **Measurable** — Can verify pass/fail
- **Testable** — Can write a test for it

### Examples

| ❌ Bad | ✅ Good |
|--------|---------|
| "Page should load fast" | "Page loads in <2s on 3G" |
| "User can login" | "User can login with email + password" |
| "Handle errors" | "Show error toast when API returns 4xx" |
| "Works on mobile" | "Layout responsive at 320px-768px widths" |

---

## Coverage Summary

Update regularly as tests are added.

| UC Group | Use Cases | E2E Coverage | Unit Coverage |
|----------|-----------|--------------|---------------|
| [Core flow] | UC001–UC005 | ~80% | ~60% |
| [Auth] | UC006–UC008 | ~50% | ~90% |
| [Admin] | UC009–UC015 | ~30% | ~70% |
| **Total** | | **~55%** | **~70%** |

**Goal:** E2E coverage > 60% on implemented use cases.

---

## Adding a New Use Case

1. Copy the UC template above
2. Number it sequentially (UC004, UC005, ...)
3. Write 2-5 specific acceptance criteria
4. Mark initial test coverage status
5. Link to relevant E2E and unit test files
6. Update the coverage summary table
