#!/usr/bin/env bash
# Vis heimsense status og seneste logs
set -euo pipefail

echo "=== PM2 Status ==="
pm2 show heimsense 2>/dev/null || echo "Heimsense kører ikke"

echo ""
echo "=== Seneste logs (out) ==="
tail -20 "${HOME}/.claude/logs/heimsense-out.log" 2>/dev/null || pm2 logs heimsense --nostream --lines 20 2>/dev/null || echo "Ingen logs fundet"

echo ""
echo "=== Seneste fejl (err) ==="
tail -20 "${HOME}/.claude/logs/heimsense-err.log" 2>/dev/null || echo "Ingen fejl-logs fundet"
