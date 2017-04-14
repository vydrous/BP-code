#!/usr/bin/python3


def square_and_multiply(ot, p, q, e):
    n = p * q
    fi = (p - 1) * (q - 1)
    st = 1
    for i in "{0:b}".format(e):
        st = (st ** 2) % n
        if i == '1':
            st = (st * ot) % n
    return st


ot = 1520
p = 43
q = 59
e = 13
print(square_and_multiply(ot, p, q, e))
