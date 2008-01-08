#! Last Change: Tue Jan 08 10:00 PM 2008 J

__docstring__ = """Code to support special facilities to scons which are only
useful for numpy.core, hence not put into numpy.distutils.scons"""

import sys
import os

from os.path import join as pjoin, dirname as pdirname, basename as pbasename
from copy import deepcopy

from code_generators.generate_array_api import \
     do_generate_api as nowrap_do_generate_array_api
from code_generators.generate_ufunc_api import \
     do_generate_api as nowrap_do_generate_ufunc_api

from numscons.numdist import process_c_str as process_str
from numscons.core.utils import rsplit, isstring

import SCons.Node
import SCons

def split_ext(string):
    sp = rsplit(string, '.', 1)
    if len(sp) == 1:
        return (sp[0], '')
    else:
        return sp
#------------------------------------
# Ufunc and multiarray API generators
#------------------------------------
def do_generate_array_api(target, source, env):
    nowrap_do_generate_array_api([str(i) for i in target], 
                                 [str(i) for i in source])
    return 0

def do_generate_ufunc_api(target, source, env):
    nowrap_do_generate_ufunc_api([str(i) for i in target], 
                                 [str(i) for i in source])
    return 0

def generate_api_emitter(target, source, env):
    """Returns the list of targets generated by the code generator for array
    api and ufunc api."""
    base, ext = split_ext(str(target[0]))
    dir = pdirname(base)
    ba = pbasename(base)
    h = pjoin(dir, '__' + ba + '.h')
    c = pjoin(dir, '__' + ba + '.c')
    txt = base + '.txt'
    #print h, c, txt
    t = [h, c, txt]
    return (t, source)

#-------------------------
# From template generators
#-------------------------
# XXX: this is general and can be used outside numpy.core.
def do_generate_from_template(targetfile, sourcefile, env):
    t = open(targetfile, 'w')
    s = open(sourcefile, 'r')
    allstr = s.read()
    s.close()
    writestr = process_str(allstr)
    t.write(writestr)
    t.close()
    return 0

def generate_from_template(target, source, env):
    for t, s in zip(target, source):
        do_generate_from_template(str(t), str(s), env)

def generate_from_template_emitter(target, source, env):
    base, ext = split_ext(pbasename(str(source[0])))
    t = pjoin(pdirname(str(target[0])), base)
    return ([t], source)
    
#----------------
# umath generator
#----------------
def do_generate_umath(targetfile, sourcefile, env):
    t = open(targetfile, 'w')
    from code_generators import generate_umath
    code = generate_umath.make_code(generate_umath.defdict, generate_umath.__file__)
    t.write(code)
    t.close()

def generate_umath(target, source, env):
    for t, s in zip(target, source):
        do_generate_umath(str(t), str(s), env)

def generate_umath_emitter(target, source, env):
    t = str(target[0]) + '.c'
    return ([t], source)
    
#-------------------
# Generate config.h 
#-------------------
def generate_config_header(target, source, env):
    t = open(str(target[0]), 'w')
    if not env.has_key('CONFIG_H_GEN'):
        # XXX
        assert 0 == 1
    sym = env['CONFIG_H_GEN']
    def write_symbol(define, value):
        if value == 1:
            return "#define %s\n\n" % define
        elif value == 0:
            return "/* #undef %s */\n\n" % define
        elif isstring(value):
            return "#define %s %s\n\n" % (define, value)
        else:
            return "#define %s %s\n\n" % (define, ','.join(value))
    t.writelines([write_symbol(i[0], i[1]) for i in sym])
    t.write('\n')
    t.close()

    print 'File: %s' % target[0]
    target_f = open(str(target[0]))
    print target_f.read()
    target_f.close()
    print 'EOF'
    return 0

def generate_config_header_emitter(target, source, env):
    """Add dependency from config list  CONFIG_H_GEN to target.  Returns
    original target, source tuple unchanged.  """
    from SCons.Script import Depends
    d = deepcopy(env['CONFIG_H_GEN']) # copy it
    Depends(target, SCons.Node.Python.Value(d))
    return target, source

#-----------------------------------------
# Other functions related to configuration
#-----------------------------------------
def CheckBrokenMathlib(context, mathlib):
    src = """
/* check whether libm is broken */
#include <math.h>
int main(int argc, char *argv[])
{
  return exp(-720.) > 1.0;  /* typically an IEEE denormal */
}
"""

    try:
        oldLIBS = deepcopy(context.env['LIBS'])
    except:
        oldLIBS = []

    try:
        context.Message("Checking if math lib %s is usable for numpy ... " % mathlib)
        context.env.AppendUnique(LIBS = mathlib)
        st = context.TryRun(src, '.c')
    finally:
        context.env['LIBS'] = oldLIBS

    if st[0]:
        context.Result(' Yes !')
    else:
        context.Result(' No !')
    return st[0]

def check_mlib(config, mlib):
    """Return 1 if mlib is available and usable by numpy, 0 otherwise.

    mlib can be a string (one library), or a list of libraries."""
    # Check the libraries in mlib are linkable
    if len(mlib) > 0:
        # XXX: put an autoadd argument to 0 here and add an autoadd argument to
        # CheckBroekenMathlib (otherwise we may add bogus libraries, the ones
        # which do not path the CheckBrokenMathlib test).
        st = config.CheckLib(mlib)
        if not st:
            return 0
    # Check the mlib is usable by numpy
    return config.CheckBrokenMathlib(mlib)

def check_mlibs(config, mlibs):
    for mlib in mlibs:
        if check_mlib(config, mlib):
            return mlib

    # No mlib was found.
    raise SCons.Errors.UserError("No usable mathlib was found: chose another "\
                                 "one using the MATHLIB env variable, eg "\
                                 "'MATHLIB=m python setup.py build'")


def is_npy_no_signal():
    """Return True if the NPY_NO_SIGNAL symbol must be defined in configuration
    header."""
    return sys.platform == 'win32'

def define_no_smp():
    """Returns True if we should define NPY_NOSMP, False otherwise."""
    #--------------------------------
    # Checking SMP and thread options
    #--------------------------------
    # Python 2.3 causes a segfault when
    #  trying to re-acquire the thread-state
    #  which is done in error-handling
    #  ufunc code.  NPY_ALLOW_C_API and friends
    #  cause the segfault. So, we disable threading
    #  for now.
    if sys.version[:5] < '2.4.2':
        nosmp = 1
    else:
        # Perhaps a fancier check is in order here.
        #  so that threads are only enabled if there
        #  are actually multiple CPUS? -- but
        #  threaded code can be nice even on a single
        #  CPU so that long-calculating code doesn't
        #  block.
        try:
            nosmp = os.environ['NPY_NOSMP']
            nosmp = 1
        except KeyError:
            nosmp = 0
    return nosmp == 1

