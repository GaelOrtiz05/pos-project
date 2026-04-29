cmake_minimum_required(VERSION 3.14)
project(POS)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(PYBIND11_FINDPYTHON NEW)

add_subdirectory(libraries/pybind11)
add_subdirectory(libraries/SQLiteCpp)

find_package(Python COMPONENTS Interpreter Development REQUIRED)

IF (UNIX)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(SODIUM REQUIRED IMPORTED_TARGET libsodium)
    set(SODIUM_TARGET PkgConfig::SODIUM)
ELSE ()
    find_package(unofficial-sodium CONFIG REQUIRED)
    set(SODIUM_TARGET unofficial-sodium::sodium)
ENDIF ()


pybind11_add_module(pos_backend src/cpp/bridge.cpp src/cpp/db.cpp src/cpp/db_insert.cpp src/cpp/db_select.cpp)
target_link_libraries(pos_backend PRIVATE
SQLiteCpp
sqlite3
${SODIUM_TARGET}
)

set_target_properties(pos_backend PROPERTIES 
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/src/python"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_SOURCE_DIR}/src/python"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_SOURCE_DIR}/src/python"
)

add_executable(pos_cpp src/cpp/main.cpp src/cpp/db.cpp src/cpp/db_insert.cpp src/cpp/db_select.cpp)
target_link_libraries(pos_cpp PRIVATE SQLiteCpp sqlite3 ${SODIUM_TARGET})

