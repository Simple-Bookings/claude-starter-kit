# Windows + WSL2 + Docker Setup Guide

Complete guide to setting up a development environment on Windows for CSK2.

**Estimated time:** 30-45 minutes

---

## Prerequisites

- Windows 10 (version 2004+) or Windows 11
- Administrator access
- 8GB+ RAM recommended
- 20GB+ free disk space

---

## Step 1: Enable WSL2

### 1.1 Open PowerShell as Administrator

Press `Win + X`, select "Windows Terminal (Admin)" or "PowerShell (Admin)".

### 1.2 Install WSL

```powershell
wsl --install
```

This installs WSL2 with Ubuntu by default.

### 1.3 Restart Your Computer

Required for WSL to complete installation.

### 1.4 Set Up Ubuntu

After restart, Ubuntu will launch automatically. Create your username and password.

### 1.5 Update Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 2: Install Docker Desktop

### 2.1 Download Docker Desktop

Visit: https://www.docker.com/products/docker-desktop/

Download the Windows installer.

### 2.2 Install Docker Desktop

Run the installer with these options:
- ✅ Use WSL 2 instead of Hyper-V
- ✅ Add shortcut to desktop

### 2.3 Configure Docker

After installation:
1. Open Docker Desktop
2. Go to Settings → Resources → WSL Integration
3. Enable integration with your Ubuntu distribution
4. Click "Apply & Restart"

### 2.4 Verify Docker

In your Ubuntu terminal:

```bash
docker --version
docker run hello-world
```

---

## Step 3: Install Development Tools

### 3.1 Git (usually pre-installed)

```bash
git --version
# If not installed:
sudo apt install git
```

Configure git:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3.2 GitHub CLI

```bash
sudo apt install gh
gh auth login
```

### 3.3 Python 3.10+

```bash
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### 3.4 Node.js (optional, for JS projects)

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs
node --version
npm --version
```

---

## Step 4: Install Claude Code

### 4.1 Install Claude Code CLI

```bash
curl -fsSL https://claude.ai/install.sh | sh
```

### 4.2 Add to PATH

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.claude/bin:$PATH"
```

Reload shell:

```bash
source ~/.bashrc
```

### 4.3 Verify Installation

```bash
claude --version
```

### 4.4 Authenticate

```bash
claude login
```

Follow the browser prompts to authenticate.

---

## Step 5: Install VS Code

### 5.1 Download VS Code

Visit: https://code.visualstudio.com/

Install for Windows.

### 5.2 Install WSL Extension

In VS Code:
1. Press `Ctrl+Shift+X` (Extensions)
2. Search "WSL"
3. Install "WSL" by Microsoft

### 5.3 Connect to WSL

1. Press `Ctrl+Shift+P`
2. Type "WSL: Connect to WSL"
3. Select your Ubuntu distribution

### 5.4 Install Recommended Extensions

In WSL-connected VS Code:
- Python
- Pylance
- GitLens
- Prettier
- ESLint

---

## Step 6: Install CSK2

### 6.1 Clone the Repository

```bash
cd ~
git clone https://github.com/Simple-Bookings/claude-starter-kit.git
cd claude-starter-kit
```

### 6.2 Install CSK CLI

```bash
pip install -e .
```

### 6.3 Verify Installation

```bash
csk doctor
```

All checks should pass.

---

## Step 7: Open in VS Code Dev Container (Optional)

For a fully isolated environment:

### 7.1 Install Dev Containers Extension

In VS Code, install "Dev Containers" extension.

### 7.2 Open in Container

1. Open the CSK2 folder in VS Code
2. Press `Ctrl+Shift+P`
3. Type "Dev Containers: Reopen in Container"
4. Wait for container to build

---

## Troubleshooting

### WSL Not Starting

```powershell
# In PowerShell (Admin)
wsl --update
wsl --shutdown
wsl
```

### Docker Not Working in WSL

1. Open Docker Desktop
2. Settings → Resources → WSL Integration
3. Ensure your distro is enabled
4. Restart Docker Desktop

### Claude CLI Not Found

```bash
# Check installation
ls ~/.claude/bin/

# Add to PATH manually
export PATH="$HOME/.claude/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.claude/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Permission Denied Errors

```bash
# Fix Docker socket permissions
sudo usermod -aG docker $USER
newgrp docker
```

### Slow File System

Use files inside WSL, not Windows drives:

```bash
# Good (fast)
cd ~/projects/my-project

# Bad (slow)
cd /mnt/c/Users/Name/projects/my-project
```

---

## Quick Reference

| Tool | Command | Purpose |
|------|---------|---------|
| WSL | `wsl` | Enter Ubuntu |
| Docker | `docker ps` | List containers |
| Git | `git status` | Check repo status |
| GitHub | `gh pr list` | List PRs |
| Claude | `claude` | Start Claude Code |
| CSK | `csk doctor` | Check environment |
| VS Code | `code .` | Open in VS Code |

---

## Next Steps

1. Run `csk doctor` to verify setup
2. Run `csk init my-project` to create a project
3. Run `csk exercises` to start learning

---

**Need help?** Open an issue at https://github.com/Simple-Bookings/claude-starter-kit/issues
