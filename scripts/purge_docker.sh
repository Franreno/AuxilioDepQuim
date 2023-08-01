#!/bin/bash

# Stop and remove the postgresdb container (if it exists)
if docker ps -a | grep -q "postgresdb"; then
  docker stop postgresdb
  docker rm postgresdb
  echo "Removed the 'postgresdb' Docker container."
else
  echo "The 'postgresdb' Docker container does not exist."
fi

# Check if the Docker volume exists
if docker volume ls -q | grep -q "^postgres_data$"; then
  # Docker volume exists, remove it
  docker volume rm postgres_data
  echo "Removed the 'postgres_data' Docker volume."
else
  echo "The 'postgres_data' Docker volume does not exist."
fi