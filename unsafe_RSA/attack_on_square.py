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


def mont_exp(m, x, n):
    r = 2 ** (len(bin(n)) - 2)
    g, n_inv, r_inv = square_and_multiply.egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        r_inv = -r_inv
        n_inv = -n_inv

    m = (m * r) % n
    x = (x * r) % n

    m_temp = m

    m0, red0 = counted_sq_mul.montgomery_product(m, m, n, r, n_inv)

    m0 = square_and_multiply.montgomery_product(m0, 1, n, r, n_inv)

    m_temp = counted_sq_mul.montgomery_product(m, x, n, r, n_inv)[0]
    m1, red1 = counted_sq_mul.montgomery_product(m_temp, m_temp, n, r, n_inv)

    m1 = counted_sq_mul.montgomery_product(m1, 1, n, r, n_inv)


    return m0, red0, m1, red1


global r
global n_inv
global n

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
message_range = 500
for i in range(0, message_range):
    tmp = random.randint(0, n)

    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

    f = t.timeit(1)

    message_times[tmp] = f

fail_cnt = 0

current_power = []

for i in range(len(message_times)):
    current_power.append(1)
    #print(list(message_times.keys())[i],)
    current_power[i] = square_and_multiply.montgomery_product(int(list(message_times.keys())[i]), 1, n, r, n_inv)
    current_power[i] = square_and_multiply.montgomery_product(current_power[i], current_power[i], n, r, n_inv)

    #print(current_power[i])


while not found:

    m1_dict = []  # (c*c^2)^2 is done with reduction [1]
    m2_dict = []  # (c*c^2)^2 is done without reduction [1]
    m3_dict = []  # (c^2)^2 is done with reduction [0]
    m4_dict = []  # (c^2)^2 is done without reduction [0]

    print(bin(exp))

    new_current_power1 = []
    new_current_power0 = []
    for j in range(1, message_range):
        m0, flag0, m1, flag1 = mont_exp(current_power[j], int(list(message_times.keys())[j]), n)

#        print("%i %i  %i %i" % m0, flag0, m1, flag1)

        if flag1:
            m1_dict.append(list(message_times.values())[j])
        else:
            m2_dict.append(list(message_times.values())[j])

        if flag0:
            m3_dict.append(list(message_times.values())[j])
        else:
            m4_dict.append(list(message_times.values())[j])

        new_current_power1.append(m1)
        new_current_power0.append(m0)

    red1avg = sum(m1_dict) / float(len(m1_dict))
    unred1avg = sum(m2_dict) / float(len(m2_dict))
    diff1 = abs(red1avg - unred1avg)

    red0avg = sum(m3_dict) / float(len(m3_dict))
    unred0avg = sum(m4_dict) / float(len(m4_dict))
    diff0 = abs(red0avg - unred0avg)

    if diff1 > diff0:
        d += '1'
        current_power = new_current_power1
    else:
        d += '0'
        current_power = new_current_power0

    """
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

        for i in range(0, message_range):
            tmp = random.randint(0, n)

            t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

            r = t.timeit(1)

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
        last_bit = 1  # change wheter tested bit is 0 or 1
        posbits += 1
    else:
        last_bit = 0
        # if r2 > r1:
        #    fail_cnt += 1
        #    print("reduced time is greater %i" % fail_cnt)

    d += str(last_bit)
    print("d = %s" % d)
    exp = (exp + last_bit - 1) * 2 + 1
    i += 1

"""
    test_msg = list(message_times.keys())[0]

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
