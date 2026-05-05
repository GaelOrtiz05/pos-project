// #include "POS.hpp"
#include "db.hpp"
#include "login.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(pos_backend, handle) {

  py::class_<User>(handle, "User")
      .def_readonly("id", &User::id)
      .def_readonly("name", &User::name)
      .def_readonly("password", &User::password)
      .def_readonly("role", &User::role)
      .def_property_readonly("isAdmin", &User::isAdmin);

  py::class_<Category>(handle, "Category")
      .def_readonly("id", &Category::id)
      .def_readonly("name", &Category::name);

  py::class_<Ingredient>(handle, "Ingredient")
      .def_readonly("id", &Ingredient::id)
      .def_readonly("name", &Ingredient::name)
      .def_readonly("stock", &Ingredient::stock);

  py::class_<Item>(handle, "Item")
      .def_readonly("id", &Item::id)
      .def_readonly("name", &Item::name)
      .def_readonly("image", &Item::image)
      .def_readonly("price", &Item::price)
      .def_readonly("inStock", &Item::inStock)
      .def_readonly("categoryId", &Item::categoryId)
      .def_readonly("categoryName", &Item::categoryName);

  py::class_<ItemIngredient>(handle, "ItemIngredient")
      .def_readonly("id", &ItemIngredient::id)
      .def_readonly("name", &ItemIngredient::name)
      .def_readonly("stock", &ItemIngredient::stock)
      .def_readonly("isRemovable", &ItemIngredient::isRemovable)
      .def_readonly("priceChange", &ItemIngredient::priceChange);

  py::class_<ComboItem>(handle, "ComboItem")
      .def_readonly("id", &ComboItem::id)
      .def_readonly("name", &ComboItem::name)
      .def_readonly("price", &ComboItem::price)
      .def_readonly("inStock", &ComboItem::inStock);

  py::class_<Order>(handle, "Order")
      .def_readonly("id", &Order::id)
      .def_readonly("time", &Order::time)
      .def_readonly("total", &Order::total);

  py::class_<OrderItem>(handle, "OrderItem")
      .def(py::init<>())
      .def_readwrite("orderId", &OrderItem::orderId)
      .def_readwrite("itemId", &OrderItem::itemId)
      .def_readwrite("itemName", &OrderItem::itemName)
      .def_readwrite("itemPrice", &OrderItem::itemPrice)
      .def_readwrite("count", &OrderItem::count)
      .def_readwrite("removedIngredients", &OrderItem::removedIngredients);

  py::class_<Login>(handle, "Login")
      .def(py::init<>())
      .def("addUser", &Login::Add_User_To_Table)
      .def("removeUser", &Login::Remove_User_From_Table)
      .def("loginUser", &Login::Process_Login_User)
      .def("getUser", &Login::Get_User)
      .def("getIsAdmin", &Login::Get_User_IsAdmin)
      .def("getListOfUsers", &Login::Get_Vector_Users)
      .def("searchUser", &Login::User_Exists);

  py::class_<Database>(handle, "Database")
      .def(py::init<>())
      .def("setIngredientStock", &Database::Inc_Dec_Ingredient_Stock)
      .def("Add_Item_Into_Checkout_Tables", &Database::Add_Item_Into_Checkout_Tables)
      .def("getCategories", &Database::Get_Vector_Categories)
      .def("getCategoryIdByName", &Database::Get_CategoryID_By_Name)
      .def("getItems", &Database::Get_Vector_Items)
      .def("getItem", &Database::Get_Struct_Item)
      .def("getIngredients", &Database::Get_Vector_Ingredients)
      .def("getCombos", &Database::Get_Vector_Combos)
      .def("getItemsByCategory", &Database::Get_Vector_Items_By_Category)
      .def("getItemIngredients", &Database::Get_Vector_ItemIngredients_by_ItemID)
      .def("Check_Stock", &Database::Check_Ingredient_Stock_Of_Item)
      .def("decrementStock", &Database::Decrement_Ingredient_Stock_Of_Item)
      .def("incrementStock", &Database::Increment_Ingredient_Stock_Of_Item)
      .def("getComboItems", &Database::Get_Vector_ComboItems_by_ComboID)
      .def("purchase", &Database::Process_Purchase)
      .def("getOrders", &Database::Get_Vector_Orders)
      .def("getOrderItemsById", &Database::Get_Vector_OrderItems_By_OrderID)
      .def("get_Checkout_Items", &Database::Get_Vector_Checkout_items)
      .def("get_Checkout_Ingredients_By_ItemID", &Database::Get_Vector_Checkout_Ingredients_By_ItemID);
}
