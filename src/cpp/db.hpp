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

class Database {
private:
  SQLite::Database db;

public:
  Database();
  void setupDatabase();
  void MenuInitialization();
  bool IsInitialized();
  void purchase();

  // insert
  int insertCategory(const std::string &name);
  int insertIngredient(const std::string &name, double price, int stock = 100);
  int insertItem(const std::string &name, double price, int categoryId);
  int insertCombo(const std::string &name, double price);
  void joinIngredientItem(int ingredientId, int itemId, int isRemovable,
                          double priceChange = 0.0);
  void joinComboItem(int comboId, int itemId);
  void addCheckout(const std::string &item);
  bool incrementIngredientStock(int ingredientId, int stock);
  bool decrementIngredientStock(int ingredientId, int stock);
  bool incrementIngredientStock(int ingredientId);
  bool decrementIngredientStock(int ingredientId);
  bool setIngredientStock(int ingredientId, int stock);
  void setIngredientStock(bool increase, const std::string &name,
                          double val = 1);

  // select
  std::vector<Category> getCategories();
  std::vector<Ingredient> getIngredients();
  std::vector<Combo> getCombos();
  std::vector<Item> getItems();
  std::vector<Item> getItemsByCategory(int categoryId);
  std::vector<ItemIngredient> getItemIngredients();
  std::vector<Item> getComboItems();
};

#endif
