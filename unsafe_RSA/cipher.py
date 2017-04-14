#!/usr/bin/python3
import encrypt
import decrypt


ot = 561315313513651364

print(ot)

st = encrypt.encrypt(ot)

print(decrypt.decrypt(st))