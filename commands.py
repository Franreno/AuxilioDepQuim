from database_handler import DatabaseHandler
from psycopg2._psycopg import connection, cursor


def getInput(startString: str = '>> '):
    return input(startString)


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


### CRIACAO DAS FUNCIONALIDADES ###

@funcionalidade("lista terceiro", help="Lista o terceiro pesquisado por nome")
def listCitites(cur: cursor, _):
    # pegar input da cidade
    print("Entrei")
    nucpfcnpj = getInput("Numero: ")

    try:
        cur.execute(
            f"SELECT * FROM terceiros t WHERE t.nucpfcnpj = '{nucpfcnpj}';")
    except:
        raise Exception(f"Erro ao pegar dados da cidade {nucpfcnpj}")

    if cur.rowcount == 0:
        print("Nao ha terceiros com esse numero")
    else:
        result = cur.fetchall()
        print(result)
