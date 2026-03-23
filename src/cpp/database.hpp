#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"

struct Ingredient {
  int id; // in my head this would be used by sqlite?
  std::string name;
  bool inStock;          // tracks if it's in stock. Should be greyed out if not
  bool isBaseIngredient; // tracks if it's in a base ingredient.
};

struct Item {
  int id; // in my head this would be used by sqlite?
  std::string name;
  double price;
  std::vector<Ingredient>
      ingredients; // each item will have a initialized vector with the base
                   // ingredients. enables customization.
};

class Database {
private:
  SQLite::Database pos_db;

public:
  // add unique item to menu
  void addItem() {}

  // add unique ingredient to menu
  void addIngredient() {}

  // update ingredient stock. used to either decrement stock on successful
  // order, or set to a value to emulate additional stock arriving
  void setIngredientStock() {}

  // delete an item based on an id?
  void removeItem() {}

  // delete an ingredient based on an id?
  void removeIngredient() {}

  // Used to fetch and display ingredient list. should also fetch availability
  std::vector<Ingredient> getItemIngredients() { return {}; }

  // fetch all items in menu. sort option?
  std::vector<Item> getItems() { return {}; }
};

#endif

// void addItem(std::string name, double price) {
//   // db.addItem() to add to db
// }
//
// void removeItem(std::string &name) {
//   // if name == name
//   // db.removeItem() to remove from db
// }
//
// double getTotal() {
//   // std::vector<Item> items = db.getItems();
//   // for loop
//   // int total += item.price;
//   // return total * SALES_TAX;
//
//   return 0;
// }
//
// void display() {
//
//   std::vector<Item> items = pos_db.getItems();
//
//   int totalWidth = 31;
//   int colWidth = 15;
//   if (items.empty() == true) {
//     std::cout << "\nMenu is empty\n";
//     return;
//   } else {
//
//     std::cout << std::setfill('-') << std::setw(31) << "\n";
//     std::cout << std::setfill(' ') << std::setw(25) << std::right
//               << "Inventory From DB\n";
//     std::cout << std::setfill('-') << std::setw(totalWidth) << "\n";
//     std::cout << std::setfill(' ');
//     std::cout << std::setw(colWidth) << std::left << "Name" << "|";
//     std::cout << std::setw(colWidth) << std::right << "Price\n";
//     std::cout << std::setfill('-') << std::setw(totalWidth) << "\n";
//     std::cout << std::setfill(' ');
//
//     for (const auto &item : items) {
//       std::cout << std::setw(colWidth) << std::left << item.name << "|";
//       std::cout << std::setw(colWidth) << std::right << item.price << "\n";
//     }
//
//     // display ingredient stock too?
//
//     std::cout << std::setfill('-') << std::setw(31) << "\n";
//     std::cout << std::setfill(' ');
//   }
// }
