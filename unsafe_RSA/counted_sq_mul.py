#!/usr/bin/python3


def montgomery_product(a, b, n, r, n_inv):
    t = (a * b)
    m = ((t & (r - 1)) * n_inv) & (r - 1)
    u = (t + m * n) >> (r.bit_length() - 1)
    if u > n:
        t = m / n
        m = t / n
        return u - n, 1
    return u, 0


#def montgomery_multiplication(a, b, n, r, n_inv):

#    a1 = (a * r) % n
#    return montgomery_product(a1, b, n_inv, r, n)


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
#        return x % m                                            #source: http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python


def square_and_multiply(ot, n, e):
    r = 2 ** (n.bit_length())
    g, n_inv, r_inv = egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        r_inv = -r_inv
        n_inv = -n_inv

    ot = (ot * r) % n
    st = r % n


    for i in "{0:b}".format(int(e)):
        st, sq = montgomery_product(st, st, n, r, n_inv)
        if i == '1':
            st, mult = montgomery_product(st, ot, n, r, n_inv)

    return montgomery_product(st, 1, n, r, n_inv), sq, mult


