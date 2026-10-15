set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR x86)

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(triple x86_64-linux-gnu)

set(TOOLCHAIN_PATH /home/ningning/llvm-project/build-x86-arm)

set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/bin/clang)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/bin/clang++)

set(RISCV64_FLAGS "--target=${triple} -Os -Wno-implicit-function-declaration -Wno-implicit-int -D__GLIBC_HAVE_LONG_LONG")
set(CMAKE_C_FLAGS "${RISCV64_FLAGS}" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "${RISCV64_FLAGS}" CACHE STRING "" FORCE)
