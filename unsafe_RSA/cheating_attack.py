#!/usr/bin/python3
import square_and_multiply
from Crypto.PublicKey import RSA
import random
import timeit
import counted_sq_mul
import encrypt


with open('../keys/private.pem') as r:

    privKey = RSA.importKey(r.read(), '1234')

n = getattr(privKey.key, 'n')
e = getattr(privKey.key, 'e')
d = getattr(privKey.key, 'd')


results = dict()

for iterator in range(1,d.bit_length()):
    results[iterator] = 0

exp = 3
posbits = 1
o = 2
n_length = n.bit_length()
message_times = dict()
message_range = 1000

d = "{0:b}".format(int(d))
print(type(d))
for z in range(0, message_range):
    tmp = random.randint(0, n)

    t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

    r = t.timeit(1)

    message_times[tmp] = r

found = 0

for stat in range(100):
  while 42:

    m1_dict = dict()  # (c*c^2)^2 is done with reduction [1]
    m2_dict = dict()  # (c*c^2)^2 is done without reduction [1]
    m3_dict = dict()  # (c^2)^2 is done with reduction [0]
    m4_dict = dict()  # (c^2)^2 is done without reduction [0]


    for j in message_times:
        dummy, sq, mult = counted_sq_mul.square_and_multiply(j, n, exp * 2)
        if sq:
            m1_dict[j] = message_times[j]
        else:
            m2_dict[j] = message_times[j]
        dummy, sq, mult = counted_sq_mul.square_and_multiply(j, n, (exp - 1) * 2)
        if sq:
            m3_dict[j] = message_times[j]
        else:
            m4_dict[j] = message_times[j]

    while not m1_dict or not m2_dict or not m3_dict or not m4_dict:
        print("generating more messages")
        #        message_times = dict()

        for bn in range(0, message_range):
            tmp = random.randint(0, n)

            t = timeit.Timer('decrypt.decrypt(int(m1))', setup='import decrypt; m1 = %i' % tmp)

            r = t.timeit(1)

            message_times[tmp] = r
        for z in message_times:
            dummy, sq, mult = counted_sq_mul.square_and_multiply(z, n, exp * 2)
            if sq:
                m1_dict[z] = message_times[z]
            else:
                m2_dict[z] = message_times[z]
            dummy, sq, mult = counted_sq_mul.square_and_multiply(z, n, (exp - 1) * 2)
            if sq:
                m3_dict[z] = message_times[z]
            else:
                m4_dict[z] = message_times[z]

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



    if last_bit == d[o]:
        results[o] += 1
    #d += str(last_bit)
    print("d = %s" % d)
    exp = int(d[:o]) * 2 + 1
    o += 1

    test_msg = m1_dict.popitem()[0]

#    if square_and_multiply.square_and_multiply(encrypt.encrypt(test_msg), n, d + '1') == test_msg:
#        print("found")
#        found = 1
#        #d += '1'
#    else:
#        if square_and_multiply.square_and_multiply(encrypt.encrypt(test_msg), n, d + '0') == test_msg:
#            print("found")
#            found = 1
#            #d += '0'
    if o >= len(d) :
            exp = 3
            posbits = 1
            i = 2
            fail_cnt = 0
            message_times = dict()
            break
for q in range(d.bit_length()):
    print("bit %i has hit ratio %f" % q, results[q] / float(500))