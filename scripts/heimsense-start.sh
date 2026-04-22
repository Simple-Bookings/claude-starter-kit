#!/usr/bin/env bash
set -euo pipefail

HEIMSENSE_BIN="${HOME}/.local/bin/heimsense"
ENV_FILE="${HOME}/.config/heimsense/.env"

if [ ! -x "${HEIMSENSE_BIN}" ]; then
  echo "heimsense ikke installeret på ${HEIMSENSE_BIN} — afventer devcontainer-setup.sh"
  exit 1
fi

GH_TOKEN=$(gh auth token 2>/dev/null || true)
if [ -z "${GH_TOKEN}" ]; then
  echo "gh ikke authenticated — prøver igen om 60s. Kør: gh auth login"
  exit 1
fi

mkdir -p "$(dirname "${ENV_FILE}")"
cat > "${ENV_FILE}" <<EOF
ANTHROPIC_BASE_URL=https://api.copilot.com/v1
ANTHROPIC_API_KEY=${GH_TOKEN}
ANTHROPIC_CUSTOM_MODEL_OPTION=sonnet
ANTHROPIC_CUSTOM_MODEL_OPTION_NAME=Sonnet via HeimSense
ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION=CoPilot via HeimSense adapter
LISTEN_ADDR=:18081
REQUEST_TIMEOUT_MS=120000
MAX_RETRIES=3
EOF
chmod 600 "${ENV_FILE}"

set -a
# shellcheck source=/dev/null
source "${ENV_FILE}"
set +a

echo "Kører heimsense sync..."
"${HEIMSENSE_BIN}" sync

echo "Starter heimsense run..."
exec "${HEIMSENSE_BIN}" run
