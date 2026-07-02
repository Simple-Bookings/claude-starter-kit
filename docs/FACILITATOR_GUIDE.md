# CSK2 Workshop Facilitator Guide

Quick reference for running a CSK2 workshop.

---

## Pre-Workshop Checklist

- [ ] Test `csk doctor` on presenter machine
- [ ] Verify workshop server: `csk workshop`
- [ ] Check projector/screen share works with slides
- [ ] Have backup of exercises in case of connectivity issues
- [ ] Confirm attendees have Claude Code installed

---

## Workshop Timeline (3 hours)

| Time | Duration | Activity | Materials |
|------|----------|----------|-----------|
| 0:00 | 15 min | **Welcome & Setup** | Slides 1-3 |
| 0:15 | 20 min | **Work-Loop Overview** | Slides 4-8, kompendium §4-7 |
| 0:35 | 10 min | **Exercise 01: Setup** | exercises/01-setup.md |
| 0:45 | 15 min | **Exercise 02: Git Workflow** | exercises/02-git-workflow.md |
| 1:00 | 10 min | **Break** | — |
| 1:10 | 30 min | **Exercise 03: TDD** | exercises/03-tdd.md |
| 1:40 | 20 min | **Exercise 04: Code Review** | exercises/04-code-review.md |
| 2:00 | 10 min | **Break** | — |
| 2:10 | 20 min | **Exercise 05: Debugging** | exercises/05-debugging.md |
| 2:30 | 25 min | **Exercise 06: Full Cycle** | exercises/06-full-cycle.md |
| 2:55 | 5 min | **Wrap-up & Q&A** | Slides 23-24 |

---

## Presenter Mode Setup

1. Open kompendium: `csk workshop` → http://localhost:9123/kompendium.html
2. Click "Open Slides" button → slides open in new window
3. Move slides window to projector/shared screen
4. Press `F` in slides window for fullscreen
5. Control slides from kompendium with `Alt+←` / `Alt+→`

**Keyboard shortcuts:**
- `←` `→` — Navigate slides
- `F` — Toggle fullscreen (slides window)
- `Alt+←` `Alt+→` — Control slides from kompendium
- `T` — Toggle dark/light mode

---

## Common Questions

### "Where do I get Claude Code?"

```bash
# Mac
brew install claude-code

# Or via npm
npm install -g @anthropic-ai/claude-code
```

### "What if I don't have a Claude API key?"

Claude Code uses your Anthropic account. Sign up at claude.ai if needed.

### "Can I use this with my existing project?"

Yes! Use `/adopt` skill or `csk init .` in an existing directory.

### "Does this work with [language X]?"

CSK2 is stack-agnostic. The workflows work with any language.

---

## Troubleshooting

### Exercises server won't start

```bash
# Check if port is in use
lsof -i :9123

# Use different port
csk exercises --port 9124
```

### Claude Code not found

```bash
# Verify installation
which claude
claude --version

# Reinstall if needed
npm install -g @anthropic-ai/claude-code
```

### Skills not loading

Claude reads skills on session start. After adding skills:

```bash
exit  # Exit Claude
claude  # Restart
```

---

## Post-Workshop

- Share handout.html (print or PDF)
- Point to https://github.com/Simple-Bookings/claude-starter-kit
- Encourage `/adopt` for existing projects
