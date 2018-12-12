#!/bin/bash

restart()
{
    PROD_SERVER="centos@$1"

    ssh -o StrictHostKeyChecking=no $PROD_SERVER 'cd /var/www/relay && docker-compose restart'
}

restart "$1"