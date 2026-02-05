#ifndef POS_HPP
#define POS_HPP
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Item {
  std::string name;
  double price;
};

class POS {
private:
  std::vector<Item> menu;
  const double SALES_TAX = 1.08;

public:
  void addItem(std::string name, double price) {
    menu.push_back({name, price});
  }

  // should remove item from vector depending on string name
  // should then call writeData()
  void removeItem(std::string name) {
    std::cout << "Not yet implemented :)\n";

    // writeData();
  }

  void clear() { menu.clear(); }

  double getTotal() {
    double total = 0;
    for (const auto &item : menu) {
      total += item.price;
    }

    return total * SALES_TAX;
  }

  // basic display function that iterates through the vector
  void display() {

    int totalWidth = 31;
    int colWidth = 15;
    if (menu.empty() == true) {
      std::cout << "\nMenu is empty\n";
      return;
    } else {

      // While still technically displaying the vector, the vector
      // will always mirror the contents of the file
      std::cout << std::setfill('-') << std::setw(31) << "\n";
      std::cout << std::setfill(' ') << std::setw(25) << std::right
                << "Inventory From File\n";
      std::cout << std::setfill('-') << std::setw(totalWidth) << "\n";
      std::cout << std::setfill(' ');
      std::cout << std::setw(colWidth) << std::left << "Name" << "|";
      std::cout << std::setw(colWidth) << std::right << "Price\n";
      std::cout << std::setfill('-') << std::setw(totalWidth) << "\n";
      std::cout << std::setfill(' ');

      for (const auto &item : menu) {
        std::cout << std::setw(colWidth) << std::left << item.name << "|";
        std::cout << std::setw(colWidth) << std::right << item.price << "\n";
      }
      std::cout << std::setfill('-') << std::setw(31) << "\n";
      std::cout << std::setfill(' ');
    }
  }

  // first function called from cppMenu
  // reads from file and adds entries to the menu vector
  void initializeFromFile() {
    std::ifstream fileRead("inventory.txt");
    if (!fileRead.is_open())
      return;

    // calling menu.clear should ensure there are no duplicate entries
    menu.clear();
    std::string name;
    double price;
    char comma;

    // only iterates when both the name and price are succesfully ran
    while (std::getline(fileRead, name, ',') && (fileRead >> price)) {
      addItem(name, price);
      // removes '\n' from buffer to ensure getline works
      fileRead.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    }
    fileRead.close();
  }

  // this fuction mirrors the contents of the vector to the file
  // should enable sorting in the future and item removal of items when
  // implemented
  void writeData() {

    std::ofstream fileWrite;
    fileWrite.open("inventory.txt", std::ios::trunc);

    if (!fileWrite.is_open()) {
      std::cout << "could not open file\n";
      return;
    }

    // saves to file in the format initializeFromFile expects
    for (const auto &item : menu) {
      fileWrite << item.name << ", " << item.price << "\n";
    }

    fileWrite.close();
  }

  void cppMenu() {

    initializeFromFile();

    display();

    int input = -1;
    while (true) {
      std::string inputName = "";
      double inputPrice = 0;

      std::cout << "\nMENU\n"
                << "1. Check Inventory\n"
                << "2. Add To Inventory\n"
                << "3. Remove From Inventory\n"
                << "0. Quit\n"
                << "Input: ";

      std::cin >> input;

      if (input == 0) {
        break;
      }

      switch (input) {
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
        writeData();
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
