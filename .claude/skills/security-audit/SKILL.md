# /security-audit — Security Audit

Systematic security review covering OWASP Top 10, dependency vulnerabilities, and authentication/authorization boundaries.

---

## Overview

This skill guides you through a comprehensive security audit. Run it:
- Before releasing to production
- After major feature additions
- When adding new dependencies
- Periodically (monthly or quarterly)

---

## Step 1: Dependency Vulnerabilities

```bash
# Check for known vulnerabilities
npm audit --production
# or
pip-audit
# or
cargo audit

# Focus on high and critical
npm audit --production --audit-level=high
```

For each `high` or `critical` finding:
- Is it exploitable in this application's usage?
- Is a patch available?
- Document findings with severity and patch path

---

## Step 2: OWASP Top 10 Review

### A01 — Broken Access Control

```bash
# Find all route definitions
grep -r "app\.\(get\|post\|put\|patch\|delete\)" --include="*.ts" --include="*.js" -n src/

# Find authorization middleware usage
grep -r "requireAuth\|isAuthenticated\|checkPermission" --include="*.ts" -l src/

# Find routes WITHOUT auth middleware
grep -r "router\.\(get\|post\|put\|delete\)" --include="*.ts" -n src/routes/
```

For each unprotected route, verify it should be public.

**IDOR Check:**
```bash
# Find direct object lookups by user-supplied ID
grep -r "findById\|findOne\|findUnique" --include="*.ts" -n src/
```

Does the query also filter by `userId` or `ownerId`? A lookup like `findById(req.params.id)` without an ownership check lets any user access any resource.

### A02 — Cryptographic Failures

```bash
# Find hardcoded secrets
grep -r "password\|secret\|apiKey\|token" --include="*.ts" -n src/ | grep -v "process\.env"

# Find weak hashing (MD5, SHA1)
grep -r "md5\|sha1\b" --include="*.ts" -n src/

# Check JWT configuration
grep -r "jwt\.sign\|jsonwebtoken" --include="*.ts" -n src/
```

**JWT Checklist:**
- [ ] Secret loaded from environment variable
- [ ] Algorithm explicitly set (not default)
- [ ] Expiry set (`expiresIn`)
- [ ] Audience/issuer validated if tokens cross services

### A03 — Injection

```bash
# Find raw SQL queries
grep -r "\.query\(\|\.raw\(\|\.execute\(" --include="*.ts" -n src/

# Check if user input is interpolated
grep -r "req\.body\|req\.params\|req\.query" --include="*.ts" -n src/ | grep "query\|sql"
```

For each raw query, verify user input is parameterized, not interpolated.

### A04 — Insecure Design

Review authentication flows:
- Is email verification required before account activation?
- Are rate limits applied to login/signup?
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

# Check for debug mode / stack traces
grep -r "NODE_ENV\|DEBUG" --include="*.ts" -n src/
```

### A07 — Authentication Failures

```bash
# Find login rate limiting
grep -r "rateLimit\|rate-limit" --include="*.ts" -l src/

# Find token validation
grep -r "jwt\.verify\|verifyToken" --include="*.ts" -n src/
```

**Token Validation Checklist:**
- [ ] Token expiry checked
- [ ] Token signature verified with correct secret
- [ ] Invalid tokens return 401 (not 500)
- [ ] Refresh token rotation implemented

### A09 — Security Logging and Monitoring

```bash
# Check audit logging
grep -r "auditLog\|audit_log\|securityLog" --include="*.ts" -l src/

# Check if failed auth attempts are logged
grep -r "401\|403\|Unauthorized" --include="*.ts" -n src/
```

---

## Step 3: Authentication Boundary Review

Map the full auth flow:

```bash
# Find all places tokens are issued
grep -r "jwt\.sign\|generateToken" --include="*.ts" -n src/

# Find all places tokens are consumed
grep -r "jwt\.verify\|validateToken\|req\.user" --include="*.ts" -n src/

# Find public endpoints
grep -r "router\." --include="*.ts" -n src/routes/ | grep -v "auth\|middleware"
```

For each endpoint, classify:
- **Public** — no auth required (intentional?)
- **Authenticated** — any valid user
- **Authorized** — specific role or ownership required

---

## Step 4: Data Exposure

```bash
# Find API responses with sensitive fields
grep -r "res\.json\|res\.send" --include="*.ts" -n src/ | grep "password\|hash\|secret\|token"

# Find user lookups that might return sensitive fields
grep -r "findUnique\|findMany" --include="*.ts" -n src/ | grep -i "user"
```

Verify password hashes, tokens, and sensitive fields are never included in API responses.

---

## Step 5: Input Validation Coverage

```bash
# Find unvalidated request body usage
grep -r "req\.body\." --include="*.ts" -n src/ | grep -v "validate\|schema\|zod"

# Find validation schemas
grep -r "z\.object\|z\.string\|Joi\.\|yup\." --include="*.ts" -l src/
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

1. Create a GitHub issue with label `security` and appropriate priority
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

[Specific remediation steps]"
```

---

## Rules

- **Document everything** — a finding with no evidence is a guess
- **Severity based on exploitability** — not theoretical risk
- **Fix in isolation** — security PRs should not include feature changes
- **Add regression tests** — every fix should have a test that fails without the fix
- **Never remove auth checks** without understanding why they exist
