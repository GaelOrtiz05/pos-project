#include <pybind11/pybind11.h>
#include <string>
#include <vector>

// #include <pybind11/stl.h>

// pybind11:: becomes py::
namespace py = pybind11;

struct Item {
  std::string name;
  double price;
};

class POS {
private:
  std::vector<Item> cart;
  const double SALES_TAX = 1.83;

public:
  void addItem(std::string name, double price) {
    cart.push_back({name, price});
  }
  void clear() { cart.clear(); }

  double getTotal() {
    double total = 0;
    for (const auto &item : cart) {
      total += item.price;
    }

    return total * SALES_TAX;
  }
};

// creates a python module named backend
PYBIND11_MODULE(backend, handle) {
  py::class_<POS>(handle, "POS")
      // must expose each constructor and functions
      .def(py::init<>()) // Constructor
      .def("addItem", &POS::addItem)
      .def("getTotal", &POS::getTotal)
      .def("clear", &POS::clear);
}
