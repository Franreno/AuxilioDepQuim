from database_handler import DatabaseHandler
from psycopg2._psycopg import connection, cursor, OperationalError, Error
from tabulate import tabulate
import sys

def outputToScreen(cursor: cursor) -> str:
    """Formata o resultado que esta dentro do cursor

    Args:
        cursor (cursor): Cursor do dbHabdler que contem os dados

    Returns:
        str: string formatada com os dadsos
    """

    # pega os dados das colunas
    table = [list(result) for result in cursor.fetchall() ]
    # pega os nomes das colunas
    table.insert(0, [desc[0].upper() for desc in cursor.description])

    return tabulate(table)

class Funcionalidades:
    """Classe que junta as possiveis funcionalidades do programa
    """
    instances = []

    dbHandler = DatabaseHandler()

    def __init__(self, name: str, handler: any, help: str = None) -> None:
        """Construtor para a classe Funcionalidades

        Args:
            name (str): Nome da funcionalidade
            handler (any): Funcao da funcionalidade
            help (str, optional): Descricao da funcionalidade. Defaults to None.
        """
        self.name = name
        self.handler = handler
        self.help = help

    def run(self, args, *param) -> str:
        """Roda o handler da funcao

        Args:
            args (any): Argumentos da funcao

        Returns:
            str: Lista com o conteudo
        """
        conn: connection
        cur: cursor
        conn, cur = self.dbHandler.connectToDatabase()
        outputList = self.handler(cur, args, param)
        self.dbHandler.disconnectFromDatabase(conn=conn, cur=cur, commit = True)
        return outputList

def funcionalidade(name: str, help: str = None):
    """Criacao do decorator @ para a funcionalidade

    Args:
        name (str): Nome da funcionalidade
        help (str, optional): Ajuda da funcionalidade. Defaults to None.
    """
    def decorator(handler):
        Funcionalidades.instances.append(
            Funcionalidades(name, handler, help=help))
        return handler

    return decorator


### CRIACAO DAS FUNCIONALIDADES ###

### Rodar o consultas.sql ###

@funcionalidade('consultas', help="Roda o arquivo de consultas.sql")
def runConsultasSQL(cur: cursor, _, __):
    """Realiza todas as consultas presentes no arquivo consultas.sql

    Args:
        cur (cursor): Cursor da conexao com o banco de dados

    Returns:
        list: lista com os dados da consulta
    """
    # Open and read all
    fd = open('./data/consultas.sql', 'r')
    sqlFile = fd.read()
    fd.close()


    # Split at ;
    sqlCommands = sqlFile.replace("\n", " ").split(';')
    sqlCommands.pop()

    # Remove comments
    for index, cmd in enumerate(sqlCommands):
        if(cmd.find('--') != -1):
            sqlCommands.pop(index)

    outputList = []

    # Execute the queries
    for command in sqlCommands:
        outputList.append(f"\nRODANDO CONSULTA:   {command}\n")
        try:
            cur.execute(command)
        except:
            return [f"[ ERRO ] Commando com erro: {command}"]

        if cur.row_factory == 0:
            outputList.append("[ INFO ] Sem resultados ")
        else:
            outputList.append(outputToScreen(cur))
    
    return outputList

@funcionalidade("runSQL", help="Roda um sql")
def runSQL(cur: cursor, args, *param):
    """Recebe uma string como parametro e executa ela como um codigo SQL.

    Args:
        cur (cursor): cursor de manipulação da database
        args (_type_): string com a consulta

    Returns:
        _type_: retorna o resultado da consulta de forma tabular/formatada. Pode retornar também ERRO ou Sem resultados.
    """
    sql = args.replace('\n', '')
    try:
        cur.execute(sql)
    except Error as e:

        return("[ ERRO ] Commando com erro" + "\n" + str(e))

    if cur.row_factory == 0:
        return("[ INFO ] Sem resultados ")
    else:
        return outputToScreen(cur)
    

@funcionalidade("tableNames", help="retorna nome das tabelas")
def tableName(cur: cursor, *params):
    """Itera sobre a base de dados a fim de gerar uma lista com o nome de todas as tabelas

    Args:
        cur (cursor): cursor de manipulação da databse

    """
    tables = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
    try:
        cur.execute(tables)
    except Exception as e:
        print(e)
    table = [result[0] for result in cur.fetchall() ]
    return(table)


@funcionalidade("columnNames", help="retorna atributos")
def columnNames(cur: cursor, args, *params):
    """Dada uma tabela, itera em cima desta e retorna uma lista com o nome de suas colunas

    Args:
        cur (cursor): cursor de manipulação da database
        args (_type_): string com o nome da tabela a ser iterada
    """
    coluna = str(args)
    try:
        cur.execute("SELECT * FROM " + coluna + " WHERE 1=0;")
    except Exception as e:
        print(e)
    table = [result for result in cur.fetchall() ]
    table.insert(0, [desc[0].upper() for desc in cur.description])
    return(table[0])

@funcionalidade("directQuery", help="insere centro")
def directQuery(cur: cursor, args, *params):
    """Query direta

    Args:
        cur (cursor): Cursor da conexao do banco de dados

    Returns:
        list: lista contendo os dados
    """
    cur.execute("SELECT "+ args[1] + " FROM "+ args[0] + ";")
    return outputToScreen(cur)


@funcionalidade("insertCentro", help="insere centro")
def insertCentro(cur: cursor, args, *params):
    """Função para geração de um SQL de inserção de novos valores dentro de centro

    Args:
        cur (cursor): cursor de manipulação da database
        args (_type_): cnpj, caixa, nome, local e presidente a serem inseridos
    """
    sqlCentro = "INSERT INTO CENTRO(CNPJ,CAIXA,NOME, LOCAL,PRESIDENTE) VALUES (%s,%s,%s,%s,%s);"
    try:
        cur.execute(sqlCentro, args)
    except Exception as e:
        return(-1)
    return

@funcionalidade("insertEmp", help="insere empresa")
def insertEmp(cur: cursor, args, *params):
    """Função para realizar a inserção de uma nova empresa. Inicialmente, os valores são inseridos em Terceiros e posteriormente, em Empresa Parceira

    Args:
        cur (cursor): cur (cursor): cursor de manipulação da database
        args (_type_): Nome, Cnpj, Numero de funcionarios e numero maximo de funcionarios

    Returns:
        _type_: retorna um ouput com o retorno do cursor para a consulta em questão, ou -1 em caso de erro
    """
    sqlTerceiros = "INSERT INTO TERCEIROS (NUCPFCNPJ,NOME,TIPO) VALUES (%s, %s,'EMPRESA PARCEIRA');"
    data = (args[1], args[0])
    try:
        cur.execute(sqlTerceiros, data)
    except Exception as e:
        print(e)
        return(-1)
    
    sqlEmpresas = "INSERT INTO EMPRESAS_PARCEIRAS(CNPJ, NUFUNCIONARIOS, MAXFUNCIONARIOS) VALUES (%s, %s, %s);"
    try:
        data = (args[1], args[2], args[3])
        cur.execute(sqlEmpresas, data)
    except Exception as e:
        print(e)
        return(-1)
    return 

@funcionalidade("insertFunc", help="insereFuncionario")
def insertFunc(cur: cursor, args, *params):
    """Gera um sql para a inserção de um novo funcionario, colocando-o inicialmente como pessoa fisica, depois na tabela do tipo de pessoa e por fim como funcionario

    Args:
        cur (cursor): cursor de manipulação da database
        args (_type_): Nome e cnpj do funcionario

    Returns:
        _type_: -1 em caso de erro ou o retorno do cursor para a inserção
    """
    sqlTerceiros = "INSERT INTO TERCEIROS (NUCPFCNPJ,NOME,TIPO) VALUES (%s, %s,'PESSOA FISICA');"
    try:
        data = (args[1], args[0])
        cur.execute(sqlTerceiros, data)
    except Exception as e:
        print(e)
        return(-1)

    sqlPF = "INSERT INTO PESSOA_FISICA(CPF) VALUES (%s);"
    sqlTipo = "INSERT INTO TIPO_PESSOA_FISICA(CPF,TIPOPF) VALUES (%s,'FUNCIONARIO');"
    sqlFunc = "INSERT INTO FUNCIONARIO(CPF,CENTRO) VALUES (%s, %s);"

    try:
        cur.execute(sqlPF, [args[1]])
        cur.execute(sqlTipo, [args[1]])

        data = (args[1], args[2])
        cur.execute(sqlFunc, data)

    except:
        return(-1)
    return 

@funcionalidade('listTables')
def listTables(cur: cursor, _, __):
    """Lista todas as tabelas do banco de dadoss

    Args:
        cur (cursor): Conexao com o banco de dados

    Raises:
        Exception: erro ao pegar os dados

    Returns:
        list: nome das tabelas
    """

    sql = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"

    try:
        cur.execute(sql)
    except:
        raise Exception(f"Erro ao pegar dados das tabelas")

    rawData = outputToScreen(cur).split('\n')
    rawData.pop(0)
    rawData.pop(0)
    rawData.pop()


    return [data.capitalize() for data in rawData]


@funcionalidade('getTableSchema')
def getTableSchema(cur: cursor, args, *param):
    """Pega os nomes, tipos e tamanho das colunas de uma certa tabela

    Args:
        cur (cursor): Conexao com o banco de dados

    Raises:
        Exception: Erro ao pegar os dados do banco de dados

    Returns:
        list: Dados da tabela
    """
    tableName: str = args
    tableName = tableName.lower()

    sql = f"select column_name as coluna, data_type as tipo, character_maximum_length as tam from INFORMATION_SCHEMA.COLUMNS  where table_name = '{tableName}';"

    try:
        cur.execute(sql)
    except:
        raise Exception(f"Erro ao pegar dados das tabelas")

    return outputToScreen(cur)