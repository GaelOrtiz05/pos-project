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

// Copies items from item table to checkout table when clicked -M
void Database::addCheckout(int itemId) {
  SQLite::Statement query(
      db, "INSERT INTO checkout(item_id, item_name, item_price) "
          "SELECT id, name, price FROM items WHERE id = ?");
  query.bind(1, itemId);
  query.exec();
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

void Database::purchase() {
  SQLite::Statement query(db, "DELETE FROM checkout");
  query.exec();
}
// bool Database::incrementIngredientStock(int ingredientId) { return true; }
// bool Database::decrementIngredientStock(int ingredientId) { return true; }
//
// bool Database::setIngredientStock(int ingredientId, int stock) {
//   SQLite::Statement query(db, "UPDATE ingredients SET stock WHERE id = ?");
//   query.bind(1, ingredientId);
//   int changed = query.exec();
//   if (changed == 0)
//     return false;
//   return true;
// }
//
