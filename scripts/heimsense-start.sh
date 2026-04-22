#!/usr/bin/env bash
set -euo pipefail

HEIMSENSE_BIN="${HOME}/.local/bin/heimsense"
ENV_FILE="${HOME}/.config/heimsense/.env"

if [ ! -x "${HEIMSENSE_BIN}" ]; then
  echo "Fejl: heimsense ikke fundet på ${HEIMSENSE_BIN}. Kør devcontainer-setup.sh først."
  exit 1
fi

GH_TOKEN=$(gh auth token 2>/dev/null || true)
if [ -z "${GH_TOKEN}" ]; then
  echo "Fejl: ikke logget ind på GitHub. Kør: gh auth login"
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

# Eksporter alle vars så pm2 arver dem (inkl. ved autorestart)
set -a
# shellcheck source=/dev/null
source "${ENV_FILE}"
set +a

pm2 delete heimsense 2>/dev/null || true
pm2 start "${HEIMSENSE_BIN}" \
  --name heimsense \
  --interpreter none \
  -- run

echo "Heimsense startet via pm2. Se status med: pm2 status"
