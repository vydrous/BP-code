#!/usr/bin/python3
import square_and_multiply
from Crypto.PublicKey import RSA

def decrypt(st):

    with open('../keys/private.pem') as r:

        privKey = RSA.importKey(r.read(), '1234')

    n = getattr(privKey.key, 'n')
    d = getattr(privKey.key, 'd')

    return square_and_multiply.square_and_multiply(st, n, d)