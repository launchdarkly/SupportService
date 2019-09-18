#!/bin/bash

until bash -c "flask db current > /dev/null 2>&1"; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up, starting SupportService"
python3 app/factory.py --host=localhost
