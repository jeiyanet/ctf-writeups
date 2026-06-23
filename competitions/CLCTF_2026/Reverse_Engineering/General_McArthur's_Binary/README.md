# General McArthur’s Binary

## Description:

General McArthur left behind a compiled binary. It asks for a password. Find it.

You don't need to brute-force it — the answer is already in there if you know where to look.

# Solution

## File information:
chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b5305f89f253b0da5fae2adfdd35073e08e6b37b, for GNU/Linux 3.2.0, not stripped

The answer is immediately in the binary file, if you to the procedure of files then strings.

## Strings:
[figure 1]

Flag: CLCTF{r3v3rs3_1t_s1mpl3_sseccatoor}

