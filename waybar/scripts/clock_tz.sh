#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="$HOME/.cache/monarch"
STATE_FILE="$STATE_DIR/clock_mode"
MODE="local"

ensure_state() {
  mkdir -p "$STATE_DIR"
  if [[ -f "$STATE_FILE" ]]; then
    MODE=$(<"$STATE_FILE")
  else
    echo "$MODE" >"$STATE_FILE"
  fi
}

print_time() {
  ensure_state
  if [[ "$MODE" == "ba" ]]; then
    TEXT=$(TZ=America/Argentina/Buenos_Aires date +"%H:%M · %A, %B %-d ·")
    CLASS="clock ba"
  else
    TEXT=$(date +"%H:%M · %A, %B %-d ·")
    CLASS="clock local"
  fi
  # Emit JSON without jq (Waybar expects a single JSON object per update)
  local t="$TEXT" c="$CLASS"
  t="${t//\\/\\\\}"
  t="${t//\"/\\\"}"
  c="${c//\\/\\\\}"
  c="${c//\"/\\\"}"
  printf '{"text":"%s","class":"%s","tooltip":false}\n' "$t" "$c"
}

toggle_mode() {
  ensure_state
  if [[ "$MODE" == "ba" ]]; then
    MODE="local"
  else
    MODE="ba"
  fi
  echo -n "$MODE" >"$STATE_FILE"
  # Refresh Waybar modules listening on RTMIN+8
  pkill -RTMIN+8 waybar 2>/dev/null || true
}

case "${1:-print}" in
  print)  print_time ;;
  toggle) toggle_mode ;;
  *) echo "Usage: $0 [print|toggle]" >&2; exit 1 ;;
esac
