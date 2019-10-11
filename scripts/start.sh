#!/bin/bash

while ! nc -zv db 5432; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up, starting SupportService"
flask db upgrade > /dev/null 2>&1
ddtrace-run gunicorn "app.factory:application" -w 4 -b 0.0.0.0:$1
