

try:
    from __version__ import version as __version__

    # Must import local ccompiler ASAP in order to get
    # customized CCompiler.spawn effective.
    import ccompiler
    import unixccompiler

    from info import __doc__
    from npy_pkg_config import *
except ImportError:
    # for py3k relative imports.
    from numpy.distutils.__version__ import version as __version__

    import numpy.distutils.ccompiler as ccompiler
    import numpy.distutils.unixccompiler as unixccompiler

    from numpy.distutils.info import __doc__
    from numpy.distutils.npy_pkg_config import *


try:
    import __config__
    _INSTALLED = True
except ImportError:
    _INSTALLED = False

if _INSTALLED:
    from numpy.testing import Tester
    test = Tester().test
    bench = Tester().bench
