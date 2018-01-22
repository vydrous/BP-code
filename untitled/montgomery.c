#include <python3.6m/Python.h>
#include <openssl/bn.h>
#include <openssl/bio.h>
/*
 * TODO:
 *
 * own MONT_CTX
 * */

/*typedef struct montgomery_context{
    int ri;         * number of bits in R /
    BIGNUM RR;      * R^2 (used to convert to Montgomery form) /
    BIGNUM N;       * The modulus
    BIGNUM Ni;      * R*(1/R mod N) - N*Ni = 1
                     (Ni is only stored for bignum algorithm) /
    BN_ULONG n0;    * least significant word of Ni /
    int flags;
} MCTX;

MCTX * init_context(){
};*/

BIGNUM * extendedEuclid (BIGNUM * a, BIGNUM * x, BIGNUM * b, BIGNUM * y){

    BIGNUM * tmp = BN_new();
    BIGNUM * y1 = BN_new();
    BIGNUM * x1 = BN_new();
    BIGNUM * res;
    BN_CTX * ctx = BN_CTX_new();



    if (BN_is_zero(a)) {
        BN_dec2bn(&x, "0");
        BN_dec2bn(&y, "1");

		return b;
	}
    BN_mod(tmp, b, a, ctx);
    res = extendedEuclid(tmp, x1, a, y1);

    BN_div(x, NULL, b, a, ctx);
    BN_mul(x, x, x1, ctx);
    BN_sub(x, y1, x);

    BN_copy(y,x1);

    /*printf("++++++++++++++++++++\na = %s\nb = %s\nx = %s\ny = %s\nx1 = %s\ny1 = %s\n",
           BN_bn2dec(a), BN_bn2dec(b),
           BN_bn2dec(x), BN_bn2dec(y),
           BN_bn2dec(x1), BN_bn2dec(y1));*/
    BN_CTX_free(ctx);
    return res;
}


int extendedEuclid_it(BIGNUM * a, BIGNUM * x, BIGNUM * b, BIGNUM * y){
/*    BIGNUM * a = BN_dup(c);
    BIGNUM * b = BN_dup(d);*/
    BIGNUM * prevx = BN_new();
    BIGNUM * prevy = BN_new();
    BIGNUM * q = BN_new();
    BIGNUM * tmp = BN_new();
    BN_CTX * ctx = BN_CTX_new();

    BN_dec2bn(&x, "0");
    BN_dec2bn(&y, "1");
    BN_dec2bn(&prevx, "1");
    BN_dec2bn(&prevy, "0");

    while (!BN_is_zero(b) ){

        BN_div(q, NULL, a, b, ctx);

        BN_mul(tmp, q, x, ctx);
        BN_sub(tmp, prevx, tmp);

        BN_copy(prevx, x);
        BN_copy(x,tmp);

        BN_mul(tmp, q, y, ctx);
        BN_sub(tmp, prevy, tmp);

        BN_copy(prevy, y);
        BN_copy(y, tmp);

        BN_mod(tmp, a, b, ctx);
        BN_copy(a, b);
        BN_copy(b, tmp);

    }

    BN_copy(x, prevx);
    BN_copy(y, prevy);

    BN_free(prevx);
    BN_free(prevy);
    BN_free(q);
    BN_free(tmp);

    return 0;

}


BIGNUM * mon_prod(BIGNUM * a, BIGNUM * b, BIGNUM * N, int R_length, BIGNUM * Ni, BIGNUM * R){

    BIGNUM * t = BN_new();
    BIGNUM * m = BN_new();
    BIGNUM * u = BN_new();

/*    //    t = (a * b)         #trvani operaci, bignum, shift po slovech
    //    m = ((t & (r - 1)) * n_inv) & (r - 1)
    //    u = (t + m * n) >> (r.bit_length() - 1)
*/
    BN_CTX * ctx = BN_CTX_new();
    BN_mul(t, a, b, ctx);

    BN_mod_mul(m, t, Ni, R ,ctx);

    BN_mul(u, m, N, ctx);

/*    printf("=======================\n");
    printf("t = (a*b) = %s\n", BN_bn2dec(t));
    printf("m = (t*Ni)mod R = %s\n", BN_bn2dec(m));
    printf("u = m*N = %s\n", BN_bn2dec(u));*/

    BN_add(m, u, t);
    BN_rshift(u, m, R_length);

/*    printf("m = u+t = %s\n", BN_bn2dec(m));
    printf("u = m/R = %s\n\n", BN_bn2dec(u));*/

    if (BN_cmp(u, N) >= 0 ){
        BN_sub(m, u, N);
/*        printf("doing final reduction \n\n\n");*/
        BN_free(u);
        BN_free(t);
        BN_CTX_free(ctx);
        return m;
    }
    BN_free(t);
    BN_free(m);
    BN_CTX_free(ctx);
    return u;

}


static PyObject *
montgomery_mult(PyObject *self, PyObject *args)
{
/*    BIGNUM * mod = BN_new();

    unsigned char mod_bin[]= "10001";
    unsigned char x_bin[]= "1011";
    unsigned char y_bin[]= "101";

    mod = BN_bin2bn((const unsigned char*) mod_bin, 1, mod);
*/
    BIGNUM * N = BN_new();
    BIGNUM * Ni = BN_new();
    BIGNUM * R = BN_new();
    BIGNUM * Ri = BN_new();

    BIGNUM * ot = BN_new();
    BIGNUM * st = BN_new();
    BIGNUM * one = BN_new();
    BN_CTX * ctx = BN_CTX_new();

    char * a, *n, *bit_exp, *sts, *n_inv;
    char *r;
    int length;
    unsigned int i, tmp;
    if (!PyArg_ParseTuple(args, "ssssis", &a, &n,  &bit_exp, &r, &length, &n_inv))
        return NULL;



    tmp = BN_dec2bn(&one, "1");
    tmp = BN_dec2bn(&N, (const char*) n);
    tmp = BN_dec2bn(&Ni,(const char*) n_inv) ;
    tmp = BN_dec2bn(&ot,(const char*) a);
/*    tmp = BN_dec2bn(&ot,(const char*) b);*/
    tmp = BN_dec2bn(&R,(const char*) r);

/*    printf("+++++++++init+++++++++++\nR = %s\nN = %s\n",
           BN_bn2dec(R), BN_bn2dec(N));*/
/*
    extendedEuclid_it(BN_dup(R), Ri, BN_dup(N), Ni);
*/


/*
    printf("bit exp=%s\n st=%s\n ot=%s\n n=%s\n ninv=%s\n l=%i\n",
           bit_exp, a, b, n, n_inv, length);
    printf("strlen exponent %i\n", (int)strlen(bit_exp));
*/

  /*  if(! BN_is_negative(Ni)){
        BN_set_negative(Ni, 1);
        BN_add(Ni, Ni, R);
    }else{
        BN_set_negative(Ni, 0);
        BN_sub(Ni, Ni, R);
    }*/

   /* printf("R = %s\nN = %s\n", BN_bn2dec(R), BN_bn2dec(N));
    printf("Ri = %s\nNi = %s\n", BN_bn2dec(Ri), BN_bn2dec(Ni));*/
    BN_mod_mul(ot, ot, R, N, ctx);

    BN_mod_mul(st, one, R, N, ctx);
/*    printf("st = %s\not = %s\n", BN_bn2dec(st), BN_bn2dec(ot));*/

    for( i = 0; i < strlen(bit_exp); i++){
        st = mon_prod(st, st, N, length, Ni,R);
        if( bit_exp[i] == '1' ){
            st = mon_prod(st, ot, N, length, Ni, R);
        }
    }

    st = mon_prod(st, one, N, length, Ni, R);

    sts = BN_bn2dec(st);
    return Py_BuildValue("s", sts);
}

static PyMethodDef MontgomeryMethods[] = {
    {"mult",  montgomery_mult, METH_VARARGS,
     "Montgomery multiplocation"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef montgomerymodule = {
    PyModuleDef_HEAD_INIT,
    "montgomery",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
   MontgomeryMethods
};

PyMODINIT_FUNC
PyInit_montgomery(void)
{
    return PyModule_Create(&montgomerymodule);
}








int main(int argc, char * argv[]) {

    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("spam", PyInit_montgomery);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("montgomery");


    PyMem_RawFree(program);
    return 0;
}