#!/bin/bash

deploy()
{
    PROD_SERVER="centos@$1"

    until bash -c "ssh -o StrictHostKeyChecking=no $PROD_SERVER 'docker ps'"; do
        >&2 echo "Server is not ready - sleeping"
        sleep 10
    done

    # Send Latest Scripts to Production Server
    rsync -e "ssh -o StrictHostKeyChecking=no" -avz scripts/ $PROD_SERVER:/var/www/app/scripts/
    rsync -e "ssh -o StrictHostKeyChecking=no" -avz etc/ $PROD_SERVER:/var/www/app/etc/
    scp -o StrictHostKeyChecking=no docker-compose.prod.yml $PROD_SERVER:/var/www/app/docker-compose.yml

    # Log into Production Server, Pull and Restart Docker
    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose pull'
    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose build'
    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose up -d'
}

deploy "$1"