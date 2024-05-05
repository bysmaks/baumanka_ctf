perm_key = bytes.fromhex("3d8714b08c91252fdddd3e0da83c49059f4a2bcef2d8ccc2")
ciphertext = bytes.fromhex("1277325b5a300bb2cef033f510f903ad9221287066090b67")
a, b, m = 125, 16, 256


def xor(s1, s2):
    return bytes([x ^ y for x, y in zip(s1, s2)])


def decrypt(data):
    res = b""
    for x in data:
        res += bytes([(x - b) % m * pow(a, -1, m) % m])
    return res


if __name__ == "__main__":
    key = decrypt(perm_key)
    flag = xor(ciphertext, key)
    print(flag)
