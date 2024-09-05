cmake_minimum_required(VERSION 3.12)
project(smoek)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake;${CMAKE_MODULE_PATH})
# Directory where COEK has been installed
set(CMAKE_PREFIX_PATH "/home/wehart/dev/coek/coek-gh/_build/install;/home/wehart/dev/coek/coek-gh/_spack/var/spack/environments/coekenv/.spack-env/view")

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++17" COMPILER_SUPPORTS_CXX17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -g")

# Can we make this dependency be implied by Coek?
#find_package(OpenMP)
find_package(coek)

#
# List smoek test function files here
#
file(GLOB sources CONFIGURE_DEPENDS
    "models/*.cpp"
    )

add_executable(smoek smoek.cpp ${sources})
TARGET_LINK_LIBRARIES(smoek coek::coek)

