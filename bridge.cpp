#include "POS.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

// creates a python module named backend
PYBIND11_MODULE(backend, handle) {
  py::class_<POS>(handle, "POS")
      // must expose each constructor and functions so that it is accessible in
      // main.py
      .def(py::init<>()) // Constructor
      .def("addItem", &POS::addItem)
      .def("getTotal", &POS::getTotal)
      .def("clear", &POS::clear);
}
