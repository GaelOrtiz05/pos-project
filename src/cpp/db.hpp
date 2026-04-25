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
  int stock;
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

struct Order {
  int id;
  std::string time;
  double total;
};

struct OrderItem {
  int orderId;
  int itemId;
  std::string itemName;
  double itemPrice;
  int count; // amount
  std::vector<int> removedIngredients;
};

class Database {
private:
  SQLite::Database db;

public:
  Database();

  // initialization
  void setupDatabase();
  void MenuInitialization();
  void purchase(const std::vector<OrderItem> &items, double total);

  // insert
  void insertCategory(const std::string &name);
  void insertIngredient(const std::string &name, double price, int stock = 100);
  void insertItem(const std::string &name, double price, int categoryId);
  void insertCombo(const std::string &name, double price);
  void joinIngredientItem(int ingredientId, int itemId, int isRemovable,
                          double priceChange = 0.0);
  void joinComboItem(int comboId, int itemId);
  void addCheckout(int itemId);
  std::vector<Order> getOrders();

  // update
  bool incrementIngredientStock(int ingredientId, int stock);
  bool decrementIngredientStock(int ingredientId, int stock);
  bool incrementIngredientStock(int ingredientId);
  bool decrementIngredientStock(int ingredientId);
  void setIngredientStock(bool increase, const std::string &name,
                          double val = 1);
  bool decrementStock(int itemId);
  bool incrementStock(int itemId);

  // select
  int getCategoryIdByName(std::string &name);
  std::vector<Category> getCategories();
  std::vector<Ingredient> getIngredients();
  std::vector<Item> getCombos();
  std::vector<Item> getItems();
  Item getItem(int itemId);
  std::vector<Item> getItemsByCategory(std::string &name);
  std::vector<ItemIngredient> getItemIngredients(int itemId);
  std::vector<ComboItem> getComboItems(int comboId);
  std::vector<OrderItem> getOrderItemsById(int orderId);
};

void database_menu(Database &db);

#endif
