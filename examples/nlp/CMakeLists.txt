cmake_minimum_required(VERSION 3.12)
project(smoek)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake;${CMAKE_MODULE_PATH})

# Directory where SPACK has been installed
set(CMAKE_PREFIX_PATH "/home/wehart/dev/coek/coek-gh/_spack/var/spack/environments/coekenv/.spack-env/view")
find_package(RapidJSON CONFIG REQUIRED)
include_directories(${RAPIDJSON_INCLUDE_DIR})

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++17" COMPILER_SUPPORTS_CXX17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -DWITH_RAPIDJSON")

#
# List smoek test function files here
#
file(GLOB sources CONFIGURE_DEPENDS
    "models/*.cpp"
    )

add_executable(run run.cpp loadlib.cpp coek/util/DataPortal.cpp ${sources})
add_dependencies(run RapidJSON)
target_include_directories(run PUBLIC ${RapidJSON_INCLUDE_DIRS}/.. ${CMAKE_CURRENT_SOURCE_DIR})
TARGET_LINK_LIBRARIES(run)

