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

found = 0


n_bit = bin(n)[2:]
print(n_bit)
n_length = len(n_bit)

exp = 3
d = '1'
posbits = 1
i = 2
message_times = dict()


#d = random.randint(n/2, n)

upper_range = 10000

for i in range(0, upper_range):
    tmp = random.randint(0, n)

    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)
    f = t.timeit(1)
    message_times[tmp] = f

#    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)
#    r = t.timeit(100)
#    [tmp] = r



fail_cnt = 0

#for i in message_times.values():
#    print(i)
#
#exit(0)


while not found:

    reduced_dict = dict()
    unreduced_dict = dict()
    print(bin(exp))

#    for i in message_times:
#        if counted_sq_mul.square_and_multiply(i, n, exp):
#            reduced_dict[i] = message_times[i]
#        else:
#            unreduced_dict[i] = message_times[i]

    for i in message_times:
        dummy, sq, mult = counted_sq_mul.square_and_multiply(i, n, exp)
        if mult:
            reduced_dict[i] = message_times[i]
        else:
            unreduced_dict[i] = message_times[i]

    while not unreduced_dict or not reduced_dict:
        print("generating more messages")

#        message_times = dict()

        for i in range(0, upper_range):

            tmp = random.randint(0, n)

            t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

            f = t.timeit(1)

            message_times[tmp] = f
            for i in message_times:
                dummy, sq, mult = counted_sq_mul.square_and_multiply(i, n, exp)
                if mult:
                    reduced_dict[i] = message_times[i]
                else:
                    unreduced_dict[i] = message_times[i]


    r1 = 0
    count = 0
    for i in reduced_dict:
        count = count + 1
        r1 += reduced_dict[i]
#        if count >= len(unreduced_dict):
#            break
    print("reduced %i" % count)
    r1 /= float(count)

    r2 = 0
    count = 0
    for i in unreduced_dict:
        count = count + 1
        r2 += unreduced_dict[i]
 #       if count >= len(reduced_dict):
 #           break
    print("unreduced %i" % count)
    r2 /= float(count)

#    tmp = reduced_dict.popitem()[0]
#    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)
#    r1 = t.timeit(100)
#
#    tmp = unreduced_dict.popitem()[0]
#    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)
#    r2 = t.timeit(100)


    print("\n%s\n\n%s" % (r1, r2))

    print("differ is %f" % (r1 - r2))
    if r1 - r2 >= 0.000002:
        last_bit = 1  # change wheter tested bit is 0 or 1
        posbits += 1
    else:
        last_bit = 0
        if r2 > r1:
            fail_cnt += 1
            print("reduced time is greater %i" % fail_cnt)

    d += str(last_bit)
    print("d = %s" % d)
    exp = (exp + last_bit - 1) * 2 + 1
    i += 1

    test_msg = reduced_dict.popitem()[0]

    if square_and_multiply.square_and_multiply(encrypt.encrypt(test_msg), n, d) == test_msg:
        print("found")
        found = 1
    else:
        if len(d) > n_length:
            exp = 3
            d = '1'
            posbits = 1
            i = 2
            fail_cnt = 0
            message_times = dict()

#desired d is 1000100011101110111011101110011010011111000001110111110111000100000110000111010001101010000100100100101101111011000000011000001