#!/usr/bin/env python3
import sys

def hmacsha256(k, v):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, hmac
    ctx = hmac.HMAC(k, hashes.SHA256(), backend=default_backend())
    ctx.update(v)
    return ctx.finalize()

def extract(salt, ikm):
    return hmacsha256(salt, ikm)

def expand(prk, info):
    return hmacsha256(prk, info + bytes([1]))

def prf(k, name):
    return k.expand(name.encode('utf8'))

# The canonical encoding of the randomness.
ikm = sys.argv[1].encode('utf8')
# This is the one-time code.
salt = bytes.fromhex(sys.argv[2])
prk = extract(salt, ikm)

for line in sys.stdin:
    label = line.strip()
    order = expand(prk, label.encode('utf8'))
    print(f"{order.hex()} {label}")
