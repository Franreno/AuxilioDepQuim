#include "libpq-fe.h"
#include <iostream>

class DatabaseHandler
{
private:
    // Atributes
    const char *conninfo = "dbname = Auxilios";
    PGconn *conn;
    PGresult *res;
    
    // Functions
    void exit_connection();


public:
    DatabaseHandler();
    ~DatabaseHandler();
};