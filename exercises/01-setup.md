# Exercise 01: Setup & First Conversation

**Goal:** Verify environment and experience Claude Code's capabilities.

**Skills:** `/onboarding`

**Time:** 15 minutes

---

## What You'll Learn

- Verifying your Claude Code installation
- The difference between commands and conversations
- How Claude reads and understands your project

## Step 1: Verify Environment

```bash
csk doctor
```

All checks should show ✓. Issues? Raise your hand.

## Step 2: Create Your Workshop Project

```bash
csk init workshop-project
cd workshop-project
git init
```

This creates a project with CLAUDE.md, skills, and rules pre-configured.

## Step 3: Start Claude Code

```bash
claude
```

You're now in a conversation with Claude. Run the onboarding:

```
/onboarding
```

Claude will verify your setup and explain what's available.

## Step 4: Explore the Project

Ask Claude:

```
What files are in this project? Explain each one briefly.
```

Notice: Claude reads the files, understands their purpose, and explains them to you. You didn't need to `cat` anything.

## Step 5: The Key Insight

**You describe intent. Claude handles execution.**

Instead of:
```bash
ls -la
cat CLAUDE.md
grep -r "TODO" .
```

You say:
```
Show me the project structure, explain CLAUDE.md, and find any TODOs.
```

Claude runs the commands, synthesizes the results, and reports back.

## Step 6: Try Something Real

```
Add a simple "Hello World" TypeScript function in src/hello.ts with a test.
```

Watch Claude:
1. Create the directory structure
2. Write the function
3. Write the test
4. Run the test

**You didn't write any code.** You described what you wanted.

## Verification

- [ ] `csk doctor` all green
- [ ] Project created with CLAUDE.md
- [ ] `/onboarding` completed
- [ ] Claude created hello.ts and test

## Key Takeaway

Claude Code is not an autocomplete. It's a developer that reads, writes, and executes code based on your descriptions.

## Next

[Exercise 02: Git Workflow](02-git-workflow.md)
