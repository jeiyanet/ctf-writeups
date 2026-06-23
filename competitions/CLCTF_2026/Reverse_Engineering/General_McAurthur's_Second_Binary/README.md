# General McArthur’s Second Binary

## Description:

The flag was encrypted with a repeating-key XOR before being compiled in. strings won't save you this time — you'll need to understand what the binary does at runtime.

# Solution 
## File information:
chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=24c43ecd71f9935f774a19288bcbd47b860672d8, for GNU/Linux 3.2.0, not stripped


## Strings:
``` 
> strings chal
/lib64/ld-linux-x86-64.so.2
puts
__libc_start_main
__cxa_finalize
printf
libc.so.6
GLIBC_2.2.5
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
PTE1
u+UH
553cc4
[ 553cc4 Decryption Engine ]
Decrypted: %s
vyp7%OM
A<WXYj
;*3$"
GCC: (Debian 15.2.0-17) 15.2.0
Scrt1.o
__abi_tag
crtstuff.c
deregister_tm_clones
__do_global_dtors_aux
completed.0
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
crackme.c
__FRAME_END__
_DYNAMIC
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_start_main@GLIBC_2.34
_ITM_deregisterTMCloneTable
puts@GLIBC_2.2.5
_edata
_fini
printf@GLIBC_2.2.5
__data_start
__gmon_start__
__dso_handle
_IO_stdin_used
_end
__bss_start
main
__TMC_END__
_ITM_registerTMCloneTable
__cxa_finalize@GLIBC_2.2.5
_init
.symtab
.strtab
.shstrtab
.note.gnu.build-id
.interp
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.note.gnu.property
.note.ABI-tag
.init_array
.fini_array
.dynamic
.got.plt
.data
.bss
.comment
```

Now the strings don’t offer much information. However it gives us a clue that there is decryption that is happening. So lets look further in Ghidra.

```
undefined8 main(void)

{
  ulong uVar1;
  byte *pbVar2;
  byte local_38 [32];
  undefined1 local_18;
  
  pbVar2 = local_38;
  uVar1 = 0;
  do {
    *pbVar2 = "553cc4"[uVar1 % 6] ^ (&enc)[uVar1];
    uVar1 = uVar1 + 1;
    pbVar2 = pbVar2 + 1;
  } while (uVar1 != 0x20);
  local_18 = 0;
  puts("[ 553cc4 Decryption Engine ]");
  printf("Decrypted: %s\n",local_38);
  return 0;
}
```

Looking at the decompiled code it looks like its doing a xor operation with an encoded text, the key is using “553cc4”.

Double clicking enc you will see a long array in the program, having the following byte string:

```
76 79 70 37 25 4f 4d 05 41 3c 57 58 59 6a 04 0b 50 6b 02 5d 02 0d 04 01 6a 00 06 50 00 57 01 48
```

Having the key and the and the encoded text, placing it into Cyberchef gives the flag. However, you need to convert it from hex then xor it to get the flag.


[figure 1]




Flag: CLCTF{x0r_4ll_7h3_7h1ng5_553cc4}

