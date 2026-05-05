#include "db.hpp"

std::vector<Category> Database::Get_Vector_Categories() {
  SQLite::Statement get_categories(db, "SELECT id, name FROM categories ORDER BY id ASC");

  std::vector<Category> vector_of_categories;

  while (get_categories.executeStep()) {
    Category category;
    category.id = get_categories.getColumn(0).getInt();
    category.name = get_categories.getColumn(1).getString();
    vector_of_categories.push_back(category);
  }
  return vector_of_categories;
}

int Database::Get_CategoryID_By_Name(std::string &name) {
  SQLite::Statement get_category_id(db, "SELECT id FROM categories WHERE name = ?");
  get_category_id.bind(1, name);

  if (!get_category_id.executeStep()) {
    throw std::runtime_error("Category " + name + " not found");
  }

  return get_category_id.getColumn(0).getInt();
}

std::vector<Ingredient> Database::Get_Vector_Ingredients() {
  SQLite::Statement get_ingredients(db, "SELECT id, name, stock FROM ingredients ORDER BY id ASC");

  std::vector<Ingredient> vector_of_ingredients;

  while (get_ingredients.executeStep()) {
    Ingredient ingredient;
    ingredient.id = get_ingredients.getColumn(0).getInt();
    ingredient.name = get_ingredients.getColumn(1).getString();
    ingredient.stock = get_ingredients.getColumn(2).getInt();
    vector_of_ingredients.push_back(ingredient);
  }
  return vector_of_ingredients;
}

std::vector<Item> Database::Get_Vector_Combos() {
  SQLite::Statement get_combos(db, "SELECT id, name, price FROM combos ORDER BY id ASC");

  std::vector<Item> vector_of_combos;

  while (get_combos.executeStep()) {
    Item combo;
    combo.id = get_combos.getColumn(0).getInt();
    combo.name = get_combos.getColumn(1).getString();
    combo.price = get_combos.getColumn(2).getDouble();
    vector_of_combos.push_back(combo);
  }
  return vector_of_combos;
}

std::vector<Item> Database::Get_Vector_Items() {
  SQLite::Statement get_items(db, R"SQL(
                          SELECT i.id, i.name, i.image, i.price, i.in_stock, i.category_id, c.name
                          FROM items i JOIN categories c ON i.category_id = c.id
                          ORDER BY i.name ASC
                          )SQL");

  std::vector<Item> vector_of_items;

  while (get_items.executeStep()) {
    Item item;
    item.id = get_items.getColumn(0).getInt();
    item.name = get_items.getColumn(1).getString();
    item.image = get_items.getColumn(2).getString();
    item.price = get_items.getColumn(3).getDouble();
    item.inStock = get_items.getColumn(4).getInt();
    item.categoryId = get_items.getColumn(5).getInt();
    item.categoryName = get_items.getColumn(6).getString();
    vector_of_items.push_back(item);
  }
  return vector_of_items;
}

Item Database::Get_Struct_Item(int itemId) {
  SQLite::Statement get_item(db, R"SQL(
                          SELECT i.id, i.name, i.image, i.price, i.in_stock, i.category_id, c.name
                          FROM items i JOIN categories c ON i.category_id = c.id
                          ORDER BY i.name ASC
                          )SQL");

  Item item;
  item.id = get_item.getColumn(0).getInt();
  item.name = get_item.getColumn(1).getString();
  item.image = get_item.getColumn(2).getString();
  item.price = get_item.getColumn(3).getDouble();
  item.inStock = get_item.getColumn(4).getInt();
  item.categoryId = get_item.getColumn(5).getInt();
  item.categoryName = get_item.getColumn(6).getString();
  return item;
}

std::vector<Item> Database::Get_Vector_Items_By_Category(std::string &name) {
  SQLite::Statement get_items(db, R"SQL(
                      SELECT i.id, i.name, i.image, i.price, i.in_stock, i.category_id, c.name
                      FROM items i JOIN categories c ON i.category_id = c.id
                      WHERE c.name = ?
                      ORDER BY i.name ASC
                      )SQL");

  get_items.bind(1, name);

  std::vector<Item> vector_of_items;
  while (get_items.executeStep()) {
    Item item;
    item.id = get_items.getColumn(0).getInt();
    item.name = get_items.getColumn(1).getString();
    item.image = get_items.getColumn(2).getString();
    item.price = get_items.getColumn(3).getDouble();
    item.inStock = get_items.getColumn(4).getInt();
    item.categoryId = get_items.getColumn(5).getInt();
    item.categoryName = get_items.getColumn(6).getString();
    vector_of_items.push_back(item);
  }
  return vector_of_items;
}

std::vector<ItemIngredient> Database::Get_Vector_ItemIngredients_by_ItemID(int itemId) {
  SQLite::Statement get_ItemIngredients(db, R"SQL(
                          SELECT ing.id, ing.name, ing.stock, ii.is_removable, ii.price_change
                          FROM ingredients ing JOIN item_ingredients ii ON ing.id = ii.ingredient_id
                          WHERE ii.item_id = ?
                          )SQL");

  get_ItemIngredients.bind(1, itemId);

  std::vector<ItemIngredient> vector_of_itemIngredients;

  while (get_ItemIngredients.executeStep()) {
    ItemIngredient itemIngredient;
    itemIngredient.id = get_ItemIngredients.getColumn(0).getInt();
    itemIngredient.name = get_ItemIngredients.getColumn(1).getString();
    itemIngredient.stock = get_ItemIngredients.getColumn(2).getInt();
    itemIngredient.isRemovable = get_ItemIngredients.getColumn(3).getInt();
    itemIngredient.priceChange = get_ItemIngredients.getColumn(4).getDouble();
    vector_of_itemIngredients.push_back(itemIngredient);
  }
  return vector_of_itemIngredients;
}

std::vector<ComboItem> Database::Get_Vector_ComboItems_by_ComboID(int comboId) {
  SQLite::Statement get_ComboItems(db, R"SQL(
                          SELECT i.id, i.name, i.price, i.in_stock
                          FROM items i
                          JOIN combo_items ci ON i.id = ci.item_id
                          WHERE ci.combo_id = ?
                          )SQL");

  get_ComboItems.bind(1, comboId);

  std::vector<ComboItem> vector_of_comboItems;

  while (get_ComboItems.executeStep()) {
    ComboItem comboitem;
    comboitem.id = get_ComboItems.getColumn(0).getInt();       // item id
    comboitem.name = get_ComboItems.getColumn(1).getString();  // item name
    comboitem.price = get_ComboItems.getColumn(2).getDouble(); // item price
    comboitem.inStock = get_ComboItems.getColumn(3).getInt();
    vector_of_comboItems.push_back(comboitem);
  }

  return vector_of_comboItems;
}

std::vector<Order> Database::Get_Vector_Orders() {
  SQLite::Statement get_orders(db,
                          "SELECT id, time, total FROM orders ORDER BY id ASC");

  std::vector<Order> vector_of_orders;

  while (get_orders.executeStep()) {
    Order order;
    order.id = get_orders.getColumn(0).getInt();
    order.time = get_orders.getColumn(1).getString();
    order.total = get_orders.getColumn(2).getDouble();
    vector_of_orders.push_back(order);
  }
  return vector_of_orders;
}

std::vector<OrderItem> Database::Get_Vector_OrderItems_By_OrderID(int orderId) {
  SQLite::Statement get_OrderItems(db, R"SQL(
                          SELECT order_id, item_id, item_name, item_price, count
                          FROM order_items
                          WHERE order_id = ?
                          ORDER BY order_id ASC
                          )SQL");

  get_OrderItems.bind(1, orderId);

  std::vector<OrderItem> vector_of_orderItems;

  while (get_OrderItems.executeStep()) {
    OrderItem orderitem;
    orderitem.orderId = get_OrderItems.getColumn(0).getInt();
    orderitem.itemId = get_OrderItems.getColumn(1).getInt();
    orderitem.itemName = get_OrderItems.getColumn(2).getString();
    orderitem.itemPrice = get_OrderItems.getColumn(3).getDouble();
    orderitem.count = get_OrderItems.getColumn(4).getInt();
    vector_of_orderItems.push_back(orderitem);
  }
  return vector_of_orderItems;
}

std::vector<Item> Database::Get_Vector_Checkout_items() {
  SQLite::Statement get_items(db, R"SQL(SELECT item_id, item_name FROM checkout_items)SQL");

  std::vector<Item> list_of_items_in_checkout;
  while (get_items.executeStep()) {
    Item item;
    item.id = get_items.getColumn(0).getInt();
    item.name = get_items.getColumn(1).getString();
    list_of_items_in_checkout.push_back(item);

  }
  return list_of_items_in_checkout;
}

bool Database::Remove_Item_From_Checkout_Tables(int checkoutID) {
  SQLite::Statement remove_ingredients(db,"DELETE FROM checkout_ingredients WHERE checkout_id = ?");
  remove_ingredients.bind(1,checkoutID);
  remove_ingredients.exec(); 

  SQLite::Statement remove_items(db, "DELETE FROM checkout_items WHERE checkout_id = ?");
  remove_items.bind(1,checkoutID);
  remove_items.exec();
  
  return true;
}

