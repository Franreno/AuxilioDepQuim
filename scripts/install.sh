#!/bin/bash

# Copy inital data

cp data/esquema.sql data/dados.sql scripts/
cat scripts/esquema.sql scripts/dados.sql > scripts/dump_data.sql
rm scripts/esquema.sql scripts/dados.sql

# Create docker image
docker build -t postgres-db ./scripts

docker images -a

docker run -d --name postgresdb -p 5433:5432 postgres-db

rm scripts/dump_data.sql

# pip install -r requirements.txt