# Obfuscated

## Description:

553cc4t00r thinks Python is "safe" from reverse engineering. Prove them wrong.

This script is obfuscated. Running it will print the flag. However, REDACTED?

Files provided: obfuscated.py


# Solution

## files

```
> file obfuscated.py 
obfuscated.py: Python script, ASCII text executable, with very long lines (355)
```

## program

```
#!/usr/bin/env python3
# 553cc4t00r Obfuscation Engine v3.1
# "If you can read this, you're already too deep."

import zlib,base64;exec(zlib.decompress(base64.b64decode("eJxVj01rgzAAQP9LTg2M4kcneOglhRZjFzAavy6hibaNrUZqkGS/fowNxm4P3ru83vZyw7kaZ/0ynG+A1F0vFwC3Xf+N/5y4LH20A3Arot2vBnI0Th7u1zpsoybAz9aPr+kBr2JsHRkylebvKxmolRNSsk50MqGyDMjaMKrK6Y6qR2ZpSZ1gcVBURyyYNbRAF+rFOg/8QrDFkdNs2efTVANGHzUK2UBcXtxsxjrUeT89Y/EivbZqXDKfp6OTJ2ylus1ptt//3cA38NKG+yGA8AtviVTg")).decode())
```

The challenge looks hard at first, but noticing that theres a base64 encoded message... somewhere... That's the best place to start, so using Cyberchef on the string converting it from base64 then decompressing with zlib will yield this:

[figure 1]
input:

output:
```
exec(__import__("codecs").decode(__import__("base64").b64decode("cmtycChfX3Z6Y2JlZ19fKCJvbmZyNjQiKS5vNjRxcnBicXIoInBVV2NvYURiVnhBWkQxRVRybU92TWFJbUxtRTBaR09oS21TbUsyNGpxUzltWjJBMXB3UjNySTgxQUdBd0xtRTBaUU9sc0ZWYyIpLnFycGJxcigpKQ==").decode(),"rot_13"))
```

So more code, and this time it looks like it only needs to be decoded from base64.

[figure 2]

output:
```
rkrp(__vzcbeg__("onfr64").o64qrpbqr("pUWcoaDbVxAZD1ETrmOvMaImLmE0ZGOhKmSmK24jqS9mZ2A1pwR3rI81AGAwLmE0ZQOlsFVc").qrpbqr())
```

Now it looks incomprehensable, but what if, it only needs one more base64?


[figure 3]

output:
```
print("CLCTF{0bfusc4t10n_1s_n0t_s3cur17y_553cc4t00r}")
```

Flag: CLCTF{0bfusc4t10n_1s_n0t_s3cur17y_553cc4t00r}
