cmake_minimum_required(VERSION 3.16)
project(FreedonLangCpp VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(FREEDON_BUILD_EXAMPLES "Build Freedon C++ examples" ON)

add_library(freedon_core STATIC
    src/freedon_core.cpp
)

target_include_directories(freedon_core
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(FREEDON_BUILD_EXAMPLES)
    add_executable(freedon_cpp
        src/main.cpp
    )
    target_link_libraries(freedon_cpp PRIVATE freedon_core)
endif()

