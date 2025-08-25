cmake_minimum_required(VERSION 3.20)

project(dotcop 
    DESCRIPTION 
    "Configuration manager"
    LANGUAGES
    CXX
) 

add_executable(dotcop src/main.cpp)
