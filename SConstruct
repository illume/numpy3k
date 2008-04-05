# Last Change: Wed Mar 05 02:00 PM 2008 J
# vim:syntax=python
import os
import sys
from os.path import join as pjoin, basename as pbasename, dirname as pdirname
from copy import deepcopy

from numscons import get_python_inc, get_pythonlib_dir
from numscons import GetNumpyEnvironment
from numscons import CheckCBLAS 
from numscons import write_info

from scons_support import CheckBrokenMathlib, define_no_smp, \
    check_mlib, check_mlibs, is_npy_no_signal

env = GetNumpyEnvironment(ARGUMENTS)
env.Append(CPPPATH = [get_python_inc()])
if os.name == 'nt':
    # NT needs the pythonlib to run any code importing Python.h, including
    # simple code using only typedef and so on, so we need it for configuration
    # checks
    env.AppendUnique(LIBPATH = [get_pythonlib_dir()])

#=======================
# Starting Configuration
#=======================
config = env.NumpyConfigure(custom_tests = {'CheckBrokenMathlib' : CheckBrokenMathlib,
    'CheckCBLAS' : CheckCBLAS}, config_h = pjoin(env['build_dir'], 'config.h'))

# numpyconfig_sym will keep the values of some configuration variables, the one
# needed for the public numpy API.
 
# Convention: list of tuples (definition, value). value:
# - 0: #undef definition
# - 1: #define definition
# - string: #define definition value
numpyconfig_sym = []

#---------------
# Checking Types
#---------------
if not config.CheckHeader("Python.h"):
    raise RuntimeError("Error: Python.h header is not found (or cannot be "
"compiled). On linux, check that you have python-dev/python-devel packages. On"
" windows, check \ that you have the platform SDK.")

def check_type(type, include = None):
    st = config.CheckTypeSize(type, includes = include)
    type = type.replace(' ', '_')
    if st:
        numpyconfig_sym.append(('SIZEOF_%s' % type.upper(), '%d' % st))
    else:
        numpyconfig_sym.append(('SIZEOF_%s' % type.upper(), 0))

for type in ('short', 'int', 'long', 'float', 'double', 'long double'):
    check_type(type)

for type in ('Py_intptr_t',):
    check_type(type, include = "#include <Python.h>\n")

# We check declaration AND type because that's how distutils does it.
if config.CheckDeclaration('PY_LONG_LONG', includes = '#include <Python.h>\n'):
    st = config.CheckTypeSize('PY_LONG_LONG', includes = '#include <Python.h>\n')
    assert not st == 0
    numpyconfig_sym.append(('DEFINE_NPY_SIZEOF_LONGLONG', '#define NPY_SIZEOF_LONGLONG %d' % st))
    numpyconfig_sym.append(('DEFINE_NPY_SIZEOF_PY_LONG_LONG', '#define NPY_SIZEOF_PY_LONG_LONG %d' % st))
else:
    numpyconfig_sym.append(('DEFINE_NPY_SIZEOF_LONGLONG', ''))
    numpyconfig_sym.append(('DEFINE_NPY_SIZEOF_PY_LONG_LONG', ''))

if not config.CheckDeclaration('CHAR_BIT', includes= '#include <Python.h>\n'):
    raise RuntimeError("Config wo CHAR_BIT is not supported with scons: please contact the maintainer (cdavid)")

#----------------------
# Checking signal stuff
#----------------------
if is_npy_no_signal():
    numpyconfig_sym.append(('DEFINE_NPY_NO_SIGNAL', '#define NPY_NO_SIGNAL\n'))
    config.Define('__NPY_PRIVATE_NO_SIGNAL', comment = "define to 1 to disable SMP support ")
else:
    numpyconfig_sym.append(('DEFINE_NPY_NO_SIGNAL', ''))

#---------------------
# Checking SMP option
#---------------------
if define_no_smp():
    nosmp = 1
else:
    nosmp = 0
numpyconfig_sym.append(('NPY_NO_SMP', nosmp))

#----------------------
# Checking the mathlib 
#----------------------
mlibs = [[], ['m'], ['cpml']]
mathlib = os.environ.get('MATHLIB')
if mathlib: 
    mlibs.insert(0, mathlib)

mlib = check_mlibs(config, mlibs)

# XXX: this is ugly: mathlib has nothing to do in a public header file
numpyconfig_sym.append(('MATHLIB', ','.join(mlib)))

#----------------------------------
# Checking the math funcs available
#----------------------------------
# Function to check:
mfuncs = ('expl', 'expf', 'log1p', 'expm1', 'asinh', 'atanhf', 'atanhl',
          'isnan', 'isinf', 'rint')

# Set value to 1 for each defined function (in math lib)
mfuncs_defined = dict([(f, 0) for f in mfuncs])

# TODO: checklib vs checkfunc ?
def check_func(f):
    """Check that f is available in mlib, and add the symbol appropriately.  """
    st = config.CheckDeclaration(f, language = 'C', includes = "#include <math.h>")
    if st:
        st = config.CheckFunc(f, language = 'C')
    if st:
	mfuncs_defined[f] = 1
    else:
	mfuncs_defined[f] = 0

for f in mfuncs:
    check_func(f)

if mfuncs_defined['expl'] == 1:
    config.Define('HAVE_LONGDOUBLE_FUNCS',
                  comment = 'Define to 1 if long double funcs are available')
if mfuncs_defined['expf'] == 1:
    config.Define('HAVE_FLOAT_FUNCS',
                  comment = 'Define to 1 if long double funcs are available')
if mfuncs_defined['asinh'] == 1:
    config.Define('HAVE_INVERSE_HYPERBOLIC',
                  comment = 'Define to 1 if inverse hyperbolic funcs are available')
if mfuncs_defined['atanhf'] == 1:
    config.Define('HAVE_INVERSE_HYPERBOLIC_FLOAT',
                  comment = 'Define to 1 if inverse hyperbolic float funcs are available')
if mfuncs_defined['atanhl'] == 1:
    config.Define('HAVE_INVERSE_HYPERBOLIC_LONGDOUBLE',
                  comment = 'Define to 1 if inverse hyperbolic long double funcs are available')

#-------------------------------------------------------
# Define the function PyOS_ascii_strod if not available
#-------------------------------------------------------
if not config.CheckDeclaration('PyOS_ascii_strtod', 
                               includes = "#include <Python.h>"):
    if config.CheckFunc('strtod'):
        config.Define('PyOS_ascii_strtod', 'strtod', 
                      "Define to a function to use as a replacement for "\
                      "PyOS_ascii_strtod if not available in python header")

#------------------------------------
# DISTUTILS Hack on AMD64 on windows
#------------------------------------
# XXX: this is ugly
if sys.platform=='win32' or os.name=='nt':
    from distutils.msvccompiler import get_build_architecture
    a = get_build_architecture()
    print 'BUILD_ARCHITECTURE: %r, os.name=%r, sys.platform=%r' % (a, os.name, sys.platform)
    if a == 'AMD64':
        distutils_use_sdk = 1
        config.Define('DISTUTILS_USE_SDK', distutils_use_sdk, 
                      "define to 1 to disable SMP support ")

#--------------
# Checking Blas
#--------------
if config.CheckCBLAS():
    build_blasdot = 1
else:
    build_blasdot = 0

config.Finish()
write_info(env)

#==========
#  Build
#==========

#---------------------------------------
# Generate the public configuration file
#---------------------------------------
config_dict = {}
# XXX: this is ugly, make the API for config.h and numpyconfig.h similar
for key, value in numpyconfig_sym:
    config_dict['@%s@' % key] = str(value)
env['SUBST_DICT'] = config_dict

include_dir = 'include/numpy'
env.SubstInFile(pjoin(env['build_dir'], 'numpyconfig.h'), 
                pjoin(env['src_dir'], include_dir, 'numpyconfig.h.in'))

env['CONFIG_H_GEN'] = numpyconfig_sym

#---------------------------
# Builder for generated code
#---------------------------
from scons_support import do_generate_array_api, do_generate_ufunc_api, \
                        generate_api_emitter,\
                        generate_from_template, generate_from_template_emitter, \
                        generate_umath, generate_umath_emitter

array_api_gen_bld = Builder(action = do_generate_array_api, 
                            emitter = generate_api_emitter)

ufunc_api_gen_bld = Builder(action = do_generate_ufunc_api, 
                            emitter = generate_api_emitter)

template_bld = Builder(action = generate_from_template, 
                       emitter = generate_from_template_emitter)

umath_bld = Builder(action = generate_umath, 
                    emitter = generate_umath_emitter)

env.Append(BUILDERS = {'GenerateMultiarrayApi' : array_api_gen_bld,
                       'GenerateUfuncApi' : ufunc_api_gen_bld,
                       'GenerateFromTemplate' : template_bld,
                       'GenerateUmath' : umath_bld})

#------------------------
# Generate generated code
#------------------------
# XXX: the use of env['build_dir'] and env['src_dir'] are really ugly. Will
# have to think about how removing them (using hierarchical scons and dir
# option ?)
from os.path import join as pjoin

scalartypes_src = env.GenerateFromTemplate(
                    pjoin(env['build_dir'], 'src', 'scalartypes'), 
                    pjoin(env['src_dir'], 'src', 'scalartypes.inc.src'))

arraytypes_src = env.GenerateFromTemplate(
                    pjoin(env['build_dir'], 'src', 'arraytypes'), 
                    pjoin(env['src_dir'], 'src', 'arraytypes.inc.src'))

sortmodule_src = env.GenerateFromTemplate(
                    pjoin(env['build_dir'], 'src', '_sortmodule'), 
                    pjoin(env['src_dir'], 'src', '_sortmodule.c.src'))

umathmodule_src = env.GenerateFromTemplate(
                    pjoin(env['build_dir'], 'src', 'umathmodule'), 
                    pjoin(env['src_dir'], 'src', 'umathmodule.c.src'))

scalarmathmodule_src = env.GenerateFromTemplate(
                    pjoin(env['build_dir'], 'src', 'scalarmathmodule'), 
                    pjoin(env['src_dir'], 'src', 'scalarmathmodule.c.src'))

umath = env.GenerateUmath(
            pjoin(env['build_dir'], '__umath_generated'), 
            pjoin(env['src_dir'], 'code_generators', 'generate_umath.py'))

multiarray_api = env.GenerateMultiarrayApi(
                        pjoin(env['build_dir'], 'multiarray_api'), 
                        [ pjoin(env['src_dir'], 'code_generators', 
                                'array_api_order.txt'),
                          pjoin(env['src_dir'], 'code_generators', 
                                'multiarray_api_order.txt')])

ufunc_api = env.GenerateUfuncApi(
                    pjoin(env['build_dir'], 'ufunc_api'), 
                    pjoin(env['src_dir'], 'code_generators', 'ufunc_api_order.txt'))

env.Append(CPPPATH = [pjoin(env['src_dir'], 'include'), env['build_dir']])

#-----------------
# Build multiarray
#-----------------
multiarray_src = [pjoin('src', 'multiarraymodule.c')]
multiarray = env.NumpyPythonExtension('multiarray', source = multiarray_src)

#------------------
# Build sort module
#------------------
sort = env.NumpyPythonExtension('_sort', source = sortmodule_src)

#-------------------
# Build umath module
#-------------------
umathmodule = env.NumpyPythonExtension('umath', source = umathmodule_src)

#------------------------
# Build scalarmath module
#------------------------
scalarmathmodule = env.NumpyPythonExtension('scalarmath', 
                                            source = scalarmathmodule_src)

#----------------------
# Build _dotblas module
#----------------------
if build_blasdot:
    dotblas_src = [pjoin('blasdot', i) for i in ['_dotblas.c']]
    blasenv = env.Clone()
    blasenv.Append(CPPPATH = pjoin(env['src_dir'], 'blasdot'))
    dotblas = blasenv.NumpyPythonExtension('_dotblas', source = dotblas_src)
