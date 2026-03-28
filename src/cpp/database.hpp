#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"

struct Ingredient {
  int id;
  int count;             // tracks if it's in stock. Should be greyed out if not
  bool isBaseIngredient; // tracks if it's in a base ingredient.
};

struct Item {
  int id;
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
  Database()
      : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
          // setupDatabase();
        };

  void setupDatabase() {
    db.exec("CREATE TABLE IF NOT EXISTS items ("
            "id               INTEGER PRIMARY KEY AUTOINCREMENT"
            "name             TEXT NOT NULL"
            "count            INTEGER NOT NULL"
            "isBaseIngredient INTEGER NOT NULL");
  }
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
