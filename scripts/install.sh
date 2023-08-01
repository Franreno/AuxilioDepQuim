#!/bin/bash

# Check if the Docker volume exists
if docker volume ls -q | grep -q "^postgres_data$"; then
  # Docker volume exists, use it for data persistence
  echo "Using existing Docker volume for data persistence..."
else
  # Docker volume does not exist, create and initialize the container using dump_data.sql
  echo "Creating Docker volume and initializing container with dump_data.sql..."
  docker volume create postgres_data
  
  cp data/esquema.sql data/dados.sql scripts/
  cat scripts/esquema.sql scripts/dados.sql > scripts/dump_data.sql
  rm scripts/esquema.sql scripts/dados.sql

  docker build -t postgres-db ./scripts
  docker run -d --name postgresdb_tmp -p 5433:5432 -v postgres_data:/var/lib/postgresql/data postgres-db
  sleep 5  # Wait a few seconds for the PostgreSQL server to start

  # Copy data from the dump_data.sql into the running container
  docker cp scripts/dump_data.sql postgresdb_tmp:/docker-entrypoint-initdb.d/

  # Stop and remove the temporary container
  docker stop postgresdb_tmp
  docker rm postgresdb_tmp
  rm scripts/dump_data.sql
fi

# Start the container with the Docker volume for data persistence
docker run -d --name postgresdb -p 5433:5432 -v postgres_data:/var/lib/postgresql/data postgres-db

# List all containers to confirm the new container is running
docker ps -a
