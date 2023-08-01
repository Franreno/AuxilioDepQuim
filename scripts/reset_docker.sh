# USAR ISSO QUANDO A CRIACAO DO DOCKER DEU PROBLEMA OU VC QUER PARAR O DOCKER
#!/bin/bash

# Stop and remove the postgresdb container (if it exists)
if docker ps -a | grep -q "postgresdb"; then
  docker stop postgresdb
  docker rm postgresdb
fi

# Run the install.sh script to handle initialization
sudo scripts/install.sh

# List all containers (including stopped ones)
docker ps -a
