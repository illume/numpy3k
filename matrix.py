
import numeric as N
from numeric import ArrayType, concatenate
from function_base import binary_repr
import types
import string as str_

__all__ = ['matrix', 'bmat', 'mat']

# make translation table
_table = [None]*256
for k in range(256):
    _table[k] = chr(k)
_table = ''.join(_table)

_numchars = str_.digits + ".-+jeEL"
del str_
_todelete = []
for k in _table:
    if k not in _numchars:
        _todelete.append(k)
_todelete = ''.join(_todelete)

def _eval(astr):
    return eval(astr.translate(_table,_todelete))

def _convert_from_string(data):
    rows = data.split(';')
    newdata = []
    count = 0
    for row in rows:
        trow = row.split(',')
        newrow = []
        for col in trow:
            temp = col.split()
            newrow.extend(map(_eval,temp))
        if count == 0:
            Ncols = len(newrow)
        elif len(newrow) != Ncols:
            raise ValueError, "Rows not the same size."
        count += 1
        newdata.append(newrow)
    return newdata


class matrix(N.ndarray):
    __array_priority__ = 10.0
    def __new__(self, data, dtype=None, copy=0):
        if isinstance(data, matrix):
            dtype2 = data.dtype
            if (dtype is None):
                dtype = dtype2
            if (dtype2 is dtype) and (not copy):
                return data
            return data.astype(dtype)

        if dtype is None:
            if isinstance(data, N.ndarray):
                dtype = data.dtype
        intype = N.obj2dtype(dtype)
        
        if isinstance(data, types.StringType):
            data = _convert_from_string(data)

        # now convert data to an array
        arr = N.array(data, dtype=intype, copy=copy)
        ndim = arr.ndim
        shape = arr.shape
        if (ndim > 2):
            raise ValueError, "matrix must be 2-dimensional"
        elif ndim == 0:
            shape = (1,1)
        elif ndim == 1:
            shape = (1,shape[0])

        fortran = False;
        if (ndim == 2) and arr.flags['FORTRAN']:
            fortran = True

        if not (fortran or arr.flags['CONTIGUOUS']):
            arr = arr.copy()

        ret = N.ndarray.__new__(matrix, shape, arr.dtype, buffer=arr,
                                fortran=fortran,
                                swap=(not arr.flags['NOTSWAPPED']))
        return ret; 

    # special methods 
    def __array_wrap__(self, obj):
        try:
            ret = matrix(obj,dtype=obj.dtype)
        except:
            ret = obj
        return ret

    def _update_meta(self, obj):
        ndim = self.ndim
        if ndim == 0:
            self.shape = (1,1)
        elif ndim == 1:
            self.shape = (1, self.shape[0])
        return

    def __getitem__(self, index):
        out = N.ndarray.__getitem__(self, index)
        # Need to swap if slice is on first index
        try:
            n = len(index)
            if (n > 1) and isinstance(index[0], types.SliceType) \
               and (isinstance(index[1], types.IntType) or
                    isinstance(index[1], types.LongType)):
                sh = out.shape
                out.shape = (sh[1], sh[0])
        except TypeError:
            pass
        return out

    def __mul__(self, other):
        if isinstance(other, N.ndarray) and other.ndim == 0:
            return N.multiply(self, other)
        else:
            return N.dot(self, other)

    def __rmul__(self, other):
        if isinstance(other, N.ndarray) and other.ndim == 0:
            return N.multiply(other, self)
        else:
            return N.dot(other, self)

    def __pow__(self, other):
        if len(shape)!=2 or shape[0]!=shape[1]:
            raise TypeError, "matrix is not square"
        if type(other) in (type(1), type(1L)):
            if other==0:
                return matrix(N.identity(shape[0]))
            if other<0:
                x = self.I
                other=-other
            else:
                x=self
            result = x
            if other <= 3:
                while(other>1):
                    result=result*x
                    other=other-1
                return result
            # binary decomposition to reduce the number of Matrix
            #  Multiplies for other > 3.
            beta = binary_repr(other)
            t = len(beta)
            Z,q = x.copy(),0
            while beta[t-q-1] == '0':
                Z *= Z
                q += 1
            result = Z.copy()
            for k in range(q+1,t):
                Z *= Z
                if beta[t-k-1] == '1':
                    result *= Z
            return result
        else:
            raise TypeError, "exponent must be an integer"

    def __rpow__(self, other):
        raise NotImplementedError

    def __repr__(self):
        return repr(self.A).replace('array','matrix')

    def __str__(self):
        return str(self.A)

    def tolist(self):
        return self.A.tolist()    

    def getA(self):
        arr = self
        fortran = False;
        if (self.ndim == 2) and arr.flags['FORTRAN']:
            fortran = True

        if not (fortran or arr.flags['CONTIGUOUS']):
            arr = arr.copy()

        return N.ndarray.__new__(N.ndarray, self.shape, self.dtype, buffer=arr,
                                fortran=fortran,
                                swap=(not arr.flags['NOTSWAPPED']))
        
    def getT(self):
        return self.transpose()

    def getH(self):
        if issubclass(self.dtype, N.complexfloating):
            return self.transpose(self.conjugate())
        else:
            return self.transpose()

    # inverse doesn't work yet....
    def getI(self):
        from scipy.linalg import inv
        return matrix(inv(self))

    A = property(getA, None, doc="base array")
    T = property(getT, None, doc="transpose")    
    H = property(getH, None, doc="hermitian (conjugate) transpose")
    I = property(getI, None, doc="inverse")



def _from_string(str,gdict,ldict):
    rows = str.split(';')
    rowtup = []
    for row in rows:
        trow = row.split(',')
        coltup = []
        for col in trow:
            col = col.strip()
            try:
                thismat = gdict[col]
            except KeyError:
                try:
                    thismat = ldict[col]
                except KeyError:
                    raise KeyError, "%s not found" % (col,)
                                    
            coltup.append(thismat)
        rowtup.append(concatenate(coltup,axis=-1))
    return concatenate(rowtup,axis=0)

    

def bmat(obj,gdict=None,ldict=None):
    """Build a matrix object from string, nested sequence, or array.

    Ex:  F = bmat('A, B; C, D')  
         F = bmat([[A,B],[C,D]])
         F = bmat(r_[c_[A,B],c_[C,D]])

        all produce the same Matrix Object    [ A  B ]
                                              [ C  D ]
                                      
        if A, B, C, and D are appropriately shaped 2-d arrays.
    """
    if isinstance(obj, types.StringType):
        if gdict is None:
            # get previous frame
            frame = sys._getframe().f_back
            glob_dict = frame.f_globals
            loc_dict = frame.f_locals
        else:
            glob_dict = gdict
            loc_dict = ldict
        
        return matrix(_from_string(obj, glob_dict, loc_dict))
    
    if isinstance(obj, (types.TupleType, types.ListType)):
        # [[A,B],[C,D]]
        arr_rows = []
        for row in obj:
            if isinstance(row, ArrayType):  # not 2-d
                return matrix(concatenate(obj,axis=-1))
            else:
                arr_rows.append(concatenate(row,axis=-1))
        return matrix(concatenate(arr_rows,axis=0))
    if isinstance(obj, ArrayType):
        return matrix(obj)

mat = matrix
    
        
