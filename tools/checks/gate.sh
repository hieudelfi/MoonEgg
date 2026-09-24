#!/usr/bin/env bash
# Cong kiem tra cua MoonEgg. Duoc devgate goi (~/.config/devgate/gate.sh), hoac chay tay:
#   bash tools/checks/gate.sh quick    truoc moi commit  (~2s)
#   bash tools/checks/gate.sh full     truoc moi push va truoc khi gop  (~10s)
set -uo pipefail
STAGE="${1:-full}"
FAIL=0

step() { printf '  %-34s' "$1"; }
pass() { printf 'dat\n'; }
fail() { printf 'HONG\n'; FAIL=1; [ -n "${1:-}" ] && printf '%s\n' "$1"; }

# --- quick: nhanh, chay truoc moi commit ------------------------------------
step "pytest tools/checks"
if out=$(python -m pytest tools/checks -q 2>&1); then pass; else fail "$out"; fi

step "verify_pack tren du lieu mau"
if out=$(python tools/checks/verify_pack.py content/lexicon/lexicon_raw_test.csv 2>&1); then
  pass; printf '    %s\n' "$(printf '%s' "$out" | head -1)"
else fail "$out"; fi

[ "$STAGE" = quick ] && { exit $FAIL; }

# --- full: them phan web, chay truoc push va truoc khi gop -------------------
if [ -f web/package.json ]; then
  if [ ! -d web/node_modules ]; then
    step "npm ci (lan dau)"
    if out=$(cd web && npm ci --silent 2>&1); then pass; else fail "$out"; fi
  fi
  step "vitest"
  if out=$(cd web && npm test 2>&1); then pass; else fail "$out"; fi

  step "cong giay phep (TC-CP-01/02)"
  if out=$(node tools/checks/check_licenses.mjs 2>&1); then
    pass; printf '    %s\n' "$(printf '%s' "$out" | head -1)"
  else fail "$out"; fi
fi

exit $FAIL
