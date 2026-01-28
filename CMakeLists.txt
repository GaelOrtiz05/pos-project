set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
cmake_minimum_required(VERSION 3.12)
project(POS)

find_package(pybind11 REQUIRED)

pybind11_add_module(backend gateway.cpp)

