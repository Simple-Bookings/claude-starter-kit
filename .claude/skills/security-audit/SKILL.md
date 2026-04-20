---
name: security-audit
description: Security audit workflow — OWASP Top 10 review, dependency vulnerabilities, auth/authorization boundaries, JWT configuration, and IDOR risk detection. Produces a findings report with severity and fix guidance.
allowed-tools: Bash, Read, Grep, Glob, Agent
---

# /security-audit — Security Audit

Systematic security review covering OWASP Top 10, dependency vulnerabilities, and authentication/authorization boundaries.

---

## Step 1: Dependency Vulnerabilities

```bash
# Check for known vulnerabilities in dependencies
npm audit --production

# Focus on high and critical
npm audit --production --audit-level=high

# Check for outdated packages with known CVEs
npm outdated
```

For each `high` or `critical` finding:
- Is it exploitable in this application's usage?
- Is a patch available?
- Document findings with severity and patch path.

---

## Step 2: OWASP Top 10 Review

### A01 — Broken Access Control

```bash
# Find all route definitions
grep -r "app\.\(get\|post\|put\|patch\|delete\)" --include="*.ts" -n src/

# Find authorization middleware usage
grep -r "requireAuth\|isAuthenticated\|checkPermission\|authorize" --include="*.ts" -l src/

# Find routes WITHOUT auth middleware
grep -r "router\.\(get\|post\|put\|delete\)" --include="*.ts" -n src/routes/
```

For each unprotected route, verify it should be public. Look for IDOR risks:

```bash
# Find direct object lookups by user-supplied ID
grep -r "findUnique\|findById\|findOne" --include="*.ts" -n src/ | grep "req\.params\|req\.body\|req\.query"
```

**IDOR check:** Does the query also filter by `userId` or `ownerId`? A lookup like `findById(req.params.id)` without an ownership check lets any authenticated user access any resource.

### A02 — Cryptographic Failures

```bash
# Find hardcoded secrets
grep -r "password\|secret\|apiKey\|token" --include="*.ts" -n src/ | grep -v "process\.env\|getenv\|config\."

# Find MD5 or SHA1 usage (weak hashing)
grep -r "md5\|sha1\b" --include="*.ts" -n src/

# Check JWT configuration
grep -r "jwt\.sign\|jsonwebtoken" --include="*.ts" -n src/
```

JWT checklist:
- [ ] Secret loaded from environment variable, not hardcoded
- [ ] Algorithm explicitly set (not default — default `HS256` is OK, but should be explicit)
- [ ] Expiry set (`expiresIn`)
- [ ] Audience/issuer validated if tokens cross service boundaries

### A03 — Injection

```bash
# Find raw SQL queries (potential SQL injection)
grep -r "\.query\(\|\.raw\(\|\.execute\(" --include="*.ts" -n src/

# Check if user input is interpolated into queries
grep -r "req\.body\|req\.params\|req\.query" --include="*.ts" -n src/ | grep "query\|sql\|exec"
```

For each raw query, verify that user input is parameterized, not interpolated.

### A04 — Insecure Design

Review authentication flows:
- Is email verification required before account activation?
- Are rate limits applied to login/signup endpoints?
- Are password reset tokens time-limited and single-use?

```bash
grep -r "resetPassword\|forgotPassword\|verifyEmail" --include="*.ts" -l src/
```

### A05 — Security Misconfiguration

```bash
# Check CORS configuration
grep -r "cors\|Access-Control" --include="*.ts" -n src/

# Check security headers
grep -r "helmet\|X-Frame-Options\|Content-Security-Policy" --include="*.ts" -n src/

# Check for debug mode / stack traces in production
grep -r "NODE_ENV\|process\.env\.DEBUG" --include="*.ts" -n src/ | grep "error\|stack\|debug"
```

### A07 — Authentication Failures

```bash
# Find login rate limiting
grep -r "rateLimit\|rate-limit\|express-rate-limit" --include="*.ts" -l src/

# Find token validation
grep -r "jwt\.verify\|verifyToken" --include="*.ts" -n src/
```

Token validation checklist:
- [ ] Token expiry checked
- [ ] Token signature verified with correct secret
- [ ] Invalid tokens return 401 (not 500)
- [ ] Refresh token rotation implemented

### A09 — Security Logging and Monitoring

```bash
# Check audit logging for sensitive operations
grep -r "auditLog\|audit_log\|securityLog" --include="*.ts" -l src/

# Check if failed auth attempts are logged
grep -r "401\|403\|Unauthorized\|Forbidden" --include="*.ts" -n src/
```

---

## Step 3: Authentication Boundary Review

Map the full auth flow:

```bash
# Find all places tokens are issued
grep -r "jwt\.sign\|generateToken\|issueToken" --include="*.ts" -n src/

# Find all places tokens are consumed
grep -r "jwt\.verify\|validateToken\|req\.user" --include="*.ts" -n src/

# Find public endpoints (no auth required)
grep -r "router\." --include="*.ts" -n src/routes/ | grep -v "auth\|middleware"
```

For each endpoint, classify:
- Public (no auth required) — intentional?
- Authenticated (any valid user)
- Authorized (specific role or ownership required)

---

## Step 4: Data Exposure

```bash
# Find API responses that may include sensitive fields
grep -r "res\.json\|res\.send" --include="*.ts" -n src/ | grep "password\|hash\|secret\|token"

# Find user lookups that might return sensitive fields
grep -r "findUnique\|findMany" --include="*.ts" -n src/ | grep -i "user"
```

Verify that password hashes, internal tokens, and sensitive fields are never included in API responses.

---

## Step 5: Input Validation Coverage

```bash
# Find unvalidated request body usage
grep -r "req\.body\." --include="*.ts" -n src/ | grep -v "validate\|schema\|zod"

# Find Zod schemas
grep -r "z\.object\|z\.string\|z\.number" --include="*.ts" -l src/
```

Every endpoint that accepts user input should validate it with a schema before use.

---

## Findings Report

Document findings in this format:

```markdown
## Security Audit — [Date]

### Critical
- [ ] **[CVE-XXXX / OWASP A0X]** — Description
  - **File:** path/to/file.ts:42
  - **Risk:** What an attacker can do
  - **Fix:** Specific remediation

### High
- [ ] **[Issue]** — Description
  - **File:** path/to/file.ts:87
  - **Risk:** ...
  - **Fix:** ...

### Medium
...

### Informational
...
```

---

## Fixing Findings

For each finding:
1. Create a GitHub issue with label `security` and appropriate priority (`P0-critical`, `P1-high`)
2. Fix in a dedicated branch — do not bundle security fixes with feature work
3. Add a test that would have caught the vulnerability
4. Verify the fix does not break existing tests

```bash
gh issue create \
  --title "security: [brief description]" \
  --label "security,P1-high" \
  --body "## Vulnerability

**Type:** [OWASP category]
**Severity:** High
**File:** path/to/file.ts:42

## Description

[What the vulnerability is]

## Risk

[What an attacker can do]

## Fix

[Specific remediation steps]

## Evidence

[How to reproduce / verify]"
```

---

## Rules

- **Document everything** — a finding with no evidence is a guess
- **Severity based on exploitability** — not theoretical risk
- **Fix in isolation** — security PRs should not include feature changes
- **Add regression tests** — every fix should have a test that fails without the fix
- **Never remove auth checks** without understanding why they exist
