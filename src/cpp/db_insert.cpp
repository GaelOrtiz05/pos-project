#include "db.hpp"

int Database::insertCategory(const std::string &name) {
  SQLite::Statement insert(db, "INSERT INTO categories (name) VALUES(?)");
  insert.bind(1, name);
  insert.exec();
  return static_cast<int>(db.getLastInsertRowid());
}

int Database::insertIngredient(const std::string &name, double price,
                               int stock) {
  SQLite::Statement insert(
      db, "INSERT INTO ingredients (name, price, stock) VALUES (?,?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.bind(3, stock);
  insert.exec();
  return static_cast<int>(db.getLastInsertRowid());
}

int Database::insertItem(const std::string &name, double price,
                         int categoryId) {
  SQLite::Statement insert(
      db, "INSERT INTO items (name, price, category_id) VALUES (?,?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.bind(3, categoryId);
  insert.exec();
  return static_cast<int>(db.getLastInsertRowid());
}

int Database::insertCombo(const std::string &name, double price) {
  SQLite::Statement insert(db, "INSERT INTO combos (name, price) VALUES (?,?)");
  insert.bind(1, name);
  insert.bind(2, price);
  insert.exec();
  return static_cast<int>(db.getLastInsertRowid());
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
void Database::addCheckout(const std::string &item) {
  SQLite::Statement query(db,
                          "INSERT INTO checkout(item,price,ingredients) SELECT "
                          "name,price,ingredients FROM items WHERE name = ?");
  query.bind(1, item);
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
