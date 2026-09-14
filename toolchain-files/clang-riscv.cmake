set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR RISCV64)

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(triple riscv64-unknown-linux-gnu)

if(DEFINED ENV{CSIBE_LLVM_BUILD_DIR}
   AND NOT "$ENV{CSIBE_LLVM_BUILD_DIR}" STREQUAL "")
  file(TO_CMAKE_PATH "$ENV{CSIBE_LLVM_BUILD_DIR}" TOOLCHAIN_PATH)
else()
  set(TOOLCHAIN_PATH
      /root/iscas/csibe/exp-4steps/llvm-project/build-ext-tsp)
endif()

if(NOT EXISTS "${TOOLCHAIN_PATH}/bin/clang")
  message(FATAL_ERROR "clang not found: ${TOOLCHAIN_PATH}/bin/clang")
endif()

set(CMAKE_C_COMPILER ${TOOLCHAIN_PATH}/bin/clang)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PATH}/bin/clang++)

if(NOT DEFINED CSIBE_RISCV_FLAGS_CONFIGURED)
set(RISCV64_FLAGS "--target=${triple} -Os -march=rv64g_zca_zcb_zcmp_zcmt --gcc-toolchain=/root/opt/riscv64gc -Wno-implicit-function-declaration -Wno-implicit-int -D__GLIBC_HAVE_LONG_LONG")
set(CSIBE_EXTRA_CFLAGS "$ENV{CSiBE_CFLAGS}")
set(CSIBE_EXTRA_CXXFLAGS "$ENV{CSiBE_CXXFLAGS}")
set(CMAKE_C_FLAGS "${RISCV64_FLAGS} ${CSIBE_EXTRA_CFLAGS}" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "${RISCV64_FLAGS} ${CSIBE_EXTRA_CXXFLAGS}" CACHE STRING "" FORCE)
  set(CSIBE_RISCV_FLAGS_CONFIGURED TRUE CACHE INTERNAL "CSiBE RISC-V flags initialized")
endif()
