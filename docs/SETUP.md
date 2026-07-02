# CSK2 Setup Guide

Get Claude Starter Kit 2.0 running in under 10 minutes.

---

## Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| Python | 3.10+ | `python3 --version` |
| Git | 2.x | `git --version` |
| GitHub CLI | 2.x | `gh --version` |
| Claude Code | Latest | `claude --version` |

---

## Quick Start

### Option 1: Install from PyPI (recommended)

```bash
pip install git+https://github.com/Simple-Bookings/claude-starter-kit.git
csk doctor
```

### Option 2: Install from source

```bash
git clone https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit
pip install -e .
csk doctor
```

### Option 3: Use devcontainer

Open in VS Code with Dev Containers extension:

```bash
git clone https://github.com/Simple-Bookings/claude-starter-kit.git
code claude-starter-kit
# Click "Reopen in Container" when prompted
```

---

## Verify Installation

```bash
# Check all dependencies
csk doctor

# Expected output:
# ✓ Python 3.12.0
# ✓ Git 2.43.0
# ✓ GitHub CLI 2.40.0
# ✓ Claude Code 1.0.0
# ✓ All checks passed!
```

---

## Create Your First Project

```bash
# Initialize a new project with CSK2 structure
csk init my-project
cd my-project

# Or add CSK2 to existing project
cd existing-project
csk init .
```

This creates:

```
my-project/
├── .claude/
│   ├── skills/       # 15 workflow skills
│   ├── agents/       # 7 agent profiles
│   └── rules/        # Coding patterns
├── docs/
│   ├── VISION.md     # Project north star
│   └── FEATURES.md   # Feature tracking
├── CLAUDE.md         # Project instructions
└── README.md
```

---

## Start Using Claude

```bash
# Start Claude Code
claude

# Try a skill
/planning #1

# Check exercise progress
csk progress
```

---

## Workshop Mode

Serve workshop materials locally:

```bash
csk workshop
# Opens http://localhost:8080 with kompendium, slides, and exercises
```

Or open files directly:
- `workshop/kompendium.html` — Full reference
- `workshop/slides.html` — Presentation
- `workshop/handout.html` — Printable summary

---

## Troubleshooting

### "csk: command not found"

```bash
# Ensure pip bin is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall
pip install --user git+https://github.com/Simple-Bookings/claude-starter-kit.git
```

### "Claude Code not found"

Install from: https://claude.ai/code

```bash
# Mac
brew install claude-code

# Or via npm
npm install -g @anthropic-ai/claude-code
```

### "gh: command not found"

```bash
# Mac
brew install gh

# Linux
sudo apt install gh

# Then login
gh auth login
```

### Skills not loading

Claude reads skills on session start. After adding new skills:

```bash
# Exit and restart Claude
exit
claude
```

### Workshop materials not styling

Workshop HTML files use CDN dependencies (Tailwind CSS, Mermaid.js).

**For offline workshops:**

```bash
# Pre-cache CDN resources (requires internet once)
# Or use the workshop server which handles caching
csk workshop

# Alternative: download and serve locally
curl -o workshop/tailwind.min.js https://cdn.tailwindcss.com
curl -o workshop/mermaid.min.js https://cdn.jsdelivr.net/npm/mermaid@10.9.6/dist/mermaid.min.js
# Then update <script src> in HTML files
```

---

## Next Steps

1. **Run `csk doctor`** — verify everything works
2. **Read `CLAUDE.md`** — understand project conventions
3. **Do Exercise 01: Setup** — verify environment
4. **Work through exercises** — 6 exercises, ~2.5 hours total
5. **Start building!**

---

## Getting Help

- **Workshop materials:** `csk workshop`
- **CLI help:** `csk --help`
- **Skill list:** `/help` in Claude
- **Issues:** https://github.com/Simple-Bookings/claude-starter-kit/issues
