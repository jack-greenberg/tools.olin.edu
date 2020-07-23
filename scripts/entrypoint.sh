#!/bin/bash
set -e

# Wait for db

until pg_isready -h tools-db -U ${POSTGRES_USER} -p ${POSTGRES_PASSWORD}; do
    sleep .5
done

# Import database stuff
alembic upgrade head

/usr/bin/python3 tools/app.py &> /var/log/tools.log &
tail -Fq /var/log/tools.log > /var/log/verbose-tools.log
