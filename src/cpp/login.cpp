
#include <SQLiteCpp/SQLiteCpp.h>
#include <iostream>
#include <string>

struct User {
  int id;
  std::string name;
  std::string password;
  // bool isAdmin = false;
};

void setupDatabase(SQLite::Database &db) {

  // "CREATE TABLE IF NOT EXISTS"
  // create table if it doesn't already exist
  // id is unique and autoimcrements
  // name and password must have a value
  db.exec("CREATE TABLE IF NOT EXISTS users ("
          "  id       INTEGER PRIMARY KEY AUTOINCREMENT,"
          "  name     TEXT NOT NULL,"
          "  password TEXT NOT NULL"
          ")");
}

bool addUser(SQLite::Database &db, const std::string &name,
             const std::string &password) {

  // 1. check if name is already taken

  // SELECT COUNT(*) - how many rows match
  // FROM users - searches the users table
  // WHERE name = ? - rows that match the name "?" (placeholder)
  SQLite::Statement query(db, "SELECT COUNT(*) FROM users WHERE name = ?");

  // The first argument (1) fills in the ? placeholder with the value for the
  // name parameter.
  query.bind(1, name);

  // executeStep() runs query
  // returns true if username is taken
  // .executeStep() is used for select staments
  query.executeStep();

  // after running query, it returns a result table with one column
  // .getColumn(0) gets the result and getInt() makes sure it's an int.
  int count = query.getColumn(0).getInt();

  // if count = 1, username is taken
  if (count > 0) {
    std::cout << "Username " << name << " is already taken.\n";
    return false;
  }

  // 2. insert user
  // if transaction fails, nothing happens
  SQLite::Transaction transaction(db);

  // similiar statement as last time
  SQLite::Statement insert(db,
                           "INSERT INTO users (name, password) VALUES (?, ?)");
  // 0 would be the id but it's handeld by AUTOINCREMENT
  // binds name
  insert.bind(1, name);
  // binds password
  insert.bind(2, password);

  // .exec() is for writes with insert,delete,update
  insert.exec();

  // commits transaction
  transaction.commit();

  std::cout << "User " << name << " registered successfully.\n";
  return true;
}

bool loginUser(SQLite::Database &db, const std::string &name,
               const std::string &password) {

  // match name to password
  SQLite::Statement statement(db, "SELECT password FROM users WHERE name = ?");

  statement.bind(1, name);

  // returns false if user doesn't exist
  bool userExists = statement.executeStep();

  if (!userExists) {
    std::cout << "Username " << name << "not found.\n";
    return false;
  }

  std::string passwordCheck = statement.getColumn(0).getString();

  if (passwordCheck == password) {
    std::cout << "login successful\n";
    return true;
  } else {
    std::cout << "login failed\n";
    return false;
  }
}

void listUsers(SQLite::Database &db) {
  SQLite::Statement query(db, "SELECT * FROM users WHERE id >= 0");

  // struct not strictly necessary but it looks nicer :)
  User user;

  while (query.executeStep()) {

    user.id = query.getColumn(0).getInt();
    user.name = query.getColumn(1).getString();
    user.password = query.getColumn(2).getString();

    std::cout << "id: " << user.id << ", username: " << user.name
              << ", password: " << user.password << std::endl;
  }
}

int main() {
  try {
    SQLite::Database db("login.db",
                        SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE);

    std::string inputUsername = "";
    std::string inputPassword = "";
    int input = 1;

    setupDatabase(db);
    while (true) {

      int input;

      if (input == 0) {
        break;
      }

      std::cout << "\nMENU\n"
                << "1. add user\n"
                << "2. login\n"
                << "3. list users \n"
                << "0. Quit\n"
                << "Input: ";

      std::cin >> input;

      switch (input) {

      case 1:
        std::cout << "username: ";
        std::cin >> inputUsername;
        std::cout << "password: ";
        std::cin >> inputPassword;
        addUser(db, inputUsername, inputPassword);
        break;

      case 2:
        std::cout << "enter username: ";
        std::cin >> inputUsername;
        std::cout << "enter password: ";
        std::cin >> inputPassword;
        loginUser(db, inputUsername, inputPassword);
        break;

      case 3:
        listUsers(db);
        break;

      case 0:
        break;

      default:
        std::cout << "invalid input\n";
      }
    }
  } catch (std::exception &e) {
    std::cerr << "error: " << e.what() << "\n";
    return 1;
  }

  return 0;
}
