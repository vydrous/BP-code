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
import gc


def mont_exp(m, x, n):
    r = 2 ** (len(bin(n)) - 2)
    g, n_inv, r_inv = square_and_multiply.egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        r_inv = -r_inv
        n_inv = -n_inv

    m_temp = m

    m0, red0 = counted_sq_mul.montgomery_multiplication(m, m, n, r, n_inv)

    m_temp = counted_sq_mul.montgomery_multiplication(m, x, n, r, n_inv)[0]
    m1, red1 = counted_sq_mul.montgomery_multiplication(m_temp,m_temp,n,r,n_inv)

    return m0, red0, m1, red1


global r
global n_inv
global n

with open('../keys/public.pem') as r:
    pubkey = RSA.importKey(r.read(), '1234')

with open('../keys/private.pem') as r:
    privKey = RSA.importKey(r.read(), '1234')

desired_d = getattr(privKey.key, 'd')

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
print(n)
n_length = len(n_bit)


r = 2 ** (len(bin(n)) - 2)
g, n_inv, r_inv = square_and_multiply.egcd(n, r)

if (r * r_inv + n * n_inv) == 1:
    r_inv = -r_inv
    n_inv = -n_inv

exp = 3
d = '1'
posbits = 1
i = 2
message_times = dict()
message_range = 10000

gc.disable()
for i in range(0, message_range):
    tmp = random.randint(0, n)

    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

    r = t.timeit(1)
    gc.collect()
    message_times[tmp] = r

gc.enable()

fail_cnt = 0

current_power = []


while not found:

    m1_dict = dict()  # (c*c^2)^2 is done with reduction [1]
    m2_dict = dict()  # (c*c^2)^2 is done without reduction [1]
    m3_dict = dict()  # (c^2)^2 is done with reduction [0]
    m4_dict = dict()  # (c^2)^2 is done without reduction [0]

    print(bin(exp))


    for i in message_times:
        dummy, sq, mult = counted_sq_mul.square_and_multiply(i, n, exp * 2)
        if sq:
            m1_dict[i] = message_times[i]
        else:
            m2_dict[i] = message_times[i]
        dummy, sq, mult = counted_sq_mul.square_and_multiply(i, n, (exp - 1) * 2)
        if sq:
            m3_dict[i] = message_times[i]
        else:
            m4_dict[i] = message_times[i]

    while not m1_dict or not m2_dict or not m3_dict or not m4_dict:
        print("generating more messages")
        #        message_times = dict()
        gc.disable()
        for i in range(0, message_range):
            tmp = random.randint(0, n)

            t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

            r = t.timeit(1)
            gc.collect()
            message_times[tmp] = r
        for i in message_times:
            dummy, sq, mult = counted_sq_mul.square_and_multiply(i, n, exp * 2)
            if sq:
                m1_dict[i] = message_times[i]
            else:
                m2_dict[i] = message_times[i]
            dummy, sq, mult = counted_sq_mul.square_and_multiply(i, n, (exp - 1) * 2)
            if sq:
                m3_dict[i] = message_times[i]
            else:
                m4_dict[i] = message_times[i]

    r1 = 0
    count = 0
    for i in m1_dict:
        count = count + 1
        r1 += m1_dict[i]
    print("m1 %i" % count)
    r1 /= count

    r2 = 0
    count = 0
    for i in m2_dict:
        count = count + 1
        r2 += m2_dict[i]
    print("m2 %i" % count)
    r2 /= count

    r3 = 0
    count = 0
    for i in m3_dict:
        count = count + 1
        r3 += m3_dict[i]
    print("m3 %i" % count)
    r3 /= count

    r4 = 0
    count = 0
    for i in m4_dict:
        count = count + 1
        r4 += m4_dict[i]
    print("m4 %i" % count)
    r4 /= count

    print("\n%s\n%s\n%s\n%s\n" % (r1, r2, r3, r4))

    O1 = r1 - r2
    O2 = r3 - r4

    # if O1 < 0:
    #    O1 = 0
    # if O2 < 0:
    #    O2 = 0

    print("differ o1 is  %f" % (O1))
    print("differ o2 is  %f" % (O2))
    if (r1 - r2) > (r3 - r4):
        last_bit = 1  # change whether tested bit is 0 or 1
        posbits += 1
    else:
        last_bit = 0
        # if r2 > r1:
        #    fail_cnt += 1
        #    print("reduced time is greater %i" % fail_cnt)

    d += str(last_bit)
    print("d = 0b%s" % d)
    print("r = %s" % str(bin(desired_d)))
    exp = (exp + last_bit - 1) * 2 + 1
    i += 1

    test_msg = m1_dict.popitem()[0]

    if square_and_multiply.square_and_multiply(encrypt.encrypt(test_msg), n, d + '1') == test_msg:
        print("found")
        found = 1
        d += '1'
    else:
        if square_and_multiply.square_and_multiply(encrypt.encrypt(test_msg), n, d + '0') == test_msg:
            print("found")
            found = 1
            d += '0'
        if len(d) > n_length:
            exp = 3
            d = '1'
            posbits = 1
            i = 2
            fail_cnt = 0
            message_times = dict()


