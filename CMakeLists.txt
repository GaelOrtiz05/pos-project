# Don't really know what any of this means but it works
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
cmake_minimum_required(VERSION 3.12)
project(POS)

find_package(pybind11 REQUIRED)
                  # module_name
pybind11_add_module(backend logic.cpp)

