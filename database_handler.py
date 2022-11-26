import psycopg2
from psycopg2._psycopg import connection, cursor


class DatabaseHandler:

    CONNECTION_CONFIG: str = "dbname='Auxilios' user='postgres' host='localhost' password='docker' port='5432'"
    """CONFIGURATION FOR THE CONNECTION OF THE DATABASE"""

    def __init__(self) -> None:
        """Constructor for `DatabaseHandler` class

        Raises:
            DatabaseExepction: raised when test connection to database failed
        """
        conn, cur = self.connectToDatabase()
        # closed == 0 -> connected
        if (conn.closed != 0):
            raise DatabaseExepction("Error initializing DatabaseHandler")

        # Connection succeed
        self.disconnectFromDatabase(conn=conn, cur=cur)

    def connectToDatabase(self) -> tuple[connection, cursor]:
        """Connect to the database via `CONNECTION_CONFIG`

        Raises:
            Exception: Raised when the connection failed

        Returns:
            tuple[connection, cursor]: Returns the connection and cursor for the database
        """
        conn: connection = None
        try:
            conn = psycopg2.connect(self.CONNECTION_CONFIG)
            cur = conn.cursor()
        except:
            raise Exception("Error connecting to databse")
        return conn, cur

    def disconnectFromDatabase(self, conn: connection, cur: cursor, commit=False):
        """Disconnect from database and commits if `commit = True`

        Args:
            conn (connection): The connection reference to this database
            cur (cursor): The cursor reference to this database
            commit (bool, optional): If the commit must happen. Defaults to False.
        """
        if commit:
            conn.commit()

        cur.close()
        conn.close()


class DatabaseExepction(Exception):
    pass
