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

  py::class_<Login>(handle, "Login")
      .def(py::init<>())
      .def("addUser", &Login::addUser)
      .def("removeUser", &Login::removeUser)
      .def("loginUser", &Login::loginUser)
      .def("getUser", &Login::getUser)
      .def("getIsAdmin", &Login::getIsAdmin)
      .def("togglePrivileges", &Login::togglePrivileges)
      .def("getListOfUsers", &Login::getListOfUsers);

  // py::class_<Database>(handle, "Database")
  //     .def(py::init<>())
  //     .def("purchase", &Database::purchase);
}
