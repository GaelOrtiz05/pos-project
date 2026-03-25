#include <iostream>
#include <string>
#include "sqlite3.h" // Include the SQLite header file
using namespace std;




int main() {
	sqlite3* ingredients_db;
	string sql_command;

	//create/open database
	sqlite3_open("Ingredients.db", &ingredients_db);

	//create table in database
	/*		NAME     QUANTITY (lbs)   
 			lettuce  10.0
			tomato   10.0
	*/
	sql_command = "CREATE TABLE ingredients(NAME TEXT, QUANTITY DOUBLE)";
	sqlite3_exec(ingredients_db, sql_command.c_str(),NULL,NULL,NULL);


	//Add data to table
	sql_command = "INSERT INTO ingredients(NAME,QUANTITY)"
		"VALUES "
		"('Meat','10'), ('Lettuce','10'), ('Tomato','10');";
	sqlite3_exec(ingredients_db, sql_command.c_str(), NULL, NULL, NULL);



}
