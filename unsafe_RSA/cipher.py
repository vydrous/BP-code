#!/usr/bin/python3
import encrypt
import decrypt


ot = 264422387516565135435430

print(ot)

st = encrypt.encrypt(ot)

print(st)

print(decrypt.decrypt(st))