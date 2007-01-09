__all__ = ['load_library', 'ndpointer', 'test', 'ctypes_load_library',
           'c_intp']

import sys, os
from numpy import integer, ndarray, dtype as _dtype, deprecate
from numpy.core.multiarray import _flagdict, flagsobj

try:
    import ctypes
except ImportError:
    ctypes = None

if ctypes is None:
    def _dummy(*args, **kwds):
        raise ImportError, "ctypes is not available."
    ctypes_load_library = _dummy
    load_library = _dummy
    from numpy import intp as c_intp
else:
    import numpy.core._internal as nic
    c_intp = nic._getintp_ctype()
    del nic

    # Adapted from Albert Strasheim
    def load_library(libname, loader_path):
        if ctypes.__version__ < '1.0.1':
            import warnings
            warnings.warn("All features of ctypes interface may not work " \
                          "with ctypes < 1.0.1")
        if '.' not in libname:
            if sys.platform == 'win32':
                libname = '%s.dll' % libname
            elif sys.platform == 'darwin':
                libname = '%s.dylib' % libname
            else:
                libname = '%s.so' % libname
        loader_path = os.path.abspath(loader_path)
        if not os.path.isdir(loader_path):
            libdir = os.path.dirname(loader_path)
        else:
            libdir = loader_path
        libpath = os.path.join(libdir, libname)
        return ctypes.cdll[libpath]

    ctypes_load_library = deprecate(load_library, 'ctypes_load_library',
                                    'load_library')

def _num_fromflags(flaglist):
    num = 0
    for val in flaglist:
        num += _flagdict[val]
    return num

_flagnames = ['C_CONTIGUOUS', 'F_CONTIGUOUS', 'ALIGNED', 'WRITEABLE',
              'OWNDATA', 'UPDATEIFCOPY']
def _flags_fromnum(num):
    res = []
    for key in _flagnames:
        value = _flagdict[key]
        if (num & value):
            res.append(key)
    return res


class _ndptr(object):
    def from_param(cls, obj):
        if not isinstance(obj, ndarray):
            raise TypeError, "argument must be an ndarray"
        if cls._dtype_ is not None \
               and obj.dtype != cls._dtype_:
            raise TypeError, "array must have data type %s" % cls._dtype_
        if cls._ndim_ is not None \
               and obj.ndim != cls._ndim_:
            raise TypeError, "array must have %d dimension(s)" % cls._ndim_
        if cls._shape_ is not None \
               and obj.shape != cls._shape_:
            raise TypeError, "array must have shape %s" % str(cls._shape_)
        if cls._flags_ is not None \
               and ((obj.flags.num & cls._flags_) != cls._flags_):
            raise TypeError, "array must have flags %s" % \
                  _flags_fromnum(cls._flags_)
        return obj.ctypes
    from_param = classmethod(from_param)


# Factory for an array-checking class with from_param defined for
#  use with ctypes argtypes mechanism
_pointer_type_cache = {}
def ndpointer(dtype=None, ndim=None, shape=None, flags=None):
    """Array-checking restype/argtypes.

    An ndpointer instance is used to describe an ndarray in restypes
    and argtypes specifications.  This approach is more flexible than
    using, for example,

    POINTER(c_double)

    since several restrictions can be specified, which are verified
    upon calling the ctypes function.  These include data type
    (dtype), number of dimensions (ndim), shape and flags (e.g.
    'C_CONTIGUOUS' or 'F_CONTIGUOUS').  If a given array does not satisfy the
    specified restrictions, a TypeError is raised.

    Example:

        clib.somefunc.argtypes = [ndpointer(dtype=float64,
                                            ndim=1,
                                            flags='C_CONTIGUOUS')]
        clib.somefunc(array([1,2,3],dtype=float64))

    """

    if dtype is not None:
        dtype = _dtype(dtype)
    num = None
    if flags is not None:
        if isinstance(flags, str):
            flags = flags.split(',')
        elif isinstance(flags, (int, integer)):
            num = flags
            flags = _flags_fromnum(num)
        elif isinstance(flags, flagsobj):
            num = flags.num
            flags = _flags_fromnum(num)
        if num is None:
            try:
                flags = [x.strip().upper() for x in flags]
            except:
                raise TypeError, "invalid flags specification"
            num = _num_fromflags(flags)
    try:
        return _pointer_type_cache[(dtype, ndim, shape, num)]
    except KeyError:
        pass
    if dtype is None:
        name = 'any'
    elif dtype.names:
        name = str(id(dtype))
    else:
        name = dtype.str
    if ndim is not None:
        name += "_%dd" % ndim
    if shape is not None:
        try:
            strshape = [str(x) for x in shape]
        except TypeError:
            strshape = [str(shape)]
            shape = (shape,)
        shape = tuple(shape)
        name += "_"+"x".join(strshape)
    if flags is not None:
        name += "_"+"_".join(flags)
    else:
        flags = []
    klass = type("ndpointer_%s"%name, (_ndptr,),
                 {"_dtype_": dtype,
                  "_shape_" : shape,
                  "_ndim_" : ndim,
                  "_flags_" : num})
    _pointer_type_cache[dtype] = klass
    return klass

def test(level=1, verbosity=1):
    from numpy.testing import NumpyTest
    return NumpyTest().test(level, verbosity)
