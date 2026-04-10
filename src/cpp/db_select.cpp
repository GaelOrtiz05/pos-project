#include "db.hpp"

std::vector<Category> Database::getCategories() {
  SQLite::Statement query(db, "SELECT id, name FROM categories");
  std::vector<Category> categories;
  while (query.executeStep()) {
    Category category;
    category.id = query.getColumn(0).getInt();
    category.name = query.getColumn(1).getString();
    categories.push_back(category);
  }
  return categories;
}

std::vector<Ingredient> Database::getIngredients() {
  SQLite::Statement query(db, "SELECT id, name, stock FROM ingredients");
  std::vector<Ingredient> ingredients;
  while (query.executeStep()) {
    Ingredient ingredient;
    ingredient.id = query.getColumn(0).getInt();
    ingredient.name = query.getColumn(1).getString();
    ingredient.stock = query.getColumn(2).getInt();
    ingredients.push_back(ingredient);
  }
  return ingredients;
}

std::vector<Combo> Database::getCombos() {
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

std::vector<Item> Database::getItems() {
  SQLite::Statement query(
      db, "SELECT i.id, i.name, i.price, i.in_stock, i.category_id, c.name "
          "FROM items i JOIN categories c ON i.category_id = c.id");
  std::vector<Item> items;
  while (query.executeStep()) {
    Item item;
    item.id = query.getColumn(0).getInt();
    item.name = query.getColumn(1).getString();
    item.price = query.getColumn(2).getDouble();
    item.inStock = query.getColumn(3).getInt();
    item.categoryId = query.getColumn(4).getInt();
    item.categoryName = query.getColumn(5).getString();
    items.push_back(item);
  }
  return items;
}

std::vector<Item> Database::getItemsByCategory(int categoryId) {
  SQLite::Statement query(
      db, "SELECT i.id, i.name, i.price, i.in_stock, i.category_id, c.name "
          "FROM items i JOIN categories c "
          "ON i.category_id = c.id "
          "WHERE i.category_id = ?");
  query.bind(1, categoryId);
  std::vector<Item> items;
  while (query.executeStep()) {
    Item item;
    item.id = query.getColumn(0).getInt();
    item.name = query.getColumn(1).getString();
    item.price = query.getColumn(2).getDouble();
    item.inStock = query.getColumn(3).getInt();
    item.categoryId = query.getColumn(4).getInt();
    item.categoryName = query.getColumn(5).getString();
    items.push_back(item);
  }
  return items;
}

std::vector<ItemIngredient> Database::getItemIngredients() {}
std::vector<Item> Database::getComboItems() {}
