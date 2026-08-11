set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR RISCV64)

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(triple riscv64-unknown-linux-gnu)

set(TOOLCHAIN_PATH /home/ningning/llvm-project/build)

set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/bin/clang)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/bin/clang++)

set(RISCV64_FLAGS "--target=${triple} -Os -march=rv64g_zca_zcb_zcmp_zcmt --gcc-toolchain=/opt/riscv -Wno-implicit-function-declaration -Wno-implicit-int -D__GLIBC_HAVE_LONG_LONG")
set(CMAKE_C_FLAGS "${RISCV64_FLAGS}" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "${RISCV64_FLAGS}" CACHE STRING "" FORCE)
