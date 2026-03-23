#ifndef LOGIN_HPP
#define LOGIN_HPP

#include <SQLiteCpp/SQLiteCpp.h>
#include <iostream>
#include <string>

struct User {
  int id;
  std::string name;
  std::string password;
  // bool isAdmin = false;
};

class Login {
private:
  SQLite::Database db;

public:
  Login() : db("login.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    setupDatabase();
  };

  void setupDatabase() {

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

  bool addUser(const std::string &name, const std::string &password) {

    // 1. check if name is already taken

    // SELECT COUNT(*) - how many rows match
    // FROM users - searches the users table
    // WHERE name = ? - rows that match the name "?" (placeholder)
    SQLite::Statement query(db, "SELECT COUNT(*) FROM users WHERE name = ?");

    // The first argument (1) fills in the ? placeholder with the value for the
    // name parameter.
    query.bind(1, name);

    // .executeStep() is used for select staments
    // executeStep() runs query
    // returns true if row already exists (username is taken)
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
    SQLite::Statement insert(
        db, "INSERT INTO users (name, password) VALUES (?, ?)");
    // id is handeld by AUTOINCREMENT
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

  bool removeUser(const std::string &name) {

    SQLite::Transaction transaction(db);

    SQLite::Statement del(db, "DELETE FROM users WHERE name = ?");

    del.bind(1, name);

    // .exec() returns amount of rows changed
    // should be 1 if user is deleted
    int changed = del.exec();

    if (changed == 0) {
      std::cout << "Username " << name << "not found.\n";
      return false;
    }

    transaction.commit();

    std::cout << "Username " << name << "deleted.\n";
    return true;
  }

  bool loginUser(const std::string &name, const std::string &password) {

    // match name to password
    SQLite::Statement statement(db,
                                "SELECT password FROM users WHERE name = ?");

    statement.bind(1, name);

    // returns false if user doesn't exist
    // .executeStep() returns true if a row is fetched
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

  void listUsers() {
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

  void loginMenu() {
    Login login;

    bool running = true;
    std::string inputUsername = "";
    std::string inputPassword = "";
    int input = 1;

    login.setupDatabase();
    while (running) {

      int input;

      if (input == 0) {
        break;
      }

      std::cout << "\nMENU\n"
                << "1. add user\n"
                << "2. remove user\n"
                << "3. login\n"
                << "4. list users \n"
                << "0. Quit\n"
                << "Input: ";

      std::cin >> input;

      switch (input) {

      case 1:
        std::cout << "username: ";
        std::cin >> inputUsername;
        std::cout << "password: ";
        std::cin >> inputPassword;
        login.addUser(inputUsername, inputPassword);
        break;

      case 2:
        std::cout << "username: ";
        std::cin >> inputUsername;
        login.removeUser(inputUsername);
        break;

      case 3:
        std::cout << "enter username: ";
        std::cin >> inputUsername;
        std::cout << "enter password: ";
        std::cin >> inputPassword;
        login.loginUser(inputUsername, inputPassword);
        break;

      case 4:
        login.listUsers();
        break;

      case 0:
        running = false;
        break;

      default:
        std::cout << "invalid input\n";
      }
    }
  }
};

#endif
