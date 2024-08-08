#!/usr/bin/env python3

# Python module to run programs natively.

# Copyright (C) 2019 Clemson University
#
# Contributor: Ola Jeppsson <ola.jeppsson@gmail.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Embench module to run benchmark programs.

This version is suitable for running programs natively.
"""

__all__ = [
    'get_target_args',
    'build_benchmark_cmd',
    'decode_results',
]

import argparse
import re
import os.path

from embench_core import log


def get_target_args(remnant):
    """Parse left over arguments"""
    parser = argparse.ArgumentParser(description='Get target specific args')

    # No target arguments
    return parser.parse_args(remnant)


def build_benchmark_cmd(bench, args):
    """Construct the command to run the benchmark.  "args" is a
       namespace with target specific arguments"""

    # Only supports .bin -- no ELF loader in the testbench. I added in a
    # "post_link" step where I can specify how to objcopy to binary in my chip
    # .cfg file.

    print(f"Running {bench}")
    tb_exec = os.getcwd() + "/../../tb_cxxrtl/tb"

    return [tb_exec, "--bin", bench + '.bin', '--cycles', '100000000']


def decode_results(stdout_str, stderr_str):
    """Extract the results from the output string of the run. Return the
       elapsed time in milliseconds or zero if the run failed."""

    # The output is of this form:

    # Initialising...
    # Starting...
    # Done.
    # 00000000
    # 00427017
    # CPU requested halt. Exit code 0
    # Ran for 4374103 cycles

    # The "Ran for" is just testbench output, which is the whole execution
    # time, not just the benchmarked period. The benchmark length, measured
    # with mcycleh/mcycle, is printed out as two u32s following "Done.".

    lines = stdout_str.strip().split("\n")
    if "CPU requested halt. Exit code 0" not in lines:
        log.debug('Warning: Bad or no return code')
        return 0.0

    if "Done." not in lines:
        log.debug("Warning: CPU never printed that it was done. Bailing out.")
        return 0.0

    index = lines.index("Done.")
    cycles_u64_hex = lines[index + 1] + lines[index + 2]
    cycles = int(cycles_u64_hex, 16)

    print(f"{cycles} cycles.")

    # 1 MHz nominal clock. Result in ms.
    return cycles * 1e-3
