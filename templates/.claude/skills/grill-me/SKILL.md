# /grill-me — Concept Clarification

Ask Socratic questions until the idea is crystal clear.

## When to use

Before writing any code, when requirements are vague or incomplete.

## The process

Ask probing questions across these dimensions:

### 1. Who (Users)
- Who is the primary user?
- Are there secondary users?
- What's their technical level?

### 2. What (Scope)
- What exactly should this do?
- What should it NOT do?
- What's the MVP vs nice-to-have?

### 3. Where (Context)
- Where does this fit in the system?
- What integrations are needed?
- What constraints exist?

### 4. When (Timing)
- When is this needed?
- What's the deadline?
- What are the milestones?

### 5. How (Implementation)
- Any technical constraints?
- Preferred approaches?
- Performance requirements?

## Rules

- Ask ONE question at a time
- Wait for answer before next question
- Stop when you can write acceptance criteria
- Don't write code — only clarify

## Output

Clear, testable acceptance criteria that can be used for planning.

## Example

```
User: I want to add a timer feature

/grill-me

Claude: I'll ask some clarifying questions. First:
What should the timer track — elapsed time, countdown, or both?

User: Elapsed time for tasks

Claude: Got it. Should users be able to run multiple timers 
simultaneously, or only one at a time?
...
```
