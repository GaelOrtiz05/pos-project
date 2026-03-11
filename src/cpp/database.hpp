#ifndef DATABASE_HPP
#define DATABASE_HPP_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"

struct Ingredient {
  int id; // in my head this would be used by sqlite?
  std::string name;
  bool inStock;  // tracks if it's in stock. Should be greyed out if not
  bool isInItem; // tracks if it's in a given item.
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
  SQLite::Database db;

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
  std::vector<Ingredient> getItemIngredients() {}

  // fetch all items in menu. sort option?
  std::vector<Item> getItems() {}
};

#endif
