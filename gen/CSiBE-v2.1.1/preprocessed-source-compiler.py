#!/usr/bin/env python3

# import argparse
# import os
# import subprocess

# if __name__ == "__main__":

#     # Use wrappers for compilers (native)
#     c_compiler_name = "gcc"

#     if "CC" in os.environ:
#         c_compiler_name = os.environ["CC"]

#     preprocessed_sources = ""

#     if "CSIBE_PREPROCESSED_SOURCES" in os.environ:
#         preprocessed_sources = os.environ["CSIBE_PREPROCESSED_SOURCES"].split()

#     compiler_preprocessed_flags = ["-x",
#                                    "cpp-output",
#                                    "-c"]

#     compiler_additional_flags = ["-fno-builtin"]

#     if c_compiler_name.endswith("g++") or c_compiler_name.endswith("clang++"):
#         compiler_additional_flags.extend(os.getenv("CSiBE_CXXFLAGS", "").split())
#     elif c_compiler_name.endswith("gcc") or c_compiler_name.endswith("clang"):
#         compiler_additional_flags.extend(os.getenv("CSiBE_CFLAGS", "").split())

#     compiler_call_list = [c_compiler_name]
#     compiler_call_list.extend(compiler_preprocessed_flags)
#     compiler_call_list.extend(compiler_additional_flags)

#     for source_path in preprocessed_sources:
#         actual_call_list = compiler_call_list
#         actual_call_list.append(source_path)
#         subprocess.call(compiler_call_list)

#!/usr/bin/env python3

import argparse
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Compile preprocessed C sources and collect object sizes"
    )

    parser.add_argument("--compiler", required=True)
    parser.add_argument("--cflags", default="")
    parser.add_argument("--object-dir", required=True)
    parser.add_argument("--size-dir", required=True)
    parser.add_argument("--result-file", required=True)
    parser.add_argument("--dump-obj-size", required=True)
    parser.add_argument("--sum-sizes", required=True)
    parser.add_argument("sources", nargs="+")

    return parser.parse_args()


def run_checked(command, description):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"{description} failed with exit code {exc.returncode}"
        ) from exc
    except OSError as exc:
        raise RuntimeError(
            f"{description} could not be started: {exc}"
        ) from exc


def make_object_path(object_dir, source_path, index, used_names):
    stem = source_path.stem or "source"
    object_name = f"{stem}.o"

    if object_name in used_names:
        object_name = f"{stem}_{index}.o"

    while object_name in used_names:
        object_name = f"{stem}_{index}_{len(used_names)}.o"

    used_names.add(object_name)
    return object_dir / object_name


def remove_old_size_fragments(size_dir):
    for fragment in size_dir.glob("*_result.txt"):
        if fragment.is_file():
            fragment.unlink()


def write_result_atomically(result_file, sum_sizes, size_dir):
    result_file.parent.mkdir(parents=True, exist_ok=True)

    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{result_file.name}.",
        dir=str(result_file.parent),
    )
    os.close(file_descriptor)

    try:
        run_checked(
            [sum_sizes, str(size_dir), temporary_name],
            "object-size aggregation",
        )
        os.replace(temporary_name, result_file)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def compile_sources(args):
    object_dir = Path(args.object_dir)
    size_dir = Path(args.size_dir)
    result_file = Path(args.result_file)

    source_paths = [Path(source) for source in args.sources]

    for source_path in source_paths:
        if not source_path.is_file():
            raise RuntimeError(f"preprocessed source does not exist: {source_path}")

    compiler_flags = shlex.split(args.cflags)

    object_dir.mkdir(parents=True, exist_ok=True)
    size_dir.mkdir(parents=True, exist_ok=True)

    remove_old_size_fragments(size_dir)

    # Do not leave a previous successful result after a failed experiment.
    if result_file.exists():
        result_file.unlink()

    used_object_names = set()

    for index, source_path in enumerate(source_paths, start=1):
        object_path = make_object_path(
            object_dir,
            source_path,
            index,
            used_object_names,
        )

        compile_command = [
            args.compiler,
            *compiler_flags,
            "-x",
            "cpp-output",
            "-fno-builtin",
            "-c",
            str(source_path),
            "-o",
            str(object_path),
        ]

        print(
            f"[{index}/{len(source_paths)}] compiling {source_path}",
            flush=True,
        )

        # Any non-zero return immediately raises and stops the experiment.
        run_checked(compile_command, f"compilation of {source_path}")

        print(
            f"[{index}/{len(source_paths)}] measuring {object_path}",
            flush=True,
        )

        run_checked(
            [
                args.dump_obj_size,
                str(object_path),
                str(size_dir),
            ],
            f"size measurement of {object_path}",
        )

    fragments = list(size_dir.glob("*_result.txt"))
    if not fragments:
        raise RuntimeError("no object-size fragments were generated")

    write_result_atomically(
        result_file,
        args.sum_sizes,
        size_dir,
    )


def main():
    args = parse_arguments()

    try:
        compile_sources(args)
    except (RuntimeError, ValueError) as exc:
        print(f"preprocessed-source-compiler.py: error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())