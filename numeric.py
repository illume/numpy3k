__all__ = ['newaxis', 'ndarray', 'flatiter', 'ufunc',
           'arange', 'array', 'zeros', 'empty', 'broadcast', 'dtype',
           'fromstring', 'fromfile', 'frombuffer','newbuffer',
           'getbuffer', 'where', 'argwhere',
           'concatenate', 'fastCopyAndTranspose', 'lexsort',
           'set_numeric_ops', 'can_cast',
           'asarray', 'asanyarray', 'ascontiguousarray', 'asfortranarray',
           'isfortran', 'empty_like', 'zeros_like',
           'correlate', 'convolve', 'inner', 'dot', 'outer', 'vdot',
           'alterdot', 'restoredot', 'cross',
           'array2string', 'get_printoptions', 'set_printoptions',
           'array_repr', 'array_str', 'set_string_function',
           'little_endian',
           'fromiter',
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

# from Fernando Perez's IPython
def zeros_like(a):
    """Return an array of zeros of the shape and typecode of a.

    If you don't explicitly need the array to be zeroed, you should instead
    use empty_like(), which is faster as it only allocates memory."""
    try:
        return zeros(a.shape, a.dtype, a.flags.fnc)
    except AttributeError:
        try:
            wrap = a.__array_wrap__
        except AttributeError:
            wrap = None
        a = asarray(a)
        res = zeros(a.shape, a.dtype)
        if wrap:
            res = wrap(res)
        return res

def empty_like(a):
    """Return an empty (uninitialized) array of the shape and typecode of a.

    Note that this does NOT initialize the returned array.  If you require
    your array to be initialized, you should use zeros_like().

    """
    try:
        return empty(a.shape, a.dtype, a.flags.fnc)
    except AttributeError:
        try:
            wrap = a.__array_wrap__
        except AttributeError:
            wrap = None
        a = asarray(a)
        res = empty(a.shape, a.dtype)
        if wrap:
            res = wrap(res)
        return res

# end Fernando's utilities


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
flatiter = multiarray.flatiter
broadcast = multiarray.broadcast
dtype = multiarray.dtype
ufunc = type(sin)

arange = multiarray.arange
array = multiarray.array
zeros = multiarray.zeros
empty = multiarray.empty
fromstring = multiarray.fromstring
fromiter = multiarray.fromiter
fromfile = multiarray.fromfile
frombuffer = multiarray.frombuffer
newbuffer = multiarray.newbuffer
getbuffer = multiarray.getbuffer
where = multiarray.where
concatenate = multiarray.concatenate
fastCopyAndTranspose = multiarray._fastCopyAndTranspose
set_numeric_ops = multiarray.set_numeric_ops
can_cast = multiarray.can_cast
lexsort = multiarray.lexsort


def asarray(a, dtype=None, order=None):
    """Returns a as an array.

    Unlike array(), no copy is performed if a is already an array. Subclasses
    are converted to base class ndarray.
    """
    return array(a, dtype, copy=False, order=order)

def asanyarray(a, dtype=None, order=None):
    """Returns a as an array, but will pass subclasses through.
    """
    return array(a, dtype, copy=False, order=order, subok=1)

def ascontiguousarray(a, dtype=None):
    """Return 'a' as an array contiguous in memory (C order).
    """
    return array(a, dtype, copy=False, order='C', ndmin=1)

def asfortranarray(a, dtype=None):
    """Return 'a' as an array laid out in Fortran-order in memory.
    """
    return array(a, dtype, copy=False, order='F', ndmin=1)

def isfortran(a):
    """Returns True if 'a' is laid out in Fortran-order in memory.
    """
    return a.flags.fnc

def argwhere(a):
    """Return a 2-d array of shape N x a.ndim where each row
    is a sequence of indices into a.  This sequence must be
    converted to a tuple in order to be used to index into a.
    """
    return transpose(a.nonzero())

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

def cross(a, b, axisa=-1, axisb=-1, axisc=-1, axis=None):
    """Return the cross product of two (arrays of) vectors.

    The cross product is performed over the last axis of a and b by default,
    and can handle axes with dimensions 2 and 3. For a dimension of 2,
    the z-component of the equivalent three-dimensional cross product is
    returned.
    """
    if axis is not None:
        axisa,axisb,axisc=(axis,)*3
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
        lf = ''
        if issubclass(arr.dtype.type, flexible):
            typename = str(arr.dtype)
            lf = '\n'+' '*len("array(")
        return cName + "(%s, %sdtype=%s)" % (lst, lf, typename)

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
    """Returns True if the type of num is a scalar type.
    """
    if isinstance(num, generic):
        return True
    else:
        return type(num) in ScalarType

_lkup = {
    '0':'0000',
    '1':'0001',
    '2':'0010',
    '3':'0011',
    '4':'0100',
    '5':'0101',
    '6':'0110',
    '7':'0111',
    '8':'1000',
    '9':'1001',
    'a':'1010',
    'b':'1011',
    'c':'1100',
    'd':'1101',
    'e':'1110',
    'f':'1111',
    'A':'1010',
    'B':'1011',
    'C':'1100',
    'D':'1101',
    'E':'1110',
    'F':'1111',    
    'L':''}

def binary_repr(num):
    """Return the binary representation of the input number as a string.

    This is equivalent to using base_repr with base 2, but about 25x
    faster.
    """
    ostr = hex(num)
    bin = ''
    for ch in ostr[2:]:
        bin += _lkup[ch]
    if '1' in bin:
        ind = 0
        while bin[ind] == '0':
            ind += 1
        return bin[ind:]
    else:
        return '0'

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
    """Wrapper around cPickle.load which accepts either a file-like object or
    a filename.
    """
    if isinstance(file, type("")):
        file = _file(file,"rb")
    return _cload(file)

# These are all essentially abbreviations
# These might wind up in a special abbreviations module

def ones(shape, dtype=int_, order='C'):
    """ones(shape, dtype=int_) returns an array of the given
    dimensions which is initialized to all ones.
    """
    a = empty(shape, dtype, order)
    a.fill(1)
    # Above is faster now after addition of fast loops.
    #a = zeros(shape, dtype, order)
    #a+=1
    return a

def identity(n,dtype=int_):
    """identity(n) returns the identity 2-d array of shape n x n.
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



_errdict = {"ignore":ERR_IGNORE,
            "warn":ERR_WARN,
            "raise":ERR_RAISE,
            "call":ERR_CALL}

_errdict_rev = {}
for key in _errdict.keys():
    _errdict_rev[_errdict[key]] = key
del key

def seterr(divide=None, over=None, under=None, invalid=None):
    """Set how floating-point errors are handled.

    Valid values for each type of error are the strings
    "ignore", "warn", "raise", and "call". Returns the old settings.

    Note that operations on integer scalar types (such as int16) are
    handled like floating point, and are affected by these settings.

    Example:

    >>> seterr(over='raise')
    {'over': 'ignore', 'divide': 'ignore', 'invalid': 'ignore', 'under': 'ignore'}
    >>> int16(32000) * int16(3)
    Traceback (most recent call last):
          File "<stdin>", line 1, in ?
    FloatingPointError: overflow encountered in short_scalars
    """

    pyvals = umath.geterrobj()
    old = geterr()

    if divide is None: divide = old['divide']
    if over is None: over = old['over']
    if under is None: under = old['under']
    if invalid is None: invalid = old['invalid']

    maskvalue = ((_errdict[divide] << SHIFT_DIVIDEBYZERO) +
                 (_errdict[over] << SHIFT_OVERFLOW ) +
                 (_errdict[under] << SHIFT_UNDERFLOW) +
                 (_errdict[invalid] << SHIFT_INVALID))

    pyvals[1] = maskvalue
    umath.seterrobj(pyvals)
    return old

def geterr():
    """Get the current way of handling floating-point errors.

    Returns a dictionary with entries "divide", "over", "under", and
    "invalid", whose values are from the strings
    "ignore", "warn", "raise", and "call".
    """
    maskvalue = umath.geterrobj()[1]
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

def setbufsize(size):
    """Set the size of the buffer used in ufuncs.
    """
    if size > 10e6:
        raise ValueError, "Buffer size too big... %s" % size
    if size < 5:
        raise ValueError, "Buffer size too small... %s" %size

    pyvals = umath.geterrobj()
    old = getbufsize()
    pyvals[0] = size
    umath.seterrobj(pyvals)
    return old

def getbufsize():
    """Return the size of the buffer used in ufuncs.
    """
    return umath.geterrobj()[0]

def seterrcall(func):
    """Set the callback function used when a floating-point error handler
    is set to 'call'.

    'func' should be a function that takes two arguments. The first is
    type of error ("divide", "over", "under", or "invalid"), and the second
    is the status flag (= divide + 2*over + 4*under + 8*invalid).

    Returns the old handler.
    """
    if func is not None and not callable(func):
        raise ValueError, "Only callable can be used as callback"
    pyvals = umath.geterrobj()
    old = geterrcall()
    pyvals[2] = func
    umath.seterrobj(pyvals)
    return old

def geterrcall():
    """Return the current callback function used on floating-point errors.
    """
    return umath.geterrobj()[2]

def _setdef():
    defval = [UFUNC_BUFSIZE_DEFAULT, ERR_DEFAULT, None]
    umath.seterrobj(defval)

# set the default values
_setdef()

Inf = inf = infty = Infinity = PINF
nan = NaN = NAN
False_ = bool_(False)
True_ = bool_(True)

import fromnumeric
from fromnumeric import *
extend_all(fromnumeric)
