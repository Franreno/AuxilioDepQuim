# Auxilio a Dependentes Químicos e Moradores de Rua
Implementação da base de dados e do sistema para o projeto de Auxilio a Dependentes Químicos e Moradores de Rua.

Este projeto é a parte 3 da disciplina de Base de Dados SCC0640.

Esta aplicação foi planejada para o seu funcionamente automatico em ambientes Linux.

# Contribuidores
Este projeto foi inicialmente desenvolvido por:

- Emanuel Lace Aranha - 11234224
- Felipe de Alcantara Tomé - 11800970
- Francisco Reis Nogueira - 11954374
- João Augusto Fernandes Barbosa - 11953348


## Instalação

É necessário estar no `root` do projeto para os comandos abaixo funcionarem corretamente. 
Também é necessário dar permissão para os scripts funcionarem. Para isso o comando abaixo deve ser executado.

```
sudo chmod +x scripts/*.sh
```

Também é necessário instalar os pacotes `python` que são utilizados na aplicação. Estes são instalados via o `package manager`: `pip`. Dessa forma, para instalar os pacotes basta executar o comando abaixo:

```
pip install -r requirements.txt
```

### Scripts

Para rodar a aplicação é necessário ter o `docker` instalado no computador. A fim de automatizar essa instalação existe o [script install_docker_ubuntu.sh](https://github.com/Franreno/AuxilioDepQuim/blob/main/scripts/install_docker_ubuntu.sh). Executando o comando abaixo instala o `docker` em ambintes `Debian`.
```
sudo scripts/install_docker_ubuntu.sh
```


Após ter instalado o `docker` é necessário rodar o [script de criação do docker](https://github.com/Franreno/AuxilioDepQuim/blob/main/scripts/install.sh). Para isso basta executar o comando: 
```
sudo scripts/install_docker.sh
```

Com isso a aplicação deverá estar corretamente instalada e operando.

## Dados

Os dados dos esquema da tabela se encontram na [pasta data](https://github.com/Franreno/AuxilioDepQuim/tree/main/data) onde existe:
- [Dados de criação das tabelas (esquema.sql)](https://github.com/Franreno/AuxilioDepQuim/blob/main/data/esquema.sql)
- [Dados de inserção iniciais (dados.sql)](https://github.com/Franreno/AuxilioDepQuim/blob/main/data/dados.sql)

Estes dados são utilizados na criação do docker. Então o banco de dados é populado durante a criação do docker.

## Consultas

As consultas de complexidade média e alta que devem ser executadas se encontram no [arquivo consultas.sql](https://github.com/Franreno/AuxilioDepQuim/blob/main/data/consultas.sql)

Estas consultas podem ser executadas dentro da interface da aplicação.

## Execução

Para iniciar o programa o comando abaixo deve ser executado:
```
python src/main.py
```

Com isso a tela inicial deve ser gerada:
![image](https://user-images.githubusercontent.com/67326251/206812965-52145625-1611-49c2-a353-98ef0679c2c6.png)

Há 7 opções que podem ser escolhidas e as sessões abaixo descrevem como elas funcionam.

### Mostrar tabelas

Essa funcionalidade mostra o nome, tipo e tamanho das colunas de uma tabela. A tabela pode ser escolhida com o `dropDown` presente na interface e o resultado irá ser escrito no campo de texto, conforme mostra a figura abaixo:

![image](https://user-images.githubusercontent.com/67326251/206813158-cc5b7e6b-1599-4cdb-9eba-ae26cd8b85d0.png)

### Rodar/Debugar SQL

Esta funcionalidade permite ao usuário rodar o SQL que deseja, como se fosse um QueryTool. 

![image](https://user-images.githubusercontent.com/67326251/206813201-0392dbba-f107-4cc3-b938-d14319e2b8dd.png)

### Rodar consultas.sql

Esta funcionalidade roda todas as consultas que estão presentes no [aquivo de consultas](https://github.com/Franreno/AuxilioDepQuim/blob/main/data/consultas.sql) indicando a consulta que está sendo realizada e seu resultado.

![image](https://user-images.githubusercontent.com/67326251/206813313-df89dcd3-059b-4a24-ab90-c151ecbc5f6c.png)


### Cadastrar novo funcionario

Permite o cadastro de um novo funcionario de acordo com os campos da tabela funcionario.

![image](https://user-images.githubusercontent.com/67326251/206813322-3502df1a-49a6-4588-b023-2c22794a0b1a.png)

### Cadastrar nova empresa

Permite o cadastro de um nova empresa de acordo com os campos da tabela empresa.

![image](https://user-images.githubusercontent.com/67326251/206813328-6bcaacaa-cc34-41ea-942b-856a34596140.png)


### Cadastrar nova empresa

Permite o cadastro de um novo centro de acordo com os campos da tabela centro.

![image](https://user-images.githubusercontent.com/67326251/206813403-83a81481-c6eb-4c24-95f3-325da75c7e08.png)

### Mostrar informações

Permite selecionar os dados das colunas especificas de cada tabela.

![image](https://user-images.githubusercontent.com/67326251/206813500-6e0faa33-4662-4de8-aaf5-91e2cb921063.png)


## Conclusões e contribuições

Com isso a parte 3 do trabalho de Base de dados é concluída.

Caso encontre algum erro [abra um Issue](https://github.com/Franreno/AuxilioDepQuim/issues/new)

E caso deseje contribuir com alguma melhoria para o projeto [abra um pull request](https://github.com/Franreno/AuxilioDepQuim/pulls)
