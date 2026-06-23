# Oh, Bummer

## Description
ssecca's most protected binary. It detects debugging and refuses to cooperate.

The flag is decrypted at runtime but only when the binary is not being debugged.

# Solution

## Files
chal: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=016e1c1287587edcba952d30c9122dc75321c19c, for GNU/Linux 3.2.0, not stripped

Upon opening the program in the Ghidra it seems to be straight forward.

```
undefined8 main(void)

{
  int iVar1;
  undefined8 uVar2;
  astruct aaStack_78 [33];
  undefined1 local_57;
  undefined8 uStack_50;
  undefined1 *local_40;
  undefined8 local_38;
  undefined8 local_30;
  size_t local_28;
  astruct *local_20;
  
  uStack_50 = 0x1011db;
  puts("[ ssecca Anti-Debug Vault ]");
  uStack_50 = 0x1011e0;
  iVar1 = is_debugged();
  if (iVar1 == 0) {
    uStack_50 = 0x10120c;
    local_28 = strlen(xkey);
    local_30 = 0x21;
    local_38 = 0x21;
    local_40 = aaStack_78;
    for (local_20 = (astruct *)0x0; local_20 < (astruct *)0x21; local_20 = local_20 + 1) {
      local_20[(long)aaStack_78] =
           (astruct)(xkey[(ulong)local_20 % local_28] ^ (byte)local_20[0x104040]);
    }
    local_57 = 0;
    printf("Vault unlocked: %s\n",aaStack_78);
    uVar2 = 0;
  }
  else {
    uStack_50 = 0x1011f3;
    puts("Debugger detected. Self-destruct initiated.");
    uVar2 = 1;
  }
  return uVar2;
}
```

Clean up the variables to make it easier to understand

```

undefined8 main(void)

{
  int debug_flag;
  undefined8 uVar1;
  astruct aaStack_78 [33];
  undefined1 local_57;
  undefined8 uStack_50;
  undefined1 *local_40;
  undefined8 local_38;
  undefined8 local_30;
  size_t key_length;
  astruct *counter;
  
  uStack_50 = 0x1011db;
  puts("[ ssecca Anti-Debug Vault ]");
  uStack_50 = 0x1011e0;
  debug_flag = is_debugged();
  if (debug_flag == 0) {
    uStack_50 = 0x10120c;
    key_length = strlen(xkey);
    local_30 = 33;
    local_38 = 33;
    local_40 = aaStack_78;
    for (counter = (astruct *)0x0; counter < (astruct *)33; counter = counter + 1) {
      counter[(long)aaStack_78] =
           (astruct)(xkey[(ulong)counter % key_length] ^ (byte)counter[0x104040]);
    }
    local_57 = 0;
    printf("Vault unlocked: %s\n",aaStack_78);
    uVar1 = 0;
  }
  else {
    uStack_50 = 0x1011f3;
    puts("Debugger detected. Self-destruct initiated.");
    uVar1 = 1;
  }
  return uVar1;
}


```

The key decryption is a bit complicated due to it using the stack multiple times and the data being hard to get, it can be solved by reversing the decryption function, however that is slow. As said in the description the key is decrypted in run time.

Upon looking at the is_debugged() function we can see that it's looking for a specific state of the program and just giving out a variable.

```

bool is_debugged(void)

{
  long lVar1;
  
  lVar1 = ptrace(PTRACE_TRACEME,0,0,0);
  if (lVar1 != -1) {
    ptrace(PTRACE_DETACH,0,0,0);
  }
  return lVar1 == -1;
}
```

If you look back at the main function, it just checks the flag


```
uStack_50 = 0x1011db;
  puts("[ ssecca Anti-Debug Vault ]");
  uStack_50 = 0x1011e0;
  debug_flag = is_debugged();
  if (debug_flag == 0)
```

Therefore in the debugger we just need to by pass this.


```
        001011db e8 89 ff        CALL       is_debugged                                      undefined is_debugged()
                 ff ff
        001011e0 85 c0           TEST       debug_flag,debug_flag
        001011e2 74 19           JZ         LAB_001011fd
```

Looking at this assembly, we can say that its the same as the decompiled version, its checking for zero, because JZ means Jump if Zero.


## Short aside
At the time we didn't really look further into what is test, because its not fully needed in solving, however here is a short explanation:

TEST operation1, operation2

It does an 'AND' operation, but its output will not be placed into the operation1, it will however affect the flag registers depending on the output.

In this case its comparing debug_flag with it self, if the TEST involve a zero, it will have the Zero Flag (ZF) register enabled, meaning that the operation resulted in zero, however, if it was any other number, let's say 1 it won't trigger the ZF register, which is needed to trigger the jump.

So in summary:
TEST debug_flag, debug_flag
If ZF is zero
    jump to to LAB_001011fd
else
    continue

## Continuation
Now, that we know that we just need to change the register of where the debug_flag is lets check on how it would look like in GNU DeBugger (GDB).

```
(gdb) set disassembly-flavor intel
(gdb) disassembly main
Dump of assembler code for function main:
   0x00000000000011bd <+0>:     push   rbp
   0x00000000000011be <+1>:     mov    rbp,rsp
   0x00000000000011c1 <+4>:     push   rbx
   0x00000000000011c2 <+5>:     sub    rsp,0x38
   0x00000000000011c6 <+9>:     mov    rax,rsp
   0x00000000000011c9 <+12>:    mov    rbx,rax
   0x00000000000011cc <+15>:    lea    rax,[rip+0xe3c]        # 0x200f
   0x00000000000011d3 <+22>:    mov    rdi,rax
   0x00000000000011d6 <+25>:    call   0x1030 <puts@plt>
   0x00000000000011db <+30>:    call   0x1169 <is_debugged>
   0x00000000000011e0 <+35>:    test   eax,eax
   0x00000000000011e2 <+37>:    je     0x11fd <main+64>
   0x00000000000011e4 <+39>:    lea    rax,[rip+0xe45]        # 0x2030
   0x00000000000011eb <+46>:    mov    rdi,rax
   0x00000000000011ee <+49>:    call   0x1030 <puts@plt>
   0x00000000000011f3 <+54>:    mov    eax,0x1
   0x00000000000011f8 <+59>:    jmp    0x12d8 <main+283>
   0x00000000000011fd <+64>:    mov    rax,QWORD PTR [rip+0x2e64]        # 0x4068 <xkey>
   0x0000000000001204 <+71>:    mov    rdi,rax
   0x0000000000001207 <+74>:    call   0x1040 <strlen@plt>
   0x000000000000120c <+79>:    mov    QWORD PTR [rbp-0x20],rax
   0x0000000000001210 <+83>:    mov    QWORD PTR [rbp-0x28],0x21
   0x0000000000001218 <+91>:    mov    rax,QWORD PTR [rbp-0x28]
   0x000000000000121c <+95>:    add    rax,0x1
   0x0000000000001220 <+99>:    mov    rdx,rax
   0x0000000000001223 <+102>:   sub    rdx,0x1
   0x0000000000001227 <+106>:   mov    QWORD PTR [rbp-0x30],rdx
   0x000000000000122b <+110>:   mov    edx,0x10
   0x0000000000001230 <+115>:   sub    rdx,0x1
   0x0000000000001234 <+119>:   add    rax,rdx
   0x0000000000001237 <+122>:   mov    esi,0x10
   0x000000000000123c <+127>:   mov    edx,0x0
   0x0000000000001241 <+132>:   div    rsi
   0x0000000000001244 <+135>:   imul   rax,rax,0x10
   0x0000000000001248 <+139>:   sub    rsp,rax
   0x000000000000124b <+142>:   mov    rax,rsp
   0x000000000000124e <+145>:   mov    QWORD PTR [rbp-0x38],rax
   0x0000000000001252 <+149>:   mov    QWORD PTR [rbp-0x18],0x0
   0x000000000000125a <+157>:   jmp    0x12a0 <main+227>
   0x000000000000125c <+159>:   lea    rdx,[rip+0x2ddd]        # 0x4040 <enc>
   0x0000000000001263 <+166>:   mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000001267 <+170>:   add    rax,rdx
   0x000000000000126a <+173>:   movzx  esi,BYTE PTR [rax]
   0x000000000000126d <+176>:   mov    rcx,QWORD PTR [rip+0x2df4]        # 0x4068 <xkey>
   0x0000000000001274 <+183>:   mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000001278 <+187>:   mov    edx,0x0
   0x000000000000127d <+192>:   div    QWORD PTR [rbp-0x20]
   0x0000000000001281 <+196>:   mov    rax,rdx
   0x0000000000001284 <+199>:   add    rax,rcx
   0x0000000000001287 <+202>:   movzx  eax,BYTE PTR [rax]
   0x000000000000128a <+205>:   xor    eax,esi
   0x000000000000128c <+207>:   mov    ecx,eax
   0x000000000000128e <+209>:   mov    rdx,QWORD PTR [rbp-0x38]
   0x0000000000001292 <+213>:   mov    rax,QWORD PTR [rbp-0x18]
   0x0000000000001296 <+217>:   add    rax,rdx
   0x0000000000001299 <+220>:   mov    BYTE PTR [rax],cl
   0x000000000000129b <+222>:   add    QWORD PTR [rbp-0x18],0x1
   0x00000000000012a0 <+227>:   mov    rax,QWORD PTR [rbp-0x18]
   0x00000000000012a4 <+231>:   cmp    rax,QWORD PTR [rbp-0x28]
   0x00000000000012a8 <+235>:   jb     0x125c <main+159>
   0x00000000000012aa <+237>:   mov    rdx,QWORD PTR [rbp-0x38]
   0x00000000000012ae <+241>:   mov    rax,QWORD PTR [rbp-0x28]
   0x00000000000012b2 <+245>:   add    rax,rdx
   0x00000000000012b5 <+248>:   mov    BYTE PTR [rax],0x0
   0x00000000000012b8 <+251>:   mov    rax,QWORD PTR [rbp-0x38]
   0x00000000000012bc <+255>:   lea    rdx,[rip+0xd99]        # 0x205c
   0x00000000000012c3 <+262>:   mov    rsi,rax
   0x00000000000012c6 <+265>:   mov    rdi,rdx
   0x00000000000012c9 <+268>:   mov    eax,0x0
   0x00000000000012ce <+273>:   call   0x1050 <printf@plt>
   0x00000000000012d3 <+278>:   mov    eax,0x0
   0x00000000000012d8 <+283>:   mov    rsp,rbx
   0x00000000000012db <+286>:   mov    rbx,QWORD PTR [rbp-0x8]
   0x00000000000012df <+290>:   leave
   0x00000000000012e0 <+291>:   ret
```


```
   0x00000000000011db <+30>:    call   0x1169 <is_debugged>
   0x00000000000011e0 <+35>:    test   eax,eax
   0x00000000000011e2 <+37>:    je     0x11fd <main+64>
```

Now Here, its much clearer on what is happening, well its mostly the same thing earlier, but now we can see which register is being used. We can see here at main+35, that eax most likely already has the value by this time, so before test is fully executed we should put a break and change the value of the register while the program is running.

Note 1: There will be some differences on how Ghidra and GDB will show the assembly of the program, but essentially it would be the same, I recommend that you check both to understand what is happening.

```
(gdb) break *main+35
Breakpoint 1 at 0x5555555551e0
(gdb) run
Starting program: /home/paeng/Downloads/Challenges/Rev Eng/Oh, Bummer/chal 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/x86_64-linux-gnu/libthread_db.so.1".
[ ssecca Anti-Debug Vault ]

Breakpoint 2, 0x00005555555551e0 in main ()
(gdb) info registers
rax            0x1                 1
rbx            0x7fffffffd820      140737488345120
rcx            0x7ffff7eb7d0b      140737352793355
rdx            0x0                 0
rsi            0x0                 0
rdi            0x0                 0
rbp            0x7fffffffd860      0x7fffffffd860
rsp            0x7fffffffd820      0x7fffffffd820
r8             0xffffffff          4294967295
r9             0x0                 0
r10            0x0                 0
r11            0x286               646
r12            0x1                 1
r13            0x7ffff7ffd000      140737354125312
r14            0x7fffffffd988      140737488345480
r15            0x555555557dd8      93824992247256
rip            0x5555555551e0      0x5555555551e0 <main+35>
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
fs_base        0x7ffff7da3740      140737351661376
gs_base        0x0                 0
(gdb) set $eax = 0
(gdb) info registers
rax            0x0                 0
rbx            0x7fffffffd820      140737488345120
rcx            0x7ffff7eb7d0b      140737352793355
rdx            0x0                 0
rsi            0x0                 0
rdi            0x0                 0
rbp            0x7fffffffd860      0x7fffffffd860
rsp            0x7fffffffd820      0x7fffffffd820
r8             0xffffffff          4294967295
r9             0x0                 0
r10            0x0                 0
r11            0x286               646
r12            0x1                 1
r13            0x7ffff7ffd000      140737354125312
r14            0x7fffffffd988      140737488345480
r15            0x555555557dd8      93824992247256
rip            0x5555555551e0      0x5555555551e0 <main+35>
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
fs_base        0x7ffff7da3740      140737351661376
gs_base        0x0                 0
(gdb) continue
Continuing.
Vault unlocked: CLCTF{4n71_d3bu9_byp4ss3d_ssecca}
[Inferior 1 (process 6115) exited normally]
```


By doing 
```
(gdb) break *main+35
```

we're saying "break at the pointer to the address of main + 35.

```
(gdb) run

Starting program: /home/paeng/Downloads/Challenges/Rev Eng/Oh, Bummer/chal 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/x86_64-linux-gnu/libthread_db.so.1".
[ ssecca Anti-Debug Vault ]

Breakpoint 2, 0x00005555555551e0 in main ()
```

Next (assuming you've chmod +x the program) you can run the program and it will stop at the address we've made earlier.

```
(gdb) info registers
rax            0x1                 1
rbx            0x7fffffffd820      140737488345120
rcx            0x7ffff7eb7d0b      140737352793355
rdx            0x0                 0
rsi            0x0                 0
rdi            0x0                 0
rbp            0x7fffffffd860      0x7fffffffd860
rsp            0x7fffffffd820      0x7fffffffd820
r8             0xffffffff          4294967295
r9             0x0                 0
r10            0x0                 0
r11            0x286               646
r12            0x1                 1
r13            0x7ffff7ffd000      140737354125312
r14            0x7fffffffd988      140737488345480
r15            0x555555557dd8      93824992247256
rip            0x5555555551e0      0x5555555551e0 <main+35>
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
fs_base        0x7ffff7da3740      140737351661376
gs_base        0x0                 0
```

Here we can see the registers at this point of the program:

```
0x00000000000011e0 <+35>:    test   eax,eax
```

The rax register (the 64 bit version of eax) has a value of one, now we need to change this by using the following command:


```
(gdb) set $eax = 0
```


```
(gdb) info registers
rax            0x0                 0
rbx            0x7fffffffd820      140737488345120
rcx            0x7ffff7eb7d0b      140737352793355
rdx            0x0                 0
rsi            0x0                 0
rdi            0x0                 0
rbp            0x7fffffffd860      0x7fffffffd860
rsp            0x7fffffffd820      0x7fffffffd820
r8             0xffffffff          4294967295
r9             0x0                 0
r10            0x0                 0
r11            0x286               646
r12            0x1                 1
r13            0x7ffff7ffd000      140737354125312
r14            0x7fffffffd988      140737488345480
r15            0x555555557dd8      93824992247256
rip            0x5555555551e0      0x5555555551e0 <main+35>
eflags         0x246               [ PF ZF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
fs_base        0x7ffff7da3740      140737351661376
gs_base        0x0                 0
```
Now looking at the registers, we finally have 0 to pass the if statement, now we continue the program and get the flag!

Clarification:
If you're confused to as why eax/rax is used here but in ghidra its is_debugger variable, its because at the beginning of the program there was a specific operation used:

```
0x00000000000011cc <+15>:    lea    rax,[rip+0xe3c]        # 0x200f
```

lea means "Load Effective Address", meaning, in the address of the current Instruction Pointer (64-bit) register + 0xe3c, load its address, which is 'is debugger', that's why rax has the address of 'is debugger' therefore its value, because it was loaded into rax.

Note 2: I don't fully understand the meaning of "lea" but, I assume its loading the specified address, however, I'm not sure if changing the contents of the register always will modify the value in the address and not the address itself.

Note 3: The instruction pointer is the pointer that is used to see what is the address of the next operation.

```
(gdb) continue
Continuing.
Vault unlocked: CLCTF{4n71_d3bu9_byp4ss3d_ssecca}
[Inferior 1 (process 6115) exited normally]
```

Now continuing the program yields the Flag!!

```
Flag: CLCTF{4n71_d3bu9_byp4ss3d_ssecca}
```


# Aside, Alternative solution

During the creation of this write up, I have suddenly thought of another way of solving the problem, instead of changing the value of eax, rip can be changed instead or using jump, I'll show it here.


## Solving by changing RIP register


Now instead of changing the eax register you can change the rip register, because it points to the next instruction to be executed, doing so will effectively jump the program to executing your specified address.

So you break the program, then change the RIP.

```
   0x00000000000011e0 <+35>:    test   eax,eax
   0x00000000000011e2 <+37>:    je     0x11fd <main+64>
```

```
(gdb) set $rip = *main+64
(gdb) continue
Continuing.
Vault unlocked: CLCTF{4n71_d3bu9_byp4ss3d_ssecca}
[Inferior 1 (process 6417) exited normally]
```

## Solving by jumping

if you saw the je or jz it will show where to jump next, so instead of changing any of the registers and understanding the program, it may be faster to just jump to the needed part of the program.

```
(gdb) jump *main+64
Continuing at 0x5555555551fd.
Vault unlocked: CLCTF{4n71_d3bu9_byp4ss3d_ssecca}
[Inferior 1 (process 6621) exited normally]
```
