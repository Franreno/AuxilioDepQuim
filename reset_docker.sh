#!/bin/bash

sudo docker rm -f $(sudo docker ps -lq)

sudo ./install.sh