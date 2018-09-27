#!/bin/bash

# SupportService Init Script 
sudo yum upgrade -y
sudo yum install -y wget unzip git htop vim epel-release

curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker centos

sudo yum install -y python34-pip
sudo pip3 install docker-compose

sudo systemctl enable docker
sudo systemctl start docker