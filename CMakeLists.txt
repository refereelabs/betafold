cmake_minimum_required(VERSION 3.31)
project(betafold)

set(CMAKE_CXX_STANDARD 23)

get_filename_component(PROJECT_ROOT "${CMAKE_SOURCE_DIR}" ABSOLUTE)

set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CBETAFOLD_PYTHON_MODULE "betafold")
set(SOURCES_ROOT "${PROJECT_ROOT}/cbetafold/src")

message(STATUS "Project root               : ${PROJECT_ROOT}")
message(STATUS "Sources root               : ${SOURCES_ROOT}")
message(STATUS "Build type                 : ${CMAKE_BUILD_TYPE}")
message(STATUS "Python executable          : ${Python_EXECUTABLE}")
message(STATUS "Python include directories : ${Python_INCLUDE_DIRS}")
message(STATUS "Python libraries           : ${Python_LIBRARIES}")
message(STATUS "Python version             : ${Python_VERSION}")
message(STATUS "Library output directory   : ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}")


add_compile_options(
        $<$<CONFIG:Debug>:-g>
        $<$<CONFIG:Debug>:-O0>
        $<$<CONFIG:Debug>:-Wall>
        $<$<CONFIG:Debug>:-Wextra>
        $<$<CONFIG:Debug>:-Wpedantic>
        $<$<CONFIG:Debug>:-Werror>

        $<$<CONFIG:Release>:-O3>
        $<$<CONFIG:Release>:-g>

        -Wall
        -Wextra
        -Wpedantic
        -Wno-odr # Required for the betafold type_caster. This is a pybind11 issue. We can fix it if we "include the type caster consistently in every compilation unit", but wtf does that mean?
        -Wshadow
        -Wundef
        -Wnull-dereference
        -Wuninitialized
)


add_link_options(
        $<$<CONFIG:Debug>:-g>
        $<$<CONFIG:Debug>:-O0>
        $<$<CONFIG:Debug>:-Wall>
        $<$<CONFIG:Debug>:-Wextra>
        $<$<CONFIG:Debug>:-Werror>
        $<$<CONFIG:Debug>:-Wpedantic>

        $<$<CONFIG:Release>:-O3>
        $<$<CONFIG:Release>:-g>

        -Wno-odr # Required for the betafold type_caster. This is a pybind11 issue. We can fix it if we "include the type caster consistently in every compilation unit", but wtf does that mean?
        -Wshadow
        -Wundef
        -Wnull-dereference
        -Wuninitialized
)

file(GLOB_RECURSE SOURCES "cbetafold/src/*.cpp")

find_package(Python 3.10 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 2.9.1 REQUIRED)

pybind11_add_module(betafold ${SOURCES})


add_definitions(-DPROJECT_SOURCE_DIR="${PROJECT_ROOT}")
add_definitions(-DSOURCES_ROOT="${SOURCES_ROOT}")

# ALL conditions on build type should go here, let's not clutter this up with a bunch of if statements:

if (CMAKE_BUILD_TYPE STREQUAL "Debug")
    message(STATUS "Configuring for Debug build")
    add_definitions(-DDEBUG_BUILD)
    set(INCLUDE_ASSERTIONS "TRUE")
    set(VERBOSE, "TRUE")
    target_compile_definitions(betafold PRIVATE INCLUDE_ASSERTIONS="${INCLUDE_ASSERTIONS}" VERBOSE="${VERBOSE}")
elseif (CMAKE_BUILD_TYPE STREQUAL "Release")
    message(STATUS "Configuring for Release build")
    add_definitions(-DRELEASE_BUILD)
else ()
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build (Debug or Release)" FORCE)
    message(STATUS "Unknown build type: ${CMAKE_BUILD_TYPE}")
    message(STATUS "Configuring for Release build")
    add_definitions(-DRELEASE_BUILD)
endif ()


target_compile_definitions(
        betafold PRIVATE SOURCES_ROOT="${SOURCES_ROOT}"
)
target_include_directories(betafold
        PRIVATE ${Python_INCLUDE_DIRS}
        ${pybind11_INCLUDE_DIRS}
        cbetafold/include
        cbetafold
)
set_target_properties(betafold PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}"
)
target_link_libraries(betafold PRIVATE pybind11::module Python::Python)

add_executable(train cbetafold/main.cpp)
target_compile_definitions(
        train PRIVATE SOURCES_ROOT="${SOURCES_ROOT}"
)
target_include_directories(train
        PRIVATE ${Python_INCLUDE_DIRS}
        ${pybind11_INCLUDE_DIRS}
        cbetafold/include
        cbetafold)
set_target_properties(train PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}"
)
target_link_libraries(train PRIVATE pybind11::module Python::Python)

add_custom_command(
        OUTPUT "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${PROJECT_NAME}.pyi"
        COMMAND cd ${CMAKE_LIBRARY_OUTPUT_DIRECTORY} && stubgen -o "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/" -m ${CBETAFOLD_PYTHON_MODULE}
        DEPENDS betafold
        COMMENT "Generating stub file in $<TARGET_PROPERTY:betafold,CMAKE_LIBRARY_OUTPUT_DIRECTORY> for ${CBETAFOLD_PYTHON_MODULE}"
)
add_custom_target(
        generate_stubs ALL
        DEPENDS "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${PROJECT_NAME}.pyi"
)
