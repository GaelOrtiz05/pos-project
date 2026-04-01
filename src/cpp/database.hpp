#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"

struct Category {
  int id;
  std::string name;
};

struct Ingredient {
  int id;
  std::string name;
  int stock; // tracks if it's in stock. Should be greyed out if not
};

struct Item {
  int id;
  std::string name;
  double price;
  bool inStock; // tracks availability
  int categoryId;
  std::string
      categoryName; // not in database, should be fetched in select query
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
  Database() : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    setupDatabase();
  };

  void setupDatabase() {

    // categories - contains items
    db.exec("CREATE TABLE IF NOT EXISTS categories ("
            "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name                       TEXT NOT NULL"
            ")");

    // items - menu items that belong to category
    db.exec("CREATE TABLE IF NOT EXISTS items ("
            "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name                       TEXT NOT NULL,"
            "price                      INTEGER NOT NULL,"
            "in_stock                   INTEGER DEFAULT 1,"
            "category_id                INTEGER NOT NULL,"
            "category_name              TEXT NOT NULL"
            "FOREIGN KEY(category_id)   REFERENCES categories(id)"
            ")");

    // ingredients - individual ingredients to track stock
    db.exec("CREATE TABLE IF NOT EXISTS ingredients ("
            "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name                       TEXT NOT NULL,"
            "stock                      INTEGER DEFAULT 100"
            ")");

    // ingredient and item junction table
    // tracks which items belong to which ingredients and vice versa
    db.exec("CREATE TABLE IF NOT EXISTS item_ingredients"
            "item_id                         INTEGER NOT NULL,"
            "ingredient_id                   INTEGER NOT NULL,"
            "is_removable                    INTEGER DEFAULT 0"
            "price_change                    INTEGER NOT NULL"
            "PRIMARY KEY (item_id, ingredient_id),"
            "FOREIGN KEY (item_id)           REFERENCES items(id),"
            "FOREIGN KEY (ingredient_id)     REFERENCES ingredients(id)"
            ")");

    // combos
    db.exec("CREATE TABLE IF NOT EXISTS combos ("
            "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name                       TEXT NOT NULL,"
            "price                      INTEGER NOT NULL"
            ")");

    // item and combos junction table
    db.exec("CREATE TABLE IF NOT EXISTS combo_items"
            "combo_id                INTEGER NOT NULL,"
            "item_id                 INTEGER NOT NULL,"
            "PRIMARY KEY (combo_id, item_id),"
            "FOREIGN KEY (combo_id)  REFERENCES combos(id),"
            "FOREIGN KEY (item_id)   REFERENCES items(id)"
            ")");

    // also need to work out orders, order_items tables
  }

  // insertion functions
  int insertCategory(const std::string &name) {
    SQLite::Statement insert(db, "INSERT INTO categories (name) VALUES (?)");
    insert.bind(1, name);

    insert.exec();
    // returns last inserted id
    // .getLastInsertRowid should return int64_t so static cast?
    // could also just use int64_t directly
    return static_cast<int>(db.getLastInsertRowid());
  };

  int insertIngredient(const std::string name, double price, int stock = 100) {
    SQLite::Statement insert(
        db, "INSERT INTO ingredients (name, price, stock) VALUE (?,?,?)");
    insert.bind(1, name);
    insert.bind(2, price);
    insert.bind(3, stock);
    insert.exec();
    return static_cast<int>(db.getLastInsertRowid());
  }

  int insertItem(const std::string &name, double price, int categoryId) {
    SQLite::Statement insert(
        db, "INSERT INTO items (name, price, category_id) VALUES (?,?,?)");
    insert.bind(1, name);
    insert.bind(2, price);
    insert.bind(3, categoryId);
    insert.exec();
    return static_cast<int>(db.getLastInsertRowid());
  }

  int insertCombo(const std::string &name, double price) {
    SQLite::Statement insert(db,
                             "INSERT INTO combos (name, price) VALUES (?,?)");
    insert.bind(1, name);
    insert.bind(2, price);
    insert.exec();
    return static_cast<int>(db.getLastInsertRowid());
  }

  // ingredient functions
  bool incrementIngredientStock(int ingredientId, int stock) { return true; }
  bool decrementIngredientStock(int ingredientId, int stock) { return true; }
  bool setIngredientStock(int ingredientId, int stock) { return true; }

  // join functions

  // join ingredient to item (item_ingredients)
  void joinIngredientItem(int ingredientId, int itemId, int isRemovable,
                          double priceChange = 0.0) {
    SQLite::Statement insert(
        db, "INSERT INTO item_ingredients (item_id, "
            "ingredient_id, is_removable, price_change) VALUES (?,?,?,?)");
    insert.bind(1, itemId);
    insert.bind(2, ingredientId);
    insert.bind(3, isRemovable);
    insert.bind(4, priceChange);
    insert.exec();
  }
  // join combo to item (combo_items)
  void joinComboItem(int comboId, int itemId) {
    SQLite::Statement insert(
        db, "INSERT INTO combo_items (combo_id, item_id) VALUES (?,?) ");
    insert.bind(1, comboId);
    insert.bind(2, itemId);
    insert.exec();
  }

  // get functions

  std::vector<Category> getCategories() {
    SQLite::Statement query(db, "SELECT id, name FROM categories");

    std::vector<Category> categories;

    while (query.executeStep()) {
      Category category;
      category.id = query.getColumn(0).getInt();
      category.name = query.getColumn(1).getString();
    }

    return categories;
  }

  std::vector<Ingredient> getIngredients() {
    SQLite::Statement query(db, "SELECT id, name, stock");

    std::vector<Ingredient> ingredients;

    while (query.executeStep()) {
      Ingredient ingredient;
      ingredient.id = query.getColumn(0).getInt();
      ingredient.name = query.getColumn(1).getInt();
      ingredient.stock = query.getColumn(2).getInt();
    }

    return ingredients;
  }

  std::vector<Combo> getCombos() {
    SQLite::Statement query(db, "SELECT id, name FROM combos");

    std::vector<Combo> combos;
    while (query.executeStep()) {
      Combo combo;
      combo.id = query.getColumn(0).getInt();
      combo.name = query.getColumn(1).getString();
      combos.push_back(combo);
    }

    return combos;
  }

  std::vector<Item> getItems() {
    SQLite::Statement query(
        db, "SELECT i.id, i.name, i.price, i.in_stock, i.category_id, "
            "c.name "
            "FROM items i JOIN categories c ON i.category_id = c.id");
    std::vector<Item> items;

    while (query.executeStep()) {
      Item item;
      item.id = query.getColumn(0).getInt();
      item.name = query.getColumn(1).getString();
      item.price = query.getColumn(2).getInt();
      item.inStock = query.getColumn(3).getInt();
      item.categoryId = query.getColumn(4).getInt();
      item.categoryName = query.getColumn(5).getString();
      items.push_back(item);
    }

    return items;
  }

  std::vector<Item> getItemsByCategory(int categoryId) {
    SQLite::Statement query(
        db, "SELECT i.id, i.name, i.price, i.in_stock, i.category_id, c.name "
            "FROM items i JOIN categories c "
            "ON i.category_id = c.id "
            "WHERE category_id = ?");

    query.bind(1, categoryId);

    std::vector<Item> items;

    while (query.executeStep()) {
      Item item;
      item.id = query.getColumn(0).getInt();
      item.name = query.getColumn(1).getString();
      item.price = query.getColumn(2).getInt();
      item.inStock = query.getColumn(3).getInt();
      item.categoryId = query.getColumn(4).getInt();
      item.categoryName = query.getColumn(5).getString();
      items.push_back(item);
    }

    return items;
  }

  std::vector<ItemIngredient> getItemIngredients() {}
  // should return a vector of all the Items within the combo
  std::vector<Item> getComboItems() {}

  // runs once on first launch
  void MenuInitialization() {
    // categories
    int categoryMeals = insertCategory("Meals");
    int categorySides = insertCategory("Sides");
    int categoryDeserts = insertCategory("Deserts");
    int categoryDrinks = insertCategory("Drinks");

    // ingredients
    int ingredientBun = insertIngredient("Bun", .50, 100);
    int ingredientPatty = insertIngredient("Patty", 1.00, 100);
    int ingredientTomato = insertIngredient("Tomato", .50, 100);
    int ingredientLettuce = insertIngredient("Lettuce", .50, 100);
    int ingredientPickles = insertIngredient("Pickles", .25, 100);
    int ingredientAmericanCheese =
        insertIngredient("American Cheese", .50, 100);
    int ingredientPepperJackCheese =
        insertIngredient("Pepper Jack Cheese", .75, 100);
    // items
    int itemBurger = insertItem("Burger", 5.99, categoryMeals);
    joinIngredientItem(itemBurger, ingredientBun, false, 0.0);
    joinIngredientItem(itemBurger, ingredientPatty, false, 0.0);
    joinIngredientItem(itemBurger, ingredientAmericanCheese, true, 0.0);
    joinIngredientItem(itemBurger, ingredientPickles, true, 0.0);
  }
};

#endif
