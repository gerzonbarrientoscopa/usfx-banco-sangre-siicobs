#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export DJANGO_SETTINGS_MODULE=siicobs_main.replit_settings
export VUE_APP_BASE_API=/api/v1
PYTHON="$PWD/.pythonlibs/bin/python"
cd backend
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py runserver 127.0.0.1:8000 --noreload &
backend_pid=$!
cd ../frontend
npm run dev -- --port 5000 &
frontend_pid=$!
trap 'kill "$backend_pid" "$frontend_pid" 2>/dev/null || true' EXIT INT TERM
wait -n "$backend_pid" "$frontend_pid"
