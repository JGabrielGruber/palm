#!/usr/bin/env bash
# Rebuild landing page CSS (Tailwind). Used on host and inside palm-docs image.
set -euo pipefail

# Prefer docs/ as cwd when seeded as docs-only (sandbox) or repo/docs (host script).
if [[ -f styles/input.css ]]; then
  :
elif [[ -f docs/styles/input.css ]]; then
  cd docs
elif [[ -n "${BASH_SOURCE[0]:-}" ]]; then
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  cd "$ROOT/docs"
else
  echo "error: cannot find styles/input.css" >&2
  exit 1
fi

# Global npm modules (palm-docs image): needed so @import "tailwindcss" resolves.
if command -v npm >/dev/null 2>&1; then
  _groot="$(npm root -g 2>/dev/null || true)"
  if [[ -n "${_groot}" ]]; then
    export NODE_PATH="${_groot}${NODE_PATH:+:}${NODE_PATH:-}"
  fi
fi

if command -v tailwindcss >/dev/null 2>&1; then
  tailwindcss -i styles/input.css -o styles/output.css
elif command -v npx >/dev/null 2>&1; then
  npx --yes @tailwindcss/cli -i styles/input.css -o styles/output.css
else
  echo "error: need tailwindcss on PATH (palm-docs image) or npx (host docs/node_modules)" >&2
  exit 1
fi

echo "✅ styles/output.css rebuilt"
