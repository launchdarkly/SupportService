#!/bin/bash

##
# SupportService Entry Point
##

set -e

source .env 
pip install -r requirements.txt

until bash -c "flask db current"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up, starting SupportService"
# Run Migrations and Start App
flask db upgrade
flask run --host=0.0.0.0
