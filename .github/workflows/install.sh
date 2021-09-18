#!/bin/bash -e
pip install -r requirements.txt
sudo apt install software-properties-common

sudo add-apt-repository -y ppa:deki/firejail
sudo apt-get update
sudo apt-get install firejail

sudo apt-get install gcc