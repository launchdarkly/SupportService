#!/bin/bash

if [ ! -d "venv" ]
then
    virtualenv -p python3 venv 
fi

source venv/bin/activate
pip install -e . 