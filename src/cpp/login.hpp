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
  int role; // 0 = emp, 1 = admin, 2 = owner

  bool isAdmin() const { return role >= 1; }
};

class Login {
private:
  SQLite::Database LOGIN_DB;

  void Setup_Database() {

    LOGIN_DB.exec("CREATE TABLE IF NOT EXISTS users ("
            "  id       INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  name     TEXT NOT NULL,"
            "  password TEXT NOT NULL,"
            "  role     INTEGER DEFAULT 0"
            ")");

    // if (User_Exists("admin") == false) {
    //   initializeAdminPassword();
    // }
  }

public:
  bool User_Exists(const std::string &name) {

    SQLite::Statement user_count(LOGIN_DB, "SELECT COUNT(*) FROM users WHERE name = ?");
    user_count.bind(1, name);
    user_count.executeStep();

    // after running user_count, it returns a result table with one column
    // .getColumn(0) gets the result and getInt() makes sure it's an int.
    int count_of_users = user_count.getColumn(0).getInt();

    if (count_of_users > 0) {
      return true;
    } else {
      return false;
    }
  }

  Login() : LOGIN_DB("data/login.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    Setup_Database();
  };

  bool Add_User_To_Table(const std::string &name, const std::string &password,const int role = 0) {

    // 1. check if name is already taken
    if (User_Exists(name) == true) {
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
    SQLite::Transaction transaction(LOGIN_DB);

    // similiar statement as last time
    SQLite::Statement insert(LOGIN_DB, "INSERT INTO users (name, password, role) VALUES (?, ?, ?)");
    // id is handeld by AUTOINCREMENT
    
    // binds name
    insert.bind(1, name);
    // binds password
    insert.bind(2, stored_hash);

    insert.bind(3, role);

    // .exec() is for writes with insert,delete,update
    insert.exec();

    // commits transaction
    transaction.commit();

    std::cout << "User " << name << " registered successfully.\n";
    return true;
  }

  bool Remove_User_From_Table(const std::string &name, const int role_of_requestor) {

    SQLite::Statement role_query(LOGIN_DB, "SELECT role FROM users WHERE name = ?");
    role_query.bind(1, name);

    if (!role_query.executeStep()) {
      std::cout << "Username " << name << "not found.\n";
      return false;
    }

    int role_of_removee = role_query.getColumn(0).getInt();

    if (role_of_removee >= 2) {
      std::cout << "Owner cannot be removed.\n";
      return false;
    }

    if (role_of_requestor <= role_of_removee) {
      std::cout << "Insufficient privileges to remove " << name << ".\n";
      return false;
    }

    SQLite::Transaction transaction(LOGIN_DB);

    SQLite::Statement delete_query(LOGIN_DB, "DELETE FROM users WHERE name = ?");
  
    delete_query.bind(1, name);

    // .exec() returns amount of rows changed
    // should be 1 if user is deleted
    int rows_changed = delete_query.exec();

    if (rows_changed == 0) {
      std::cout << "Username " << name << "not found.\n";
      return false;
    }

    transaction.commit();

    std::cout << "Username " << name << "deleted.\n";
    return true;
  }

  bool Get_User_IsAdmin(const std::string &name) {

    if (User_Exists(name) == false) {
      std::cout << "Username does not exist";
      return false;
    }

    SQLite::Statement role_query(LOGIN_DB, "SELECT role FROM users WHERE name = ?");

    role_query.bind(1, name);

    // we can validate input without searchUser because this is a select query
    // otherwise, we use searchUser
    bool userExists = role_query.executeStep();

    if (!userExists) {
      std::cout << "Username " << name << " not found.\n";
      return false;
    }

    int user_role = role_query.getColumn(0).getInt();

    if (user_role >= 1) {
      std::cout << "User " << name << " is an admin";
      return true;
    } else {
      std::cout << "User " << name << " is not an admin";
      return false;
    }
  }

  bool Process_Login_User(const std::string &name, const std::string &password) {

    // match name to password
    SQLite::Statement select_password(LOGIN_DB, "SELECT password FROM users WHERE name = ?");

    select_password.bind(1, name);

    // returns false if user doesn't exist
    // .executeStep() returns true if a row is fetched
    bool userExists = select_password.executeStep();

    if (!userExists) {
      std::cout << "Username " << name << "not found.\n";
      return false;
    }

    std::string stored_hash = select_password.getColumn(0).getString();

    if (!check_password(password.c_str(), stored_hash.c_str())) {
      std::cout << "wrong password";
      return false;
    }
    std::cout << "login successful\n";
    return true;
  }

  User Get_User(const std::string &name) {

    SQLite::Statement select_user(LOGIN_DB, "SELECT * FROM users WHERE name = ?");

    select_user.bind(1, name);

    // can't return false so throw error if user not found
    if (!select_user.executeStep()) {
      throw std::runtime_error("Username " + name + " not found");
    }

    User user;

    user.id = select_user.getColumn(0).getInt();
    user.name = select_user.getColumn(1).getString();
    user.password = select_user.getColumn(2).getString();
    user.role = select_user.getColumn(3).getInt();

    return user;
  }

  std::vector<User> Get_Vector_Users() {

    SQLite::Statement select_user(
        LOGIN_DB, "SELECT name FROM users where id >=0 ORDER BY role DESC, name ASC");

    std::vector<User> vector_of_users;

    while (select_user.executeStep()) {
      // call Get_User with the name fetched by query and add to vector
      vector_of_users.push_back(Get_User(select_user.getColumn(0).getString()));
    }

    return vector_of_users;
  }
};

namespace {
inline void Add_User(Login &login) {
  std::string input_username;
  std::string input_password;
  int input_role;
  std::cout << "Username: ";
  std::cin >> input_username;
  std::cout << "Password: ";
  std::cin >> input_password;
  std::cout << "Role (0 = employee, 1 = admin, 2 = owner): ";
  std::cin >> input_role;
  login.Add_User_To_Table(input_username, input_password, input_role);
}

inline void Remove_User(Login &login) {
  std::string input_username;
  std::cout << "Username: ";
  std::cin >> input_username;
  login.Remove_User_From_Table(input_username, 2);
}

inline void Login_User(Login &login) {
  std::string input_username;
  std::string input_password;
  std::cout << "Username: ";
  std::cin >> input_username;
  std::cout << "Password: ";
  std::cin >> input_password;
  login.Process_Login_User(input_username, input_password);
}

inline void List_Users(Login &login) {
  // if you're curious
  // https://stackoverflow.com/a/12702744
  std::vector<User> vector_of_users = login.Get_Vector_Users();

  for (const User &user : vector_of_users) {
    std::cout << "username: " << user.name << "\n";
  }
}

inline void Fetch_Privileges(Login &login) {
  std::string input_username;
  std::cout << "Username: ";
  std::cin >> input_username;
  login.Get_User_IsAdmin(input_username);
}

inline void Return_User(Login &login) {
  std::string input_username;
  std::cout << "Username: ";
  std::cin >> input_username;
  User user = login.Get_User(input_username);
  std::cout << "id: " << user.id << " username: " << user.name
            << " password: " << user.password << " role: " << user.role << "\n";
}

inline void Print_Headers() {
  std::cout << "\nMENU\n"
            << "1. Add user\n"
            << "2. Remove user\n"
            << "3. Login\n"
            << "4. List users \n"
            << "5. Fetch Privileges\n"
            << "6. Return User\n"
            << "0. Quit\n"
            << "Input: ";
}
} // namespace

inline void Login_Menu(Login &login) {
  bool running = true;
  int menu_selection = 1;

  while (running) {
    Print_Headers();
    std::cin >> menu_selection;
    
    switch (menu_selection) {
    case 1:
      Add_User(login);
      break;
    case 2:
      Remove_User(login);
      break;
    case 3:
      Login_User(login);
      break;
    case 4:
      List_Users(login);
      break;
    case 5:
      Fetch_Privileges(login);
      break;
    case 6:
      Return_User(login);
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
