# Don't really know what any of this means but it works
cmake_minimum_required(VERSION 3.12)
project(POS)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(PYBIND11_FINDPYTHON ON)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

pybind11_add_module(backend logic.cpp)
