#ifndef LOGIN_HPP
#define LOGIN_HPP

#include <SQLiteCpp/SQLiteCpp.h>
#include <iostream>
#include <string>

// things to implement
// change user password/username

// INSERT INTO <table> (<column1>, <column2>, ...) VALUES (?, ?, ...)
//
// SELECT <columns> FROM <table> WHERE <condition>
//
// UPDATE <table> SET <column> = <value> WHERE <condition>
//
// DELETE FROM <table> WHERE <condition>

struct User {
  int id;
  std::string name;
  std::string password;
  bool isAdmin;
};

class Login {
private:
  SQLite::Database db;
  void setupDatabase() {

    // create table if it doesn't already exist
    // id is unique and autoimcrements
    // name and password must have a value
    // is_admin is set to 0 by default
    db.exec("CREATE TABLE IF NOT EXISTS users ("
            "  id       INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  name     TEXT NOT NULL,"
            "  password TEXT NOT NULL,"
            "  is_admin INTEGER DEFAULT 0"
            ")");

    // adds admin user on database initialization
    if (searchUser("admin") == false) {
      addUser("admin", "changeme", true);
    }
  }

  // helper function
  bool searchUser(const std::string &name) {

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

    // if count = 1, username exists
    if (count > 0) {
      return true;
    } else {
      return false;
    }
  }

public:
  Login() : db("data/login.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    setupDatabase();
  };

  // if a parameter is not given for isAdmin, defaults to false
  bool addUser(const std::string &name, const std::string &password,
               const bool isAdmin = false) {

    // 1. check if name is already taken
    if (searchUser(name) == true) {
      std::cout << "Username " << name << "already taken.\n";
      return false;
    };

    // 2. insert user
    // if transaction fails, nothing happens
    SQLite::Transaction transaction(db);

    // similiar statement as last time
    SQLite::Statement insert(
        db, "INSERT INTO users (name, password, is_admin) VALUES (?, ?, ?)");
    // id is handeld by AUTOINCREMENT

    // binds name
    insert.bind(1, name);
    // binds password
    insert.bind(2, password);

    insert.bind(3, isAdmin);

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

  bool togglePrivileges(const std::string &name) {

    // 1. make sure username exists
    if (searchUser(name) == false) {
      std::cout << "Username does not exist\n";
      return false;
    }

    // 2. toggle privileges
    SQLite::Transaction transaction(db);

    // is_admin = 1 - is_admin toggles between 1 and 0
    // if is_admin = 0, 1 - 0 = 1
    // if is_admin = 1, 1 - 1 = 0
    SQLite::Statement update(
        db, "UPDATE users SET is_admin = 1 - is_admin WHERE name = ?");

    update.bind(1, name);

    int changed = update.exec();

    if (changed == 0) {
      std::cout << "no change made\n";
      return false;
    }

    transaction.commit();

    std::cout << "privileges toggeled\n";
    return true;
  }

  bool getIsAdmin(const std::string &name) {

    if (searchUser(name) == false) {
      std::cout << "Username does not exist";
      return false;
    }

    SQLite::Statement query(db, "SELECT is_admin FROM users WHERE name = ?");

    query.bind(1, name);

    // we can validate input without searchUser because this is a select query
    // otherwise, we use searchUser
    bool userExists = query.executeStep();

    if (!userExists) {
      std::cout << "Username " << name << " not found.\n";
      return false;
    }

    bool isAdmin = query.getColumn(0).getInt();

    if (isAdmin) {
      std::cout << "User " << name << " is an admin";
      return true;
    } else {
      std::cout << "User " << name << " is not an admin";
      return false;
    }
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

  User getUser(const std::string &name) {

    SQLite::Statement query(db, "SELECT * FROM users WHERE name = ?");

    query.bind(1, name);

    // can't return false so throw error if user not found
    if (!query.executeStep()) {
      throw std::runtime_error("Username " + name + " not found");
    }

    User user;

    user.id = query.getColumn(0).getInt();
    user.name = query.getColumn(1).getString();
    user.password = query.getColumn(2).getString();
    user.isAdmin = query.getColumn(3).getInt();

    return user;
  }

  std::vector<User> getListOfUsers() {

    SQLite::Statement query(db, "SELECT name FROM users where id >=0 ");

    std::vector<User> users;

    while (query.executeStep()) {
      // call getUser with the name fetched by query and add to vector
      users.push_back(getUser(query.getColumn(0).getString()));
    }

    return users;
  }

  void loginMenu() {
    bool running = true;
    std::string inputUsername = "";
    std::string inputPassword = "";
    int inputIsAdmin;
    int input = 1;

    while (running) {

      std::cout << "\nMENU\n"
                << "1. Add user\n"
                << "2. Remove user\n"
                << "3. Login\n"
                << "4. List users \n"
                << "5. Toggle privileges\n"
                << "6. Fetch Privileges\n"
                << "7. Return User\n"
                << "0. Quit\n"
                << "Input: ";

      std::cin >> input;

      switch (input) {

      case 1: {
        std::cout << "Username: ";
        std::cin >> inputUsername;
        std::cout << "Password: ";
        std::cin >> inputPassword;
        std::cout << "Is Admin (1 = true, 0 = false): ";
        std::cin >> inputIsAdmin;
        addUser(inputUsername, inputPassword, inputIsAdmin);
        break;
      }
      case 2: {
        std::cout << "Username: ";
        std::cin >> inputUsername;
        removeUser(inputUsername);
        break;
      }
      case 3: {
        std::cout << "Username: ";
        std::cin >> inputUsername;
        std::cout << "Password: ";
        std::cin >> inputPassword;
        loginUser(inputUsername, inputPassword);
        break;
      }
      case 4: {
        // if you're curious
        // https://stackoverflow.com/a/12702744
        std::vector<User> users = getListOfUsers();
        for (const User &i : users) {
          std::cout << "username: " << i.name << "\n";
        }
        break;
      }
      case 5: {
        std::cout << "Username: ";
        std::cin >> inputUsername;
        togglePrivileges(inputUsername);
        break;
      }
      case 6: {
        std::cout << "Username: ";
        std::cin >> inputUsername;
        getIsAdmin(inputUsername);
        break;
      }
      case 7: {
        std::cout << "Username: ";
        std::cin >> inputUsername;
        User user = getUser(inputUsername);
        std::cout << "id: " << user.id << " username: " << user.name
                  << " password: " << user.password
                  << " is_admin: " << user.isAdmin << "\n";
        break;
      }
      case 0: {
        running = false;
        break;
      }
      default: {
        std::cout << "Invalid Input\n";
      }
      }
    }
  }
};

#endif
