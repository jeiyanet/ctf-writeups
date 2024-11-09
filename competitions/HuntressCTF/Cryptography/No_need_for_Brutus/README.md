# No need for Brutus

## Challenge

![challenge](challenge.png)

## Solution

![solution1](solution1.png)

![solution2](solution2.png)

![solution3](solution3.png)

In this challenge, we are tasked with buying the flag from a website that can buy and sell items. We only have $50 in our inventory which is insufficient for the flag. There are other items we can buy and sell.

At first, I tried buying an apple with a ridiculously large number to attempt an overflow but it didn't work. I then tried inputting a negative number, and to my surprise, the website did not have input sanitation and we were able to buy more money. 

## FLAG

```text
flag{18bdd83cee5690321bb14c70465d3408}
```
