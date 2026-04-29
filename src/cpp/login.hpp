#ifndef LOGIN_HPP
#define LOGIN_HPP

#include "login_pass_hash.hpp"
#include <SQLiteCpp/SQLiteCpp.h>
#include <iostream>
#include <string>

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

    db.exec("CREATE TABLE IF NOT EXISTS users ("
            "  id       INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  name     TEXT NOT NULL,"
            "  password TEXT NOT NULL,"
            "  is_admin INTEGER DEFAULT 0"
            ")");

    // if (searchUser("admin") == false) {
    //   initializeAdminPassword();
    // }
  }

public:
  bool searchUser(const std::string &name) {

    SQLite::Statement query(db, "SELECT COUNT(*) FROM users WHERE name = ?");
    query.bind(1, name);
    query.executeStep();

    // after running query, it returns a result table with one column
    // .getColumn(0) gets the result and getInt() makes sure it's an int.
    int count = query.getColumn(0).getInt();

    if (count > 0) {
      return true;
    } else {
      return false;
    }
  }

  Login() : db("data/login.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    setupDatabase();
  };

  // void initializeAdminPassword() {
  //   std::string password;
  //   std::cout << "First-time setup. Set admin password: ";
  //   std::cin >> password;
  //   addUser("admin", password, true);
  // }

  // if a parameter is not given for isAdmin, defaults to false
  bool addUser(const std::string &name, const std::string &password,
               const bool isAdmin = false) {

    // 1. check if name is already taken
    if (searchUser(name) == true) {
      std::cout << "Username " << name << "already taken.\n";
      return false;
    };

    // 2. hash password
    char stored_hash[crypto_pwhash_STRBYTES];

    if (hash_password(password.c_str(), stored_hash) != 0) {
      std::cout << "hash failed\n";
      return false;
    }

    // 3. insert user
    // if transaction fails, nothing happens
    SQLite::Transaction transaction(db);

    // similiar statement as last time
    SQLite::Statement insert(
        db, "INSERT INTO users (name, password, is_admin) VALUES (?, ?, ?)");
    // id is handeld by AUTOINCREMENT

    // binds name
    insert.bind(1, name);
    // binds password
    insert.bind(2, stored_hash);

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

    std::string stored_hash = statement.getColumn(0).getString();

    if (!check_password(password.c_str(), stored_hash.c_str())) {
      std::cout << "wrong password";
      return false;
    }
    std::cout << "login successful\n";
    return true;
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

    SQLite::Statement query(
        db,
        "SELECT name FROM users where id >=0 ORDER BY is_admin DESC, name ASC");

    std::vector<User> users;

    while (query.executeStep()) {
      // call getUser with the name fetched by query and add to vector
      users.push_back(getUser(query.getColumn(0).getString()));
    }

    return users;
  }
};

namespace {
inline void add_user(Login &login) {
  std::string inputUsername;
  std::string inputPassword;
  int inputIsAdmin;
  std::cout << "Username: ";
  std::cin >> inputUsername;
  std::cout << "Password: ";
  std::cin >> inputPassword;
  std::cout << "Is Admin (1 = true, 0 = false): ";
  std::cin >> inputIsAdmin;
  login.addUser(inputUsername, inputPassword, inputIsAdmin);
}

inline void remove_user(Login &login) {
  std::string inputUsername;
  std::cout << "Username: ";
  std::cin >> inputUsername;
  login.removeUser(inputUsername);
}

inline void login_user(Login &login) {
  std::string inputUsername;
  std::string inputPassword;
  std::cout << "Username: ";
  std::cin >> inputUsername;
  std::cout << "Password: ";
  std::cin >> inputPassword;
  login.loginUser(inputUsername, inputPassword);
}

inline void list_users(Login &login) {
  // if you're curious
  // https://stackoverflow.com/a/12702744
  std::vector<User> users = login.getListOfUsers();
  for (const User &i : users) {
    std::cout << "username: " << i.name << "\n";
  }
}

inline void toggle_privileges(Login &login) {
  std::string inputUsername;
  std::cout << "Username: ";
  std::cin >> inputUsername;
  login.togglePrivileges(inputUsername);
}

inline void fetch_privileges(Login &login) {
  std::string inputUsername;
  std::cout << "Username: ";
  std::cin >> inputUsername;
  login.getIsAdmin(inputUsername);
}

inline void return_user(Login &login) {
  std::string inputUsername;
  std::cout << "Username: ";
  std::cin >> inputUsername;
  User user = login.getUser(inputUsername);
  std::cout << "id: " << user.id << " username: " << user.name
            << " password: " << user.password << " is_admin: " << user.isAdmin
            << "\n";
}

inline void print_headers() {
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
}
} // namespace

inline void login_menu(Login &login) {
  bool running = true;
  int input = 1;

  while (running) {
    print_headers();
    std::cin >> input;
    switch (input) {
    case 1:
      add_user(login);
      break;
    case 2:
      remove_user(login);
      break;
    case 3:
      login_user(login);
      break;
    case 4:
      list_users(login);
      break;
    case 5:
      toggle_privileges(login);
      break;
    case 6:
      fetch_privileges(login);
      break;
    case 7:
      return_user(login);
      break;
    case 0:
      running = false;
      break;
    default:
      std::cout << "Invalid Input\n";
    }
  }
}

#endif
