#!/bin/bash

sudo apt install -y rsync

PROD_SERVER=centos@52.37.10.150

# Send Latest Scripts to Production Server
rsync -e "ssh -o StrictHostKeyChecking=no" -avz scripts/ $PROD_SERVER:/var/www/app/scripts/
rsync -e "ssh -o StrictHostKeyChecking=no" -avz etc/ $PROD_SERVER:/var/www/app/etc/
scp -o StrictHostKeyChecking=no docker-compose.prod.yml $PROD_SERVER:/var/www/app/docker-compose.yml

# Log into Production Server, Pull and Restart Docker
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/zadacha && docker-compose pull'
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/zadacha && docker-compose build'
ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/zadacha && source scripts/secrets.sh && docker-compose up -d'