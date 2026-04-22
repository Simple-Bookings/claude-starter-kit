#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

command -v pm2 >/dev/null 2>&1 || { echo "FEJL: pm2 ikke fundet i PATH"; exit 1; }

pm2 delete heimsense 2>/dev/null || true

# Dræb eventuel hængende proces på port 18081
fuser -k 18081/tcp 2>/dev/null || true

pm2 start "${SCRIPT_DIR}/heimsense-start.sh" \
  --name heimsense \
  --interpreter bash \
  --restart-delay 30000

pm2 save
