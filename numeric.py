__all__ = ['newaxis', 'ndarray', 'bigndarray', 'flatiter', 'ufunc',
           'arange', 'array', 'zeros', 'empty', 'broadcast', 'dtype',
           'fromstring', 'fromfile', 'frombuffer','newbuffer',
           'getbuffer',
           'where', 'concatenate', 'fastCopyAndTranspose', 'lexsort',
           'register_dtype', 'set_numeric_ops', 'can_cast',
           'asarray', 'asanyarray', 'isfortran', 'zeros_like', 'empty_like',
           'correlate', 'convolve', 'inner', 'dot', 'outer', 'vdot',
           'alterdot', 'restoredot', 'cross',
           'array2string', 'get_printoptions', 'set_printoptions',
           'array_repr', 'array_str', 'set_string_function',
           'little_endian',
           'indices', 'fromfunction',
           'load', 'loads', 'isscalar', 'binary_repr', 'base_repr',
           'ones', 'identity', 'allclose',
           'seterr', 'geterr', 'setbufsize', 'getbufsize',
           'seterrcall', 'geterrcall',
           'Inf', 'inf', 'infty', 'Infinity',
           'nan', 'NaN', 'False_', 'True_']

import sys
import multiarray
import umath
from umath import *
import numerictypes
from numerictypes import *

def extend_all(module):
    adict = {}
    for a in __all__:
        adict[a] = 1
    try:
        mall = getattr(module, '__all__')
    except AttributeError:
        mall = [k for k in module.__dict__.keys() if not k.startswith('_')]
    for a in mall:
        if a not in adict:
            __all__.append(a)

extend_all(umath)
extend_all(numerictypes)

newaxis = None

ndarray = multiarray.ndarray
bigndarray = multiarray.bigndarray
flatiter = multiarray.flatiter
broadcast = multiarray.broadcast
dtype=multiarray.dtype
ufunc = type(sin)

arange = multiarray.arange
array = multiarray.array
zeros = multiarray.zeros
empty = multiarray.empty
fromstring = multiarray.fromstring
fromfile = multiarray.fromfile
frombuffer = multiarray.frombuffer
newbuffer = multiarray.newbuffer
getbuffer = multiarray.getbuffer
where = multiarray.where
concatenate = multiarray.concatenate
fastCopyAndTranspose = multiarray._fastCopyAndTranspose
register_dtype = multiarray.register_dtype
set_numeric_ops = multiarray.set_numeric_ops
can_cast = multiarray.can_cast
lexsort = multiarray.lexsort


def asarray(a, dtype=None, fortran=False, ndmin=0):
    """returns a as an array.  Unlike array(),
    no copy is performed if a is already an array.  Subclasses are converted
    to base class ndarray.
    """
    return array(a, dtype, copy=False, fortran=fortran, ndmin=ndmin)

def asanyarray(a, dtype=None, copy=False, fortran=False, ndmin=0):
    """will pass subclasses through...
    """
    return array(a, dtype, copy=False, fortran=fortran, subok=1, ndmin=ndmin)

def isfortran(a):
    return a.flags['FNC']

# from Fernando Perez's IPython
def zeros_like(a):
    """Return an array of zeros of the shape and typecode of a.

    If you don't explicitly need the array to be zeroed, you should instead
    use empty_like(), which is faster as it only allocates memory."""
    a = asanyarray(a)
    return a.__array_wrap__(zeros(a.shape, a.dtype, a.flags['FNC']))

def empty_like(a):
    """Return an empty (uninitialized) array of the shape and typecode of a.

    Note that this does NOT initialize the returned array.  If you require
    your array to be initialized, you should use zeros_like().

    """
    a = asanyarray(a)
    return a.__array_wrap__(empty(a.shape, a.dtype, a.flags['FNC']))

# end Fernando's utilities

_mode_from_name_dict = {'v': 0,
                        's' : 1,
                        'f' : 2}

def _mode_from_name(mode):
    if isinstance(mode, type("")):
        return _mode_from_name_dict[mode.lower()[0]]
    return mode

def correlate(a,v,mode='valid'):
    mode = _mode_from_name(mode)
    return multiarray.correlate(a,v,mode)


def convolve(a,v,mode='full'):
    """Returns the discrete, linear convolution of 1-D
    sequences a and v; mode can be 0 (valid), 1 (same), or 2 (full)
    to specify size of the resulting sequence.
    """
    if (len(v) > len(a)):
        a, v = v, a
    mode = _mode_from_name(mode)
    return multiarray.correlate(a,asarray(v)[::-1],mode)


inner = multiarray.inner
dot = multiarray.dot

def outer(a,b):
    """outer(a,b) returns the outer product of two vectors.
    result(i,j) = a(i)*b(j) when a and b are vectors
    Will accept any arguments that can be made into vectors.
    """
    a = asarray(a)
    b = asarray(b)
    return a.ravel()[:,newaxis]*b.ravel()[newaxis,:]

def vdot(a, b):
    """Returns the dot product of 2 vectors (or anything that can be made into
    a vector). NB: this is not the same as `dot`, as it takes the conjugate
    of its first argument if complex and always returns a scalar."""
    return dot(asarray(a).ravel().conj(), asarray(b).ravel())

# try to import blas optimized dot if available
try:
    # importing this changes the dot function for basic 4 types
    # to blas-optimized versions.
    from _dotblas import dot, vdot, inner, alterdot, restoredot
except ImportError:
    def alterdot():
        pass
    def restoredot():
        pass


def _move_axis_to_0(a, axis):
    if axis == 0:
        return a
    n = a.ndim
    if axis < 0:
        axis += n
    axes = range(1, axis+1) + [0,] + range(axis+1, n)
    return a.transpose(axes)

def cross(a, b, axisa=-1, axisb=-1, axisc=-1):
    """Return the cross product of two (arrays of) vectors.

    The cross product is performed over the last axis of a and b by default,
    and can handle axes with dimensions 2 and 3. For a dimension of 2,
    the z-component of the equivalent three-dimensional cross product is
    returned.
    """
    a = _move_axis_to_0(asarray(a), axisa)
    b = _move_axis_to_0(asarray(b), axisb)
    msg = "incompatible dimensions for cross product\n"\
          "(dimension must be 2 or 3)"
    if (a.shape[0] not in [2,3]) or (b.shape[0] not in [2,3]):
        raise ValueError(msg)
    if a.shape[0] == 2:
        if (b.shape[0] == 2):
            cp = a[0]*b[1] - a[1]*b[0]
            if cp.ndim == 0:
                return cp
            else:
                return cp.swapaxes(0,axisc)
        else:
            x = a[1]*b[2]
            y = -a[0]*b[2]
            z = a[0]*b[1] - a[1]*b[0]
    elif a.shape[0] == 3:
        if (b.shape[0] == 3):
            x = a[1]*b[2] - a[2]*b[1]
            y = a[2]*b[0] - a[0]*b[2]
            z = a[0]*b[1] - a[1]*b[0]
        else:
            x = -a[2]*b[1]
            y = a[2]*b[0]
            z = a[0]*b[1] - a[1]*b[0]
    cp = array([x,y,z])
    if cp.ndim == 1:
        return cp
    else:
        return cp.swapaxes(0,axisc)


#Use numarray's printing function
from arrayprint import array2string, get_printoptions, set_printoptions

_typelessdata = [int_, float_, complex_]
if issubclass(intc, int):
    _typelessdata.append(intc)

if issubclass(longlong, int):
    _typelessdata.append(longlong)

def array_repr(arr, max_line_width=None, precision=None, suppress_small=None):
    if arr.size > 0 or arr.shape==(0,):
        lst = array2string(arr, max_line_width, precision, suppress_small,
                           ', ', "array(")
    else: # show zero-length shape unless it is (0,)
        lst = "[], shape=%s" % (repr(arr.shape),)
    typeless = arr.dtype.type in _typelessdata

    if arr.__class__ is not ndarray:
        cName= arr.__class__.__name__
    else:
        cName = "array"
    if typeless and arr.size:
        return cName + "(%s)" % lst
    else:
        typename=arr.dtype.type.__name__[:-6]
        if issubclass(arr.dtype.type, flexible):
            if typename not in ['unicode','string','void']:
                typename = arr.dtype.type.__name__
            if typename == 'unicode':
                size = arr.itemsize >> 2
            else:
                size = arr.itemsize;
            typename = "(%s,%d)" % (typename, size)
        return cName + "(%s, dtype=%s)" % (lst, typename)

def array_str(a, max_line_width=None, precision=None, suppress_small=None):
    return array2string(a, max_line_width, precision, suppress_small, ' ', "", str)

set_string_function = multiarray.set_string_function
set_string_function(array_str, 0)
set_string_function(array_repr, 1)


little_endian = (sys.byteorder == 'little')

def indices(dimensions, dtype=int_):
    """indices(dimensions,dtype=int_) returns an array representing a grid
    of indices with row-only, and column-only variation.
    """
    tmp = ones(dimensions, dtype)
    lst = []
    for i in range(len(dimensions)):
        lst.append( add.accumulate(tmp, i, )-1 )
    return array(lst)

def fromfunction(function, dimensions, **kwargs):
    """fromfunction(function, dimensions) returns an array constructed by
    calling function on a tuple of number grids.  The function should
    accept as many arguments as there are dimensions which is a list of
    numbers indicating the length of the desired output for each axis.

    The function can also accept keyword arguments which will be
    passed in as well.
    """
    args = indices(dimensions)
    return function(*args,**kwargs)

def isscalar(num):
    if isinstance(num, generic):
        return True
    else:
        return type(num) in ScalarType

_lkup = {'0':'000',
         '1':'001',
         '2':'010',
         '3':'011',
         '4':'100',
         '5':'101',
         '6':'110',
         '7':'111',
         'L':''}

def binary_repr(num):
    """Return the binary representation of the input number as a string.

    This is equivalent to using base_repr with base 2, but about 25x
    faster.
    """
    ostr = oct(num)
    bin = ''
    for ch in ostr[1:]:
        bin += _lkup[ch]
    ind = 0
    while bin[ind] == '0':
        ind += 1
    return bin[ind:]

def base_repr (number, base=2, padding=0):
    """Return the representation of a number in any given base.
    """
    chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    import math
    lnb = math.log(base)
    res = padding*chars[0]
    if number == 0:
        return res + chars[0]
    exponent = int (math.log (number)/lnb)
    while(exponent >= 0):
        term = long(base)**exponent
        lead_digit = int(number / term)
        res += chars[lead_digit]
        number -= term*lead_digit
        exponent -= 1
    return res

from cPickle import load, loads
_cload = load
_file = file

def load(file):
    if isinstance(file, type("")):
        file = _file(file,"rb")
    return _cload(file)

# These are all essentially abbreviations
# These might wind up in a special abbreviations module

def ones(shape, dtype=int_, fortran=False):
    """ones(shape, dtype=int_) returns an array of the given
    dimensions which is initialized to all ones. 
    """
    # This appears to be slower...
    #a = empty(shape, dtype, fortran)
    #a.fill(1)
    a = zeros(shape, dtype, fortran)
    a+=1
    return a

def identity(n,dtype=int_):
    """identity(n) returns the identity matrix of shape n x n.
    """
    a = array([1]+n*[0],dtype=dtype)
    b = empty((n,n),dtype=dtype)
    b.flat = a
    return b

def allclose (a, b, rtol=1.e-5, atol=1.e-8):
    """ allclose(a,b,rtol=1.e-5,atol=1.e-8)
        Returns true if all components of a and b are equal
        subject to given tolerances.
        The relative error rtol must be positive and << 1.0
        The absolute error atol comes into play for those elements
        of y that are very small or zero; it says how small x must be also.
    """
    x = array(a, copy=False)
    y = array(b, copy=False)
    d = less(absolute(x-y), atol + rtol * absolute(y))
    return d.ravel().all()

def _setpyvals(lst, frame, where=0):
    if not isinstance(lst, list) or len(lst) != 3:
        raise ValueError, "Invalid pyvalues (length 3 list needed)."

    try:
        wh = where.lower()[0]
    except (AttributeError, TypeError, IndexError):
        wh = None

    if where==0 or wh == 'l':
        frame.f_locals[UFUNC_PYVALS_NAME] = lst
    elif where == 1 or wh == 'g':
        frame.f_globals[UFUNC_PYVALS_NAME] = lst
    elif where == 2 or wh == 'b':
        frame.f_builtins[UFUNC_PYVALS_NAME] = lst 

    umath.update_use_defaults()
    return

def _getpyvals(frame):
    try:
        return frame.f_locals[UFUNC_PYVALS_NAME]
    except KeyError:
        try:
            return frame.f_globals[UFUNC_PYVALS_NAME]
        except KeyError:
            try:
                return frame.f_builtins[UFUNC_PYVALS_NAME]
            except KeyError:
                return [UFUNC_BUFSIZE_DEFAULT, ERR_DEFAULT, None]

_errdict = {"ignore":ERR_IGNORE,
            "warn":ERR_WARN,
            "raise":ERR_RAISE,
            "call":ERR_CALL}

_errdict_rev = {}
for key in _errdict.keys():
    _errdict_rev[_errdict[key]] = key
del key

def seterr(divide="ignore", over="ignore", under="ignore",
           invalid="ignore", where=0):
    maskvalue = ((_errdict[divide] << SHIFT_DIVIDEBYZERO) +
                 (_errdict[over] << SHIFT_OVERFLOW ) +
                 (_errdict[under] << SHIFT_UNDERFLOW) +
                 (_errdict[invalid] << SHIFT_INVALID))

    frame = sys._getframe().f_back
    pyvals = _getpyvals(frame)
    pyvals[1] = maskvalue
    _setpyvals(pyvals, frame, where)

def geterr():
    frame = sys._getframe().f_back
    maskvalue = _getpyvals(frame)[1]

    mask = 3
    res = {}
    val = (maskvalue >> SHIFT_DIVIDEBYZERO) & mask
    res['divide'] = _errdict_rev[val]
    val = (maskvalue >> SHIFT_OVERFLOW) & mask
    res['over'] = _errdict_rev[val]
    val = (maskvalue >> SHIFT_UNDERFLOW) & mask
    res['under'] = _errdict_rev[val]
    val = (maskvalue >> SHIFT_INVALID) & mask
    res['invalid'] = _errdict_rev[val]
    return res

def setbufsize(size, where=0):
    if size > 10e6:
        raise ValueError, "Very big buffers.. %s" % size

    frame = sys._getframe().f_back
    pyvals = _getpyvals(frame)
    pyvals[0] = size
    _setpyvals(pyvals, frame, where)

def getbufsize():
    frame = sys._getframe().f_back
    return _getpyvals(frame)[0]

def seterrcall(func, where=0):
    if not callable(func):
        raise ValueError, "Only callable can be used as callback"
    frame = sys._getframe().f_back
    pyvals = _getpyvals(frame)
    pyvals[2] = func
    _setpyvals(pyvals, frame, where)

def geterrcall():
    frame = sys._getframe().f_back
    return _getpyvals(frame)[2]

def _setdef():
    frame = sys._getframe()
    defval = [UFUNC_BUFSIZE_DEFAULT, ERR_DEFAULT, None]
    frame.f_globals[UFUNC_PYVALS_NAME] = defval
    frame.f_builtins[UFUNC_PYVALS_NAME] = defval
    umath.update_use_defaults()

# set the default values
_setdef()

Inf = inf = infty = Infinity = PINF
nan = NaN = NAN
False_ = bool_(False)
True_ = bool_(True)

import oldnumeric
from oldnumeric import *
extend_all(oldnumeric)
