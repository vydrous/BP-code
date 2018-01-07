#!/usr/bin/python3
import montgomery

def montgomery_product(a, b, n, r, n_inv):
    t = (a * b)         #trvani operaci, bignum, shift po slovech
    m = ((t & (r - 1)) * n_inv) & (r - 1)
    u = (t + m * n) >> (r.bit_length() - 1)
    if u > n:
        m = t / n
        temp = t*t / n * m ** 5
        return u - n #- int(temp) + int(temp)
    return u




def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


#def modinv(a, m):
#    g, x, y = egcd(a, m)
#    if g != 1:
#        raise Exception('modular inverse does not exist')
#    else:
#        return x % m


def square_and_multiply(ot, n, e):
    r = 2 ** (n.bit_length())
    g, n_inv, r_inv = egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        n_inv = -n_inv % r
    else:
        raise Exception("bad GCD")

    ot = (ot * r) % n
    st = (1 * r) % n

#    print("r = ", r)
#    print("st =", st, "\not =", ot)

#    for i in "{0:b}".format(int(e)):
#        st = montgomery_product(st, st, n, r, n_inv)
#        if i == '1':
#            st = montgomery_product(st, ot, n, r, n_inv)
#    return montgomery_product(st, 1, n, r, n_inv)



#    print("getting to C")
    st = montgomery.mult(str(st), str(ot), str(n), r.bit_length() - 1, str(n_inv), "{0:b}".format(int(e)), str(r))
 #   print("leaving C ", st)
    return int(st)




a = 5
e = 3
n = 13

print(square_and_multiply(a, n, e)) # 8

#ot = 1520
#p = 43
#q = 59
#e = 13
#n = p * q
#print(n)
#fi = (p - 1) * (q - 1)
#print(square_and_multiply(ot, n, e)) # 95
