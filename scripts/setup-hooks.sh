#!/bin/bash
# Install git hooks for CSK2 project
#
# Run this once after cloning:
#   bash scripts/setup-hooks.sh

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$REPO_ROOT/.husky"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "🔧 Setting up git hooks..."

# Copy hooks to .git/hooks
if [ -d "$HOOKS_DIR" ]; then
  for hook in "$HOOKS_DIR"/*; do
    if [ -f "$hook" ]; then
      HOOK_NAME=$(basename "$hook")
      cp "$hook" "$GIT_HOOKS_DIR/$HOOK_NAME"
      chmod +x "$GIT_HOOKS_DIR/$HOOK_NAME"
      echo "  ✓ Installed $HOOK_NAME"
    fi
  done
else
  echo "  ⚠️  No hooks found in .husky/"
  exit 1
fi

echo ""
echo "✅ Git hooks installed!"
echo ""
echo "Hooks will now run automatically on:"
echo "  - pre-commit: Checks for debug statements, secrets, large files"
echo ""
echo "To skip hooks (not recommended): git commit --no-verify"
