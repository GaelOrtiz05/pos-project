#ifndef POS_HPP
#define POS_HPP
#include "db.hpp"
#include "login.hpp"
#include <iomanip>
#include <iostream>
#include <string>

class POS {
private:
  Login login;
  Database database;
  const double SALES_TAX = 1.08;

public:
  POS() {};
  void TopMenu() {

    bool running = true;
    int input;
    std::string inputName = "";
    double inputPrice = 0;

    while (running) {
      std::cout << "\nMENU\n"
                << "1. Inventory\n"
                << "2. Login Menu\n"
                << "0. Quit\n"
                << "Input: ";

      std::cin >> input;

      switch (input) {

      case 1: {
        try {
          database_menu(database);
          break;
        } catch (std::exception &e) {
          std::cerr << "error: " << e.what() << "\n";
          break;
        }
        break;
      }

      case 2: {
        try {
          login_menu(login);
          break;
        } catch (std::exception &e) {
          std::cerr << "error: " << e.what() << "\n";
          break;
        }
      }
      case 0:
        running = false;
        break;

      default:
        std::cout << "Invalid Input\n";
        break;
      }
    }
  }
};

#endif
