#!/bin/bash

until bash -c "flask db current > /dev/null 2>&1"; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up, starting SupportService"
flask db upgrade > /dev/null 2>&1
gunicorn --reload "app.factory:create_app('production')" -b 0.0.0.0:$1