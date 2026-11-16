#!/bin/sh
set -eu

python - <<'PY'
import os
import re
import time

import pyodbc

database_name = os.environ.get("DB_NAME", "siicobs")
if not re.fullmatch(r"[A-Za-z0-9_]+", database_name):
    raise SystemExit("DB_NAME solo puede contener letras, números y guion bajo.")

host = os.environ.get("DB_HOST", "sqlserver")
port = os.environ.get("DB_PORT", "1433")
user = os.environ.get("DB_USER", "sa")
password = os.environ.get("DB_PASSWORD", "")
odbc_password = "{" + password.replace("}", "}}") + "}"
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={host},{port};DATABASE=master;UID={user};PWD={odbc_password};"
    "Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=5;"
)

for attempt in range(60):
    try:
        connection = pyodbc.connect(connection_string, autocommit=True)
        break
    except pyodbc.Error:
        if attempt == 59:
            raise
        time.sleep(2)
else:
    raise SystemExit("No se pudo conectar a SQL Server.")

try:
    cursor = connection.cursor()
    if cursor.execute("SELECT DB_ID(?)", database_name).fetchone()[0] is None:
        cursor.execute(f"CREATE DATABASE [{database_name}]")
finally:
    connection.close()
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn siicobs_main.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}"
