cmake_minimum_required(VERSION 3.13)
project(smoek)

option(with_debug "Debug build" OFF)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake;${CMAKE_MODULE_PATH})
# Directory where COEK has been installed
set(CMAKE_PREFIX_PATH "/home/wehart/dev/coek/coek-gh/_build/install;/home/wehart/dev/coek/coek-gh/_spack/var/spack/environments/coekenv/.spack-env/view")

include(GNUInstallDirs)
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++17" COMPILER_SUPPORTS_CXX17)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")
if(${with_debug})
    set(CMAKE_BUILD_TYPE debug)
    if (MSVC)
        set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /Wall /DDEBUG /permissive-")
    else()
        set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -Wall -DDEBUG")
    endif()
else()
    if (MSVC)
        set(CMAKE_CXX_FLAGS_RELEASE "/permissive-")
    endif()
endif()

# Can we make this dependency be implied by Coek?
#find_package(OpenMP)
find_package(coek)

#
# List smoek test function files here
#
file(GLOB sources CONFIGURE_DEPENDS
    "models/*.cpp"
    )

add_executable(run run.cpp ${sources})
TARGET_LINK_LIBRARIES(run coek::coek)

