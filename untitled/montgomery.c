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


BIGNUM * mon_prod(BIGNUM * a, BIGNUM * b, BIGNUM * N, int R_length, BIGNUM * Ni){

    BIGNUM * t = BN_new();
    BIGNUM * m = BN_new();
    BIGNUM * u = BN_new();

/*    //    t = (a * b)         #trvani operaci, bignum, shift po slovech
    //    m = ((t & (r - 1)) * n_inv) & (r - 1)
    //    u = (t + m * n) >> (r.bit_length() - 1)
*/
    BN_CTX * ctx = BN_CTX_new();
    BN_mul(t, a, b, ctx);
    BN_mask_bits(t,  R_length); /*t mod r*/


    BN_mul(m, t, Ni, ctx);
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

    BIGNUM * ot = BN_new();
    BIGNUM * st = BN_new();

/*    st = BN_bin2bn(y_bin, 4, st);
    x = BN_bin2bn(x_bin, 5, x);
*/

    char * a, *b, *n, *n_inv, *bit_exp, *sts;
    int length;
    int i, tmp;
    if (!PyArg_ParseTuple(args, "sssiss", &a, &b, &n, &length, &n_inv, &bit_exp ))
        return NULL;

    tmp = BN_dec2bn(&N, (const char*) n);
    tmp = BN_dec2bn(&Ni,(const char*) n_inv) ;
    tmp = BN_dec2bn(&ot,(const char*) a);
    tmp = BN_dec2bn(&st,(const char*) b);

    for( i = 0; i < strlen(bit_exp); i++){
        st = mon_prod(st, st, N, length, Ni);
        if( i == '1' ){
            st = mon_prod(st, ot, N, length, Ni);
        }
    }

    sts =  BN_bn2dec(st);
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