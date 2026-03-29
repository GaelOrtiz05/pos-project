#include "POS.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

// deprecated?
// creates a python module named backend
// PYBIND11_MODULE(pos_backend, handle) {
//   py::class_<POS>(handle, "POS")
//       // must expose each constructor and functions so that it is accessible
//       in
//       // main.py
//       .def(py::init<>()) // Constructor
//       .def("addItem", &POS::addItem)
//       .def("getTotal", &POS::getTotal)
//       .def("clear", &POS::clear)
//       .def("initializeMenu", &POS::initializeFromFile);
// }

PYBIND11_MODULE(pos_backend, handle) {
  py::class_<Login>(handle, "Login")
      .def(py::init<>())
      .def("addUser", &Login::addUser)
      .def("removeUser", &Login::removeUser)
      .def("loginUser", &Login::loginUser)
      .def("getUser", &Login::getUser)
      .def("getIsAdmin", &Login::getIsAdmin)
      .def("togglePrivileges", &Login::togglePrivileges)
      .def("getListOfUsers", &Login::getListOfUsers);
}
