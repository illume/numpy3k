"""\
NumPy
==========

You can support the development of NumPy and SciPy by purchasing
the book "Guide to NumPy" at

  http://www.trelgol.com

It is being distributed for a fee for only a few years to
cover some of the costs of development.  After the restriction period
it will also be freely available.

Additional documentation is available in the docstrings and at

http://www.scipy.org.
"""

try:
    from __config__ import show as show_config
except ImportError:
    show_config = None

if show_config is None:
    import sys as _sys
    print >> _sys.stderr, 'Running from numpy source directory.'
    del _sys
else:
    from version import version as __version__

    from _import_tools import PackageLoader
    pkgload = PackageLoader()

    import testing
    from testing import ScipyTest, NumpyTest
    import core
    from core import *
    import lib
    from lib import *
    import linalg
    import fft
    import random
    import ctypeslib

    # Make these accessible from numpy name-space
    #  but not imported in from numpy import *
    from __builtin__ import bool, int, long, float, complex, \
         object, unicode, str
    from core import round, abs, max, min

    __all__ = ['__version__', 'pkgload', 'PackageLoader',
               'ScipyTest', 'NumpyTest', 'show_config']
    __all__ += core.__all__
    __all__ += lib.__all__
    __all__ += ['linalg', 'fft', 'random', 'ctypeslib']

    if __doc__ is not None:
        __doc__ += """

Available subpackages
---------------------
core      --- Defines a multi-dimensional array and useful procedures
              for Numerical computation.
lib       --- Basic functions used by several sub-packages and useful
              to have in the main name-space.
random    --- Core Random Tools
linalg    --- Core Linear Algebra Tools
fft       --- Core FFT routines
testing   --- Numpy testing tools

  These packages require explicit import
f2py      --- Fortran to Python Interface Generator.
distutils --- Enhancements to distutils with support for
              Fortran compilers support and more.


Global symbols from subpackages
-------------------------------
core    --> *
lib     --> *
testing --> NumpyTest
"""

    def test(level=1, verbosity=1):
        if level <= 10:
           return NumpyTest().test(level, verbosity)
        else:
           return NumpyTest().testall(level, verbosity)
    test.__doc__ = NumpyTest.test.__doc__

    import add_newdocs

    __all__.extend(['add_newdocs','test'])

    if __doc__ is not None:
        __doc__ += """

Utility tools
-------------

  test        --- Run numpy unittests
  pkgload     --- Load numpy packages
  show_config --- Show numpy build configuration
  dual        --- Overwrite certain functions with high-performance Scipy tools
  matlib      --- Make everything matrices.
  __version__ --- Numpy version string
"""
