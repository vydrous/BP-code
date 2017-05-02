#!/usr/bin/python3


def square_and_multiply(ot, n, e):
    st = 1
    for i in "{0:b}".format(e):
        st = (st ** 2) % n
        if i == '1':
         #   if st * ot > n:
          #      print("reduction")
            st = (st * ot) % n

    return st


#ot = 1520
#p = 43
#q = 59
#e = 13
#n = p * q
#fi = (p - 1) * (q - 1)
#print(square_and_multiply(ot, p, q, e))
