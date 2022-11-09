#include "database_handler.hpp"

DatabaseHandler::DatabaseHandler()
{
    // Connect to database
    conn = PQconnectdb(this->conninfo);

    // Check connection success
    if(PQstatus(conn) != CONNECTION_OK) 
    {
        std::cout << "Connection to database failed: " << PQerrorMessage(conn) << "\n";
        this->exit_connection();
    }
    // Check connection success
    if(PQstatus(conn) == CONNECTION_OK) 
    {
        std::cout << "Connection to database success\n";
        this->exit_connection();
    }
}

DatabaseHandler::~DatabaseHandler()
{
}


void DatabaseHandler::exit_connection() 
{
    // Closes connection
    if(PQstatus(conn) == CONNECTION_OK) 
        PQfinish(this->conn);
}