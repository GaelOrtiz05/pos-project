# Don't really know what any of this means but it works
cmake_minimum_required(VERSION 3.12)
project(POS)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

pybind11_add_module(backend logic.cpp)