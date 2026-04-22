#!/usr/bin/env bash
set -euo pipefail

if pm2 describe heimsense > /dev/null 2>&1; then
  pm2 restart heimsense
else
  pm2 start scripts/heimsense-start.sh \
    --name heimsense \
    --interpreter bash \
    --restart-delay 60000
fi
