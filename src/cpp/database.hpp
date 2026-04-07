#ifndef DATABASE_HPP
#define DATABASE_HPP
#include "SQLiteCpp/Database.h"
#include "SQLiteCpp/SQLiteCpp.h"
//added vvv
#include <sstream>
#include <stdexcept>
#include <vector>
#include <iostream>
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
    void setupDatabase() {

    // categories - contains items
    // db.exec("CREATE TABLE IF NOT EXISTS categories ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL"
    //         ")");

    // items - menu items that belong to category
    // db.exec("CREATE TABLE IF NOT EXISTS items ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL,"
    //         "price                      INTEGER NOT NULL,"
    //         "in_stock                   INTEGER DEFAULT 1,"
    //         "category_id                INTEGER NOT NULL,"
    //         "FOREIGN KEY(category_id)   REFERENCES categories(id)"
    //         "ingredients                TEXT NOT NULL"
    //         ")");

    // ingredients - individual ingredients to track stock
    // db.exec("CREATE TABLE IF NOT EXISTS ingredients ("
    //         "id                         INTEGER PRIMARY KEY AUTOINCREMENT,"
    //         "name                       TEXT NOT NULL,"
    //         "stock                      INTEGER DEFAULT 100"
    //         ")");

    // ingredient and item junction table
    // tracks which items belong to which ingredients and vice versa
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


        
          //We have 4 categories: 1-Entrees, 2-Sides, 3-Dessert, 4-Drinks
          //Table to store items                                        // ID  name                 price  ingredients
        db.exec("CREATE TABLE IF NOT EXISTS items ("                  // 01  Cheeseburger         2.99   "bun,beef,cheese,lettuce,tomato,bun"
          "id               INTEGER PRIMARY KEY AUTOINCREMENT,"   // 02  Double Cheeseburger  4.99   "bun,beef,beef,cheese,lettuce,tomato,bun"
          "name             TEXT NOT NULL UNIQUE,"                       // 03  Chicken Nuggets      3.99   "chicken"
          "price            DOUBLE NOT NULL,"
          "Ingredient_id    INTEGER NOT NULL,"
          "category_id      INTEGER NOT NULL);");

        db.exec("CREATE TABLE IF NOT EXISTS ingredients( "            // 01  bun       10
            "id               integer PRIMARY KEY AUTOINCREMENT,"   // 02  beef      10
            "name             TEXT NOT NULL,"                       // 03  chicken   10
            "stock            DOUBLE NOT NULL);");

          //hard-coded sample data -M
        if(db.execAndGet("SELECT COUNT(*) FROM items").getInt() == 0) {
            addDefaultItems();
        }
        if (db.execAndGet("SELECT COUNT(*) FROM ingredients").getInt() == 0) {
            addDefaultIngredients();
        }

        // Clear checkout table when program opens anew.
        db.exec("DROP TABLE IF EXISTS checkout;");
    

        //Table to track items added to checkout                     // item             price   ingredients
        db.exec("CREATE TABLE IF NOT EXISTS checkout("               // Cheeseburger     2.99    "bun,beef,cheese,lettuce,tomato,bun"
            "item             TEXT NOT NULL,"                        // Cheeseburger     4.99    "bun,beef,cheese,lettuce,tomato,bun"
            "price            DOUBLE NOT NULL,"                      // Chicken Nuggets  3.99    "chicken"
            "ingredient_id    INTEGER NOT NULL); ");
  }

public:
  Database() : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
    setupDatabase();
  };

  //sample data
void addDefaultItems();
void addDefaultIngredients();

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

//   int insertCombo() { return 0; }

  // ingredient functions
//   bool incrementIngredientStock(int ingredientId) { return true; }
//   bool decrementIngredientStock(int ingredientId) { return true; }
//   bool setIngredientStock(int ingredientId, const int stock) { return true; }

  // join functions

  // join ingredient to item (item_ingredients)
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

  //added by M
// ----------------------------------------------------------------------------------------
// update ingredient stock. used to either decrement stock on successful
  // order, or set to a value to emulate additional stock arriving
void setIngredientStock(bool increase, int id, double val = 1) {
    //Determine whether we are decreasing or increasing

      //increate == true -> increase stock
    if (increase) {
        SQLite::Statement query(db,
            "UPDATE ingredients SET stock = stock + ? WHERE id = ?");

        query.bind(1, val);
        query.bind(2, id);
        query.exec();
    }
    else {
        SQLite::Statement query(db,
            "UPDATE ingredients SET stock = stock - ? WHERE id = ?");

        query.bind(1, val);
        query.bind(2, id);
        query.exec();
    }
}

//Copies items from item table to checkout table when clicked -M
void addCheckout(int item) {
    SQLite::Statement query(db,
        "INSERT INTO checkout(item,price,ingredient_id) SELECT name,price,ingredient_id FROM items WHERE id = ?");
    query.bind(1, item);
    std::cout << item << " added to checkout." << std::endl;
    query.exec();
    //Copies the item name, price, and ingredient list
}

int getCartCount() {
    int test = db.execAndGet("SELECT COUNT(*) FROM checkout").getInt();
    std::cout << "Cart amount: " << test << std::endl;
    return test;
}
std::string getCheckoutName(int row) {
    
    SQLite::Statement query(db,
        "SELECT item FROM checkout LIMIT 1 OFFSET ?");
        query.bind(1, row);

    if (query.executeStep()) {
    std::string item = query.getColumn(0).getText();
    return item;
    }
    else {
        return "Empty";
    }
}
double getCheckoutPrice(int row) {
    SQLite::Statement query(db,
        "SELECT price FROM checkout LIMIT 1 OFFSET ?");
        query.bind(1, row);

    if (query.executeStep()) {
    double price = query.getColumn(0).getDouble();
    return price;
    }
    else {
        return 0.0;
    }
}

//Reads checkout table and reduces the stock of ingredients in the ingredients table
  //uses a try/catch and TRANSACTION(sequence of statements) to prevent errors -M
void purchase() {
    db.exec("BEGIN TRANSACTION");
    try {
        SQLite::Statement query(db,
            "SELECT ingredient_id FROM checkout");

        while (query.executeStep()) {
            int id = query.getColumn(0).getInt();
            if (!id) continue;

            std::cout << "Ingredient ID: " << id << std::endl;
            
            
            while (id > 0) {
                int item = id % 10;
                setIngredientStock(false, item);
                id /= 10;
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
    //1 - Entrees
    //01 - Cheeseburger
    //02 - Double Cheeseburger
    //03 - Chicken Nuggets
    //04 - Chicken Tenders
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Cheeseburger',2.99,125641,1); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Double Cheeseburger', 4.99,1225641,1); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Chicken Nuggets', 3.99,3,1); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Chicken Tenders', 4.99,3,1); ");

    //2 - Sides
    //05 - Small Fries
    //06 - Medium Fries
    //07 - Large Fries
    //08 - XL Fries
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Small Fries', 0.99,8,2); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Medium Fries', 1.99,8,2); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Large Fries', 2.99,8,2); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('XL Fries', 3.99,8,2); ");

    //4 - Drinks
    //09 - Small Drink
    //10 - Medium Drink
    //11 - Large Drink
    //12 - XL Drink
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Small Drink', 0.99,7,4); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Medium Drink', 1.99, 7,4); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('Large Drink', 2.99,7,4); ");
    db.exec("INSERT into items (name,price,ingredient_id,category_id)"
        " VALUES('XL Drink', 3.99,7,4); ");
}
void Database::addDefaultIngredients() {
    //01 - bun
    //02 - beef
    //03 - chicken
    //04 - tomato
    //05 - cheese
    //06 - lettuce
    //07 - cup
    //08 - potato
    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('buns',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('beef',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('chicken',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('tomatos',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('cheese',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('lettuce',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('cups',100); ");

    db.exec("INSERT INTO ingredients(name, stock)"
        " VALUES('potatoes',100); ");
}

#endif
