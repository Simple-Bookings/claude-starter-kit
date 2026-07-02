#!/usr/bin/env bash
set -euo pipefail

echo "🚀 CSK2 Devcontainer Setup"
echo ""

# ─── Ensure ~/.local/bin is on PATH ───────────────────────────────────────
mkdir -p "${HOME}/.local/bin"
if ! grep -q '\.local/bin' "${HOME}/.bashrc" 2>/dev/null; then
  echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${HOME}/.bashrc"
fi
if ! grep -q '\.local/bin' "${HOME}/.zshrc" 2>/dev/null; then
  echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${HOME}/.zshrc"
fi

# ─── Install CSK2 CLI ─────────────────────────────────────────────────────
echo "📦 Installing CSK2 CLI..."
pip install -e . --quiet

# ─── Install git hooks ────────────────────────────────────────────────────
echo ""
echo "🔧 Installing git hooks..."
bash scripts/setup-hooks.sh

# ─── Verify installation ──────────────────────────────────────────────────
echo ""
echo "🔍 Running csk doctor..."
csk doctor

echo ""
echo "✅ CSK2 setup complete!"
echo ""
echo "Next steps:"
echo "  csk exercises    # Start the exercise server"
echo "  csk workshop     # Start the workshop materials server"
echo "  claude           # Start Claude Code"
