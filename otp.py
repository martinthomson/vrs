#!/usr/bin/env python3
import hashlib
import sys

count = 25
input = bytes.fromhex(sys.argv[1])
# Or, for a hard-coded ASCII string: input = b"secret"

print(f" 0: {input.hex()}")
x = hashlib.sha256(input)
for i in range(1,count):
    print(f"{i:>2}: {x.hexdigest()}")
    x = hashlib.sha256(x.digest())

print(f"{count:>2}: {x.hexdigest()}")
