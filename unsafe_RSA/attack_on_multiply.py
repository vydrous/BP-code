#!/usr/bin/python3
import math
from Crypto.PublicKey import RSA
import random
import decrypt
from random import SystemRandom
import decimal
import timeit
import encrypt
import square_and_multiply

with open('../keys/public.pem') as r:
    pubkey = RSA.importKey(r.read(), '1234')

# n = decimal.Decimal(getattr(pubkey.key, 'n'))
n = getattr(pubkey.key, 'n')
e = getattr(pubkey.key, 'e')
dec_n = decimal.Decimal(n)
# todo
# find messages to compare times
# m1 = 5348513  # m1^(2i + posbits) < n and m1^(2i + posbits +1) >= n
# m2 = 10354135  # m2^(2i + posbits +1) < n
found = 0


n_bit = bin(n)[2:]
print(n_bit)
n_length = len(n_bit)

exp = 3
d = '1'
posbits = 1
i = 2

while not found:
    # m1 = cryptGen.randrange(decimal.Decimal(n ** (1 / 6)), decimal.Decimal(n ** (1 / 5)), 1)
    # m2 = cryptGen.seed(decimal.Decimal(n ** (1 / 6)))

    sufficient = 0
    while not sufficient:
        m1 = random.randint(0, n)
        if n < m1 * ((m1 ** (exp - 1)) % n):
            sufficient = 1
        else:
            print("m1 bad")

    sufficient = 0
    while not sufficient:
        m2 = random.randint(0, dec_n ** 1/exp )
        print(m2)
        if (m2 * ((m2 ** (exp - 1)) % n) ) < n:
            sufficient = 1
        else:
            print("m2 bad")

    print(bin(m1))
    print(bin(m2))

    t1 = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt;import attack_on_multiply; m1 = %i' % m1)
    t2 = timeit.Timer('decrypt.decrypt(int(m2))', setup='import decrypt;import attack_on_multiply; m2 = %i' % m2)

    r1 = t1.timeit(100)
    r2 = t2.timeit(100)

    print("\n%s\n\n%s" % (r1, r2))

    if r1 - r2 > 0.003:
        last_bit = 1  # change wheter tested bit is 0 or 1
        posbits += 1
    else:
        last_bit = 0

    d += str(last_bit)
    print("d = %s" % d)
    exp = (exp + last_bit - 1) * 2
    i += 1

    if square_and_multiply.square_and_multiply(int(encrypt.encrypt(m1)), n, d) == m1:
        found = 1
        # else:
        #
        # exp = 3
        # d = '1'
        # posbits = 1
        # i = 2
