#!/usr/bin/python3


def montgomery_product(a, b, n_inv, r, n):
    t = a * b
    m = (t * n_inv) % r
    u = (t + m * n) // r
    if u > n:
        return u - n, 1
    return u, 0


def montgomery_multiplication(a, b, n, r, n_inv):

    a1 = (a * r) % n
    return montgomery_product(a1, b, n_inv, r, n)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m                                            #source: http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python


def square_and_multiply(ot, n, e):
    r = 2 ** (len(bin(n)) - 2)
    g, n_inv, r_inv = egcd(n, r)

    if (r * r_inv + n * n_inv) == 1:
        r_inv = -r_inv
        n_inv = -n_inv

    st = 1
    for i in "{0:b}".format(int(e)):
        st, cnt = montgomery_multiplication(st, st, n, r, n_inv)
        cnt = 0
        if i == '1':
            st, cnt = montgomery_multiplication(st, ot, n, r, n_inv)

    return cnt


