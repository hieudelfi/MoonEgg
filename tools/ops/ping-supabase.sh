#!/usr/bin/env bash
# Keep-alive ping for the free Supabase project.
#
# A free project pauses after a week with no activity (docs/03-bang-chung-xac-thuc.md:34).
# This script reads one row through the REST API with the anon key, so it also proves the
# public path still answers, not only that the server is awake.
#
# Row level security means the anon key sees zero rows. That is the expected result.
# What is being checked is the HTTP code, not the body.
#
# Usage:
#   bash tools/ops/ping-supabase.sh
#
# Reads VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY from the environment, or from .env
# and .env.local at the repo root. Both names are read because Vite treats .env.local as
# the machine-local file, and the web app will read the same two variables later.
# Appends one line per run to tools/ops/ping-supabase.log, so a run that never happened
# shows up later as a gap between dates.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_FILE="$REPO_ROOT/tools/ops/ping-supabase.log"

# A file only fills in a variable that is not already set, so a scheduled task can pass
# the values in without editing anything. .env.local is read after .env, but the rule
# above still means the first value found wins.
for env_file in "$REPO_ROOT/.env" "$REPO_ROOT/.env.local"; do
  [ -f "$env_file" ] || continue
  while IFS='=' read -r key value; do
    case "$key" in
      ''|\#*) continue ;;
    esac
    key="${key// /}"
    value="${value%$'\r'}"
    value="${value%\"}"; value="${value#\"}"
    if [ -n "$key" ] && [ -z "${!key:-}" ]; then
      export "$key=$value"
    fi
  done < "$env_file"
done

URL="${VITE_SUPABASE_URL:-}"
KEY="${VITE_SUPABASE_ANON_KEY:-}"

if [ -z "$URL" ] || [ -z "$KEY" ]; then
  echo "ping-supabase: VITE_SUPABASE_URL or VITE_SUPABASE_ANON_KEY is missing." >&2
  echo "ping-supabase: set them in $REPO_ROOT/.env or in the environment." >&2
  exit 2
fi

URL="${URL%/}"
STAMP="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

# select one row, ask for as little as possible
CODE="$(curl -s -o /dev/null -w '%{http_code}' \
  --max-time 30 \
  -H "apikey: $KEY" \
  -H "Authorization: Bearer $KEY" \
  "$URL/rest/v1/review_event?select=event_id&limit=1")"

if [ "$CODE" = "200" ]; then
  RESULT="ok"
  EXIT=0
else
  RESULT="FAIL"
  EXIT=1
fi

LINE="$STAMP  http=$CODE  $RESULT"
echo "$LINE"
mkdir -p "$(dirname "$LOG_FILE")"
echo "$LINE" >> "$LOG_FILE"

exit "$EXIT"
