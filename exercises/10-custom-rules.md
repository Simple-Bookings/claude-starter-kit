# Exercise 10: Custom Rules (Bonus)

**Goal:** Create path-activated rules for your team.

**Skills:** Rules system, glob patterns

**Time:** 15 minutes

---

## What You'll Learn

- Global vs path-activated rules
- When Claude loads which rules
- Writing effective rules

## Rules vs Skills

```
Aspect    Rules                            Skills
────────────────────────────────────────────────────────────────
When      Always loaded (or path-matched)  On demand (/command)
Purpose   "Always do X"                    "How to do Y"
Example   "Never use any"                  "/planning" workflow
```

## The Challenge

Create 3 rules:
1. Global coding standard
2. Test-specific rule (only for test files)
3. API-specific rule (only for API code)

## Step 1: Explore Existing Rules

```
List all files in .claude/rules/ and explain each one.
```

## Step 2: Create a Global Rule

```
Create .claude/rules/typescript-strict.md with these rules:
- Never use `any` type
- Always use explicit return types on functions
- Prefer `const` over `let`
- No console.log in production code
```

This loads for EVERY conversation.

## Step 3: Create a Path-Activated Rule

```
Create .claude/rules/testing-patterns.md with frontmatter:

---
path: **/*.test.ts
---

When writing tests:
- One assertion per test
- Use descriptive test names ("should X when Y")
- Always include negative test cases
- Mock external dependencies
```

This ONLY loads when working on test files.

## Step 4: Create an API Rule

```
Create .claude/rules/api-design.md with frontmatter:

---
path: src/api/**
---

API endpoints must:
- Validate all input with Zod
- Return consistent error format
- Include rate limiting headers
- Log request/response for debugging
```

## Step 5: Test Path Activation

Open a test file:
```
Read src/hello.test.ts
```

Ask Claude:
```
What rules are currently active?
```

Now open an API file:
```
Read src/api/users.ts
```

Ask again — different rules should be active!

## Rule Writing Tips

```
Good                        Bad
────────────────────────────────────────────────────────────────
"Use Zod for validation"    "Validate input" (vague)
"Never use any"             "Avoid bad patterns"
Include examples            Only describe don'ts
```

## Verification

- [ ] Created global rule (no frontmatter)
- [ ] Created path-activated rule (with frontmatter)
- [ ] Verified rules activate correctly
- [ ] Rules are specific and actionable

## Key Takeaway

**Rules are passive guardrails.** They shape Claude's behavior automatically without you remembering to mention them.

## Workshop Complete!

You've learned:
1. Claude Code as pair programmer
2. The 4-phase work-loop
3. TDD with Claude
4. Code review and integration
5. Handling Claude's mistakes
6. Guardrails and automation
7. Agent teams for parallel work
8. Custom rules for your team

**Next steps:**
1. Apply to a REAL project this week
2. Create 2-3 custom skills for your workflow
3. Share with your team
4. Practice daily — it becomes natural fast
