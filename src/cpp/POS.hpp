#ifndef POS_HPP
#define POS_HPP
#include "database.hpp"
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

class POS {
private:
  Database db;
  const double SALES_TAX = 1.08;

public:
  // Constructor should call getItems which returns vector of all items
  // POS() { menu = db.getItems(); }

  void addItem(std::string name, double price) {
    // db.addItem() to add to db
  }

  void removeItem(std::string &name) {
    // if name == name
    // db.removeItem() to remove from db
  }

  double getTotal() {
    // std::vector<Item> items = db.getItems();
    // for loop
    // int total += item.price;
    // return total * SALES_TAX;
  }

  void display() {

    std::vector<Item> items = db.getItems();

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

  void cppMenu() {

    display();

    int input = -1;
    while (true) {
      std::string inputName = "";
      double inputPrice = 0;

      std::cin >> input;

      if (input == 0) {
        break;
      }

      switch (input) {

        std::cout << "\nMENU\n"
                  << "1. Check Inventory\n"
                  << "2. Add To Inventory\n"
                  << "3. Remove From Inventory\n"
                  << "0. Quit\n"
                  << "Input: ";
      case 1:
        display();
        break;

      case 2:
        // removes '\n\' from buffer to prevent getline from reading it
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        std::cout << "Name: ";
        std::getline(std::cin, inputName);
        std::cout << "Price: ";
        std::cin >> inputPrice;
        addItem(inputName, inputPrice);
        break;
      case 3:
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        std::cout << "Input Name of Item to Remove: ";
        std::getline(std::cin, inputName);
        removeItem(inputName);
        break;

      default:
        std::cout << "Invalid Input\n";
        break;
      }
    }
  }
};

#endif
