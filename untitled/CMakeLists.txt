cmake_minimum_required(VERSION 3.8)
project(untitled)

link_libraries(crypto)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES montgomery.c)
add_executable(untitled ${SOURCE_FILES})