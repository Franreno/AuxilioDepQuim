# Comando uteis do docker

Para listar os dockers:

```
sudo docker ps -a
```

Remover um docker:

Pegar o id do container com o comando acima e rodar

```
sudo docker rm -f <id>
```

Entrar em um docker:

```
sudo docker exec -it <id> /bin/bash
```