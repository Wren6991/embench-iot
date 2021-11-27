/* Copyright (C) 2017 Embecosm Limited and University of Bristol

   Contributor Graham Markall <graham.markall@embecosm.com>

   This file is part of Embench and was formerly part of the Bristol/Embecosm
   Embedded Benchmark Suite.

   SPDX-License-Identifier: GPL-3.0-or-later */

#include <support.h>
#include <stdint.h>

// ----------------------------------------------------------------------------
// Hazard3 testbench IO

#define IO_BASE 0x80000000

struct io_hw {
  volatile uint32_t print_char;
  volatile uint32_t print_u32;
  volatile uint32_t exit;
};

#define mm_io ((struct io_hw *const)IO_BASE)

static inline void tb_putc(char c) {
  mm_io->print_char = (uint32_t)c;
}

static inline void tb_puts(const char *s) {
  while (*s)
    tb_putc(*s++);
}

static inline void tb_put_u32(uint32_t x) {
  mm_io->print_u32 = x;
}

static inline void tb_exit(uint32_t ret) {
  mm_io->exit = ret;
}

// ----------------------------------------------------------------------------

void
initialise_board ()
{
  // ...what? Is this supposed to be a memory clobber to stop the benchmark
  // from getting optimised out or leaking past the timer?
  tb_puts("Initialising...\n");
  __asm__ volatile ("li a0, 0" : : : "memory");
}

void __attribute__ ((noinline)) __attribute__ ((externally_visible))
start_trigger ()
{
  tb_puts("Starting...\n");
  asm volatile (
    "csrw mcycle, zero\n"
    "csrw mcycleh, zero\n"
    : : : "memory"
  );
}

void __attribute__ ((noinline)) __attribute__ ((externally_visible))
stop_trigger ()
{
  // Account for mcycleh incrementing
  uint32_t h0, l, h1;
  asm volatile (
    "csrr %0, mcycleh\n"
    "csrr %1, mcycle\n"
    "csrr %2, mcycleh\n"
    : "=r" (h0), "=r" (l), "=r" (h1)
    : : "memory"
  );
  tb_puts("Done.\n");
  tb_put_u32(h1);
  tb_put_u32(h0 == h1 ? l : 0);

}
