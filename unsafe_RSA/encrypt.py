#!/usr/bin/python3

import square_and_multiply

from Crypto.PublicKey import RSA

def encrypt(ot):

    with open('../keys/public.pem') as r:

        RSAkey = RSA.importKey(r.read(), '1234')

#    print(getattr(RSAkey.key, 'n'))
#    print(getattr(RSAkey.key, 'e'))

    n = getattr(RSAkey.key, 'n')
    e = getattr(RSAkey.key, 'e')
    return square_and_multiply.square_and_multiply(ot, n, e, r)





#ot = 651351613684158318684
#print(encrypt(ot))