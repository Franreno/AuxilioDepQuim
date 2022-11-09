#!/bin/bash

# Copy inital data

cp data/test_data.sql scripts/

# Create docker image
docker build -t postgres-db ./scripts

docker images -a

docker run -d --name postgresdb -p 5432:5432 postgres-db

rm scripts/test_data.sql