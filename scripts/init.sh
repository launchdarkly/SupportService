#!/bin/bash

# SupportService Init Script 
# used by cli.py LightSailApi.provisionInstance() as the user data

# get ready to be an app
sudo mkdir -p /var/www/app/scripts
sudo mkdir -p /var/www/app/etc
sudo chown -R centos:centos /var/www/app

# Make Swap
# Otherwise docker-compose up will sometimes be killed by the OOMkiller.
sudo dd if=/dev/zero of=/swap bs=1024 count=1048576
sudo mkswap /swap
sudo chmod 600 /swap
sudo swapon /swap
echo "/swap  none  swap  sw 0  0" | sudo tee -a /etc/fstab

# Install dependencies
sudo yum install -y epel-release
sudo yum install -y wget unzip git htop tmux vim python34-pip 
sudo pip3 install docker-compose 

# Update all packages 
sudo yum upgrade -y

# Install and Enable Docker
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker centos

sudo systemctl enable docker
sudo systemctl start docker
