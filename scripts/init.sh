#!/bin/bash

# SupportService Init Script 
# used by cli.py LightSailApi.provisionInstance() as the user data 
sudo yum upgrade -y
sudo yum install -y wget unzip git htop vim epel-release

curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker centos

sudo yum install -y python34-pip
sudo pip3 install docker-compose

sudo systemctl enable docker
sudo systemctl start docker

# get ready to be an app
sudo mkdir -p /var/www/app/scripts
sudo touch /var/www/app/scripts/secrets.sh
sudo chown -R centos:centos /var/www/app