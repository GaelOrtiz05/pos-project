#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"
//added vvv
#include <sstream>
#include <stdexcept>
//-----------------


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
};

struct ItemIngredient {
  int id;
  std::string name;
  // should keep track of item removal
  // and price adjustmen
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

          //hard-coded sample data -M
      addDefaultItems();
      addDefaultIngredients();

      //Table to track items added to checkout                     // item             price   ingredients
      db.exec("CREATE TABLE IF NOT EXISTS checkout("               // Cheeseburger     2.99    "bun,beef,cheese,lettuce,tomato,bun"
          "item             TEXT NOT NULL,"                        // Cheeseburger     4.99    "bun,beef,cheese,lettuce,tomato,bun"
          "price            DOUBLE NOT NULL,"                      // Chicken Nuggets  3.99    "chicken"
          "ingredients      TEXT NOT NULL); ");
  }

  //sample data
void addDefaultItems();
void addDefaultIngredients();

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

  int insertCombo() { return 0; }

  // ingredient functions
  bool incrementIngredientStock(int ingredientId) { return true; }
  bool decrementIngredientStock(int ingredientId) { return true; }
  bool setIngredientStock(int ingredientId, const int stock) { return true; }

  // join functions

  // join ingredient to item (item_ingredients)
  void joinIngredientItem(int ingredientId, int itemId) {}
  // join combo to item (combo_items)
  void joinComboItem(int comboId, int itemId) {}

  // get functions
  std::vector<Item> getItems() {}
  std::vector<Item> getItemsByCategory() {}
  std::vector<Combo> getCombos() {}
  std::vector<Ingredient> getIngredients() {}
  std::vector<ItemIngredient> getItemIngredients() {}

  // runs once on first launch
  void MenuInitialization() {
    // categories
    int categoryMeals = insertCategory("Meals");
    int categoryDrinks = insertCategory("Drinks");
    int categoryDeserts = insertCategory("Deserts");
    // ingredients
    int ingredientBun = insertIngredient("Bun", .50, 100);
    // items
    int itemBurger = insertItem("Burger", 5.99, categoryMeals);
    // joinIngredientItem(itemBurger, ingredientBun);
  }

  //added by M
// ----------------------------------------------------------------------------------------
// update ingredient stock. used to either decrement stock on successful
  // order, or set to a value to emulate additional stock arriving
void setIngredientStock(bool increase, const std::string& name, double val = 1) {
    //Determine whether we are decreasing or increasing

      //increate == true -> increase stock
    if (increase) {
        SQLite::Statement query(db,
            "UPDATE ingredients SET stock = stock + ? WHERE name = ?");

        query.bind(1, val);
        query.bind(2, name);
        query.exec();
    }
    else {
        SQLite::Statement query(db,
            "UPDATE ingredients SET stock = stock - ? WHERE name = ?");

        query.bind(1, val);
        query.bind(2, name);
        query.exec();
    }
}

//Copies items from item table to checkout table when clicked -M
void addCheckout(const std::string& item) {
    SQLite::Statement query(db,
        "INSERT INTO checkout(item,price,ingredients) SELECT name,price,ingredients FROM items WHERE name = ?");
    query.bind(1, item);
    query.exec();
    //Copies the item name, price, and ingredient list
}


//Reads checkout table and reduces the stock of ingredients in the ingredients table
  //uses a try/catch and TRANSACTION(sequence of statements) to prevent errors -M
void purchase() {
    db.exec("BEGIN TRANSACTION");
    try {
        SQLite::Statement query(db,
            "SELECT ingredients FROM checkout");

        while (query.executeStep()) {
            const char* list = query.getColumn(0).getText();
            if (!list) continue;

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
    }
    catch (const std::exception& e) {
        db.exec("ROLLBACK");
        std::cerr << "Purchase error: " << e.what() << std::endl;
    }
}
};

//SAMPLE HARDCODED DATA FOR TABLES -M
void Database::addDefaultItems() {
    db.exec("INSERT into items (name,price,ingredients)"
        " VALUES('Cheeseburger',2.99,'bun,beef,cheese,lettuce,tomato,bun'); ");
    db.exec("INSERT into items (name,price,ingredients)"
        " VALUES('Double Cheeseburger', 4.99,'bun,beef,beef,cheese,lettuce,tomato,bun'); ");

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
