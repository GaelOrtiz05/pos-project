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
      .def_readonly("isAdmin", &User::isAdmin);

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
      .def_readonly("price", &Item::price)
      .def_readonly("inStock", &Item::inStock)
      .def_readonly("categoryId", &Item::categoryId)
      .def_readonly("categoryName", &Item::categoryName);

  py::class_<ItemIngredient>(handle, "ItemIngredient")
      .def_readonly("id", &ItemIngredient::id)
      .def_readonly("name", &ItemIngredient::name)
      .def_readonly("isRemovable", &ItemIngredient::isRemovable)
      .def_readonly("priceChange", &ItemIngredient::priceChange);

  py::class_<Combo>(handle, "Combo")
      .def_readonly("id", &Combo::id)
      .def_readonly("name", &Combo::name)
      .def_readonly("price", &Combo::price);

  py::class_<ComboItem>(handle, "ComboItem")
      .def_readonly("id", &ComboItem::id)
      .def_readonly("name", &ComboItem::name)
      .def_readonly("price", &ComboItem::price)
      .def_readonly("inStock", &ComboItem::inStock);

  py::class_<Checkout>(handle, "Checkout")
      .def_readonly("itemId", &Checkout::itemId)
      .def_readonly("itemName", &Checkout::itemName)
      .def_readonly("itemPrice", &Checkout::itemPrice);

  py::class_<Login>(handle, "Login")
      .def(py::init<>())
      .def("addUser", &Login::addUser)
      .def("removeUser", &Login::removeUser)
      .def("loginUser", &Login::loginUser)
      .def("getUser", &Login::getUser)
      .def("getIsAdmin", &Login::getIsAdmin)
      .def("togglePrivileges", &Login::togglePrivileges)
      .def("getListOfUsers", &Login::getListOfUsers);

  py::class_<Database>(handle, "Database")
      .def(py::init<>())
      // old
      // .def("getItemCount", &Database::getItemCount)
      // .def("getIngredientCount", &Database::getIngredientCount)
      // .def("getCategoryID", &Database::getCategoryID)
      // .def("getItemName", &Database::getItemName)
      .def("setIngredientStock", &Database::setIngredientStock)
      .def("addCheckout", &Database::addCheckout)
      .def("getCheckout", &Database::getCheckout)
      // new
      .def("getCategories", &Database::getCategories)
      .def("getCategoryIdByName", &Database::getCategoryIdByName)
      .def("getItems", &Database::getItems)
      .def("getIngredients", &Database::getIngredients)
      .def("getCombos", &Database::getCombos)
      .def("getItemsByCategory", &Database::getItemsByCategory)
      .def("getItemIngredients", &Database::getItemIngredients)
      .def("getComboItems", &Database::getComboItems)
      .def("purchase", &Database::purchase)
      .def("getItems", &Database::getItems);
}
