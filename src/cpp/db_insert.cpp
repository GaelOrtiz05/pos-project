#include "SQLiteCpp/Statement.h"
#include "db.hpp"

void Database::insertCategory(const std::string &name) {
  SQLite::Statement insert(db, "INSERT INTO categories (name) VALUES(?)");
  insert.bind(1, name);
  insert.exec();
}

void Database::insertIngredient(const std::string &name, double price,
                                int stock) {
  SQLite::Statement insert(
      db, "INSERT INTO ingredients (name, price, stock) VALUES (?,?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.bind(3, stock);
  insert.exec();
}

void Database::insertItem(const std::string &name, double price,
                          int categoryId) {
  SQLite::Statement insert(
      db, "INSERT INTO items (name, price, category_id) VALUES (?,?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.bind(3, categoryId);
  insert.exec();
}

void Database::insertCombo(const std::string &name, double price) {
  SQLite::Statement insert(db, "INSERT INTO combos (name, price) VALUES (?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.exec();
}

void Database::joinIngredientItem(int ingredientId, int itemId, int isRemovable,
                                  double priceChange) {
  SQLite::Statement insert(
      db, "INSERT INTO item_ingredients (item_id, "
          "ingredient_id, is_removable, price_change) VALUES (?,?,?,?)");
  insert.bind(1, itemId);
  insert.bind(2, ingredientId);
  insert.bind(3, isRemovable);
  insert.bind(4, priceChange);
  insert.exec();
}

void Database::joinComboItem(int comboId, int itemId) {
  SQLite::Statement insert(
      db, "INSERT INTO combo_items (combo_id, item_id) VALUES (?,?)");
  insert.bind(1, comboId);
  insert.bind(2, itemId);
  insert.exec();
}

void Database::setIngredientStock(bool increase, const std::string &name,
                                  double val) {
  if (increase) {
    SQLite::Statement query(
        db, "UPDATE ingredients SET stock = stock + ? WHERE name = ?");
    query.bind(1, val);
    query.bind(2, name);
    query.exec();
  } else {
    SQLite::Statement query(
        db, "UPDATE ingredients SET stock = stock - ? WHERE name = ?");
    query.bind(1, val);
    query.bind(2, name);
    query.exec();
  }
}

void Database::addCheckout(int itemId) {
  SQLite::Statement query(
      db, "INSERT INTO checkout(item_id, item_name, item_price) "
          "SELECT id, name, price FROM items WHERE id = ?");
  query.bind(1, itemId);
  query.exec();
}

void Database::purchase(const std::vector<OrderItem> &items, double total) {
  SQLite::Transaction tx(db);

  SQLite::Statement insertOrderId(db, R"SQL(
                                  INSERT INTO orders (total)
                                  VALUES (?)
  )SQL");

  // insert total
  insertOrderId.bind(1, total);
  insertOrderId.exec();
  int orderId = static_cast<int>(db.getLastInsertRowid());

  SQLite::Statement insertOrderItems(db, R"SQL(
                                       INSERT INTO order_items (order_id, item_id, item_name, item_price)
                                       VALUES (?,?,?,?)
                                       )SQL");

  SQLite::Statement decrementStock(db, R"SQL(
                                   UPDATE ingredients SET stock = stock - 1
                                   WHERE id IN (
                                     SELECT ingredient_id
                                     FROM item_ingredients
                                     WHERE item_id = ?
                                   )
                                   )SQL");
  // for loop to insert every item
  // decrements stock
  for (const auto &oi : items) {

    insertOrderItems.bind(1, orderId);
    insertOrderItems.bind(2, oi.itemId);
    insertOrderItems.bind(3, oi.itemName);
    insertOrderItems.bind(4, oi.itemPrice);
    insertOrderItems.exec();
    insertOrderItems.reset();

    decrementStock.bind(1, oi.itemId);
    decrementStock.exec();
    decrementStock.reset();
  }

  tx.commit();
}
