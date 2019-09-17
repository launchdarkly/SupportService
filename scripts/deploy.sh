#!/bin/bash
# Support Service Deployment Script
#
# This script deploys the necessary files to the main supportservice server
# it copies over updated nginx configuration, any changes to scripts, and
# a generate docker-compose file. Then it prunes older docker images, pulls
# the latest docker image and restarts docker-compose.
#
PRODUCTION_SERVER="ubuntu@production.ldsolutions.org"

until bash -c "ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'docker ps'"; do
    >&2 echo "Server is not ready - sleeping"
    sleep 10
done

# Send Latest Scripts to Production Server
rsync -e "ssh -o StrictHostKeyChecking=no" -avz scripts/ $PRODUCTION_SERVER:/var/www/app/scripts/
scp -o StrictHostKeyChecking=no nginx.conf $PRODUCTION_SERVER:/etc/nginx/nginx.conf
scp -o StrictHostKeyChecking=no docker-compose.prod.yml $PRODUCTION_SERVER:/var/www/app/docker-compose.yml

# Clean up old images
ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'docker system prune --force --volumes'

# Log into Production Server, Pull and Restart Docker
ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'cd /var/www/app && docker-compose pull'
ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'cd /var/www/app && docker-compose build'
ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'cd /var/www/app && docker-compose down --remove-orphans'
ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'cd /var/www/app && docker-compose up -d'

# Restart Nginx 
ssh -o StrictHostKeyChecking=no $PRODUCTION_SERVER 'sudo nginx -s reload'
