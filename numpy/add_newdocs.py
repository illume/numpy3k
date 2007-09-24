from lib import add_newdoc

add_newdoc('numpy.core','dtype',
           [('fields', "Fields of the data-type or None if no fields"),
            ('names', "Names of fields or None if no fields"),
            ('alignment', "Needed alignment for this data-type"),
            ('byteorder',
             "Little-endian (<), big-endian (>), native (=), or "\
             "not-applicable (|)"),
            ('char', "Letter typecode for this data-type"),
            ('type', "Type object associated with this data-type"),
            ('kind', "Character giving type-family of this data-type"),
            ('itemsize', "Size of each item"),
            ('hasobject', "Non-zero if Python objects are in "\
             "this data-type"),
            ('num', "Internally-used number for builtin base"),
            ('newbyteorder',
"""self.newbyteorder(<endian>)
returns a copy of the dtype object with altered byteorders.
If <endian> is not given all byteorders are swapped.
Otherwise endian can be '>', '<', or '=' to force a particular
byteorder.  Data-types in all fields are also updated in the
new dtype object.
"""),
            ("__reduce__", "self.__reduce__() for pickling"),
            ("__setstate__", "self.__setstate__() for pickling"),
            ("subdtype", "A tuple of (descr, shape) or None"),
            ("descr", "The array_interface data-type descriptor."),
            ("str", "The array interface typestring."),
            ("name", "The name of the true data-type"),
            ("base", "The base data-type or self if no subdtype"),
            ("shape", "The shape of the subdtype or (1,)"),
            ("isbuiltin", "Is this a built-in data-type?"),
            ("isnative", "Is the byte-order of this data-type native?")
            ]
           )

###############################################################################
#
# flatiter
#
# flatiter needs a toplevel description
#
###############################################################################

# attributes
add_newdoc('numpy.core', 'flatiter', ('base',
    """documentation needed

    """))



add_newdoc('numpy.core', 'flatiter', ('coords',
    """An N-d tuple of current coordinates.

    """))



add_newdoc('numpy.core', 'flatiter', ('index',
    """documentation needed

    """))



# functions
add_newdoc('numpy.core', 'flatiter', ('__array__',
    """__array__(type=None) Get array from iterator

    """))


add_newdoc('numpy.core', 'flatiter', ('copy',
    """copy() Get a copy of the iterator as a 1-d array

    """))


###############################################################################
#
# broadcast
#
###############################################################################

# attributes
add_newdoc('numpy.core', 'broadcast', ('index',
    """current index in broadcasted result

    """))


add_newdoc('numpy.core', 'broadcast', ('iters',
    """tuple of individual iterators

    """))


add_newdoc('numpy.core', 'broadcast', ('nd',
    """number of dimensions of broadcasted result

    """))


add_newdoc('numpy.core', 'broadcast', ('numiter',
    """number of iterators

    """))


add_newdoc('numpy.core', 'broadcast', ('shape',
    """shape of broadcasted result

    """))


add_newdoc('numpy.core', 'broadcast', ('size',
    """total size of broadcasted result

    """))


###############################################################################
#
# numpy functions
#
###############################################################################

add_newdoc('numpy.core.multiarray','array',
    """array(object, dtype=None, copy=1,order=None, subok=0,ndmin=0)

    Return an array from object with the specified date-type.

    Inputs:
      object - an array, any object exposing the array interface, any
                object whose __array__ method returns an array, or any
                (nested) sequence.
      dtype  - The desired data-type for the array.  If not given, then
                the type will be determined as the minimum type required
                to hold the objects in the sequence.  This argument can only
                be used to 'upcast' the array.  For downcasting, use the
                .astype(t) method.
      copy   - If true, then force a copy.  Otherwise a copy will only occur
                if __array__ returns a copy, obj is a nested sequence, or
                a copy is needed to satisfy any of the other requirements
      order  - Specify the order of the array.  If order is 'C', then the
                array will be in C-contiguous order (last-index varies the
                fastest).  If order is 'FORTRAN', then the returned array
                will be in Fortran-contiguous order (first-index varies the
                fastest).  If order is None, then the returned array may
                be in either C-, or Fortran-contiguous order or even
                discontiguous.
      subok  - If True, then sub-classes will be passed-through, otherwise
                the returned array will be forced to be a base-class array
      ndmin  - Specifies the minimum number of dimensions that the resulting
                array should have.  1's will be pre-pended to the shape as
                needed to meet this requirement.

    """)

add_newdoc('numpy.core.multiarray','empty',
    """empty((d1,...,dn),dtype=float,order='C')

    Return a new array of shape (d1,...,dn) and given type with all its
    entries uninitialized. This can be faster than zeros.

    """)


add_newdoc('numpy.core.multiarray','scalar',
    """scalar(dtype,obj)

    Return a new scalar array of the given type initialized with
    obj. Mainly for pickle support.  The dtype must be a valid data-type
    descriptor.  If dtype corresponds to an OBJECT descriptor, then obj
    can be any object, otherwise obj must be a string. If obj is not given
    it will be interpreted as None for object type and zeros for all other
    types.

    """)

add_newdoc('numpy.core.multiarray','zeros',
    """zeros((d1,...,dn),dtype=float,order='C')

    Return a new array of shape (d1,...,dn) and type typecode with all
    it's entries initialized to zero.

    """)

add_newdoc('numpy.core.multiarray','set_typeDict',
    """set_typeDict(dict)

    Set the internal dictionary that can look up an array type using a
    registered code.

    """)

add_newdoc('numpy.core.multiarray','fromstring',
    """fromstring(string, dtype=float, count=-1, sep='')

    Return a new 1d array initialized from the raw binary data in string.

    If count is positive, the new array will have count elements, otherwise its
    size is determined by the size of string.  If sep is not empty then the
    string is interpreted in ASCII mode and converted to the desired number type
    using sep as the separator between elements (extra whitespace is ignored).

    """)

add_newdoc('numpy.core.multiarray','fromiter',
    """fromiter(iterable, dtype, count=-1)

    Return a new 1d array initialized from iterable. If count is
    nonegative, the new array will have count elements, otherwise it's
    size is determined by the generator.

    """)

add_newdoc('numpy.core.multiarray','fromfile',
    """fromfile(file=, dtype=float, count=-1, sep='') -> array.

    Required arguments:
        file -- open file object or string containing file name.

    Keyword arguments:
        dtype -- type and order of the returned array (default float)
        count -- number of items to input (default all)
        sep -- separater between items if file is a text file (default "")

    Return an array of the given data type from a text or binary file. The
    'file' argument can be an open file or a string with the name of a file to
    read from.  If 'count' == -1 the entire file is read, otherwise count is the
    number of items of the given type to read in.  If 'sep' is "" it means to
    read binary data from the file using the specified dtype, otherwise it gives
    the separator between elements in a text file. The 'dtype' value is also
    used to determine the size and order of the items in binary files.


    Data written using the tofile() method can be conveniently recovered using
    this function.

    WARNING: This function should be used sparingly as the binary files are not
    platform independent. In particular, they contain no endianess or datatype
    information. Nevertheless it can be useful for reading in simply formatted
    or binary data quickly.

    """)

add_newdoc('numpy.core.multiarray','frombuffer',
    """frombuffer(buffer=, dtype=float, count=-1, offset=0)

    Returns a 1-d array of data type dtype from buffer. The buffer
    argument must be an object that exposes the buffer interface.  If
    count is -1 then the entire buffer is used, otherwise, count is the
    size of the output.  If offset is given then jump that far into the
    buffer. If the buffer has data that is out not in machine byte-order,
    than use a propert data type descriptor. The data will not be
    byteswapped, but the array will manage it in future operations.

    """)

add_newdoc('numpy.core.multiarray','concatenate',
    """concatenate((a1, a2, ...), axis=0)

    Join arrays together.

    The tuple of sequences (a1, a2, ...) are joined along the given axis
    (default is the first one) into a single numpy array.

    Example:

    >>> concatenate( ([0,1,2], [5,6,7]) )
    array([0, 1, 2, 5, 6, 7])

    """)

add_newdoc('numpy.core.multiarray','inner',
    """inner(a,b)

    Returns the dot product of two arrays, which has shape a.shape[:-1] +
    b.shape[:-1] with elements computed by the product of the elements
    from the last dimensions of a and b.

    """)

add_newdoc('numpy.core','fastCopyAndTranspose',
    """_fastCopyAndTranspose(a)""")

add_newdoc('numpy.core.multiarray','correlate',
    """cross_correlate(a,v, mode=0)""")

add_newdoc('numpy.core.multiarray','arange',
    """arange([start,] stop[, step,], dtype=None)

    For integer arguments, just like range() except it returns an array
    whose type can be specified by the keyword argument dtype.  If dtype
    is not specified, the type of the result is deduced from the type of
    the arguments.

    For floating point arguments, the length of the result is ceil((stop -
    start)/step).  This rule may result in the last element of the result
    being greater than stop.

    """)

add_newdoc('numpy.core.multiarray','_get_ndarray_c_version',
    """_get_ndarray_c_version()

    Return the compile time NDARRAY_VERSION number.

    """)

add_newdoc('numpy.core.multiarray','_reconstruct',
    """_reconstruct(subtype, shape, dtype)

    Construct an empty array. Used by Pickles.

    """)


add_newdoc('numpy.core.multiarray','set_string_function',
    """set_string_function(f, repr=1)

    Set the python function f to be the function used to obtain a pretty
    printable string version of an array whenever an array is printed.
    f(M) should expect an array argument M, and should return a string
    consisting of the desired representation of M for printing.

    """)

add_newdoc('numpy.core.multiarray','set_numeric_ops',
    """set_numeric_ops(op=func, ...)

    Set some or all of the number methods for all array objects.  Do not
    forget **dict can be used as the argument list.  Return the functions
    that were replaced, which can be stored and set later.

    """)

add_newdoc('numpy.core.multiarray','where',
    """where(condition, x, y) or where(condition)

    Return elements from `x` or `y`, depending on `condition`.

    *Parameters*:
        condition : array of bool
            When True, yield x, otherwise yield y.
        x,y : 1-dimensional arrays
            Values from which to choose.

    *Notes*
        This is equivalent to

            [xv if c else yv for (c,xv,yv) in zip(condition,x,y)]

        The result is shaped like `condition` and has elements of `x`
        or `y` where `condition` is respectively True or False.

        In the special case, where only `condition` is given, the
        tuple condition.nonzero() is returned, instead.

    *Examples*
        >>> where([True,False,True],[1,2,3],[4,5,6])
        array([1, 5, 3])

    """)


add_newdoc('numpy.core.multiarray','lexsort',
    """lexsort(keys=, axis=-1) -> array of indices. Argsort with list of keys.

    Perform an indirect sort using a list of keys. The first key is sorted,
    then the second, and so on through the list of keys. At each step the
    previous order is preserved when equal keys are encountered. The result is
    a sort on multiple keys.  If the keys represented columns of a spreadsheet,
    for example, this would sort using multiple columns (the last key being
    used for the primary sort order, the second-to-last key for the secondary
    sort order, and so on).  The keys argument must be a sequence of things
    that can be converted to arrays of the same shape.

    Parameters:

        a : array type
            Array containing values that the returned indices should sort.

        axis : integer
            Axis to be indirectly sorted. None indicates that the flattened
            array should be used. Default is -1.

    Returns:

        indices : integer array
            Array of indices that sort the keys along the specified axis. The
            array has the same shape as the keys.

    SeeAlso:

        argsort : indirect sort
        sort : inplace sort

    """)

add_newdoc('numpy.core.multiarray','can_cast',
    """can_cast(from=d1, to=d2)

    Returns True if data type d1 can be cast to data type d2 without
    losing precision.

    """)

add_newdoc('numpy.core.multiarray','newbuffer',
    """newbuffer(size)

    Return a new uninitialized buffer object of size bytes

    """)

add_newdoc('numpy.core.multiarray','getbuffer',
    """getbuffer(obj [,offset[, size]])

    Create a buffer object from the given object referencing a slice of
    length size starting at offset.  Default is the entire buffer. A
    read-write buffer is attempted followed by a read-only buffer.

    """)

##############################################################################
#
# Documentation for ndarray attributes and methods
#
##############################################################################


##############################################################################
#
# ndarray object
#
##############################################################################


add_newdoc('numpy.core.multiarray', 'ndarray',
    """An array object represents a multidimensional, homogeneous array
    of fixed-size items.  An associated data-type-descriptor object
    details the data-type in an array (including byteorder and any
    fields).  An array can be constructed using the numpy.array
    command. Arrays are sequence, mapping and numeric objects.
    More information is available in the numpy module and by looking
    at the methods and attributes of an array.

    ndarray.__new__(subtype, shape=, dtype=float, buffer=None,
                    offset=0, strides=None, order=None)

     There are two modes of creating an array using __new__:
     1) If buffer is None, then only shape, dtype, and order
        are used
     2) If buffer is an object exporting the buffer interface, then
        all keywords are interpreted.
     The dtype parameter can be any object that can be interpreted
        as a numpy.dtype object.

     No __init__ method is needed because the array is fully
     initialized after the __new__ method.

    """)


##############################################################################
#
# ndarray attributes
#
##############################################################################


add_newdoc('numpy.core.multiarray', 'ndarray', ('__array_interface__',
    """Array protocol: Python side."""))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__array_finalize__',
    """None."""))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__array_priority__',
    """Array priority."""))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__array_struct__',
    """Array protocol: C-struct side."""))


add_newdoc('numpy.core.multiarray', 'ndarray', ('_as_parameter_',
    """Allow the array to be interpreted as a ctypes object by returning the
    data-memory location as an integer

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('base',
    """Base object if memory is from some other object.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('ctypes',
    """A ctypes interface object.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('data',
    """Buffer object pointing to the start of the data.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('dtype',
    """Data-type for the array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('imag',
    """Imaginary part of the array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('itemsize',
    """Length of one element in bytes.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('flags',
    """Special object providing array flags.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('flat',
    """A 1-d flat iterator.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('nbytes',
    """Number of bytes in the array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('ndim',
    """Number of array dimensions.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('real',
    """Real part of the array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('shape',
    """Tuple of array dimensions.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('size',
    """Number of elements in the array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('strides',
    """Tuple of bytes to step in each dimension.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('T',
    """Same as self.transpose() except self is returned for self.ndim < 2.

    """))


##############################################################################
#
# ndarray methods
#
##############################################################################


add_newdoc('numpy.core.multiarray', 'ndarray', ('__array__',
    """ a.__array__(|dtype) -> reference if type unchanged, copy otherwise.

    Returns either a new reference to self if dtype is not given or a new array
    of provided data type if dtype is different from the current dtype of the
    array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__array_wrap__',
    """a.__array_wrap__(obj) -> Object of same type as a from ndarray obj.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__copy__',
    """a.__copy__(|order) -> copy, possibly with different order.

    Return a copy of the array.

    Argument:
        order -- Order of returned copy (default 'C')
            If order is 'C' (False) then the result is contiguous (default).
            If order is 'Fortran' (True) then the result has fortran order.
            If order is 'Any' (None) then the result has fortran order
            only if m is already in fortran order.;

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__deepcopy__',
    """a.__deepcopy__() -> Deep copy of array.

    Used if copy.deepcopy is called on an array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__reduce__',
    """a.__reduce__()

    For pickling.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('__setstate__',
    """a.__setstate__(version, shape, typecode, isfortran, rawdata)

    For unpickling.

    Arguments:
        version -- optional pickle version. If omitted defaults to 0.
        shape -- a tuple giving the shape
        typecode -- a typecode
        isFortran --  a bool stating if Fortran or no
        rawdata -- a binary string with the data (or a list if Object array)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('all',
    """ a.all(axis=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('any',
    """ a.any(axis=None, out=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('argmax',
    """ a.argmax(axis=None, out=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('argmin',
    """ a.argmin(axis=None, out=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('argsort',
    """a.argsort(axis=-1, kind='quicksort', order=None) -> indices

    Perform an indirect sort along the given axis using the algorithm specified
    by the kind keyword. It returns an array of indices of the same shape as
    'a' that index data along the given axis in sorted order.

    :Parameters:

        axis : integer
            Axis to be indirectly sorted. None indicates that the flattened
            array should be used. Default is -1.

        kind : string
            Sorting algorithm to use. Possible values are 'quicksort',
            'mergesort', or 'heapsort'. Default is 'quicksort'.

        order : list type or None
            When a is an array with fields defined, this argument specifies
            which fields to compare first, second, etc.  Not all fields need be
            specified.

    :Returns:

        indices : integer array
            Array of indices that sort 'a' along the specified axis.

    :SeeAlso:

      - lexsort : indirect stable sort with multiple keys
      - sort : inplace sort

    :Notes:
    ------

    The various sorts are characterized by average speed, worst case
    performance, need for work space, and whether they are stable. A stable
    sort keeps items with the same key in the same relative order. The three
    available algorithms have the following properties:

    |------------------------------------------------------|
    |    kind   | speed |  worst case | work space | stable|
    |------------------------------------------------------|
    |'quicksort'|   1   | O(n^2)      |     0      |   no  |
    |'mergesort'|   2   | O(n*log(n)) |    ~n/2    |   yes |
    |'heapsort' |   3   | O(n*log(n)) |     0      |   no  |
    |------------------------------------------------------|

    All the sort algorithms make temporary copies of the data when the sort is not
    along the last axis. Consequently, sorts along the last axis are faster and use
    less space than sorts along other axis.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('astype',
    """a.astype(t) -> Copy of array cast to type t.

    Cast array m to type t.  t can be either a string representing a typecode,
    or a python type object of type int, float, or complex.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('byteswap',
    """a.byteswap(False) -> View or copy. Swap the bytes in the array.

    Swap the bytes in the array.  Return the byteswapped array.  If the first
    argument is True, byteswap in-place and return a reference to self.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('choose',
    """ a.choose(b0, b1, ..., bn, out=None, mode='raise')

    Return an array that merges the b_i arrays together using 'a' as
    the index The b_i arrays and 'a' must all be broadcastable to the
    same shape.  The output at a particular position is the input
    array b_i at that position depending on the value of 'a' at that
    position.  Therefore, 'a' must be an integer array with entries
    from 0 to n+1.;

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('clip',
    """a.clip(min=, max=, out=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('compress',
    """a.compress(condition=, axis=None, out=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('conj',
    """a.conj()

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('conjugate',
    """a.conjugate()

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('copy',
    """a.copy(|order) -> copy, possibly with different order.

    Return a copy of the array.

    Argument:
        order -- Order of returned copy (default 'C')
            If order is 'C' (False) then the result is contiguous (default).
            If order is 'Fortran' (True) then the result has fortran order.
            If order is 'Any' (None) then the result has fortran order
            only if m is already in fortran order.;

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('cumprod',
    """a.cumprod(axis=None, dtype=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('cumsum',
    """a.cumsum(axis=None, dtype=None, out=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('diagonal',
    """a.diagonal(offset=0, axis1=0, axis2=1) -> diagonals

    If a is 2-d, return the diagonal of self with the given offset, i.e., the
    collection of elements of the form a[i,i+offset]. If a is n-d with n > 2,
    then the axes specified by axis1 and axis2 are used to determine the 2-d
    subarray whose diagonal is returned. The shape of the resulting array can
    be determined by removing axis1 and axis2 and appending an index to the
    right equal to the size of the resulting diagonals.

    :Parameters:
        offset : integer
            Offset of the diagonal from the main diagonal. Can be both positive
            and negative. Defaults to main diagonal.
        axis1 : integer
            Axis to be used as the first axis of the 2-d subarrays from which
            the diagonals should be taken. Defaults to first index.
        axis2 : integer
            Axis to be used as the second axis of the 2-d subarrays from which
            the diagonals should be taken. Defaults to second index.

    :Returns:
        array_of_diagonals : same type as original array
            If a is 2-d, then a 1-d array containing the diagonal is returned.
            If a is n-d, n > 2, then an array of diagonals is returned.

    :SeeAlso:
        - diag : matlab workalike for 1-d and 2-d arrays.
        - diagflat : creates diagonal arrays
        - trace : sum along diagonals

    Examples
    --------

    >>> a = arange(4).reshape(2,2)
    >>> a
    array([[0, 1],
           [2, 3]])
    >>> a.diagonal()
    array([0, 3])
    >>> a.diagonal(1)
    array([1])

    >>> a = arange(8).reshape(2,2,2)
    >>> a
    array([[[0, 1],
            [2, 3]],

           [[4, 5],
            [6, 7]]])
    >>> a.diagonal(0,-2,-1)
    array([[0, 3],
           [4, 7]])

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('dump',
    """a.dump(file) Dump a pickle of the array to the specified file.

    The array can be read back with pickle.load or numpy.load

    Arguments:
        file -- string naming the dump file.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('dumps',
    """a.dumps() returns the pickle of the array as a string.

    pickle.loads or numpy.loads will convert the string back to an array.
    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('fill',
    """a.fill(value) -> None. Fill the array with the scalar value.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('flatten',
    """a.flatten([fortran]) return a 1-d array (always copy)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('getfield',
    """a.getfield(dtype, offset) -> field of array as given type.

    Returns a field of the given array as a certain type. A field is a view of
    the array data with each itemsize determined by the given type and the
    offset into the current array.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('item',
    """a.item() ->  copy of first array item as Python scalar.

    Copy the first element of array to a standard Python scalar and return
    it. The array must be of size one.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('max',
    """a.max(axis=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('mean',
    """a.mean(axis=None, dtype=None, out=None) -> mean

    Returns the average of the array elements.  The average is taken over the
    flattened array by default, otherwise over the specified axis.

    :Parameters:

        axis : integer
            Axis along which the means are computed. The default is
            to compute the standard deviation of the flattened array.

        dtype : type
            Type to use in computing the means. For arrays of
            integer type the default is float32, for arrays of float types it
            is the same as the array type.

        out : ndarray
            Alternative output array in which to place the result. It must have
            the same shape as the expected output but the type will be cast if
            necessary.

    :Returns:

        mean : The return type varies, see above.
            A new array holding the result is returned unless out is specified,
            in which case a reference to out is returned.

    :SeeAlso:

        - var : variance
        - std : standard deviation

    Notes
    -----

        The mean is the sum of the elements along the axis divided by the
        number of elements.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('min',
    """a.min(axis=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('newbyteorder',
    """a.newbyteorder(<byteorder>) is equivalent to
    a.view(a.dtype.newbytorder(<byteorder>))

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('nonzero',
    """a.nonzero() returns a tuple of arrays

    Returns a tuple of arrays, one for each dimension of a,
    containing the indices of the non-zero elements in that
    dimension.  The corresponding non-zero values can be obtained
    with
        a[a.nonzero()].

    To group the indices by element, rather than dimension, use
        transpose(a.nonzero())
    instead. The result of this is always a 2d array, with a row for
    each non-zero element.;

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('prod',
    """a.prod(axis=None, dtype=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('ptp',
    """a.ptp(axis=None) a.max(axis)-a.min(axis)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('put',
    """a.put(indices, values, mode) sets a.flat[n] = values[n] for
    each n in indices. If values is shorter than indices then it
    will repeat.
    """))


add_newdoc('numpy.core.multiarray', 'putmask',
    """putmask(a, mask, values) sets a.flat[n] = values[n] for each n where
    mask.flat[n] is true.  If values is not the same size of a and mask then
    it will repeat.  This gives different behavior than a[mask] = values.
    """)


add_newdoc('numpy.core.multiarray', 'ndarray', ('ravel',
    """a.ravel([fortran]) return a 1-d array (copy only if needed)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('repeat',
    """a.repeat(repeats=, axis=none)

    copy elements of a, repeats times.  the repeats argument must be a sequence
    of length a.shape[axis] or a scalar.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('reshape',
    """a.reshape(d1, d2, ..., dn, order='c')

    Return a new array from this one.  The new array must have the same number
    of elements as self.  Also always returns a view or raises a ValueError if
    that is impossible.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('resize',
    """a.resize(new_shape, refcheck=True, order=False) -> None. Change array shape.

    Change size and shape of self inplace.  Array must own its own memory and
    not be referenced by other arrays.    Returns None.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('round',
    """a.round(decimals=0, out=None) -> out (a). Rounds to 'decimals' places.

    Keyword arguments:
        decimals -- number of decimals to round to (default 0). May be negative.
        out -- existing array to use for output (default a).

    Return:
        Reference to out, where None specifies the original array a.

    Round to the specified number of decimals. When 'decimals' is negative it
    specifies the number of positions to the left of the decimal point. The
    real and imaginary parts of complex numbers are rounded separately. Nothing
    is done if the array is not of float type and 'decimals' is >= 0.

    The keyword 'out' may be used to specify a different array to hold the
    result rather than the default 'a'. If the type of the array specified by
    'out' differs from that of 'a', the result is cast to the new type,
    otherwise the original type is kept. Floats round to floats by default.

    Numpy rounds to even. Thus 1.5 and 2.5 round to 2.0, -0.5 and 0.5 round to
    0.0, etc. Results may also be surprising due to the inexact representation
    of decimal fractions in IEEE floating point and the errors introduced in
    scaling the numbers when 'decimals' is something other than 0.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('searchsorted',
    """a.searchsorted(v, side='left') -> index array.

    Find the indices into a sorted array such that if the corresponding keys in
    v were inserted before the indices the order of a would be preserved.  If
    side='left', then the first such index is returned. If side='right', then
    the last such index is returned. If there is no such index because the key
    is out of bounds, then the length of a is returned, i.e., the key would
    need to be appended. The returned index array has the same shape as v.

    :Parameters:

        v : array or list type
            Array of keys to be searched for in a.

        side : string
            Possible values are : 'left', 'right'. Default is 'left'. Return
            the first or last index where the key could be inserted.

    :Returns:

        indices : integer array
            The returned array has the same shape as v.

    :SeeAlso:

        - sort
        - histogram

    :Notes:
    -------

        The array a must be 1-d and is assumed to be sorted in ascending order.
        Searchsorted uses binary search to find the required insertion points.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('setfield',
    """m.setfield(value, dtype, offset) -> None.
    places val into field of the given array defined by the data type and offset.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('setflags',
    """a.setflags(write=None, align=None, uic=None)

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('sort',
    """a.sort(axis=-1, kind='quicksort', order=None) -> None.

    Perform an inplace sort along the given axis using the algorithm specified
    by the kind keyword.

    :Parameters:

        axis : integer
            Axis to be sorted along. None indicates that the flattened array
            should be used. Default is -1.

        kind : string
            Sorting algorithm to use. Possible values are 'quicksort',
            'mergesort', or 'heapsort'. Default is 'quicksort'.

        order : list type or None
            When a is an array with fields defined, this argument specifies
            which fields to compare first, second, etc.  Not all fields need be
            specified.

    :Returns:

        None

    :SeeAlso:

      - argsort : indirect sort
      - lexsort : indirect stable sort on multiple keys
      - searchsorted : find keys in sorted array

    :Notes:
    ------

    The various sorts are characterized by average speed, worst case
    performance, need for work space, and whether they are stable. A stable
    sort keeps items with the same key in the same relative order. The three
    available algorithms have the following properties:

    |------------------------------------------------------|
    |    kind   | speed |  worst case | work space | stable|
    |------------------------------------------------------|
    |'quicksort'|   1   | O(n^2)      |     0      |   no  |
    |'mergesort'|   2   | O(n*log(n)) |    ~n/2    |   yes |
    |'heapsort' |   3   | O(n*log(n)) |     0      |   no  |
    |------------------------------------------------------|

    All the sort algorithms make temporary copies of the data when the sort is not
    along the last axis. Consequently, sorts along the last axis are faster and use
    less space than sorts along other axis.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('squeeze',
    """m.squeeze() eliminate all length-1 dimensions

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('std',
    """a.std(axis=None, dtype=None, out=None) -> standard deviation.

    Returns the standard deviation of the array elements, a measure of the
    spread of a distribution. The standard deviation is computed for the
    flattened array by default, otherwise over the specified axis.

    :Parameters:

        axis : integer
            Axis along which the standard deviation is computed. The default is
            to compute the standard deviation of the flattened array.

        dtype : type
            Type to use in computing the standard deviation. For arrays of
            integer type the default is float32, for arrays of float types it
            is the same as the array type.

        out : ndarray
            Alternative output array in which to place the result. It must have
            the same shape as the expected output but the type will be cast if
            necessary.

    :Returns:

        standard deviation : The return type varies, see above.
            A new array holding the result is returned unless out is specified,
            in which case a reference to out is returned.

    :SeeAlso:

        - var : variance
        - mean : average

    Notes
    -----

      The standard deviation is the square root of the average of the squared
      deviations from the mean, i.e. var = sqrt(mean((x - x.mean())**2)).  The
      computed standard deviation is biased, i.e., the mean is computed by
      dividing by the number of elements, N, rather than by N-1.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('sum',
    """a.sum(axis=None, dtype=None) -> Sum of array over given axis.

    Sum the array over the given axis.  If the axis is None, sum over
    all dimensions of the array.

    The optional dtype argument is the data type for the returned
    value and intermediate calculations.  The default is to upcast
    (promote) smaller integer types to the platform-dependent int.
    For example, on 32-bit platforms:

      a.dtype                         default sum dtype
      ---------------------------------------------------
      bool, int8, int16, int32        int32

    Warning: The arithmetic is modular and no error is raised on overflow.

    Examples:

    >>> array([0.5, 1.5]).sum()
    2.0
    >>> array([0.5, 1.5]).sum(dtype=int32)
    1
    >>> array([[0, 1], [0, 5]]).sum(axis=0)
    array([0, 6])
    >>> array([[0, 1], [0, 5]]).sum(axis=1)
    array([1, 5])
    >>> ones(128, dtype=int8).sum(dtype=int8) # overflow!
    -128

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('swapaxes',
    """a.swapaxes(axis1, axis2) -> new view with axes swapped.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('take',
    """a.take(indices, axis=None, out=None, mode='raise') -> new array.

    The new array is formed from the elements of a indexed by indices along the
    given axis.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('tofile',
    """a.tofile(fid, sep="", format="%s") -> None. Write the data to a file.

    Required arguments:
        file -- an open file object or a string containing a filename

    Keyword arguments:
        sep -- separator for text output. Write binary if empty (default "")
        format -- format string for text file output (default "%s")

    A convenience function for quick storage of array data. Information on
    endianess and precision is lost, so this method is not a good choice for
    files intended to archive data or transport data between machines with
    different endianess. Some of these problems can be overcome by outputting
    the data as text files at the expense of speed and file size.

    If 'sep' is empty this method is equivalent to file.write(a.tostring()). If
    'sep' is not empty each data item is converted to the nearest Python type
    and formatted using "format"%item. The resulting strings are written to the
    file separated by the contents of 'sep'. The data is always written in "C"
    (row major) order independent of the order of 'a'.

    The data produced by this method can be recovered by using the function
    fromfile().

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('tolist',
    """a.tolist() -> Array as hierarchical list.

    Copy the data portion of the array to a hierarchical python list and return
    that list. Data items are converted to the nearest compatible Python type.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('tostring',
    """a.tostring(order='C') -> raw copy of array data as a Python string.

    Keyword arguments:
        order -- order of the data item in the copy {"C","F","A"} (default "C")

    Construct a Python string containing the raw bytes in the array. The order
    of the data in arrays with ndim > 1 is specified by the 'order' keyword and
    this keyword overrides the order of the array. The
    choices are:

        "C"       -- C order (row major)
        "Fortran" -- Fortran order (column major)
        "Any"     -- Current order of array.
        None      -- Same as "Any"

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('trace',
    """a.trace(offset=0, axis1=0, axis2=1, dtype=None, out=None)
    return the sum along the offset diagonal of the array's indicated
    axis1 and axis2.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('transpose',
    """a.transpose(*axes)

    Returns a view of 'a' with axes transposed. If no axes are given,
    or None is passed, switches the order of the axes. For a 2-d
    array, this is the usual matrix transpose. If axes are given,
    they describe how the axes are permuted.

    Example:
    >>> a = array([[1,2],[3,4]])
    >>> a
    array([[1, 2],
           [3, 4]])
    >>> a.transpose()
    array([[1, 3],
           [2, 4]])
    >>> a.transpose((1,0))
    array([[1, 3],
           [2, 4]])
    >>> a.transpose(1,0)
    array([[1, 3],
           [2, 4]])

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('var',
    """a.var(axis=None, dtype=None, out=None) -> variance

    Returns the variance of the array elements, a measure of the spread of a
    distribution.  The variance is computed for the flattened array by default,
    otherwise over the specified axis.

    :Parameters:

        axis : integer
            Axis along which the variance is computed. The default is to
            compute the variance of the flattened array.

        dtype : type
            Type to use in computing the variance. For arrays of integer type
            the default is float32, for arrays of float types it is the same as
            the array type.

        out : ndarray
            Alternative output array in which to place the result. It must have
            the same shape as the expected output but the type will be cast if
            necessary.

    :Returns:

        variance : The return type varies, see above.
            A new array holding the result is returned unless out is specified,
            in which case a reference to out is returned.

    :SeeAlso:

        - std : standard deviation
        - mean: average

    Notes
    -----

      The variance is the average of the squared deviations from the mean, i.e.
      var = mean((x - x.mean())**2).  The computed variance is biased, i.e.,
      the mean is computed by dividing by the number of elements, N, rather
      than by N-1.

    """))


add_newdoc('numpy.core.multiarray', 'ndarray', ('view',
    """a.view(<type>) -> new view of array with same data.

    Type can be either a new sub-type object or a data-descriptor object

    """))
