# :Author:    Robert Kern
# :Copyright: 2004, Enthought, Inc.
# :License:   BSD Style


cdef extern from "scipy/arrayobject.h":
    ctypedef enum PyArray_TYPES:
        PyArray_BOOL
        PyArray_BYTE
        PyArray_UBYTE
        PyArray_SHORT
        PyArray_USHORT 
        PyArray_INT
        PyArray_UINT 
        PyArray_LONG
        PyArray_ULONG
        PyArray_FLOAT
        PyArray_DOUBLE 
        PyArray_LONGDOUBLE
        PyArray_CFLOAT
        PyArray_CDOUBLE
        PyArray_CLONGDOUBLE
        PyArray_OBJECT
        PyArray_STRING
        PyArray_UNICODE
        PyArray_VOID
        PyArray_NTYPES
        PyArray_NOTYPE

    ctypedef int intp 

    ctypedef extern class scipy.dtypedescr [object PyArray_Descr]:
        cdef int type_num, elsize
        cdef char type

    ctypedef extern class scipy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef object base
        cdef dtypedescr descr
        cdef int flags

    ndarray PyArray_SimpleNew(int ndims, intp* dims, int item_type)
    int PyArray_Check(object obj)
    ndarray PyArray_ContiguousFromObject(object obj, PyArray_TYPES type, 
        int mindim, int maxdim)
    intp PyArray_SIZE(ndarray arr)
    void *PyArray_DATA(ndarray arr)

    void import_array()
