#include <iostream>
#include "libpq-fe.h"

class DatabaseHandler
{
private:
    // Atributes
    const char *conninfo = "host=localhost port=5432 dbname=Auxilios password=docker user=postgres connect_timeout=10";
    PGconn *conn;
    PGresult *res;
    
    // Functions
    void exit_connection();


public:
    DatabaseHandler();
    ~DatabaseHandler();
};