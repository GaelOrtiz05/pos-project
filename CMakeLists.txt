set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
cmake_minimum_required(VERSION 3.12)
project(MyBigProject)

find_package(pybind11 REQUIRED)

pybind11_add_module(fast_logic gateway.cpp)
