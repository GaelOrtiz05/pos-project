# Don't really know what any of this means but it works
cmake_minimum_required(VERSION 3.14)
project(POS)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(PYBIND11_FINDPYTHON NEW)

add_subdirectory(libraries/pybind11)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

pybind11_add_module(pos_backend src/cpp/bridge.cpp)

set_target_properties(pos_backend PROPERTIES 
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/python"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/python"
)
