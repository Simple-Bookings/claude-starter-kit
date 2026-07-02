# /adopt — Import CSK2 Into Existing Project

Import Claude Starter Kit 2.0 into an existing repository — interactive guide that handles conflicts, merges config files, and sets up the structure.

---

## When to Use

- You have an existing project and want to add CSK2 workflows
- You're migrating from a different Claude setup
- You want to adopt CSK2's skills and structure without starting fresh

---

## Step 1: Identify Source and Target

**Source:** CSK2 repository (where you're running this skill)
**Target:** Your existing project

```bash
# Find CSK2 root
CSK2_ROOT=$(git rev-parse --show-toplevel)
echo "CSK2 location: $CSK2_ROOT"

# Set your target project path
TARGET="/path/to/your/project"

# Verify target is a git repo
if [ -d "$TARGET/.git" ]; then
  echo "✓ Target is a git repository"
else
  echo "✗ Target is not a git repository — run 'git init' first"
fi
```

---

## Step 2: Scan for Conflicts

Check what already exists in your project:

```bash
echo "=== Scanning target for existing files ==="
echo ""
echo "CLAUDE.md:      $([ -f "$TARGET/CLAUDE.md" ] && echo "EXISTS" || echo "missing")"
echo ".claude/:       $([ -d "$TARGET/.claude" ] && echo "EXISTS" || echo "missing")"
echo ".devcontainer/: $([ -d "$TARGET/.devcontainer" ] && echo "EXISTS" || echo "missing")"
echo "docs/:          $([ -d "$TARGET/docs" ] && echo "EXISTS ($(ls $TARGET/docs 2>/dev/null | wc -l) files)" || echo "missing")"
echo ".gitignore:     $([ -f "$TARGET/.gitignore" ] && echo "EXISTS ($(wc -l < $TARGET/.gitignore) lines)" || echo "missing")"
```

**Conflict resolution strategy:**
- **EXISTS + will overwrite:** Backup to `.bak` first
- **EXISTS + will merge:** Combine intelligently (e.g., .gitignore)
- **missing:** Copy directly

---

## Step 3: Copy Core Structure

### 3.1 Copy .claude/ directory

```bash
# Backup existing .claude if present
if [ -d "$TARGET/.claude" ]; then
  cp -r "$TARGET/.claude" "$TARGET/.claude.bak"
  echo "Backed up existing .claude/ to .claude.bak/"
fi

# Copy skills
mkdir -p "$TARGET/.claude/skills"
cp -r "$CSK2_ROOT/.claude/skills/"* "$TARGET/.claude/skills/"
echo "✓ Copied skills/"

# Copy agents (if present)
if [ -d "$CSK2_ROOT/.claude/agents" ]; then
  mkdir -p "$TARGET/.claude/agents"
  cp -r "$CSK2_ROOT/.claude/agents/"* "$TARGET/.claude/agents/"
  echo "✓ Copied agents/"
fi

# Copy rules (if present)
if [ -d "$CSK2_ROOT/.claude/rules" ]; then
  mkdir -p "$TARGET/.claude/rules"
  cp -r "$CSK2_ROOT/.claude/rules/"* "$TARGET/.claude/rules/"
  echo "✓ Copied rules/"
fi
```

### 3.2 Copy docs templates (skip if content exists)

```bash
mkdir -p "$TARGET/docs"

# Copy VISION.md if not present or empty
if [ ! -s "$TARGET/docs/VISION.md" ]; then
  cp "$CSK2_ROOT/docs/VISION.md" "$TARGET/docs/"
  echo "✓ Copied docs/VISION.md template"
else
  echo "— Skipped docs/VISION.md (already has content)"
fi

# Copy FEATURES.md if not present or empty
if [ ! -s "$TARGET/docs/FEATURES.md" ]; then
  cp "$CSK2_ROOT/docs/FEATURES.md" "$TARGET/docs/"
  echo "✓ Copied docs/FEATURES.md template"
else
  echo "— Skipped docs/FEATURES.md (already has content)"
fi
```

### 3.3 Merge .gitignore

```bash
if [ -f "$TARGET/.gitignore" ]; then
  # Add CSK2 patterns that aren't already present
  cat >> "$TARGET/.gitignore" << 'EOF'

# === CSK2 additions ===
.claude/state/
.worktrees/
*.bak
.env.local
EOF
  echo "✓ Appended CSK2 patterns to .gitignore"
else
  cp "$CSK2_ROOT/.gitignore" "$TARGET/.gitignore"
  echo "✓ Copied .gitignore"
fi
```

---

## Step 4: Create or Update CLAUDE.md

If the target already has a CLAUDE.md, help merge it:

```bash
if [ -f "$TARGET/CLAUDE.md" ]; then
  echo "Target already has CLAUDE.md"
  echo "Options:"
  echo "  1. Keep existing (add CSK2 skills reference manually)"
  echo "  2. Append CSK2 template to existing"
  echo "  3. Replace with CSK2 template (backup existing)"
else
  # Create new CLAUDE.md from template
  cat > "$TARGET/CLAUDE.md" << 'EOF'
# CLAUDE.md

## Project Overview

[Describe your project here]

## Skills

CSK2 skills are available in `.claude/skills/`. Key skills:

| Skill | Trigger | Purpose |
|-------|---------|---------|
| Planning | `/planning` | Analyze issue, create task list |
| Execution | `/execution` | TDD implementation |
| Reviewing | `/reviewing` | Code review against ACs |
| Integration | `/integration` | PR, merge, close issue |

## Key Commands

```bash
# Add your project's key commands here
npm install
npm test
npm run build
```

## Conventions

- [Add your project's conventions]

## Don't

- Don't commit to main directly
- Don't skip tests
- [Add your project's rules]
EOF
  echo "✓ Created CLAUDE.md template"
fi
```

---

## Step 5: Verify Installation

```bash
echo "=== CSK2 Adoption Summary ==="
echo ""
echo "Skills:     $(ls $TARGET/.claude/skills 2>/dev/null | wc -l) skills"
echo "Agents:     $(ls $TARGET/.claude/agents 2>/dev/null | wc -l 2>/dev/null || echo "0") agents"
echo "Rules:      $(ls $TARGET/.claude/rules 2>/dev/null | wc -l 2>/dev/null || echo "0") rules"
echo "Docs:       $(ls $TARGET/docs/*.md 2>/dev/null | wc -l) templates"
echo "CLAUDE.md:  $([ -f $TARGET/CLAUDE.md ] && echo "present" || echo "missing")"
echo ""
echo "Next steps:"
echo "  1. Edit CLAUDE.md with your project specifics"
echo "  2. Fill in docs/VISION.md with your mission"
echo "  3. Run 'claude' and try '/planning' on an issue"
```

---

## Manual Steps (if needed)

If the automated copy doesn't work, here's the manual approach:

```bash
# Clone CSK2 to temp location
git clone https://github.com/Simple-Bookings/claude-starter-kit /tmp/csk2

# Copy what you need
cp -r /tmp/csk2/.claude/skills/* my-project/.claude/skills/
cp /tmp/csk2/docs/VISION.md my-project/docs/
cp /tmp/csk2/docs/FEATURES.md my-project/docs/

# Cleanup
rm -rf /tmp/csk2
```

---

## Troubleshooting

### "Permission denied" when copying

```bash
# Check permissions
ls -la "$TARGET/.claude"

# Fix if needed
chmod -R u+w "$TARGET/.claude"
```

### Skills not recognized by Claude

Claude reads skills on startup. After copying:

```bash
# Restart Claude session
exit
claude
```

### Conflicts with existing .claude structure

If you have an existing `.claude/` with different structure:

1. Backup: `mv .claude .claude.old`
2. Copy CSK2: `cp -r /path/to/csk2/.claude .`
3. Merge what you need from `.claude.old`
4. Remove backup when done

---

## Output

When adoption is complete:

```
✅ CSK2 Adopted

Skills: 14 copied to .claude/skills/
Docs: VISION.md, FEATURES.md templates ready
CLAUDE.md: Created (customize for your project)

Start with: claude → /planning #1
```
