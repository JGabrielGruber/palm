#!/usr/bin/env bash
# Rebuild landing page CSS (Tailwind). Used on host and inside palm-docs image.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/docs"

if command -v tailwindcss >/dev/null 2>&1; then
  # Global CLI (palm-docs image) — Tailwind v4 package ships as `tailwindcss`.
  tailwindcss -i styles/input.css -o styles/output.css
elif command -v npx >/dev/null 2>&1; then
  npx --yes @tailwindcss/cli -i styles/input.css -o styles/output.css
else
  echo "error: need tailwindcss on PATH (palm-docs image) or npx (host docs/node_modules)" >&2
  exit 1
fi

echo "✅ docs/styles/output.css rebuilt"
