#!/usr/bin/python3

def montgomery_product(a, b, n_inv, r, n, cnt):
    t = a * b
    m = (t * n_inv) % r
    u = (t + m * n) // r
    if u > n:
        return u - n, ++cnt
    return u, cnt

def montgomery_multiplication(a, b, n, cnt):
    r = 2 ** (len(bin(n)) - 2)
    g, n_inv, r_inv = egcd(n, r)



    if (r * r_inv + n * n_inv) == 1:
        r_inv = abs(r_inv)
        n_inv = -n_inv

    a1 = (a * r) % n
    return montgomery_product(a1, b, n_inv, r, n, cnt)

#    print(r)
#    t = a * b
#    print(t)
#    m = (modinv(n, r) * (t % r)) % r
#    print(m)
#    t = (t + m * n) // r
#    print(t)
#    if t > n:
#        t = t - n
#    return t

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
        return x % m


def square_and_multiply(ot, n, e):
    st = 1
    cnt = 0
    for i in "{0:b}".format(int(e)):
        st, cnt = montgomery_multiplication(st, st, n, cnt)
        if i == '1':
         #   if st * ot > n:
          #      print("reduction")
            st, cnt = montgomery_multiplication(st, ot, n, cnt)

    return cnt


