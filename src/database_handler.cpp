#include "database_handler.hpp"

DatabaseHandler::DatabaseHandler()
{
    // Test connection
    if(this->connect())
        std::cout << "Conexao estabelecida com sucesso\n";

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

bool DatabaseHandler::connect()
{
    bool success = false;
    // Connect to database
    conn = PQconnectdb(this->conninfo);

    // Check connection success
    if(PQstatus(conn) != CONNECTION_OK) 
    {
        std::cout << "Connection to database failed: " << PQerrorMessage(conn) << "\n";
        this->exit_connection();
        success = false;
    }
    // Check connection success
    if(PQstatus(conn) == CONNECTION_OK) 
        success = true;

    return success;
}