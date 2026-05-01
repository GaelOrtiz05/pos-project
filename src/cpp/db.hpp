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
  void Setup_Database();
  void Initalize_Menu();
  void Process_Purchase(const std::vector<OrderItem> &items, double total);

  // insert
  void Insert_Into_Category_Table(const std::string &name);
  void Insert_Into_Ingredient_Table(const std::string &name, double price, int stock = 100);
  void Insert_Into_Item_Table(const std::string &name, double price, int categoryId);
  void Insert_Into_Combo_Table(const std::string &name, double price);
  
  void Combine_Into_IngredientItem_Table(int ingredientId, int itemId, int isRemovable, double priceChange = 0.0);
  void Combine_Into_ComboItem_Table(int comboId, int itemId);
  void Add_Item_Into_Checkout_Table(int itemId);
  std::vector<Order> Get_Vector_Orders();

  // update stock
  bool Check_Ingredient_Stock_Of_Item(int itemID);
  void Inc_Dec_Ingredient_Stock(bool increase_isTRUE, const std::string &name, double val = 1);
  bool Decrement_Ingredient_Stock_Of_Item(int itemId);
  bool Increment_Ingredient_Stock_Of_Item(int itemId);

  // select
  int Get_CategoryID_By_Name(std::string &name);
  std::vector<Category> Get_Vector_Categories();
  std::vector<Ingredient> Get_Vector_Ingredients();
  std::vector<Item> Get_Vector_Combos();
  std::vector<Item> Get_Vector_Items();
  Item Get_Struct_Item(int itemId);
  std::vector<Item> Get_Vector_Items_By_Category(std::string &name);
  std::vector<ItemIngredient> Get_Vector_ItemIngredients_by_ItemID(int itemId);
  std::vector<ComboItem> Get_Vector_ComboItems_by_ComboID(int comboId);
  std::vector<OrderItem> Get_Vector_OrderItems_By_OrderID(int orderId);
};

void database_menu(Database &db);

#endif
