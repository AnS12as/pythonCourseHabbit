#!/usr/bin/env bash
# Use this script to wait until a given host is reachable

set -e

TIMEOUT=30
QUIET=0
HOST=""
PORT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --timeout=*)
      TIMEOUT="${1#*=}"
      ;;
    --quiet)
      QUIET=1
      ;;
    *)
      if [[ -z "$HOST" ]]; then
        HOST="$1"
      elif [[ -z "$PORT" ]]; then
        PORT="$1"
      fi
      ;;
  esac
  shift
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
  echo "Usage: wait-for-it.sh <host> <port> [--timeout=SECONDS] [--quiet]"
  exit 1
fi

start_time=$(date +%s)
while :; do
  nc -z "$HOST" "$PORT" && break
  if (( $(date +%s) - start_time >= TIMEOUT )); then
    echo "Timeout: Unable to connect to $HOST:$PORT"
    exit 1
  fi
  sleep 1
done

[[ $QUIET -eq 0 ]] && echo "$HOST:$PORT is up"
