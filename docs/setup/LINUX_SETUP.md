# Linux Setup Guide

Get Claude Starter Kit 2.0 running on Linux (Ubuntu/Debian, Fedora, Arch).

---

## Prerequisites

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python 3.10+
sudo apt install python3 python3-pip python3-venv

# Install Git
sudo apt install git

# Verify
python3 --version  # Should be 3.10+
git --version
```

### Fedora

```bash
# Install Python and Git
sudo dnf install python3 python3-pip git

# Verify
python3 --version
git --version
```

### Arch Linux

```bash
# Install Python and Git
sudo pacman -S python python-pip git

# Verify
python --version
git --version
```

---

## GitHub CLI

### Ubuntu/Debian

```bash
# Add GitHub CLI repository
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Authenticate
gh auth login
```

### Fedora

```bash
sudo dnf install gh
gh auth login
```

### Arch Linux

```bash
sudo pacman -S github-cli
gh auth login
```

---

## Claude Code

```bash
# Install via npm (requires Node.js)
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

### If Node.js not installed

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Fedora
sudo dnf install nodejs

# Arch
sudo pacman -S nodejs npm
```

---

## Install CSK2

### Option 1: PyPI (recommended)

```bash
pip3 install --user git+https://github.com/Simple-Bookings/claude-starter-kit.git
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
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Reload
source ~/.bashrc
```

### "externally-managed-environment" error (Ubuntu 23.04+, Fedora 38+)

Use `--break-system-packages` or a virtual environment:

```bash
# Option 1: Break system packages (simple)
pip3 install --user --break-system-packages git+https://github.com/Simple-Bookings/claude-starter-kit.git

# Option 2: Virtual environment (recommended)
python3 -m venv ~/.csk-venv
source ~/.csk-venv/bin/activate
pip install git+https://github.com/Simple-Bookings/claude-starter-kit.git
```

### Permission denied

Never use `sudo pip`. Use `--user` flag instead:

```bash
pip3 install --user git+https://github.com/Simple-Bookings/claude-starter-kit.git
```

---

## WSL2

If running Linux via WSL2 on Windows, see [WINDOWS_WSL2_SETUP.md](./WINDOWS_WSL2_SETUP.md).

---

## Next Steps

1. Run `csk doctor` to verify
2. Run `csk init my-project` to create a new project
3. Open `workshop/index.html` in browser
4. Start with Exercise 01
