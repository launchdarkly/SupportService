#!/bin/sh
# wait-for-postgres.sh

set -e

cmd="$@"

until bash -c "flask db current"; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - running migrations"
exec $cmd