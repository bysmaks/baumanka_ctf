import os
from math import gcd
from random import *
from secret import flag

m = 256
b = randint(1, 255)
while True:
    a = randint(1, 255)
    if gcd(m, a) == 1:
        break


def xor(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("byte strings are not equal length")
    return bytes([x ^ y for x, y in zip(s1, s2)])


def encrypt(msg, key):
    ciphertext = xor(msg, key)
    return ciphertext


def permutation(data):
    res = b""
    for x in data:
        res += bytes([(a * x + b) % m])
    return res


if __name__ == '__main__':
    size = len(flag)
    key = os.urandom(size)
    ct = encrypt(flag, key)
    perm = permutation(key)
    assert(len(perm) == len(key))
    with open("output", 'w') as f:
        f.write(f'ciphertext = {ct.hex()}\n')
        f.write(f'permutaion = {perm.hex()}\n')
        f.write(f'parameters = {a}, {b}, {m}\n')
