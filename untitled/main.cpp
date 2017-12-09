#include <iostream>
#include <openssl/bn.h>
#include <openssl/bio.h>

/*
 * TODO:
 *
 * own MONT_CTX
 * */

//typedef struct montgomery_context{
//    int ri;         /* number of bits in R */
//    BIGNUM RR;      /* R^2 (used to convert to Montgomery form) */
//    BIGNUM N;       /* The modulus */
//    BIGNUM Ni;      /* R*(1/R mod N) - N*Ni = 1
//                    * (Ni is only stored for bignum algorithm) */
//    BN_ULONG n0;    /* least significant word of Ni */
//    int flags;
//} MCTX;
//
//MCTX * init_context(){
//

//}

BIGNUM * mon_prod(BIGNUM * a, BIGNUM * b, BIGNUM * N, int R_length, BIGNUM * Ni){

    BIGNUM * t = BN_new();
    BIGNUM * m = BN_new();
    BIGNUM * u = BN_new();

    //    t = (a * b)         #trvani operaci, bignum, shift po slovech
    //    m = ((t & (r - 1)) * n_inv) & (r - 1)
    //    u = (t + m * n) >> (r.bit_length() - 1)

    BN_CTX * ctx = BN_CTX_new();
    BN_mul(t, a, b, ctx);

    BN_mask_bits(t,  R_length);
    BN_mul(m, t, Ni,  ctx);
    BN_mask_bits( m, R_length);

    BN_mul(u, m, N, ctx);
    BN_add(m, u, t);
    BN_rshift(u, m, R_length);


    if (BN_cmp(u, N) >= 0 ){
        BN_sub(m, u, N);
        BN_free(u);
        BN_free(t);
        return m;
    }
    BN_free(t);
    BN_free(m);
    return u;

}




int main(int argc, char * argv) {

    BN_MONT_CTX * mont = BN_MONT_CTX_new();
    BN_CTX * ctx = BN_CTX_new();
    BN_CTX_start(ctx);
    BIGNUM * mod = BN_new();

    unsigned char mod_bin[]= "10001";
    unsigned char x_bin[]= "1011";
    unsigned char y_bin[]= "101";

    mod = BN_bin2bn((const unsigned char*) mod_bin, 1, mod);

    BIGNUM * N = BN_new();
    BIGNUM * Ni = BN_new();

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