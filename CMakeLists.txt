cmake_minimum_required(VERSION 3.20)

project(dotcop DESCRIPTION "Configuration manager" LANGUAGES CXX)

find_package(yaml-cpp REQUIRED)

add_executable(dotcop src/main.cpp src/cli_parser.cpp src/config_loader.cpp src/file_manager.cpp src/options.cpp)
target_link_libraries(dotcop PRIVATE yaml-cpp::yaml-cpp)
