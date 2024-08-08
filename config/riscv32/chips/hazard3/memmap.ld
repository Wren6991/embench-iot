MEMORY
  {
    RAM   (wx) : ORIGIN = 0x00000000, LENGTH = 4M
  }

OUTPUT_FORMAT("elf32-littleriscv", "elf32-littleriscv", "elf32-littleriscv")
OUTPUT_ARCH(riscv)
ENTRY(_start)

SECTIONS
{
  .text : {
    *(.vectors)
    *(.text*)
    . = ALIGN(4);
  } > RAM

  .rodata : {
    *(.rodata*)
    . = ALIGN(4);
  } > RAM

  .data : {
    PROVIDE(__global_pointer$ = . + 0x2000);
    *(.sdata*)
    *(.data*)
    . = ALIGN(4);
  } > RAM
  _edata = .; PROVIDE (_edata = .);
  .bss : {
    PROVIDE(__bss_start = .);
    *(.sbss*)
    *(.bss .bss.*)
    . = ALIGN(4);
  } > RAM
  _end = .; PROVIDE (_end = .);

  PROVIDE(__stack_top = ORIGIN(RAM) + LENGTH(RAM));
}


