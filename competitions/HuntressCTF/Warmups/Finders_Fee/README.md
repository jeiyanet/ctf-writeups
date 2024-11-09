# Finders Fee

## Challenge

![challenge](challenge.png)

> The hint in this challenge is the "Find".

## Solution

We check the permissions of the find program with the following command:

```bash
ls -la $(which find)
```

From the output, we can see that it has special permissions.

After checking the man pages of find, we can use the *-files0-from* argument to get the contents of a file.

```bash
find -files0-from /home/finder/flag.txt
```

## FLAG

```text
flag{63a10f0440218364424b20f9ddf6ad39}
```
