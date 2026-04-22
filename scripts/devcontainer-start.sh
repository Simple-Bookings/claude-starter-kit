#!/usr/bin/env bash
set -euo pipefail

pm2 delete heimsense 2>/dev/null || true
pm2 start scripts/heimsense-start.sh \
  --name heimsense \
  --interpreter bash \
  --restart-delay 60000 \
  --no-autorestart false

pm2 save --force
