#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"
#include <iostream>

struct User {
  int id;
  std::string name;
  std::string pass;
  bool isManager;
};

// initialize users.db somehow idk

class UserDatabase {
private:
  SQLite::Database db;

public:
  void addUser();
  void removeUser();
  void validateCredentials();
};
