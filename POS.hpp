#ifndef POS_HPP
#define POS_HPP
#include <iostream>
#include <string>
#include <vector>

struct Item {
  std::string name;
  double price;
};

class POS {
private:
  std::vector<Item> cart;
  const double SALES_TAX = 1.08;

public:
  void addItem(std::string name, double price) {
    cart.push_back({name, price});
  }

  void clear() { cart.clear(); }

  double getTotal() {
    double total = 0;
    for (const auto &item : cart) {
      total += item.price;
    }

    return total * SALES_TAX;
  }

  // meant for debugging
  void initialize() {
    std::vector<Item> menu = {{"Salad", 8.00}, {"Patty Melt", 5.49}};

    for (const auto &item : menu) {
      addItem(item.name, item.price);
    }
  }

  // meant for debugging
  void display() {
    if (cart.empty() == true) {
      std::cout << "\nCart is empty\n";
    } else {
      for (const auto &item : cart) {
        std::cout << "Name: " << item.name << "\n";
        std::cout << "Price: " << item.price << "\n";
      }
    }
  }
};

#endif
