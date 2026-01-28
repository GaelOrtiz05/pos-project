#include <pybind11/pybind11.h>

// A simple function to simulate a "Big Project" calculation
int add_numbers(int a, int b) { return a + b; }

// This block creates the Python module named "fast_logic"
PYBIND11_MODULE(fast_logic, m) {
  m.doc() = "C++ logic for our Python GUI";
  m.def("add", &add_numbers, "A function that adds two integers");
}
