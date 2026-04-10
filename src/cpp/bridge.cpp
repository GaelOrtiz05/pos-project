//#include "POS.hpp"
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
      .def("getItemCount", &Database::getItemCount)
      .def("getIngredientCount", &Database::getIngredientCount)
      .def("getCategoryID", &Database::getCategoryID)
      .def("getItemName", &Database::getItemName)
      .def("setIngredientStock", &Database::setIngredientStock)
      .def("addCheckout", &Database::addCheckout)
      .def("getCartCount", &Database::getCartCount)
      .def("getCheckoutName", &Database::getCheckoutName)
      .def("getCheckoutPrice", &Database::getCheckoutPrice)
      .def("purchase", &Database::purchase);
}
