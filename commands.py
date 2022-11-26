from database_handler import DatabaseHandler
from psycopg2._psycopg import connection, cursor
from utils import getInput


class Funcionalidades:
    instances = []

    dbHandler = DatabaseHandler()

    def __init__(self, name: str, handler: any, help: str = None) -> None:
        self.name = name
        self.handler = handler
        self.help = help

    def run(self, args):
        conn: connection
        cur: cursor
        conn, cur = self.dbHandler.connectToDatabase()
        self.handler(cur, args)
        self.dbHandler.disconnectFromDatabase(conn=conn, cur=cur)

    def displayHelp(self):
        print(self.help or "...sem mensagem...")


def funcionalidade(name: str, help: str = None):
    def decorator(handler):
        Funcionalidades.instances.append(
            Funcionalidades(name, handler, help=help))
        return handler

    return decorator


def getAllCommands():
    return Funcionalidades.instances


def commandNames() -> list:
    return list(map(lambda x: x.name, Funcionalidades.instances))


### CRIACAO DAS FUNCIONALIDADES ###

@funcionalidade("lista cidade", help="Lista a cidade pesquisada por nome")
def listCitites(cur: cursor, _):
    # pegar input da cidade
    print("Entrei")
    cityName = getInput("Nome da cidade: ")

    try:
        cur.execute(f"SELECT * FROM city c WHERE c.name = '{cityName}';")
    except:
        raise Exception(f"Erro ao pegar dados da cidade {cityName}")

    if cur.rowcount == 0:
        print("Nao ha cidades")
    else:
        result = cur.fetchall()
        print(result)
