#include "SQLiteCpp/Statement.h"
#include "db.hpp"

void Database::Insert_Into_Category_Table(const std::string &name) {
  SQLite::Statement insert(db, "INSERT INTO categories (name) VALUES(?)");
  insert.bind(1, name);
  insert.exec();
}

void Database::Insert_Into_Ingredient_Table(const std::string &name, double price, int stock) {
  SQLite::Statement insert(db, "INSERT INTO ingredients (name, price, stock) VALUES (?,?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.bind(3, stock);
  insert.exec();
}

void Database::Insert_Into_Item_Table(const std::string &name, double price, int categoryId) {
  SQLite::Statement insert(db, "INSERT INTO items (name, price, category_id) VALUES (?,?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.bind(3, categoryId);
  insert.exec();
}

void Database::Insert_Into_Combo_Table(const std::string &name, double price) {
  SQLite::Statement insert(db, "INSERT INTO combos (name, price) VALUES (?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.exec();
}

void Database::Combine_Into_IngredientItem_Table(int ingredientId, int itemId, int isRemovable, double priceChange) {
  SQLite::Statement insert(db, "INSERT INTO item_ingredients (item_id, ingredient_id, is_removable, price_change) VALUES (?,?,?,?)");
  insert.bind(1, itemId);
  insert.bind(2, ingredientId);
  insert.bind(3, isRemovable);
  insert.bind(4, priceChange);
  insert.exec();
}

void Database::Combine_Into_ComboItem_Table(int comboId, int itemId) {
  SQLite::Statement insert(db, "INSERT INTO combo_items (combo_id, item_id) VALUES (?,?)");
  insert.bind(1, comboId);
  insert.bind(2, itemId);
  insert.exec();
}

bool Database::Decrement_Ingredient_Stock_Of_Item(int itemId) {
  std::vector<ItemIngredient> Vector_Of_Ingredients = Get_Vector_ItemIngredients_by_ItemID(itemId);

  for (const auto &ingredient : Vector_Of_Ingredients) {
    if (ingredient.stock < 1)
      return false;
  }

  SQLite::Statement decrement(
      db, "UPDATE ingredients SET stock = stock - 1 WHERE id = ?");

  for (const auto &ingredient : Vector_Of_Ingredients) {
    decrement.bind(1, ingredient.id);
    decrement.exec();
    decrement.reset();
  }
  return true;
}

bool Database::Increment_Ingredient_Stock_Of_Item(int itemId) {
  std::vector<ItemIngredient> Vector_Of_Ingredients = Get_Vector_ItemIngredients_by_ItemID(itemId);

  SQLite::Statement increment(
      db, "UPDATE ingredients SET stock = stock + 1 WHERE id = ?");

  for (const auto &ingredient : Vector_Of_Ingredients) {
    increment.bind(1, ingredient.id);
    increment.exec();
    increment.reset();
  }
  return true;
}

void Database::Inc_Dec_Ingredient_Stock(bool increase_isTRUE, const std::string &name, double value) {
  if (increase_isTRUE) {
    SQLite::Statement increase(db, "UPDATE ingredients SET stock = stock + ? WHERE name = ?");
    increase.bind(1, value);
    increase.bind(2, name);
    increase.exec();
  }
  else {
    SQLite::Statement decrease(db, "UPDATE ingredients SET stock = stock - ? WHERE name = ?");
    decrease.bind(1, value);
    decrease.bind(2, name);
    decrease.exec();
  }
}

void Database::Add_Item_Into_Checkout_Table(int itemId) {
  SQLite::Statement query(
      db, "INSERT INTO checkout(item_id, item_name, item_price) "
          "SELECT id, name, price FROM items WHERE id = ?");
  query.bind(1, itemId);
  query.exec();
}

void Database::Process_Purchase(const std::vector<OrderItem> &Vector_Of_Items, double total) {
  SQLite::Transaction tx(db);

  SQLite::Statement insertOrderId(db, R"SQL(INSERT INTO orders (total) VALUES (?) )SQL");
  // insert total
  insertOrderId.bind(1, total);
  insertOrderId.exec();
  int orderId = static_cast<int>(db.getLastInsertRowid());

  SQLite::Statement Insert_Items_Into_OrderItems(db, R"SQL(
                                       INSERT INTO order_items (order_id, item_id, item_name, item_price, count)
                                       VALUES (?,?,?,?,?)
                                       )SQL");

  for (const auto &item : Vector_Of_Items) {
    Insert_Items_Into_OrderItems.bind(1, orderId);
    Insert_Items_Into_OrderItems.bind(2, item.itemId);
    Insert_Items_Into_OrderItems.bind(3, item.itemName);
    Insert_Items_Into_OrderItems.bind(4, item.itemPrice);
    Insert_Items_Into_OrderItems.bind(5, item.count);
    Insert_Items_Into_OrderItems.exec();
    Insert_Items_Into_OrderItems.reset();
  }

  tx.commit();
}
