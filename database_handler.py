import psycopg2
from psycopg2._psycopg import connection, cursor


class DatabaseHandler:

    CONNECTION_CONFIG: str = "dbname='Auxilios' user='postgres' host='localhost' password='docker' port='5432'"

    def __init__(self) -> None:
        # Test the connection
        conn, cur = self.connectToDatabase()
        if (conn == None and cur == None):
            raise Exception("Error initializing DatabaseHandler")

        # Connection succeed
        self.disconnectFromDatabase(conn=conn, cur=cur)

    # Connect to the database via CONNECTION_CONFIG

    def connectToDatabase(self) -> tuple[connection, cursor]:
        conn: connection = None
        try:
            conn = psycopg2.connect(self.CONNECTION_CONFIG)
            cur = conn.cursor()
        except:
            raise Exception("Error connecting to databse")
        return conn, cur

    # Disconnect from database and commits if `commit = True`
    def disconnectFromDatabase(self, conn: connection, cur: cursor, commit=False):
        if commit:
            conn.commit()

        cur.close()
        conn.close()

    def _checkIfExist(conn: connection, cur: cursor, text: str) -> bool:
        try:
            cur.execute(f"SELECT * FROM RANDOM_TEXT WHERE TEXT = {text};")
        except:
            raise Exception("Error getting text from data base!")
        querry_result = cur.fetchone()
        if (querry_result is None):
            return False
        else:
            return True

    def insertValuesIntoTable(self, table: str, columns: list, values: list):
        conn, cur = self._connectToDatabase()

        try:
            cur.execute(f"INSERT INTO {table}({columns}) VALUES ({values});")
        except:
            self._disconnectFromDatabase(conn=conn, cur=cur)
            raise Exception(
                f"Error inserting values {values} into table ${table}")

        self._disconnectFromDatabase(conn=conn, cur=cur)

    def runSQL(self, sql: str):
        conn, cur = self._connectToDatabase()

        # TODO Sanatize sql here!

        try:
            cur.execute(sql)
        except:
            self._disconnectFromDatabase(conn=conn, cur=cur)
            raise Exception(f"[ERROR] Cannot execute sql: {sql}")

        queryResult = cur.fetchone()
        self._disconnectFromDatabase(conn=conn, cur=cur)
        return queryResult
