#!/bin/bash
# Support Service Deployment Script
#
# This script deploys the necessary files to the main supportservice server
# it copies over updated nginx configuration, any changes to scripts, and
# a generate docker-compose file. Then it prunes older docker images, pulls
# the latest docker image and restarts docker-compose.
#
# We have two enrivonments: production and staging. Please specify which host target
# you wish to deploy when executing the script. For example, to deploy to production,
# execute "deploy.sh production".

if [ -z "$1" ]
  then
  	echo "ERROR: no environment argument supplied"
  	exit 1
  else
  	SERVER="ubuntu@$1"
fi

until bash -c "ssh -o StrictHostKeyChecking=no $SERVER 'docker ps'"; do
    >&2 echo "Server is not ready - sleeping"
    sleep 10
done

# Send Latest Scripts to Production Server
rsync -e "ssh -o StrictHostKeyChecking=no" -avz scripts/ $SERVER:/var/www/app/scripts/
scp -o StrictHostKeyChecking=no docker-compose.prod.yml $SERVER:/var/www/app/docker-compose.yml

# Clean up old images
ssh -o StrictHostKeyChecking=no $SERVER 'docker system prune -a --force --volumes'

# Log into Production Server, Pull and Restart Docker
ssh -o StrictHostKeyChecking=no $SERVER 'cd /var/www/app && docker stack deploy --resolve-image always --prune -c docker-compose.yml support-service'
