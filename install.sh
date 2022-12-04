#!/bin/bash

# Copy inital data

# cp data/esquema.sql data/dados.sql scripts/
# cat scripts/esquema.sql scripts/dados.sql > scripts/dump_data.sql
# rm scripts/esquema.sql scripts/dados.sql

cat esquema.sql dados.sql > dump_data.sql

# Create docker image
#docker build -t postgres-db ./scripts
docker build -t postgres-db ./

docker images -a

docker run -d --name postgresdb -p 5432:5432 postgres-db

rm dump_data.sql

# pip install -r requirements.txt