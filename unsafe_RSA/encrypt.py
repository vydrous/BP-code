#!/usr/bin/python3

import square_and_multiply

from Crypto.PublicKey import RSA

def encrypt(ot):

    with open('../keys/public.pem') as fr:

        RSAkey = RSA.importKey(fr.read(), '1234')

#    print(getattr(RSAkey.key, 'n'))
#    print(getattr(RSAkey.key, 'e'))

    n = getattr(RSAkey.key, 'n')
    e = getattr(RSAkey.key, 'e')

    r = 2 ** (len(bin(n)) - 2)

    g, n_inv, r_inv = square_and_multiply.egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        n_inv = -n_inv % r
    else:
        raise Exception("bad GCD")

    return square_and_multiply.square_and_multiply(ot, n, e, r, n_inv)





#ot = 651351613684158318684
#print(encrypt(ot))