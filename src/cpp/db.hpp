#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

struct Category {
  int id;
  std::string name;
};

struct Ingredient {
  int id;
  std::string name;
  int stock;
};

struct Item {
  int id;
  std::string name;
  double price;
  bool inStock;
  int categoryId;
  std::string categoryName; // not in table, fetched in join select
};

struct ItemIngredient {
  int id;
  std::string name;
  bool isRemovable;
  double priceChange;
};

struct Combo {
  int id;
  std::string name;
  double price;
};

// same struct as item buth with categoryName dropped
struct ComboItem {
  int id;
  std::string name;
  double price;
  bool inStock;
};

struct OrderItem {
  int itemId;
  std::string itemName;
  double itemPrice;
  std::vector<int> removedIngredients;
};

class Database {
private:
  SQLite::Database db;

public:
  Database();
  void setupDatabase();
  void MenuInitialization();
  bool IsInitialized();
  void purchase(const std::vector<OrderItem> &items, double total);
  void DatabaseMenu();

  // insert
  void insertCategory(const std::string &name);
  void insertIngredient(const std::string &name, double price, int stock = 100);
  void insertItem(const std::string &name, double price, int categoryId);
  void insertCombo(const std::string &name, double price);
  void joinIngredientItem(int ingredientId, int itemId, int isRemovable,
                          double priceChange = 0.0);
  void joinComboItem(int comboId, int itemId);
  void addCheckout(int itemId);
  std::vector<OrderItem> getOrder();

  // update
  bool incrementIngredientStock(int ingredientId, int stock);
  bool decrementIngredientStock(int ingredientId, int stock);
  bool incrementIngredientStock(int ingredientId);
  bool decrementIngredientStock(int ingredientId);
  // bool setIngredientStock(int ingredientId, int stock);
  void setIngredientStock(bool increase, const std::string &name,
                          double val = 1);

  // select
  int getCategoryIdByName(std::string &name);
  std::vector<Category> getCategories();
  std::vector<Ingredient> getIngredients();
  std::vector<Item> getCombos();
  std::vector<Item> getItems();
  Item getItem(int itemId);
  std::vector<Item> getItemsByCategory(std::string &name);
  std::vector<ItemIngredient> getItemIngredients(std::string &name);
  std::vector<ComboItem> getComboItems(int comboId);
};

#endif
