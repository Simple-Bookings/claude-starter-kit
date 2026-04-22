#!/usr/bin/env bash
set -euo pipefail

HEIMSENSE_VERSION="v0.1.3"
HEIMSENSE_BIN="${HOME}/.local/bin/heimsense"

# SHA256 checksums per platform — opdatér begge ved version-bump
HEIMSENSE_SHA256_AMD64="a141935685ab126a3e2d835dd020fe34c6039454e37b3e53f9a69e6375e2e384"
HEIMSENSE_SHA256_ARM64="e596cf256d6a6a5fea38f135a83449d1014cf5d3070a8789f6c043f808f03e5d"

# Detektér platform
ARCH=$(uname -m)
if [ "${ARCH}" = "aarch64" ] || [ "${ARCH}" = "arm64" ]; then
  PLATFORM="linux-arm64"
  HEIMSENSE_SHA256="${HEIMSENSE_SHA256_ARM64}"
else
  PLATFORM="linux-amd64"
  HEIMSENSE_SHA256="${HEIMSENSE_SHA256_AMD64}"
fi

mkdir -p "${HOME}/.local/bin"

# Spring over hvis korrekt version allerede er installeret
if [ -x "${HEIMSENSE_BIN}" ] && "${HEIMSENSE_BIN}" version 2>/dev/null | grep -q "${HEIMSENSE_VERSION}"; then
  echo "Heimsense ${HEIMSENSE_VERSION} allerede installeret — springer over."
else
  echo "Installerer Heimsense ${HEIMSENSE_VERSION} (${PLATFORM})..."
  curl -fsSL \
    "https://github.com/fajarhide/heimsense/releases/download/${HEIMSENSE_VERSION}/heimsense-${PLATFORM}" \
    -o "${HEIMSENSE_BIN}"

  echo "${HEIMSENSE_SHA256}  ${HEIMSENSE_BIN}" | sha256sum -c || {
    echo "FEJL: Checksum-verifikation fejlede — binæren er muligvis kompromitteret"
    rm -f "${HEIMSENSE_BIN}"
    exit 1
  }

  chmod +x "${HEIMSENSE_BIN}"
  echo "Heimsense ${HEIMSENSE_VERSION} installeret."
fi

if ! grep -q '\.local/bin' "${HOME}/.bashrc" 2>/dev/null; then
  echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${HOME}/.bashrc"
fi

echo "Heimsense ${HEIMSENSE_VERSION} installeret."
