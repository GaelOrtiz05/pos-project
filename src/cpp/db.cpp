#include "db.hpp"

Database::Database()
    : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
  // db.exec("PRAGMA foreign_keys = ON");

  setupDatabase();
}

void Database::setupDatabase() {
  // categories - contains items
  db.exec("CREATE TABLE IF NOT EXISTS categories ("
          "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
          "name                       TEXT NOT NULL"
          ")");

  // items - menu items that belong to a category
  db.exec("CREATE TABLE IF NOT EXISTS items ("
          "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
          "name                       TEXT NOT NULL,"
          "price                      REAL NOT NULL,"
          "in_stock                   INTEGER DEFAULT 1,"
          "category_id                INTEGER NOT NULL,"
          "ingredients                TEXT NOT NULL,"
          "FOREIGN KEY(category_id)   REFERENCES categories(id)"
          ")");

  // ingredients - individual ingredients to track stock
  db.exec("CREATE TABLE IF NOT EXISTS ingredients ("
          "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
          "name                       TEXT NOT NULL,"
          "stock                      INTEGER DEFAULT 100"
          ")");

  // ingredient and item junction table
  db.exec("CREATE TABLE IF NOT EXISTS item_ingredients ("
          "item_id                         INTEGER NOT NULL,"
          "ingredient_id                   INTEGER NOT NULL,"
          "is_removable                    INTEGER DEFAULT 0,"
          "price_change                    REAL NOT NULL,"
          "PRIMARY KEY (item_id, ingredient_id),"
          "FOREIGN KEY (item_id)           REFERENCES items(id),"
          "FOREIGN KEY (ingredient_id)     REFERENCES ingredients(id)"
          ")");

  // combos
  db.exec("CREATE TABLE IF NOT EXISTS combos ("
          "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
          "name                       TEXT NOT NULL,"
          "price                      REAL NOT NULL"
          ")");

  // item and combos junction table
  db.exec("CREATE TABLE IF NOT EXISTS combo_items ("
          "combo_id                INTEGER NOT NULL,"
          "item_id                 INTEGER NOT NULL,"
          "PRIMARY KEY (combo_id, item_id),"
          "FOREIGN KEY (combo_id)  REFERENCES combos(id),"
          "FOREIGN KEY (item_id)   REFERENCES items(id)"
          ")");

  db.exec("CREATE TABLE IF NOT EXISTS checkout ("
          "item             TEXT NOT NULL,"
          "price            DOUBLE NOT NULL,"
          "ingredients      TEXT NOT NULL)");
}

bool Database::IsInitialized() {
  SQLite::Statement query(db, "SELECT COUNT(*)) FROM items");

  int changed = query.exec();

  if (changed == 0) {
    return false;
  }

  return true;
}

void Database::MenuInitialization() {

  if (!IsInitialized()) {

    db.exec(R"SQL(
            INSERT INTO categories (id, name) VALUES
              (1, "Entrees")
              (2, "Sides")
              (3, "Desserts")
              (4, "Drinks")

            INSERT INTO items (id, name, price, in_stock, category_id, )
            )SQL");
  }
}

// Reads checkout table and reduces ingredient stock.
// Uses a TRANSACTION to roll back on error. -M
void Database::purchase() {
  db.exec("BEGIN TRANSACTION");
  try {
    SQLite::Statement query(db, "SELECT ingredients FROM checkout");

    while (query.executeStep()) {
      const char *list = query.getColumn(0).getText();
      if (!list)
        continue;

      std::string ingredientList = list;
      std::cout << ingredientList;

      std::istringstream input(ingredientList);
      std::string item;

      while (std::getline(input, item, ',')) {
        setIngredientStock(false, item);
      }
    }
    db.exec("DELETE FROM checkout;");
    db.exec("COMMIT");
  } catch (const std::exception &e) {
    db.exec("ROLLBACK");
    std::cerr << "Purchase error: " << e.what() << std::endl;
  }
}
