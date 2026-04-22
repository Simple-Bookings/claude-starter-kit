#!/usr/bin/env bash
set -euo pipefail

pm2 delete heimsense 2>/dev/null || true

# Dræb eventuel hængende proces på port 18081
fuser -k 18081/tcp 2>/dev/null || true

pm2 start scripts/heimsense-start.sh \
  --name heimsense \
  --interpreter bash \
  --restart-delay 5000
