# macOS Setup Guide

Get Claude Starter Kit 2.0 running on macOS.

---

## Prerequisites

### 1. Homebrew

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Python 3.10+

```bash
# Install Python via Homebrew
brew install python@3.12

# Verify
python3 --version  # Should be 3.10+
```

### 3. Git

```bash
# Usually pre-installed, but to update:
brew install git

# Verify
git --version
```

### 4. GitHub CLI

```bash
# Install
brew install gh

# Authenticate
gh auth login

# Verify
gh auth status
```

### 5. Claude Code

```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Or via Homebrew (if available)
brew install claude-code

# Verify
claude --version
```

---

## Install CSK2

### Option 1: PyPI (recommended)

```bash
pip3 install git+https://github.com/Simple-Bookings/claude-starter-kit.git
csk doctor
```

### Option 2: From source

```bash
git clone https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit
pip3 install -e .
csk doctor
```

---

## Verify Installation

```bash
csk doctor
```

Expected output:
```
✓ Python 3.12.0
✓ Git 2.43.0
✓ GitHub CLI 2.40.0
✓ Claude Code 1.0.0
✓ All checks passed!
```

---

## Common Issues

### "command not found: csk"

Add pip bin to PATH:

```bash
# Add to ~/.zshrc (or ~/.bash_profile)
export PATH="$HOME/Library/Python/3.12/bin:$PATH"

# Reload
source ~/.zshrc
```

### "Permission denied" during pip install

Use `--user` flag:

```bash
pip3 install --user git+https://github.com/Simple-Bookings/claude-starter-kit.git
```

### Xcode Command Line Tools required

```bash
xcode-select --install
```

---

## Apple Silicon (M1/M2/M3)

CSK2 works natively on Apple Silicon. No Rosetta required.

If you encounter architecture issues:

```bash
# Force native ARM64
arch -arm64 pip3 install git+https://github.com/Simple-Bookings/claude-starter-kit.git
```

---

## Next Steps

1. Run `csk doctor` to verify
2. Run `csk init my-project` to create a new project
3. Open `workshop/index.html` in browser
4. Start with Exercise 01
