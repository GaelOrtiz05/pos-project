#ifndef POS_HPP
#define POS_HPP
#include "database.hpp"
#include "login.hpp"
#include <iostream>
#include <string>

class POS {
private:
  Login login;
  Database pos_db;
  const double SALES_TAX = 1.08;

public:
  POS() {};

  void displayInventory() {

    std::vector<Item> items = pos_db.getItems();

    int totalWidth = 31;
    int colWidth = 15;
    if (items.empty() == true) {
      std::cout << "\nMenu is empty\n";
      return;
    } else {

      std::cout << std::setfill('-') << std::setw(31) << "\n";
      std::cout << std::setfill(' ') << std::setw(25) << std::right
                << "Inventory From DB\n";
      std::cout << std::setfill('-') << std::setw(totalWidth) << "\n";
      std::cout << std::setfill(' ');
      std::cout << std::setw(colWidth) << std::left << "Name" << "|";
      std::cout << std::setw(colWidth) << std::right << "Price\n";
      std::cout << std::setfill('-') << std::setw(totalWidth) << "\n";
      std::cout << std::setfill(' ');

      for (const auto &item : items) {
        std::cout << std::setw(colWidth) << std::left << item.name << "|";
        std::cout << std::setw(colWidth) << std::right << item.price << "\n";
      }

      // display ingredient stock too?

      std::cout << std::setfill('-') << std::setw(31) << "\n";
      std::cout << std::setfill(' ');
    }
  }

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
      case 1:
        std::cout << "This should be the inventory\n";
        break;
      case 2:
        try {
          Login login;
          login.loginMenu();
          break;
        } catch (std::exception &e) {
          std::cerr << "error: " << e.what() << "\n";
          break;
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
