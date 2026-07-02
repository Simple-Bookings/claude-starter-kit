# Security Best Practices

Common security patterns to follow when building applications.

---

## Authentication & Authorization

### Never trust client-side data

```typescript
// ❌ WRONG — Anyone can access data by knowing an email
await page.goto('/profile?email=victim@example.com');

// ✅ CORRECT — Require authentication
const user = await requireAuth(request);
const profile = await getProfile(user.id);
```

### Use time-limited tokens

```typescript
// ❌ WRONG — Token never expires
const token = jwt.sign({ userId }, secret);

// ✅ CORRECT — Token expires in 15 minutes
const token = jwt.sign({ userId }, secret, { expiresIn: '15m' });
```

### Verify ownership before access

```typescript
// ❌ WRONG — No ownership check
app.get('/api/orders/:id', async (req, res) => {
  const order = await db.orders.findById(req.params.id);
  res.json(order);
});

// ✅ CORRECT — Verify user owns the resource
app.get('/api/orders/:id', async (req, res) => {
  const order = await db.orders.findById(req.params.id);
  if (order.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  res.json(order);
});
```

---

## Input Validation

### Validate all user input

```typescript
// ❌ WRONG — No validation
const { email, password } = req.body;
await createUser(email, password);

// ✅ CORRECT — Validate with schema
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});
const { email, password } = schema.parse(req.body);
await createUser(email, password);
```

### Sanitize for SQL injection

```typescript
// ❌ WRONG — SQL injection vulnerable
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ CORRECT — Parameterized query
db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### Prevent XSS attacks

```typescript
// ❌ WRONG — XSS vulnerable (never set innerHTML with user input)
// element.innerHTML = userInput;  // DO NOT DO THIS

// ✅ CORRECT — Use textContent for plain text
element.textContent = userInput;

// ✅ CORRECT — Use sanitization library for HTML (e.g., DOMPurify)
element.innerHTML = DOMPurify.sanitize(userInput);
```

---

## Secrets Management

### Never commit secrets

```bash
# .gitignore
.env
.env.local
*.pem
*_secret*
```

### Use environment variables

```typescript
// ❌ WRONG — Hardcoded secret
const API_KEY = 'sk-1234567890';

// ✅ CORRECT — Environment variable
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error('API_KEY required');
```

---

## Rate Limiting

### Protect sensitive endpoints

```typescript
// ✅ CORRECT — Rate limit login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: 'Too many login attempts',
});

app.post('/api/login', loginLimiter, loginHandler);
```

---

## HTTPS & Transport Security

### Always use HTTPS in production

```typescript
// Redirect HTTP to HTTPS
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
      return res.redirect(`https://${req.headers.host}${req.url}`);
    }
    next();
  });
}
```

### Set security headers

```typescript
app.use(helmet()); // Sets various security headers
```

---

## Audit Logging

### Log security-relevant events

```typescript
// Log authentication attempts
logger.info('Login attempt', {
  email: user.email,
  success: true,
  ip: req.ip,
  timestamp: new Date().toISOString(),
});

// Log authorization failures
logger.warn('Access denied', {
  userId: user.id,
  resource: req.path,
  reason: 'insufficient permissions',
});
```

---

## Quick Checklist

Before deploying, verify:

- [ ] All endpoints require authentication (unless public)
- [ ] User input is validated and sanitized
- [ ] SQL queries use parameterized statements
- [ ] Secrets are in environment variables, not code
- [ ] HTTPS is enforced in production
- [ ] Rate limiting on login and signup
- [ ] Security headers are set (CSP, HSTS, etc.)
- [ ] Audit logging for auth events
