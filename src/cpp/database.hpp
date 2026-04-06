#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"
// added vvv
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>
#include <iostream>
//-----------------

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
<<<<<<< HEAD

public:
  Database() : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    db.exec("PRAGMA foreign_keys = ON");

    setupDatabase();
  };

=======
>>>>>>> c79c6ce995caf775088b027646118db1504efc4b
  void setupDatabase() {

    // categories - contains items
    // db.exec("CREATE TABLE IF NOT EXISTS categories ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL"
    //         ")");

    // items - menu items that belong to category
<<<<<<< HEAD
    db.exec("CREATE TABLE IF NOT EXISTS items ("
            "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name                       TEXT NOT NULL,"
            "price                      REAL NOT NULL,"
            "in_stock                   INTEGER DEFAULT 1,"
            "category_id                INTEGER NOT NULL,"
            "FOREIGN KEY(category_id)   REFERENCES categories(id)"
            "ingredients                TEXT NOT NULL"
            ")");
=======
    // db.exec("CREATE TABLE IF NOT EXISTS items ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL,"
    //         "price                      INTEGER NOT NULL,"
    //         "in_stock                   INTEGER DEFAULT 1,"
    //         "category_id                INTEGER NOT NULL,"
    //         "FOREIGN KEY(category_id)   REFERENCES categories(id)"
    //         "ingredients                TEXT NOT NULL"
    //         ")");
>>>>>>> c79c6ce995caf775088b027646118db1504efc4b

    // ingredients - individual ingredients to track stock
    // db.exec("CREATE TABLE IF NOT EXISTS ingredients ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL,"
    //         "stock                      INTEGER DEFAULT 100"
    //         ")");

    // ingredient and item junction table
    // tracks which items belong to which ingredients and vice versa
<<<<<<< HEAD
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

    // also need to work out orders, order_items tables

    // hard-coded sample data -M
    addDefaultItems();
    addDefaultIngredients();
=======
    // db.exec("CREATE TABLE IF NOT EXISTS item_ingredients"
    //         "item_id                         INTEGER NOT NULL,"
    //         "ingredient_id                   INTEGER NOT NULL,"
    //         "PRIMARY KEY (item_id, ingredient_id),"
    //         "FOREIGN KEY (item_id)           REFERENCES items(id),"
    //         "FOREIGN KEY (ingredient_id)     REFERENCES ingredients(id)"
    //         ")");

    // combos
    // db.exec("CREATE TABLE IF NOT EXISTS combos ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL,"
    //         "price                      INTEGER NOT NULL"
    //         ")");

    // item and combos junction table
    // db.exec("CREATE TABLE IF NOT EXISTS combo_items"
    //         "combo_id                INTEGER NOT NULL,"
    //         "item_id                 INTEGER NOT NULL,"
    //         "PRIMARY KEY (combo_id, item_id),"
    //         "FOREIGN KEY (combo_id)  REFERENCES combos(id),"
    //         "FOREIGN KEY (item_id)   REFERENCES items(id)"
    //         ")");

    // also need to work out orders, order_items tables


    //Table to store items                                       // ID  name                 price  ingredients
    db.exec("CREATE TABLE IF NOT EXISTS items ("                 // 01  Cheeseburger         2.99   "bun,beef,cheese,lettuce,tomato,bun"
          "id               INTEGER PRIMARY KEY AUTOINCREMENT,"    // 02  Double Cheeseburger  4.99   "bun,beef,beef,cheese,lettuce,tomato,bun"
          "name             TEXT NOT NULL,"                        // 03  Chicken Nuggets      3.99   "chicken"
          "price            DOUBLE NOT NULL,"
          "ingredients      TEXT NOT NULL);");

    db.exec("CREATE TABLE IF NOT EXISTS ingredients( "           // 01  bun      10
          "id               integer PRIMARY KEY AUTOINCREMENT,"    // 02  beef     10
          "name             TEXT NOT NULL,"                        // 03  chicke   10
          "stock            DOUBLE NOT NULL);");

          //hard-coded sample data -M
      addDefaultItems();
      addDefaultIngredients();
>>>>>>> c79c6ce995caf775088b027646118db1504efc4b

    // Table to track items added to checkout                     // item price
    // ingredients
    db.exec(
        "CREATE TABLE IF NOT EXISTS checkout(" // Cheeseburger     2.99
                                               // "bun,beef,cheese,lettuce,tomato,bun"
        "item             TEXT NOT NULL," // Cheeseburger     4.99
                                          // "bun,beef,cheese,lettuce,tomato,bun"
        "price            DOUBLE NOT NULL," // Chicken Nuggets  3.99 "chicken"
        "ingredients      TEXT NOT NULL); ");
  }

<<<<<<< HEAD
  // sample data
  void addDefaultItems();
  void addDefaultIngredients();
=======
public:
  Database() : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    setupDatabase();
  };

  //sample data
void addDefaultItems();
void addDefaultIngredients();
>>>>>>> c79c6ce995caf775088b027646118db1504efc4b

  // insertion functions
//   int insertCategory(const std::string &name) {
//     SQLite::Statement insert(db, "INSERT INTO categories (name) VALUES (?)");
//     insert.bind(1, name);

    // insert.exec();
    // returns last inserted id
    // .getLastInsertRowid should return int64_t so static cast?
    // could also just use int64_t directly
//     return static_cast<int>(db.getLastInsertRowid());
//   };

//   int insertIngredient(const std::string name, double price, int stock = 100) {
//     SQLite::Statement insert(
//         db, "INSERT INTO ingredients (name, price, stock) VALUE (?,?,?)");
//     insert.bind(1, name);
//     insert.bind(2, price);
//     insert.bind(3, stock);
//     insert.exec();
//     return static_cast<int>(db.getLastInsertRowid());
//   }

//   int insertItem(const std::string &name, double price, int categoryId) {
//     SQLite::Statement insert(
//         db, "INSERT INTO items (name, price, category_id) VALUES (?,?,?)");
//     insert.bind(1, name);
//     insert.bind(2, price);
//     insert.bind(3, categoryId);
//     insert.exec();
//     return static_cast<int>(db.getLastInsertRowid());
//   }

<<<<<<< HEAD
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
  bool setIngredientStock(int ingredientId, int stock) {
    SQLite::Statement query(db, "UPDATE ingredients SET stock WHERE id = ?");
    query.bind(1, ingredientId);

    int changed = query.exec();
  }
=======
//   int insertCombo() { return 0; }

  // ingredient functions
//   bool incrementIngredientStock(int ingredientId) { return true; }
//   bool decrementIngredientStock(int ingredientId) { return true; }
//   bool setIngredientStock(int ingredientId, const int stock) { return true; }
>>>>>>> c79c6ce995caf775088b027646118db1504efc4b

  // join functions

  // join ingredient to item (item_ingredients)
<<<<<<< HEAD
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
      ingredients.push_back(ingredient);
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
=======
//   void joinIngredientItem(int ingredientId, int itemId) {}
  // join combo to item (combo_items)
//   void joinComboItem(int comboId, int itemId) {}

    // get functions
    std::vector<Item> getItems() {}
    std::vector<Item> getItemsByCategory() {}
    std::vector<Combo> getCombos() {}
    std::vector<Ingredient> getIngredients() {}
    std::vector<ItemIngredient> getItemIngredients() {}

    // runs once on first launch
//   void MenuInitialization() {
//     // categories
//     int categoryMeals = insertCategory("Meals");
//     int categoryDrinks = insertCategory("Drinks");
//     int categoryDeserts = insertCategory("Deserts");
//     // ingredients
//     int ingredientBun = insertIngredient("Bun", .50, 100);
//     // items
//     int itemBurger = insertItem("Burger", 5.99, categoryMeals);
//     // joinIngredientItem(itemBurger, ingredientBun);
//   }
>>>>>>> c79c6ce995caf775088b027646118db1504efc4b

  // added by M
  // ----------------------------------------------------------------------------------------
  // update ingredient stock. used to either decrement stock on successful
  // order, or set to a value to emulate additional stock arriving
  void setIngredientStock(bool increase, const std::string &name,
                          double val = 1) {
    // Determine whether we are decreasing or increasing

    // increate == true -> increase stock
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

  // Copies items from item table to checkout table when clicked -M
  void addCheckout(const std::string &item) {
    SQLite::Statement query(
        db, "INSERT INTO checkout(item,price,ingredients) SELECT "
            "name,price,ingredients FROM items WHERE name = ?");
    query.bind(1, item);
    query.exec();
    // Copies the item name, price, and ingredient list
  }

  // Reads checkout table and reduces the stock of ingredients in the
  // ingredients table uses a try/catch and TRANSACTION(sequence of statements)
  // to prevent errors -M
  void purchase() {
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
};

// SAMPLE HARDCODED DATA FOR TABLES -M
void Database::addDefaultItems() {
  db.exec(
      "INSERT into items (name,price,ingredients)"
      " VALUES('Cheeseburger',2.99,'bun,beef,cheese,lettuce,tomato,bun'); ");
  db.exec("INSERT into items (name,price,ingredients)"
          " VALUES('Double Cheeseburger', "
          "4.99,'bun,beef,beef,cheese,lettuce,tomato,bun'); ");

  db.exec("INSERT into items (name,price,ingredients)"
          " VALUES('Chicken Nuggets', 3.99, 'chicken'); ");
  db.exec("INSERT into items (name,price,ingredients)"
          " VALUES('Chicken Tenders', 4.99, 'chicken'); ");

  db.exec("INSERT into items (name,price,ingredients)"
          " VALUES('Hot Dog', 2.99, 'bun,beef'); ");

  db.exec("INSERT into items (name,price,ingredients)"
          " VALUES('Medium Drink', 1.99, 'cup'); ");
}
void Database::addDefaultIngredients() {
  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('bun',10); ");

  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('beef',10); ");

  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('chicken',10); ");

  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('tomato',10); ");

  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('cheese',10); ");

  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('lettuce',10); ");

  db.exec("INSERT INTO ingredients(name, stock)"
          " VALUES('cup',10); ");
}

#endif
