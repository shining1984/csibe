set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(triple aarch64-linux-gnu)

set(CMAKE_C_COMPILER /home/ningning/llvm-project/build-aarch64/bin/clang)
set(CMAKE_CXX_COMPILER /home/ningning/llvm-project/build-aarch64/bin/clang++)

set(CORTEX_M4_FLAGS "--target=${triple} -Os -msoft-float -Wno-implicit-function-declaration -Wno-implicit-int -D__GLIBC_HAVE_LONG_LONG")
set(CMAKE_C_FLAGS "${CORTEX_M4_FLAGS}" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "${CORTEX_M4_FLAGS}" CACHE STRING "" FORCE)
