from distutils.core import setup, Extension
setup(name='montgomery', version='1.0',
      ext_modules=[Extension('montgomery',
                             sources=['/home/vydra/PycharmProjects/untitled/montgomery.c'],
                             libraries=['crypto', 'ssl'],
                             extra_compile_args=['-g2']
                             )])