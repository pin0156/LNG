#!/bin/bash

# for linux: Red Hat Enterprise Linux 7.5
sudo yum install git-core
sudo yum install wget
sudo yum install tmux

# install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py

# for www: install tornado
sudo pip install tornado
