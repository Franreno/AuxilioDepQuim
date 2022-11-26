#!/bin/bash

sudo docker rm -f $(sudo docker ps -lq)

sudo scripts/install.sh

sudo docker ps -a