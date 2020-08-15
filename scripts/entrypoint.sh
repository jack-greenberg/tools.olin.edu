#!/bin/bash
set -e

# Wait for db
until pg_isready -h ${POSTGRES_DB_NAME:-tools-db} -U ${POSTGRES_USER:-tools}; do
    sleep .5
done

# Import database
alembic upgrade head

uwsgi uwsgi.ini &> /var/log/tools.log
