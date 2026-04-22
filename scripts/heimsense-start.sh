#!/usr/bin/env bash
set -euo pipefail

HEIMSENSE_BIN="${HOME}/.local/bin/heimsense"
ENV_FILE="${HOME}/.heimsense/.env"

if [ ! -x "${HEIMSENSE_BIN}" ]; then
  echo "heimsense ikke installeret på ${HEIMSENSE_BIN} — afventer devcontainer-setup.sh"
  exit 1
fi

GH_TOKEN=$(gh auth token 2>/dev/null || true)
if [ -z "${GH_TOKEN}" ]; then
  echo "gh ikke authenticated — prøver igen om 30s. Kør: gh auth login"
  exit 1
fi

mkdir -p "$(dirname "${ENV_FILE}")"
(umask 077; cat > "${ENV_FILE}" <<EOF
ANTHROPIC_BASE_URL=https://api.githubcopilot.com
ANTHROPIC_API_KEY=${GH_TOKEN}
ANTHROPIC_CUSTOM_MODEL_OPTION=claude-sonnet-4.6
ANTHROPIC_CUSTOM_MODEL_OPTION_NAME=Sonnet via HeimSense
ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION=CoPilot via HeimSense adapter
LISTEN_ADDR=:18081
REQUEST_TIMEOUT_MS=120000
MAX_RETRIES=3
EOF
)

while IFS='=' read -r key value; do
  [[ -z "$key" || "$key" == \#* ]] && continue
  export "$key=$value"
done < "${ENV_FILE}"

echo "Kører heimsense sync..."
"${HEIMSENSE_BIN}" sync

# Kør maks 8 timer — PM2 genstarter derefter med frisk GH token
# (GitHub OAuth-tokens roterer typisk inden for 8 timer)
# timeout returnerer 124 ved planlagt stop, heimsense's exit code ellers
echo "Starter heimsense run (max 8 timer, derefter genstart for frisk token)..."
timeout 28800 "${HEIMSENSE_BIN}" run
EXIT_CODE=$?
if [ "${EXIT_CODE}" -eq 124 ]; then
  echo "Heimsense stoppet efter 8 timer — PM2 genstarter med frisk token."
  exit 0
else
  echo "Heimsense afsluttede med exit code ${EXIT_CODE}"
  exit "${EXIT_CODE}"
fi
