# /mockup-to-story — Convert Wireframes to User Stories

Transform ASCII mockups into structured user stories with acceptance criteria.

## When to use

When you have a wireframe or mockup and need to create actionable user stories.

## Input format

A Mermaid block diagram (preferred) or ASCII wireframe:

```mermaid
block-beta
    columns 1
    block:header["Login"]
    end
    block:form["Form"]
        columns 2
        email["Email:"] input1["[____________]"]
        pass["Password:"] input2["[____________]"]
    end
    block:actions
        columns 1
        login["[ Login ]"]
        forgot["Forgot password?"]
    end
```

Or ASCII fallback for terminals:

```
┌─────────────────────────────┐
│ Login                       │
├─────────────────────────────┤
│ Email:    [____________]    │
│ Password: [____________]    │
│      [  Login  ]            │
│ Forgot password?            │
└─────────────────────────────┘
```

## Process

1. **Identify elements** — List all UI components
2. **Map interactions** — What can users click/type/do?
3. **Define flows** — Happy path and error paths
4. **Write stories** — One per distinct user goal

## Output format

```markdown
### US-001: User Login

**As a** registered user
**I want to** log in with my credentials
**So that** I can access my account

#### Acceptance Criteria

- [ ] AC1: Email field accepts valid email format
- [ ] AC2: Password field masks input
- [ ] AC3: Login button validates both fields
- [ ] AC4: Show error message for invalid credentials
- [ ] AC5: Redirect to dashboard on success
```

## Rules

- One user story per distinct user goal
- Every interactive element needs acceptance criteria
- Include error states, not just happy paths
- Keep stories small and focused
