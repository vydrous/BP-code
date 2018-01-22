#!/usr/bin/python3
import square_and_multiply
from Crypto.PublicKey import RSA

def decrypt(st):

    with open('../keys/private.pem') as fr:

        privKey = RSA.importKey(fr.read(), '1234')

    n = getattr(privKey.key, 'n')
    d = getattr(privKey.key, 'd')


    r = 2 ** (len(bin(n)) - 2)

    g, n_inv, r_inv = square_and_multiply.egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        n_inv = -n_inv % r
    else:
        raise Exception("bad GCD")

    return square_and_multiply.square_and_multiply(int(st), n, d, r, n_inv)