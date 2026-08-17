
set(SIZE_RESULT "${PROJECT_BINARY_DIR}/result.csv")
set(OBJECT_DIR "${PROJECT_BINARY_DIR}/preprocessed-objects")
set(SIZE_FRAGMENT_DIR "${PROJECT_BINARY_DIR}/preprocessed-sizes")

file(GLOB_RECURSE SRC "${PROJECT_SOURCE_DIR}/*.i")
list(SORT SRC)

if(NOT SRC)
    message(FATAL_ERROR "No preprocessed sources found: ${PROJECT_SOURCE_DIR}")
endif()

include(${CSiBE_GEN_DIR}/CSiBE_flags.inc)

set(PREPROCESSED_C_FLAGS "${CMAKE_C_FLAGS}")

if(CMAKE_BUILD_TYPE)
    string(TOUPPER "${CMAKE_BUILD_TYPE}" BUILD_TYPE_UPPER)
    set(PREPROCESSED_C_FLAGS
        "${PREPROCESSED_C_FLAGS} ${CMAKE_C_FLAGS_${BUILD_TYPE_UPPER}}")
endif()

add_custom_command(OUTPUT "${SIZE_RESULT}"

    COMMAND "${PROJECT_GEN_DIR}/../preprocessed-source-compiler.py"
        --compiler "${CMAKE_C_COMPILER}"
        --cflags "${PREPROCESSED_C_FLAGS}"
        --object-dir "${OBJECT_DIR}"
        --size-dir "${SIZE_FRAGMENT_DIR}"
        --result-file "${SIZE_RESULT}"
        --dump-obj-size "${DUMP_OBJ_SIZE}"
        --sum-sizes "${SUM_SIZES}"
        -- ${SRC}
    DEPENDS ${SRC}
            "${PROJECT_GEN_DIR}/../preprocessed-source-compiler.py"
            "${DUMP_OBJ_SIZE}"
            "${SUM_SIZES}"
    VERBATIM
)

add_custom_target(${PROJECT_NAME}_size DEPENDS "${SIZE_RESULT}")


