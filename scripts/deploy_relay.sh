#!/bin/bash

deploy()
{
    PROD_SERVER="centos@relay.ldsolutions.tk"

    until bash -c "ssh -o StrictHostKeyChecking=no $PROD_SERVER 'docker ps'"; do
        >&2 echo "Server is not ready - sleeping"
        sleep 10
    done

    # Send Generated Docker Compose File to Production Server
    scp -o StrictHostKeyChecking=no docker-compose.relay.yml $PROD_SERVER:/var/www/relay/docker-compose.yml

    # Log into Production Server, Pull and Restart Docker
    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/relay && docker-compose pull'
    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/relay && docker-compose build'
    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/relay && docker-compose up -d'
}

deploy