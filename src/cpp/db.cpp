#include "db.hpp"

Database::Database()
    : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
  // db.exec("PRAGMA foreign_keys = ON");

  setupDatabase();
  MenuInitialization();
}

void Database::setupDatabase() {
  db.exec(R"SQL(            
    CREATE TABLE IF NOT EXISTS categories (
      id                        INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                                     
      name                      TEXT NOT NULL
    );                                                                                                                                                                                 
                                                                                                                                                                                       
    CREATE TABLE IF NOT EXISTS items (
      id                        INTEGER PRIMARY KEY AUTOINCREMENT,                                                                                                                     
      name                      TEXT NOT NULL,
      price                     REAL NOT NULL,
      category_id               INTEGER NOT NULL,
      in_stock                  INTEGER DEFAULT 1,
      FOREIGN KEY(category_id)  REFERENCES categories(id)
    );                                                                                                                                                                                 
   
    CREATE TABLE IF NOT EXISTS ingredients (                                                                                                                                           
      id                        INTEGER PRIMARY KEY AUTOINCREMENT,
      name                      TEXT NOT NULL,
      stock                     INTEGER DEFAULT 100
    );                                                                                                                                                                                 
   
    CREATE TABLE IF NOT EXISTS item_ingredients (                                                                                                                                      
      item_id                       INTEGER NOT NULL,
      ingredient_id                 INTEGER NOT NULL,
      is_removable                  INTEGER DEFAULT 0,
      price_change                  REAL NOT NULL,
      PRIMARY KEY (item_id, ingredient_id),                                                                                                                                            
      FOREIGN KEY (item_id)         REFERENCES items(id),
      FOREIGN KEY (ingredient_id)   REFERENCES ingredients(id)                                                                                                                         
    );                                    

    CREATE TABLE IF NOT EXISTS combos (
      id                        INTEGER PRIMARY KEY AUTOINCREMENT,
      name                      TEXT NOT NULL,                                                                                                                                         
      price                     REAL NOT NULL
    );                                                                                                                                                                                 
                                          
    CREATE TABLE IF NOT EXISTS combo_items (
      combo_id                INTEGER NOT NULL,
      item_id                 INTEGER NOT NULL,
      PRIMARY KEY (combo_id, item_id),                                                                                                                                                 
      FOREIGN KEY (combo_id)  REFERENCES combos(id),
      FOREIGN KEY (item_id)   REFERENCES items(id)                                                                                                                                     
    );                                    

    CREATE TABLE IF NOT EXISTS orders (
      id                 INTEGER PRIMARY KEY AUTOINCREMENT,
      time               STRING NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')), 
      total              REAL NOT NULL
      );

    CREATE TABLE IF NOT EXISTS order_items (
      id              INTEGER PRIMARY KEY AUTOINCREMENT,
      order_id        INTEGER NOT NULL,
      item_id         INTEGER NOT NULL,
      item_name       TEXT NOT NULL,
      item_price      DOUBLE NOT NULL,
      count           INTEGER NOT NULL,
      FOREIGN KEY (order_id) REFERENCES orders(id)
      );
  )SQL");
}

namespace {
inline bool is_initialized(SQLite::Database &db) {
  SQLite::Statement query(db, "SELECT COUNT(*) FROM categories");
  query.executeStep();
  int count = query.getColumn(0).getInt();
  if (count > 0) {
    return true;
  }
  return false;
}

} // namespace

void Database::MenuInitialization() {
  if (!is_initialized(db)) {
    db.exec(R"SQL(
  BEGIN TRANSACTION;

            INSERT INTO categories (id, name) VALUES
              (1, 'Entrees'),
              (2, 'Sides'),
              (3, 'Desserts'),
              (4, 'Drinks');

            INSERT INTO items (id, name, price, category_id, in_stock) VALUES
              (1,  'Burger'               , 5.99, 1, 1),
              (2,  'Chicken Sandwich'     , 5.49, 1, 1),
              (3,  'Cheese Burger'        , 6.49, 1, 1),
              (4,  'French Fries'         , 1.49, 2, 1),
              (5,  'Onion Rings'          , 1.69, 2, 1),
              (6,  'Chocolate Cake Slice' , 0.99, 3, 1),
              (7,  'Apple Pie'            , 1.89, 3, 1),
              (8,  'Soda'                 , 1.49, 4, 1),
              (9,  'Orange Soda'          , 1.49, 4, 1),
              (10, 'Diet Soda'            , 1.39, 4, 1),
              (11, 'Vanilla Shake'        , 3.99, 4, 1),
              (12, 'Lemonade'             , 3.99, 4, 1),
              (13, 'Orange Juice'         , 3.99, 4, 1);

            INSERT INTO ingredients (id, name, stock) VALUES
              (1, 'Beef Patty'    , 100),
              (2, 'Chicken Patty' , 100),
              (3, 'Bun'           , 100),
              (4, 'Lettuce'       , 100),
              (5, 'Tomato'        , 100),
              (6, 'Pickles'       , 100),
              (7, 'Cheese'        , 100),
              (8, 'Bacon'         , 100);

            INSERT INTO item_ingredients (item_id, ingredient_id, is_removable, price_change) VALUES
             -- Burger
               (1, 1, 0, 0.0), -- Beef Patty 
               (1, 3, 0, 0.0), -- Bun
               (1, 4, 1, 0.0), -- Lettuce
               (1, 5, 1, 0.0), -- Tomato
               (1, 6, 1, 0.0), -- Pickles

            -- Chicken Sandwhich
               (2, 2, 0, 0.0), -- Chicken Patty 
               (2, 3, 0, 0.0), -- Bun
               (2, 4, 1, 0.0), -- Lettuce
               (2, 5, 1, 0.0), -- Tomato
               (2, 6, 1, 0.0), -- Pickles

            -- Cheese Burger
               (3, 1, 0, 0.0), -- Beef Patty 
               (3, 3, 0, 0.0), -- Bun
               (3, 4, 1, 0.0), -- Lettuce
               (3, 5, 1, 0.0), -- Tomato
               (3, 6, 1, 0.0), -- Pickles
               (3, 7, 1, 0.0), -- Cheese
               (3, 8, 1, 0.0); -- Bacon

            INSERT INTO combos (id, name, price) VALUES
              (1, 'Burger Combo', 9.99),
              (2, 'Chicken Sandwhich Combo', 9.99),
              (3, 'Cheese Burger Combo', 9.99);

            INSERT INTO combo_items (combo_id, item_id) VALUES
            -- Burger Combo
              (1, 1), -- Burger
              (1, 4), -- French Fries
              (1, 8), -- Soda

            -- Chicken Sandwhich Combo
              (2, 2), -- Chicken Sandwich 
              (2, 4), -- French Fries
              (2, 8), -- Soda

            -- Cheese Burger Combo
              (3, 3),   -- Cheese Burger
              (3, 5),   -- Onion Rings
              (3, 11);  -- Vanilla Shake

             COMMIT;
            )SQL");
  }
}

namespace {
inline void print_categories(Database &db) {
  std::vector<Category> outputCategories = db.getCategories();
  std::cout << "Categories\n";
  for (const auto &c : outputCategories) {
    std::cout << "Category: " << c.name << "\n";
  }
}
inline void print_items(Database &db) {
  std::vector<Item> outputItems = db.getItems();
  std::cout << "Items\n";

  for (const auto &i : outputItems) {
    std::cout << "Item: " << i.name << "\n";
  }
}

inline void print_ingredients(Database &db) {
  std::vector<Ingredient> outputIngredients = db.getIngredients();
  std::cout << "Ingredients: \n";
  for (const auto &i : outputIngredients) {
    std::cout << "Id: " << i.id << ", ";
    std::cout << "Name: " << i.name << ", ";
    std::cout << "Stock: " << i.stock << "\n";
  }
}

inline void print_item_ingredients(Database &db) {
  std::cout << "Item ID: \n";
  int inputItemId;
  std::cin >> inputItemId;

  std::vector<ItemIngredient> itemIngredients =
      db.getItemIngredients(inputItemId);

  for (const auto &ii : itemIngredients) {
    std::cout << "Id: " << ii.id << ", ";
    std::cout << "Name: " << ii.name << ", ";
    std::cout << "Is Removable: " << ii.isRemovable << ", ";
    std::cout << "Price Change: " << ii.priceChange << "\n";
  }
}

inline void print_combos(Database &db) {
  std::vector<Item> outputCombos = db.getCombos();
  std::cout << "Combos: \n";

  for (const auto &c : outputCombos) {
    std::cout << "Id: " << c.id << ", ";
    std::cout << "Name: " << c.name << ", ";
    std::cout << "Price: " << c.price << "\n";
  }
}

inline void print_combo_items(Database &db) {
  int inputCombo;
  std::cout << "Combo #: \n";
  std::cin >> inputCombo;

  std::vector<ComboItem> outputComboItems = db.getComboItems(inputCombo);

  for (const auto &c : outputComboItems) {
    std::cout << "Id: " << c.id << ", ";
    std::cout << "Name: " << c.name << ", ";
    std::cout << "Price: " << c.price << ", ";
    std::cout << "Available: " << c.inStock << "\n";
  }
}

inline void print_orders(Database &db) {
  std::vector<Order> allOrders = db.getOrders();
  std::cout << "All Orders:\n";

  for (const auto &o : allOrders) {
    std::cout << "Id: " << o.id << ", ";
    std::cout << "Time " << o.time << ", ";
    std::cout << "Total: " << o.total << "\n";
  }
}
inline void print_order_items(Database &db) {
  int orderId;
  std::cout << "Order ID: \n";
  std::cin >> orderId;
  std::vector<OrderItem> orderItems = db.getOrderItemsById(orderId);
  std::cout << "Order Items for order " << orderId << ":\n";

  for (const auto &oi : orderItems) {
    std::cout << "Order Id: " << oi.orderId << ", ";
    std::cout << "Name: " << oi.itemName << ", ";
    std::cout << "Price: " << oi.itemPrice << ", ";
    std::cout << "Count: " << oi.count << "\n";
  }
}

void print_headers() {
  std::cout << "\nMENU\n"
            << "1. Get Categories\n"
            << "2. Get Items\n"
            << "3. Get Ingredients\n"
            << "4. Get Item Ingredients\n"
            << "5. Get Combos\n"
            << "6. Get Combo Items\n"
            << "7. Get All Order Items\n"
            << "8. Get Order Items by Order ID\n"
            << "0. Quit\n"
            << "Input: ";
}
} // namespace

void database_menu(Database &db) {
  bool running = true;
  int input = 1;

  while (running) {
    print_headers();
    std::cin >> input;
    switch (input) {
    case 1:
      print_categories(db);
      break;
    case 2:
      print_items(db);
      break;
    case 3:
      print_ingredients(db);
      break;
    case 4:
      print_item_ingredients(db);
      break;
    case 5:
      print_combos(db);
      break;
    case 6:
      print_combo_items(db);
      break;
    case 7:
      print_orders(db);
      break;
    case 8:
      print_order_items(db);
      break;
    case 0:
      running = false;
      break;
    default:
      std::cout << "Invalid Input\n";
    }
  }
}
