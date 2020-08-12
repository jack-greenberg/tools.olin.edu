#!/bin/bash
set -e

# Wait for db

until pg_isready -h ${POSTGRES_DB_NAME:-tools-db} -U ${POSTGRES_USER:-tools}; do
    sleep .5
done

# Import database stuff
alembic upgrade head

/usr/bin/python3 tools/app.py &> /var/log/tools.log &
tail -Fq /var/log/tools.log > /var/log/verbose-tools.log
