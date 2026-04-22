#!/usr/bin/env bash
set -euo pipefail

HEIMSENSE_VERSION="v0.1.3"
HEIMSENSE_BIN="${HOME}/.local/bin/heimsense"
HEIMSENSE_SHA256="a141935685ab126a3e2d835dd020fe34c6039454e37b3e53f9a69e6375e2e384"

mkdir -p "${HOME}/.local/bin"

echo "Installerer Heimsense ${HEIMSENSE_VERSION}..."
curl -fsSL \
  "https://github.com/fajarhide/heimsense/releases/download/${HEIMSENSE_VERSION}/heimsense-linux-amd64" \
  -o "${HEIMSENSE_BIN}"

echo "${HEIMSENSE_SHA256}  ${HEIMSENSE_BIN}" | sha256sum -c || {
  echo "FEJL: Checksum-verifikation fejlede — binæren er muligvis kompromitteret"
  rm -f "${HEIMSENSE_BIN}"
  exit 1
}

chmod +x "${HEIMSENSE_BIN}"

if ! grep -q '\.local/bin' "${HOME}/.bashrc" 2>/dev/null; then
  echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${HOME}/.bashrc"
fi

echo "Heimsense ${HEIMSENSE_VERSION} installeret."
