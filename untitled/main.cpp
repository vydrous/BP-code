#include <iostream>
#include <openssl/bn.h>
#include <openssl/bio.h>

/*
 * TODO:
 *
 * own MONT_CTX
 * */

//int mon_prod(BIGNUM * a, BIGNUM * b, BN_MONT_CTX * mont){
//
//    BIGNUM * t = BN_new();
//    BIGNUM * m = BN_new();
//    BIGNUM * u = BN_new();
//    //    t = (a * b)         #trvani operaci, bignum, shift po slovech
//    //    m = ((t & (r - 1)) * n_inv) & (r - 1)
//    //    u = (t + m * n) >> (r.bit_length() - 1)
//
//    BN_mul(t, a, b, (BN_CTX *) mont);
//
//    BN_mul(m, BN_mask_bits(t,  &mont->ri), mont -> Ni);
//    BN_mask_bits( m, &mont->ri);
//
//    BN_mul(u, m, mont -> N);
//    BN_add(m, u, t);
//    BN_rshift(u, m, mont-> ri);
//
//}


int main() {

    BN_MONT_CTX * mont = BN_MONT_CTX_new();
    BN_CTX * ctx = BN_CTX_new();
    BN_CTX_start(ctx);
    BIGNUM * mod = BN_new();

    unsigned char mod_bin[]= "10001";
    unsigned char x_bin[]= "1011";
    unsigned char y_bin[]= "101";

    mod = BN_bin2bn((const unsigned char*) mod_bin, 1, mod);

    BIGNUM * x = BN_new();
    BIGNUM * y = BN_new();

    y = BN_bin2bn(y_bin, 4, y);
    x = BN_bin2bn(x_bin, 5, x);

    BN_MONT_CTX_set(mont, mod, ctx);

    BIO *out;

    out = BIO_new_fp(stdout, BIO_NOCLOSE);

    BN_print(out, mod);

 //   mon_prod(x, y, mont);

    std::cout << std::endl << "Hello, World!" << std::endl;
    return 0;
}