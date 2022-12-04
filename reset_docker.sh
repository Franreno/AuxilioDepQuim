#!/bin/bash

sudo docker rm -f $(sudo docker ps -lq)

sudo ./install.sh

sudo docker ps -a