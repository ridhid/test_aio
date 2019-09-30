#!/bin/sh

# wait for Postgres to start
function postgres_ready(){
python << END
import sys
import psycopg2
import os
try:
    conn = psycopg2.connect(
    dbname="${POSTGRES_DB:-test_aio}",
    user="${POSTGRES_USER:-test_aio}",
    password="${POSTGRES_PASSWORD:-test_aio}",
    host="${POSTGRES_HOST:-postgres}",
    port="${POSTGRES_PORT:-5432}")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

alembic upgrade head
run_test_aio

