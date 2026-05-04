#include "db.hpp"

Database::Database()
    : db("data/pos.db", SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE) {
  // db.exec("PRAGMA foreign_keys = ON");

  Setup_Database();
  Initalize_Menu();
}

void Database::Setup_Database() {
  db.exec(R"SQL(
    CREATE TABLE IF NOT EXISTS categories (
      id                        INTEGER PRIMARY KEY AUTOINCREMENT,
      name                      TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS items (
      id                        INTEGER PRIMARY KEY AUTOINCREMENT,
      name                      TEXT NOT NULL,
      image                     TEXT,
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

    CREATE TABLE IF NOT EXISTS checkout_items (
      id              INTEGER PRIMARY KEY AUTOINCREMENT,
      item_id         INTEGER NOT NULL,
      item_name       TEXT NOT NULL,
      item_price      DOUBLE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS checkout_ingredients (
      id              INTEGER PRIMARY KEY AUTOINCREMENT,
      item_id         INTEGER NOT NULL,
      ingredient_id   INTEGER NOT NULL
    );
  )SQL");
}

namespace {
inline bool is_initialized(SQLite::Database &db) {
  SQLite::Statement count_categories(db, "SELECT COUNT(*) FROM categories");
  count_categories.executeStep();
  int count_of_table_columns = count_categories.getColumn(0).getInt();
  if (count_of_table_columns > 0) {
    return true;
  }
  return false;
}

} // namespace

void Database::Initalize_Menu() {
  if (!is_initialized(db)) {
    db.exec(R"SQL(
  BEGIN TRANSACTION;

            INSERT INTO categories (id, name) VALUES
              (1, 'Entrees'),
              (2, 'Sides'),
              (3, 'Desserts'),
              (4, 'Drinks');

            INSERT INTO items (id, name, image, price, category_id, in_stock) VALUES
              (1,  'Burger'               , 'data/images/burger.png', 5.99, 1, 1),
              (2,  'Chicken Sandwich'     , 'data/images/chicken_sandwich.png', 5.49, 1, 1),
              (3,  'Cheese Burger'        , 'data/images/roblox_burger.png', 6.49, 1, 1),
              (4,  'French Fries'         , 'data/images/french_fries.png', 1.49, 2, 1),
              (5,  'Onion Rings'          , 'data/images/onion_rings.png', 1.69, 2, 1),
              (6,  'Chocolate Cake Slice' , 'data/images/chocolate_cake_slice.png', 0.99, 3, 1),
              (7,  'Apple Pie'            , 'data/images/apple_pie.png', 1.89, 3, 1),
              (8,  'Bloxy Soda'           , 'data/images/bloxy_cola.png', 1.49, 4, 1),
              (9,  'Orange Soda'          , 'data/images/orange_soda.png', 1.49, 4, 1),
              (10, 'Diet Soda'            , 'data/images/diet_soda.png', 1.39, 4, 1),
              (11, 'Vanilla Shake'        , 'data/images/vanilla_shake.png', 3.99, 4, 1),
              (12, 'Lemonade'             , 'data/images/lemonade.png', 3.99, 4, 1),
              (13, 'Orange Juice'         , 'data/images/orange_juice.png', 3.99, 4, 1);

            INSERT INTO ingredients (id, name, stock) VALUES
              (1 , 'Beef Patty'    , 100),
              (2 , 'Chicken Patty' , 100),
              (3 , 'Bun'           , 100),
              (4 , 'Lettuce'       , 100),
              (5 , 'Tomato'        , 100),
              (6 , 'Pickles'       , 100),
              (7 , 'Cheese'        , 100),
              (8 , 'Bacon'         , 100),
              (9 , 'Ketchup'       , 100),
              (10, 'Mayonnaise'    , 100),
              (11, 'Mustard'       , 100);


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
  std::vector<Category> vector_categories = db.Get_Vector_Categories();

  std::cout << "Categories\n";
  for (const auto &category : vector_categories) {
    std::cout << "Category: " << category.name << "\n";
  }
}

inline void print_items(Database &db) {
  std::vector<Item> vector_items = db.Get_Vector_Items();

  std::cout << "Items\n";
  for (const auto &item : vector_items) {
    std::cout << "Item: " << item.name << "\n";
  }
}

inline void print_ingredients(Database &db) {
  std::vector<Ingredient> vector_ingredients = db.Get_Vector_Ingredients();

  std::cout << "Ingredients: \n";
  for (const auto &ingredient : vector_ingredients) {
    std::cout << "Id: " << ingredient.id << ", ";
    std::cout << "Name: " << ingredient.name << ", ";
    std::cout << "Stock: " << ingredient.stock << "\n";
  }
}

inline void print_item_ingredients(Database &db) {
  std::cout << "Item ID: \n";
  int input_ItemId;
  std::cin >> input_ItemId;

  std::vector<ItemIngredient> vector_itemIngredients =
      db.Get_Vector_ItemIngredients_by_ItemID(input_ItemId);

  for (const auto &itemingredient : vector_itemIngredients) {
    std::cout << "Id: " << itemingredient.id << ", ";
    std::cout << "Name: " << itemingredient.name << ", ";
    std::cout << "Is Removable: " << itemingredient.isRemovable << ", ";
    std::cout << "Price Change: " << itemingredient.priceChange << "\n";
  }
}

inline void print_combos(Database &db) {
  std::vector<Item> vector_outputCombos = db.Get_Vector_Combos();
  std::cout << "Combos: \n";

  for (const auto &combo : vector_outputCombos) {
    std::cout << "Id: " << combo.id << ", ";
    std::cout << "Name: " << combo.name << ", ";
    std::cout << "Price: " << combo.price << "\n";
  }
}

inline void print_combo_items(Database &db) {
  int input_ComboID;
  std::cout << "Combo #: \n";
  std::cin >> input_ComboID;

  std::vector<ComboItem> vector_outputComboItems =
      db.Get_Vector_ComboItems_by_ComboID(input_ComboID);

  for (const auto &comboitem : vector_outputComboItems) {
    std::cout << "Id: " << comboitem.id << ", ";
    std::cout << "Name: " << comboitem.name << ", ";
    std::cout << "Price: " << comboitem.price << ", ";
    std::cout << "Available: " << comboitem.inStock << "\n";
  }
}

inline void print_orders(Database &db) {
  std::vector<Order> vector_allOrders = db.Get_Vector_Orders();
  std::cout << "All Orders:\n";

  for (const auto &order : vector_allOrders) {
    std::cout << "Id: " << order.id << ", ";
    std::cout << "Time " << order.time << ", ";
    std::cout << "Total: " << order.total << "\n";
  }
}

inline void print_order_items(Database &db) {
  int input_orderId;
  std::cout << "Order ID: \n";
  std::cin >> input_orderId;

  std::vector<OrderItem> vector_orderItems =
      db.Get_Vector_OrderItems_By_OrderID(input_orderId);
  std::cout << "Order Items for order " << input_orderId << ":\n";

  for (const auto &orderitem : vector_orderItems) {
    std::cout << "Order Id: " << orderitem.orderId << ", ";
    std::cout << "Name: " << orderitem.itemName << ", ";
    std::cout << "Price: " << orderitem.itemPrice << ", ";
    std::cout << "Count: " << orderitem.count << "\n";
  }
}

void Print_Headers() {
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
  int menu_selection = 1;

  while (running) {
    Print_Headers();
    std::cin >> menu_selection;
    switch (menu_selection) {
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
