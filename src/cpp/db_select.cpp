#include "db.hpp"


std::vector<Category> Database::getCategories() {
  SQLite::Statement query(db,
                          "SELECT id, name FROM categories ORDER BY id ASC");
  std::vector<Category> categories;
  while (query.executeStep()) {
    Category c;
    c.id = query.getColumn(0).getInt();
    c.name = query.getColumn(1).getString();
    categories.push_back(c);
  }
  return categories;
}

int Database::getCategoryIdByName(std::string &name) {
  SQLite::Statement query(db, "SELECT id FROM categories WHERE name = ?");
  query.bind(1, name);

  if (!query.executeStep()) {
    throw std::runtime_error("Category " + name + " not found");
  }

  return query.getColumn(0).getInt();
}

std::vector<Ingredient> Database::getIngredients() {
  SQLite::Statement query(
      db, "SELECT id, name, stock FROM ingredients ORDER BY id ASC");
  std::vector<Ingredient> ingredients;
  while (query.executeStep()) {
    Ingredient i;
    i.id = query.getColumn(0).getInt();
    i.name = query.getColumn(1).getString();
    i.stock = query.getColumn(2).getInt();
    ingredients.push_back(i);
  }
  return ingredients;
}

std::vector<Item> Database::getCombos() {
  SQLite::Statement query(db,
                          "SELECT id, name, price FROM combos ORDER BY id ASC");
  std::vector<Item> combos;
  while (query.executeStep()) {
    Item c;
    c.id = query.getColumn(0).getInt();
    c.name = query.getColumn(1).getString();
    c.price = query.getColumn(2).getDouble();
    combos.push_back(c);
  }
  return combos;
}

std::vector<Item> Database::getItems() {
  SQLite::Statement query(db, R"SQL(
                          SELECT i.id, i.name, i.price, i.in_stock, i.category_id, c.name 
                          FROM items i JOIN categories c ON i.category_id = c.id
                          ORDER BY i.name ASC
                          )SQL");

  std::vector<Item> items;
  while (query.executeStep()) {
    Item i;
    i.id = query.getColumn(0).getInt();
    i.name = query.getColumn(1).getString();
    i.price = query.getColumn(2).getDouble();
    i.inStock = query.getColumn(3).getInt();
    i.categoryId = query.getColumn(4).getInt();
    i.categoryName = query.getColumn(5).getString();
    items.push_back(i);
  }
  return items;
}

Item Database::getItem(int itemId) {
  SQLite::Statement query(db, R"SQL(
                          SELECT i.id, i.name, i.price, i.in_stock, i.category_id, c.name 
                          FROM items i JOIN categories c ON i.category_id = c.id
                          ORDER BY i.name ASC
                          )SQL");

  Item i;
  i.id = query.getColumn(0).getInt();
  i.name = query.getColumn(1).getString();
  i.price = query.getColumn(2).getDouble();
  i.inStock = query.getColumn(3).getInt();
  i.categoryId = query.getColumn(4).getInt();
  i.categoryName = query.getColumn(5).getString();
  return i;
}

std::vector<Item> Database::getItemsByCategory(std::string &name) {
  SQLite::Statement query(db, R"SQL(
                      SELECT i.id, i.name, i.price, i.in_stock, i.category_id, c.name 
                      FROM items i JOIN categories c ON i.category_id = c.id 
                      WHERE c.name = ?
                      ORDER BY i.name ASC
                      )SQL");

  query.bind(1, name);

  std::vector<Item> items;
  while (query.executeStep()) {
    Item i;
    i.id = query.getColumn(0).getInt();
    i.name = query.getColumn(1).getString();
    i.price = query.getColumn(2).getDouble();
    i.inStock = query.getColumn(3).getInt();
    i.categoryId = query.getColumn(4).getInt();
    i.categoryName = query.getColumn(5).getString();
    items.push_back(i);
  }
  return items;
}

std::vector<ItemIngredient> Database::getItemIngredients(int itemId) {
  SQLite::Statement query(db, R"SQL(
                          SELECT ing.id, ing.name, ing.stock, ii.is_removable, ii.price_change
                          FROM ingredients ing JOIN item_ingredients ii ON ing.id = ii.ingredient_id
                          WHERE ii.item_id = ?
                          )SQL");

  query.bind(1, itemId);

  std::vector<ItemIngredient> itemIngredients;
  while (query.executeStep()) {
    ItemIngredient ii;
    ii.id = query.getColumn(0).getInt();
    ii.name = query.getColumn(1).getString();
    ii.stock = query.getColumn(2).getInt();
    ii.isRemovable = query.getColumn(3).getInt();
    ii.priceChange = query.getColumn(4).getDouble();
    itemIngredients.push_back(ii);
  }
  return itemIngredients;
}

std::vector<ComboItem> Database::getComboItems(int comboId) {
  SQLite::Statement query(db, R"SQL(
                          SELECT i.id, i.name, i.price, i.in_stock
                          FROM items i
                          JOIN combo_items ci ON i.id = ci.item_id
                          WHERE ci.combo_id = ?
                          )SQL");

  query.bind(1, comboId);

  std::vector<ComboItem> comboItems;

  while (query.executeStep()) {
    ComboItem ci;
    ci.id = query.getColumn(0).getInt();       // item id
    ci.name = query.getColumn(1).getString();  // item name
    ci.price = query.getColumn(2).getDouble(); // item price
    ci.inStock = query.getColumn(3).getInt();
    comboItems.push_back(ci);
  }

  return comboItems;
}

std::vector<Order> Database::getOrders() {
  SQLite::Statement query(db, "SELECT id, total FROM orders ORDER BY id ASC");
  std::vector<Order> orders;
  while (query.executeStep()) {
    Order o;
    o.id = query.getColumn(0).getInt();
    o.total = query.getColumn(1).getDouble();
    orders.push_back(o);
  }
  return orders;
}

std::vector<OrderItem> Database::getOrderItems(int orderId) {
  SQLite::Statement query(db, R"SQL(
                          SELECT item_id, item_name, item_price
                          FROM order_items
                          WHERE order_id = ?
                          )SQL");

  query.bind(1, orderId);

  std::vector<OrderItem> orderItems;
  while (query.executeStep()) {
    OrderItem oi;
    oi.itemId = query.getColumn(0).getInt();
    oi.itemName = query.getColumn(1).getString();
    oi.itemPrice = query.getColumn(2).getDouble();
    orderItems.push_back(oi);
  }
  return orderItems;
}
