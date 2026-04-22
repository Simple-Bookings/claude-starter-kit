#!/usr/bin/env bash
# Fjerner heimsense-settings fra ~/.claude/settings.json og stopper PM2-processen.
set -euo pipefail

SETTINGS="${HOME}/.claude/settings.json"

echo "Stopper heimsense i PM2..."
pm2 delete heimsense 2>/dev/null && echo "  ✓ PM2-process slettet" || echo "  – ingen PM2-process fundet"

if [ ! -f "${SETTINGS}" ]; then
  echo "Ingen settings.json fundet — intet at rydde op."
  exit 0
fi

echo "Rydder heimsense-settings ud af ${SETTINGS}..."
python3 - "${SETTINGS}" <<'EOF'
import sys, json

path = sys.argv[1]
with open(path) as f:
    cfg = json.load(f)

heimsense_env_keys = {
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_CUSTOM_MODEL_OPTION",
    "ANTHROPIC_CUSTOM_MODEL_OPTION_NAME",
    "ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION",
}

env = cfg.get("env", {})
removed = [k for k in heimsense_env_keys if k in env]
for k in removed:
    del env[k]

if not env:
    cfg.pop("env", None)

with open(path, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")

if removed:
    print(f"  ✓ Fjernet: {', '.join(removed)}")
else:
    print("  – ingen heimsense env-keys fundet")
EOF

echo "Fjerner ~/.heimsense/.env..."
rm -f "${HOME}/.heimsense/.env" && echo "  ✓ ~/.heimsense/.env slettet" || true

echo "Færdig. Genstart Claude Code for at ændringerne træder i kraft."
