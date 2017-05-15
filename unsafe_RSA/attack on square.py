#!/usr/bin/python3

from Crypto.PublicKey import RSA
import random
import decrypt
from random import SystemRandom
import decimal
import timeit
import encrypt
import square_and_multiply
import counted_sq_mul
import bigfloat



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
message_times = dict()

for i in range(0, 10000):
   tmp = random.randint(0, n)

   t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

   r = t.timeit(1)

   message_times[tmp] = r




while not found:

    reduced_dict = dict()
    unreduced_dict = dict()

    for i in message_times:
        if counted_sq_mul.square_and_multiply(i, n, exp):
            reduced_dict[tmp] = message_times[i]
        else:
            unreduced_dict[tmp] = message_times[i]

    r1 = 0
    count = 0
    for i in reduced_dict:
        count += 1
        r1 += reduced_dict[i]
    r1 /= count

    r2 = 0
    count = 0
    for i in unreduced_dict:
        count += 1
        r2 += unreduced_dict[i]
    r2 /= count


    print("\n%s\n\n%s" % (r1, r2))

    if r1 - r2 > 0.000001:
        last_bit = 1  # change wheter tested bit is 0 or 1
        posbits += 1
    else:
        last_bit = 0

    d += str(last_bit)
    print("d = %s" % d)
    exp = (exp + last_bit - 1) * 2
    i += 1

