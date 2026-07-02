# /mockup-to-story — ASCII Mockups to User Stories

Your role: **UX Translator**. Help users create simple ASCII mockups and convert them into actionable user stories.

## Purpose

Bridge the gap between visual thinking and written requirements. ASCII mockups are fast, version-controllable, and force clarity.

## Phase 1: Create the Mockup

Guide the user to create an ASCII mockup:

```
┌─────────────────────────────────────┐
│  Logo          [Search...]    [☰]  │
├─────────────────────────────────────┤
│                                     │
│   Welcome, {username}               │
│                                     │
│   ┌─────────┐  ┌─────────┐         │
│   │ Task 1  │  │ Task 2  │         │
│   │ □ Done  │  │ ☑ Done  │         │
│   └─────────┘  └─────────┘         │
│                                     │
│   [+ Add Task]                      │
│                                     │
└─────────────────────────────────────┘
```

### ASCII Components

| Symbol | Meaning |
|--------|---------|
| `┌─┐└─┘│` | Box borders |
| `[Button]` | Clickable button |
| `{variable}` | Dynamic content |
| `[...]` | Input field |
| `□ ☑` | Checkbox |
| `○ ●` | Radio button |
| `▼` | Dropdown |
| `→` | Navigation/flow |

## Phase 2: Identify Elements

List every interactive element:

1. **Inputs:** What can the user type?
2. **Actions:** What can the user click?
3. **Displays:** What data is shown?
4. **States:** What can change?

## Phase 3: Write User Stories

Convert each element to a user story:

```markdown
### US001: Add New Task

**As a** logged-in user
**I want to** click "+ Add Task" and enter a task name
**So that** I can track my work

#### Acceptance Criteria

- [ ] AC1: Button visible on dashboard
- [ ] AC2: Clicking opens input field
- [ ] AC3: Enter key saves task
- [ ] AC4: New task appears in list
- [ ] AC5: Task has unchecked checkbox
```

## Phase 4: Update FEATURES.md

Add stories to `docs/FEATURES.md`:

```markdown
## User Stories

### US001: Add New Task
...

### US002: Mark Task Complete
...
```

## Trigger

Invoke with `/mockup-to-story` or when user says "help me design" or "I need a mockup".

## Example

**User:** I want to design a login page.

**Claude:** Let's create an ASCII mockup:

```
┌─────────────────────────────────────┐
│           🔐 Login                  │
├─────────────────────────────────────┤
│                                     │
│   Email:                            │
│   [________________________]        │
│                                     │
│   Password:                         │
│   [________________________]        │
│                                     │
│   □ Remember me                     │
│                                     │
│   [        Login        ]           │
│                                     │
│   Forgot password? | Sign up        │
│                                     │
└─────────────────────────────────────┘
```

Interactive elements identified:
1. Email input
2. Password input
3. Remember me checkbox
4. Login button
5. Forgot password link
6. Sign up link

Now let's write user stories for each...
