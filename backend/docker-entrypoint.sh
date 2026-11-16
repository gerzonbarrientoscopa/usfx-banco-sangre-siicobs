#!/bin/sh
set -eu

python - <<'PY'
import os
import time

import pyodbc

database_name = os.environ.get("DB_NAME", "siicobs")
host = os.environ.get("DB_HOST", "localhost")
port = os.environ.get("DB_PORT", "62548")
user = os.environ.get("DB_USER", "sa")
password = os.environ.get("DB_PASSWORD", "")
odbc_database = "{" + database_name.replace("}", "}}") + "}"
odbc_password = "{" + password.replace("}", "}}") + "}"
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={host},{port};DATABASE={odbc_database};"
    f"UID={user};PWD={odbc_password};"
    "Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=5;"
)

print(
    f"Esperando SQL Server en {host}:{port}, base de datos {database_name}.",
    flush=True,
)
for attempt in range(60):
    try:
        connection = pyodbc.connect(connection_string, autocommit=True)
        connection.cursor().execute("SELECT 1")
        break
    except pyodbc.Error:
        if attempt == 59:
            raise
        time.sleep(2)
else:
    raise SystemExit("No se pudo conectar a SQL Server.")
connection.close()
PY

python manage.py collectstatic --noinput

exec gunicorn siicobs_main.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}"
