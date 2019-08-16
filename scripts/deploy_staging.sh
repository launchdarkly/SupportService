#!/bin/bash
# Support Service Deployment Script
#
# This script deploys the necessary files to the main supportservice server
# it copies over updated nginx configuration, any changes to scripts, and
# a generate docker-compose file. Then it prunes older docker images, pulls
# the latest docker image and restarts docker-compose.
#
PROD_SERVER="ld@staging.ldsolutions.org"

until bash -c "ssh -o StrictHostKeyChecking=no $PROD_SERVER 'docker ps'"; do
    >&2 echo "Server is not ready - sleeping"
    sleep 10
done

# Send Latest Scripts to Production Server
rsync -e "ssh -o StrictHostKeyChecking=no" -avz scripts/ $PROD_SERVER:/var/www/app/scripts/
scp -o StrictHostKeyChecking=no nginx.conf $PROD_SERVER:/var/www/app/etc/nginx/nginx.conf
scp -o StrictHostKeyChecking=no docker-compose.prod.yml $PROD_SERVER:/var/www/app/docker-compose.yml

# Clean up old images
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'docker system prune --force --volumes'

# Log into Production Server, Pull and Restart Docker
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose pull'
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose build'
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose down --remove-orphans'
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose up -d'
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/app && docker-compose restart web'
