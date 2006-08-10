
/* Should only be used if x is known to be an nd-array */
#define _ARET(x) PyArray_Return((PyArrayObject *)(x))

static char doc_take[] = "a.take(indices, axis=None).  Selects the elements "\
	"in indices from array a along the given axis.";

static PyObject *
array_take(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int dimension=MAX_DIMS;
	PyObject *indices;
        PyArrayObject *out=NULL;
        NPY_CLIPMODE mode=NPY_RAISE;
	static char *kwlist[] = {"indices", "axis", "out", "mode", NULL};
	
	dimension=0;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O&O&O&", kwlist, 
					 &indices, PyArray_AxisConverter,
					 &dimension,
                                         PyArray_OutputConverter,
                                         &out,
                                         PyArray_ClipmodeConverter,
                                         &mode))
		return NULL;
	
	return _ARET(PyArray_TakeOut(self, indices, dimension, out, mode));
}

static char doc_fill[] = "a.fill(value) places the scalar value at every "\
	"position in the array.";

static PyObject *
array_fill(PyArrayObject *self, PyObject *args)
{
	PyObject *obj;
	if (!PyArg_ParseTuple(args, "O", &obj))
		return NULL;
	if (PyArray_FillWithScalar(self, obj) < 0) return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static char doc_put[] = "a.put(values, indices, mode) sets a.flat[n] = v[n] "\
	"for each n in indices. v can be scalar or shorter than indices, "\
	"will repeat.";

static PyObject *
array_put(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	PyObject *indices, *values;
        NPY_CLIPMODE mode=NPY_RAISE;
	static char *kwlist[] = {"values", "indices", "mode", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|O&", kwlist,
					 &values, &indices,
                                         PyArray_ClipmodeConverter,
                                         &mode))
		return NULL;
	return PyArray_PutIn(self, values, indices, mode);
}

static char doc_putmask[] = "a.putmask(values, mask) sets a.flat[n] = v[n] "\
	"for each n where mask.flat[n] is TRUE. v can be scalar.";

static PyObject *
array_putmask(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	PyObject *mask, *values;

	static char *kwlist[] = {"values", "mask", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist,
					 &values, &mask))
		return NULL;
	return PyArray_PutMask(self, values, mask);
}

static char doc_reshape[] = \
	"self.reshape(d1, d2, ..., dn, order='C') \n"	
	"Return a new array from this one. \n"				
	"\n  The new array must have the same number of elements as self. " 
	"Also\n always returns a view or raises a ValueError if that is \n"
	"impossible.";

static PyObject *
array_reshape(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
        PyArray_Dims newshape;
        PyObject *ret;
	PyArray_ORDER order=PyArray_CORDER;
	int n;
	
	if (kwds != NULL) {
		PyObject *ref;
		ref = PyDict_GetItemString(kwds, "order");
		if (ref == NULL ||                                      \
		    (PyArray_OrderConverter(ref, &order) == PY_FAIL))
			return NULL;
	}

	n = PyTuple_Size(args);
	if (n <= 1) {
		if (!PyArg_ParseTuple(args, "O&", PyArray_IntpConverter, 
				      &newshape)) return NULL;
	}
        else {
		if (!PyArray_IntpConverter(args, &newshape)) {
			if (!PyErr_Occurred()) {
				PyErr_SetString(PyExc_TypeError, 
						"invalid shape");
			} 
			goto fail;
		}
	}
	ret = PyArray_Newshape(self, &newshape, order);
	PyDimMem_FREE(newshape.ptr);
        return ret;

 fail:
	PyDimMem_FREE(newshape.ptr);
	return NULL;
}

static char doc_squeeze[] = "m.squeeze() eliminate all length-1 dimensions";

static PyObject *
array_squeeze(PyArrayObject *self, PyObject *args)
{
        if (!PyArg_ParseTuple(args, "")) return NULL;
        return PyArray_Squeeze(self);
}

static char doc_view[] = "a.view(<type>) return a new view of array with same data. type can be either a new sub-type object or a data-descriptor object";

static PyObject *
array_view(PyArrayObject *self, PyObject *args)
{
	PyObject *otype=NULL;
        PyArray_Descr *type=NULL;

	if (!PyArg_ParseTuple(args, "|O", &otype)) return NULL;

	if (otype) {
		if (PyType_Check(otype) &&			\
		    PyType_IsSubtype((PyTypeObject *)otype, 
				     &PyArray_Type)) {
			return PyArray_View(self, NULL, 
                                            (PyTypeObject *)otype);
                }
		else {
			if (PyArray_DescrConverter(otype, &type) == PY_FAIL) 
				return NULL;
		}
	}
	return PyArray_View(self, type, NULL);
}

static char doc_argmax[] = "a.argmax(axis=None, out=None)";

static PyObject *
array_argmax(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	
	
	return _ARET(PyArray_ArgMax(self, axis, out));
}

static char doc_argmin[] = "a.argmin(axis=None, out=None)";

static PyObject *
array_argmin(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	
	
	return _ARET(PyArray_ArgMin(self, axis, out));
}

static char doc_max[] = "a.max(axis=None)";

static PyObject *
array_max(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	
	
	return PyArray_Max(self, axis, out);
}

static char doc_ptp[] = "a.ptp(axis=None) a.max(axis)-a.min(axis)";

static PyObject *
array_ptp(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	
		
	return PyArray_Ptp(self, axis, out);
}


static char doc_min[] = "a.min(axis=None)";

static PyObject *
array_min(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	
	
	return PyArray_Min(self, axis, out);
}

static char doc_swapaxes[] = "a.swapaxes(axis1, axis2)  returns new view with axes swapped.";

static PyObject *
array_swapaxes(PyArrayObject *self, PyObject *args)
{
	int axis1, axis2;

	if (!PyArg_ParseTuple(args, "ii", &axis1, &axis2)) return NULL;

	return PyArray_SwapAxes(self, axis1, axis2);
}

static char doc_getfield[] = "m.getfield(dtype, offset) returns a field "\
	" of the given array as a certain type.  A field is a view of "\
	" the array's data with each itemsize determined by the given type"\
	" and the offset into the current array.";

/* steals typed reference */
/*OBJECT_API
 Get a subset of bytes from each element of the array
*/
static PyObject *
PyArray_GetField(PyArrayObject *self, PyArray_Descr *typed, int offset)
{
	PyObject *ret=NULL;

	if (offset < 0 || (offset + typed->elsize) > self->descr->elsize) {
		PyErr_Format(PyExc_ValueError,
			     "Need 0 <= offset <= %d for requested type "  \
			     "but received offset = %d",
			     self->descr->elsize-typed->elsize, offset);
		Py_DECREF(typed);
		return NULL;
	}
	ret = PyArray_NewFromDescr(self->ob_type, 
				   typed,
				   self->nd, self->dimensions,
				   self->strides, 
				   self->data + offset,
				   self->flags, (PyObject *)self);
	if (ret == NULL) return NULL;
	Py_INCREF(self);
	((PyArrayObject *)ret)->base = (PyObject *)self; 

	PyArray_UpdateFlags((PyArrayObject *)ret, UPDATE_ALL);
	return ret;
}

static PyObject *
array_getfield(PyArrayObject *self, PyObject *args, PyObject *kwds)
{

        PyArray_Descr *dtype;
	int offset = 0;
	static char *kwlist[] = {"dtype", "offset", 0};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O&|i", kwlist,
					 PyArray_DescrConverter,
					 &dtype, &offset)) return NULL;
	
	return _ARET(PyArray_GetField(self, dtype, offset));
}


static char doc_setfield[] = "m.setfield(value, dtype, offset) places val "\
	"into field of the given array defined by the data type and offset.";

/*OBJECT_API
 Set a subset of bytes from each element of the array
*/
static int
PyArray_SetField(PyArrayObject *self, PyArray_Descr *dtype,
		 int offset, PyObject *val)
{
	PyObject *ret=NULL;
	int retval = 0;
        
	if (offset < 0 || (offset + dtype->elsize) > self->descr->elsize) {
		PyErr_Format(PyExc_ValueError,
			     "Need 0 <= offset <= %d for requested type "  \
			     "but received offset = %d",
			     self->descr->elsize-dtype->elsize, offset);
		Py_DECREF(dtype);
		return -1;
	}
	ret = PyArray_NewFromDescr(self->ob_type, 
				   dtype, self->nd, self->dimensions,
				   self->strides, self->data + offset,
				   self->flags, (PyObject *)self);
	if (ret == NULL) return -1;
	Py_INCREF(self);
	((PyArrayObject *)ret)->base = (PyObject *)self;

	PyArray_UpdateFlags((PyArrayObject *)ret, UPDATE_ALL);	
	retval = PyArray_CopyObject((PyArrayObject *)ret, val);
	Py_DECREF(ret);
	return retval;
}

static PyObject *
array_setfield(PyArrayObject *self, PyObject *args, PyObject *kwds)
{
        PyArray_Descr *dtype;
	int offset = 0;
	PyObject *value;
	static char *kwlist[] = {"value", "dtype", "offset", 0};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO&|i", kwlist,
					 &value, PyArray_DescrConverter,
					 &dtype, &offset)) return NULL;

	if (PyArray_SetField(self, dtype, offset, value) < 0)
		return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

/* This doesn't change the descriptor just the actual data...
 */

/*OBJECT_API*/
static PyObject *
PyArray_Byteswap(PyArrayObject *self, Bool inplace)
{
        PyArrayObject *ret;
	intp size;
	PyArray_CopySwapNFunc *copyswapn;
	PyArrayIterObject *it;

        copyswapn = self->descr->f->copyswapn;
	if (inplace) {
                if (!PyArray_ISWRITEABLE(self)) {
                        PyErr_SetString(PyExc_RuntimeError,
                                        "Cannot byte-swap in-place on a " \
                                        "read-only array");
                        return NULL;
                }
		size = PyArray_SIZE(self);
		if (PyArray_ISONESEGMENT(self)) {
			copyswapn(self->data, self->descr->elsize, NULL, -1, size, 1, self);
		}
		else { /* Use iterator */
                        int axis = -1;
                        intp stride;
			it = (PyArrayIterObject *)                      \
				PyArray_IterAllButAxis((PyObject *)self, &axis);
                        stride = self->strides[axis];
                        size = self->dimensions[axis];
			while (it->index < it->size) {
                                copyswapn(it->dataptr, stride, NULL, -1, size, 1, self);
				PyArray_ITER_NEXT(it);
			}
			Py_DECREF(it);
		}
		
		Py_INCREF(self);
		return (PyObject *)self;
	}
	else {
                PyObject *new;
		if ((ret = (PyArrayObject *)PyArray_NewCopy(self,-1)) == NULL) 
			return NULL;
                new = PyArray_Byteswap(ret, TRUE);
                Py_DECREF(new);
		return (PyObject *)ret;
	}
}

static char doc_byteswap[] = "m.byteswap(False)  Swap the bytes in"\
	" the array.  Return the byteswapped array.  If the first argument"\
	" is TRUE, byteswap in-place and return a reference to self.";

static PyObject *
array_byteswap(PyArrayObject *self, PyObject *args) 
{
	Bool inplace=FALSE;
	
	if (!PyArg_ParseTuple(args, "|O&", PyArray_BoolConverter, &inplace))
		return NULL;
	
	return PyArray_Byteswap(self, inplace);
}

static char doc_tolist[] = "m.tolist().	 Copy the data portion of the array"\
	" to a hierarchical python list and return that list.";

static PyObject *
array_tolist(PyArrayObject *self, PyObject *args) 
{
        if (!PyArg_ParseTuple(args, "")) return NULL;	
        return PyArray_ToList(self);
}

static char doc_tostring[] = "m.tostring(order='C')  Construct a Python string "\
        "containing the raw bytes in the array";

static PyObject *
array_tostring(PyArrayObject *self, PyObject *args, PyObject *kwds)
{
	NPY_ORDER order=NPY_CORDER;
	static char *kwlist[] = {"order", NULL};
	
        if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&", kwlist,
					 PyArray_OrderConverter,
					 &order)) return NULL;
        return PyArray_ToString(self, order);
}

static char doc_tofile[] = "m.tofile(fid, sep="") write the data to a file.";

static PyObject *
array_tofile(PyArrayObject *self, PyObject *args, PyObject *kwds)
{
	int ret;
        PyObject *file;
	FILE *fd;
        char *sep="";
	char *format="";
	static char *kwlist[] = {"file", "sep", "format", NULL};
        
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|ss", kwlist, 
                                         &file, &sep, &format)) return NULL;

	if (PyString_Check(file) || PyUnicode_Check(file)) {
		file = PyObject_CallFunction((PyObject *)&PyFile_Type,
					     "Os", file, "wb");
		if (file==NULL) return NULL;
	}
	else {
		Py_INCREF(file);
	}
	fd = PyFile_AsFile(file);
	if (fd == NULL) {
		PyErr_SetString(PyExc_IOError, "first argument must be a " \
				"string or open file");
		Py_DECREF(file);
		return NULL;
	}
	ret = PyArray_ToFile(self, fd, sep, format);
	Py_DECREF(file);
	if (ret < 0) return NULL;
        Py_INCREF(Py_None);
        return Py_None;
}

static char doc_toscalar[] = "m.item().  Copy the first data point of "\
	"the array to a standard Python scalar and return it.";

static PyObject *
array_toscalar(PyArrayObject *self, PyObject *args) {
        if (!PyArg_ParseTuple(args, "")) return NULL;
	if (self->nd == 0 || PyArray_SIZE(self) == 1) 
		return self->descr->f->getitem(self->data, self);
	else {
		PyErr_SetString(PyExc_ValueError, "can only convert an"	\
				" array of size 1 to Python scalar.");
		return NULL;
	}
}

static char doc_cast[] = "m.astype(t).	Cast array m to type t.	 \n\n"\
	"t can be either a string representing a typecode, or a python type"\
	" object of type int, float, or complex.";

static PyObject *
array_cast(PyArrayObject *self, PyObject *args) 
{
	PyArray_Descr *descr=NULL;
	PyObject *obj;
	
        if (!PyArg_ParseTuple(args, "O&", PyArray_DescrConverter,
			      &descr)) return NULL;
	
	if (descr == self->descr) {
		obj = _ARET(PyArray_NewCopy(self,0));
		Py_XDECREF(descr);
		return obj;
	}
	return _ARET(PyArray_CastToType(self, descr, 0));
}	  

/* default sub-type implementation */

static char doc_wraparray[] = "m.__array_wrap__(obj) returns an object of "\
	"type m from the ndarray object obj";

static PyObject *
array_wraparray(PyArrayObject *self, PyObject *args)
{
	PyObject *arr;
	PyObject *ret;
	
	if (PyTuple_Size(args) < 1) {
		PyErr_SetString(PyExc_TypeError,
				"only accepts 1 argument");
		return NULL;
	}
	arr = PyTuple_GET_ITEM(args, 0);
	if (!PyArray_Check(arr)) {
		PyErr_SetString(PyExc_TypeError,
				"can only be called with ndarray object");
		return NULL;
	}	

	Py_INCREF(PyArray_DESCR(arr));
	ret = PyArray_NewFromDescr(self->ob_type, 
				   PyArray_DESCR(arr),
				   PyArray_NDIM(arr),
				   PyArray_DIMS(arr), 
				   PyArray_STRIDES(arr), PyArray_DATA(arr),
				   PyArray_FLAGS(arr), (PyObject *)self);
	if (ret == NULL) return NULL;
	Py_INCREF(arr);
	PyArray_BASE(ret) = arr;
	return ret;
}


static char doc_array_getarray[] = "m.__array__(|dtype) just returns either a new reference to self if dtype is not given or a new array of provided data type if dtype is different from the current dtype of the array.";

static PyObject *
array_getarray(PyArrayObject *self, PyObject *args) 
{
	PyArray_Descr *newtype=NULL;
	PyObject *ret;
	
	if (!PyArg_ParseTuple(args, "|O&", PyArray_DescrConverter,
			      &newtype)) return NULL;
	
	/* convert to PyArray_Type */
	if (!PyArray_CheckExact(self)) {
		PyObject *new;
		PyTypeObject *subtype = &PyArray_Type;

		if (!PyType_IsSubtype(self->ob_type, &PyArray_Type)) {
			subtype = &PyArray_Type;
		}
		
		Py_INCREF(PyArray_DESCR(self));
		new = PyArray_NewFromDescr(subtype, 
					   PyArray_DESCR(self),
					   PyArray_NDIM(self),
					   PyArray_DIMS(self), 
					   PyArray_STRIDES(self), 
					   PyArray_DATA(self),
					   PyArray_FLAGS(self), NULL);
		if (new == NULL) return NULL;
		Py_INCREF(self);
		PyArray_BASE(new) = (PyObject *)self;
		self = (PyArrayObject *)new;
	}
	else {
		Py_INCREF(self);
	}
		
	if ((newtype == NULL) || \
	    PyArray_EquivTypes(self->descr, newtype)) {
		return (PyObject *)self;
	}
	else {
		ret = PyArray_CastToType(self, newtype, 0);
		Py_DECREF(self);
		return ret;
	}
}

static char doc_copy[] = "m.copy(|order). Return a copy of the array.\n"\
	"If order is 'C' (False) then the result is contiguous (default). \n"\
	"If order is 'Fortran' (True) then the result has fortran order. \n"\
	"If order is 'Any' (None) then the result has fortran order \n"\
	"only if m is already in fortran order.";

static PyObject *
array_copy(PyArrayObject *self, PyObject *args) 
{
	PyArray_ORDER fortran=PyArray_CORDER;
        if (!PyArg_ParseTuple(args, "|O&", PyArray_OrderConverter,
			      &fortran)) return NULL;
	
        return PyArray_NewCopy(self, fortran);
}

static char doc_resize[] = "self.resize(new_shape, refcheck=True, order=False).  "\
	"Change size and shape of self inplace.\n"\
	"\n    Array must own its own memory and not be referenced by other " \
	"arrays\n    Returns None.";

static PyObject *
array_resize(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
        PyArray_Dims newshape;
        PyObject *ret;
	int n;
	int refcheck = 1;
	PyArray_ORDER fortran=PyArray_ANYORDER;
	
	if (kwds != NULL) {
		PyObject *ref;
		ref = PyDict_GetItemString(kwds, "refcheck");
		if (ref) {
			refcheck = PyInt_AsLong(ref);
			if (refcheck==-1 && PyErr_Occurred()) {
				return NULL;
			}
		}
		ref = PyDict_GetItemString(kwds, "order");
		if (ref != NULL || 
		    (PyArray_OrderConverter(ref, &fortran) == PY_FAIL))
			return NULL;
	}
	n = PyTuple_Size(args);
	if (n <= 1) {
		if (!PyArg_ParseTuple(args, "O&", PyArray_IntpConverter, 
				      &newshape)) return NULL;
	}
        else {
		if (!PyArray_IntpConverter(args, &newshape)) {
			if (!PyErr_Occurred()) {
				PyErr_SetString(PyExc_TypeError, 
						"invalid shape");
			} 
			return NULL;			
		}
	}	
	ret = PyArray_Resize(self, &newshape, refcheck, fortran);
        PyDimMem_FREE(newshape.ptr);
        if (ret == NULL) return NULL;
	Py_DECREF(ret);
	Py_INCREF(Py_None);
	return Py_None;
}

static char doc_repeat[] = "a.repeat(repeats=, axis=None)\n"\
	"\n"\
	" Copy elements of a, repeats times.  The repeats argument must\n"\
	"  be a sequence of length a.shape[axis] or a scalar.";

static PyObject *
array_repeat(PyArrayObject *self, PyObject *args, PyObject *kwds) {
	PyObject *repeats;
	int axis=MAX_DIMS;
	static char *kwlist[] = {"repeats", "axis", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O&", kwlist, 
					 &repeats, PyArray_AxisConverter,
					 &axis)) return NULL;
	
	return _ARET(PyArray_Repeat(self, repeats, axis));
}

static char doc_choose[] = "a.choose(b0, b1, ..., bn, out=None, mode='raise')\n"\
	"\n"                                                            \
	"Return an array that merges the b_i arrays together using 'a' as the index\n"
        "The b_i arrays and 'a' must all be broadcastable to the same shape.\n"
        "The output at a particular position is the input array b_i at that position\n"
        "depending on the value of 'a' at that position.  Therefore, 'a' must be\n"
        "an integer array with entries from 0 to n+1.";

static PyObject *
array_choose(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	PyObject *choices;
	int n;
        PyArrayObject *out=NULL;
        NPY_CLIPMODE clipmode=NPY_RAISE;
	
	n = PyTuple_Size(args);
	if (n <= 1) {
		if (!PyArg_ParseTuple(args, "O", &choices))
			return NULL;
	}
        else {
		choices = args;
	}
        if (kwds && PyDict_Check(kwds)) {
                if (PyArray_OutputConverter(PyDict_GetItemString(kwds, 
                                                                 "out"),
                                            &out) == PY_FAIL)
                        return NULL;
                if (PyArray_ClipmodeConverter(PyDict_GetItemString(kwds, 
                                                                   "mode"), 
                                              &clipmode) == PY_FAIL)
                        return NULL;
        }
	
	return _ARET(PyArray_Choose(self, choices, out, clipmode));
}

static char doc_sort[] = "a.sort(axis=-1,kind='quicksort') sorts in place along axis.  Return is None and kind can be 'quicksort', 'mergesort', or 'heapsort'";

static PyObject *
array_sort(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=-1;
	int val;
	PyArray_SORTKIND which=PyArray_QUICKSORT;
	static char *kwlist[] = {"axis", "kind", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iO&", kwlist, &axis,
					 PyArray_SortkindConverter, &which))
		return NULL;
	
	val = PyArray_Sort(self, axis, which);
	if (val < 0) return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static char doc_argsort[] = "a.argsort(axis=-1,kind='quicksort')\n"\
	"  Return the indexes into a that would sort it along the"\
	" given axis; kind can be 'quicksort', 'mergesort', or 'heapsort'";

static PyObject *
array_argsort(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=-1;
	PyArray_SORTKIND which=PyArray_QUICKSORT;
	static char *kwlist[] = {"axis", "kind", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iO&", kwlist, &axis,
					 PyArray_SortkindConverter, &which))
		return NULL;
	
	return _ARET(PyArray_ArgSort(self, axis, which));
}

static char doc_searchsorted[] = "a.searchsorted(v)\n"\
	" Assuming that a is a 1-D array, in ascending order and\n"\
	" represents bin boundaries, then a.searchsorted(values) gives an\n"\
	" array of bin numbers, giving the bin into which each value would\n"\
	" be placed.  This method is helpful for histograming.  \n"\
	" Note: No warning is given if the boundaries, in a, are not \n"\
	" in ascending order.";

static PyObject *
array_searchsorted(PyArrayObject *self, PyObject *args) 
{
	PyObject *values;
	
	if (!PyArg_ParseTuple(args, "O", &values)) return NULL;
	
	return _ARET(PyArray_SearchSorted(self, values));
}

static void
_deepcopy_call(char *iptr, char *optr, PyArray_Descr *dtype,
	       PyObject *deepcopy, PyObject *visit)
{
	if (dtype->hasobject == 0) return;
	if (dtype->type_num == PyArray_OBJECT) {
		PyObject **itemp, **otemp;
		PyObject *res;
		itemp = (PyObject **)iptr;
		otemp = (PyObject **)optr;
		Py_XINCREF(*itemp);
		/* call deepcopy on this argument */
		res = PyObject_CallFunctionObjArgs(deepcopy, 
						   *itemp, visit, NULL);
		Py_XDECREF(*itemp);
		Py_XDECREF(*otemp);
		*otemp = res;
	}
	else if (PyDescr_HASFIELDS(dtype)) {
                PyObject *key, *value, *title=NULL;
                PyArray_Descr *new;
                int offset, pos=0;
                while (PyDict_Next(dtype->fields, &pos, &key, &value)) {
 			if (!PyArg_ParseTuple(value, "Oi|O", &new, &offset, 
					      &title)) return;
                        _deepcopy_call(iptr + offset, optr + offset, new,
				       deepcopy, visit);
                }
        }
}

static char doc_deepcopy[] = "Used if copy.deepcopy is called on an array.";

static PyObject *
array_deepcopy(PyArrayObject *self, PyObject *args) 
{
        PyObject* visit;
	char *optr;
        PyArrayIterObject *it;
        PyObject *copy, *ret, *deepcopy;

        if (!PyArg_ParseTuple(args, "O", &visit)) return NULL;
        ret = PyArray_Copy(self);
        if (self->descr->hasobject) {
                copy = PyImport_ImportModule("copy");
                if (copy == NULL) return NULL;
                deepcopy = PyObject_GetAttrString(copy, "deepcopy");
                Py_DECREF(copy);
                if (deepcopy == NULL) return NULL;
                it = (PyArrayIterObject *)PyArray_IterNew((PyObject *)self);
                if (it == NULL) {Py_DECREF(deepcopy); return NULL;}
                optr = PyArray_DATA(ret);
                while(it->index < it->size) {
			_deepcopy_call(it->dataptr, optr, self->descr,
				       deepcopy, visit);
			optr += self->descr->elsize;
                        PyArray_ITER_NEXT(it);
                }
                Py_DECREF(deepcopy);
                Py_DECREF(it);
        }
        return _ARET(ret);
}

/* Convert Array to flat list (using getitem) */
static PyObject *
_getlist_pkl(PyArrayObject *self)
{
	PyObject *theobject;
	PyArrayIterObject *iter=NULL;
	PyObject *list;
	PyArray_GetItemFunc *getitem;

	getitem = self->descr->f->getitem;
	iter = (PyArrayIterObject *)PyArray_IterNew((PyObject *)self);
	if (iter == NULL) return NULL;
	list = PyList_New(iter->size);
	if (list == NULL) {Py_DECREF(iter); return NULL;}
	while (iter->index < iter->size) {
		theobject = getitem(iter->dataptr, self);
		PyList_SET_ITEM(list, (int) iter->index, theobject);
		PyArray_ITER_NEXT(iter);
	}
	Py_DECREF(iter);
	return list;
}

static int
_setlist_pkl(PyArrayObject *self, PyObject *list)
{
	PyObject *theobject;
	PyArrayIterObject *iter=NULL;
	PyArray_SetItemFunc *setitem;

	setitem = self->descr->f->setitem;
	iter = (PyArrayIterObject *)PyArray_IterNew((PyObject *)self);
	if (iter == NULL) return -1;
	while(iter->index < iter->size) {
		theobject = PyList_GET_ITEM(list, (int) iter->index);
		setitem(theobject, iter->dataptr, self);
		PyArray_ITER_NEXT(iter);
	}
	Py_XDECREF(iter);
	return 0;
}

static char doc_reduce[] = "a.__reduce__()  for pickling.";

static PyObject *
array_reduce(PyArrayObject *self, PyObject *args)
{
        /* version number of this pickle type. Increment if we need to
           change the format. Be sure to handle the old versions in
           array_setstate. */
        const int version = 1;
	PyObject *ret=NULL, *state=NULL, *obj=NULL, *mod=NULL;
	PyObject *mybool, *thestr=NULL;
	PyArray_Descr *descr;

	/* Return a tuple of (callable object, arguments, object's state) */
	/*  We will put everything in the object's state, so that on UnPickle
	    it can use the string object as memory without a copy */

	ret = PyTuple_New(3);
	if (ret == NULL) return NULL;
	mod = PyImport_ImportModule("numpy.core.multiarray");
	if (mod == NULL) {Py_DECREF(ret); return NULL;}
	obj = PyObject_GetAttrString(mod, "_reconstruct");
	Py_DECREF(mod);
	PyTuple_SET_ITEM(ret, 0, obj);
	PyTuple_SET_ITEM(ret, 1, 
			 Py_BuildValue("ONc",
				       (PyObject *)self->ob_type,
				       Py_BuildValue("(N)",
						     PyInt_FromLong(0)),
				       /* dummy data-type */
				       'b'));
	
	/* Now fill in object's state.  This is a tuple with 
	   5 arguments

           1) an integer with the pickle version.
	   2) a Tuple giving the shape
	   3) a PyArray_Descr Object (with correct bytorder set)
	   4) a Bool stating if Fortran or not
	   5) a Python object representing the data (a string, or
	        a list or any user-defined object).

	   Notice because Python does not describe a mechanism to write 
	   raw data to the pickle, this performs a copy to a string first
	*/

	state = PyTuple_New(5);
	if (state == NULL) {
		Py_DECREF(ret); return NULL;
	}
        PyTuple_SET_ITEM(state, 0, PyInt_FromLong(version));
	PyTuple_SET_ITEM(state, 1, PyObject_GetAttrString((PyObject *)self, 
							  "shape"));
	descr = self->descr;
	Py_INCREF(descr);
	PyTuple_SET_ITEM(state, 2, (PyObject *)descr);
	mybool = (PyArray_ISFORTRAN(self) ? Py_True : Py_False);
	Py_INCREF(mybool);
	PyTuple_SET_ITEM(state, 3, mybool);
	if (self->descr->hasobject || self->descr->f->listpickle) {
		thestr = _getlist_pkl(self);
	}
	else {
                thestr = PyArray_ToString(self, NPY_ANYORDER);
	}
	if (thestr == NULL) {
		Py_DECREF(ret);
		Py_DECREF(state);
		return NULL;
	}
	PyTuple_SET_ITEM(state, 4, thestr);
	PyTuple_SET_ITEM(ret, 2, state);
	return ret;
}

static char doc_setstate[] = "a.__setstate__(tuple) for unpickling.";

/*
	   1) a Tuple giving the shape
	   2) a PyArray_Descr Object
	   3) a Bool stating if Fortran or not
	   4) a binary string with the data (or a list if Object array) 
*/

static size_t _array_fill_strides(intp *, intp *, int, size_t, int, int *);

static int _IsAligned(PyArrayObject *); 

static PyArray_Descr * _array_typedescr_fromstr(char *);

static PyObject *
array_setstate(PyArrayObject *self, PyObject *args)
{
	PyObject *shape;
	PyArray_Descr *typecode;
        int version = 1;
	int fortran;
	PyObject *rawdata;
	char *datastr;
	int len;
	intp size, dimensions[MAX_DIMS];
	int nd;
	
	/* This will free any memory associated with a and
	   use the string in setstate as the (writeable) memory.
	*/
	if (!PyArg_ParseTuple(args, "(iO!O!iO)", &version, &PyTuple_Type,
			      &shape, &PyArrayDescr_Type, &typecode,
			      &fortran, &rawdata)) {
            PyErr_Clear();
            version = 0;
	    if (!PyArg_ParseTuple(args, "(O!O!iO)", &PyTuple_Type,
			      &shape, &PyArrayDescr_Type, &typecode, 
			      &fortran, &rawdata)) {
		return NULL;
            }
        }

        /* If we ever need another pickle format, increment the version
           number. But we should still be able to handle the old versions.
           We've only got one right now. */
        if (version != 1 && version != 0) {
            PyErr_Format(PyExc_ValueError,
                         "can't handle version %d of numpy.ndarray pickle",
                         version);
            return NULL;
        }

	Py_XDECREF(self->descr);
	self->descr = typecode;
	Py_INCREF(typecode);
	nd = PyArray_IntpFromSequence(shape, dimensions, MAX_DIMS);
	if (nd < 0) return NULL;
	size = PyArray_MultiplyList(dimensions, nd);
	if (self->descr->elsize == 0) {
		PyErr_SetString(PyExc_ValueError, "Invalid data-type size.");
		return NULL;
	}
	if (size < 0 || size > MAX_INTP / self->descr->elsize) {
		PyErr_NoMemory();
		return NULL;
	}

	if (typecode->hasobject || typecode->f->listpickle) {
		if (!PyList_Check(rawdata)) {
			PyErr_SetString(PyExc_TypeError, 
					"object pickle not returning list");
			return NULL;
		}
	}
	else {
		if (!PyString_Check(rawdata)) {
			PyErr_SetString(PyExc_TypeError, 
					"pickle not returning string");
			return NULL;
		}

		if (PyString_AsStringAndSize(rawdata, &datastr, &len))
			return NULL;

		if ((len != (self->descr->elsize * size))) {
			PyErr_SetString(PyExc_ValueError, 
					"buffer size does not"	\
					" match array size");
			return NULL;
		}
	}

        if ((self->flags & OWNDATA)) {
		if (self->data != NULL)
			PyDataMem_FREE(self->data);
		self->flags &= ~OWNDATA;
        }
	Py_XDECREF(self->base);

	self->flags &= ~UPDATEIFCOPY;

        if (self->dimensions != NULL) {
                PyDimMem_FREE(self->dimensions); 
		self->dimensions = NULL;
	}

	self->flags = DEFAULT;

	self->nd = nd;

	if (nd > 0) {
		self->dimensions = PyDimMem_NEW(nd * 2);
		self->strides = self->dimensions + nd;
		memcpy(self->dimensions, dimensions, sizeof(intp)*nd);
		(void) _array_fill_strides(self->strides, dimensions, nd,
					   (size_t) self->descr->elsize, 
                                           (fortran ? FORTRAN : CONTIGUOUS),
					   &(self->flags));
	}

	if (typecode->hasobject != 1 && !typecode->f->listpickle) {
                int swap=!PyArray_ISNOTSWAPPED(self);
		self->data = datastr;
		if (!_IsAligned(self) || swap) {
			intp num = PyArray_NBYTES(self);
			self->data = PyDataMem_NEW(num);
			if (self->data == NULL) {
				self->nd = 0;
				PyDimMem_FREE(self->dimensions);
				return PyErr_NoMemory();
			}
                        if (swap) { /* byte-swap on pickle-read */
				intp numels = num / self->descr->elsize;
                                self->descr->f->copyswapn(self->data, self->descr->elsize,
                                                          datastr, self->descr->elsize,
                                                          numels, 1, self);
				if (!PyArray_ISEXTENDED(self)) {
					self->descr = PyArray_DescrFromType(self->descr->type_num);
				}
				else {
					self->descr = PyArray_DescrNew(typecode);
					if (self->descr->byteorder == PyArray_BIG) 
						self->descr->byteorder = PyArray_LITTLE;
					else if (self->descr->byteorder == PyArray_LITTLE)
						self->descr->byteorder = PyArray_BIG;
				}
				Py_DECREF(typecode);
                        }
                        else {
                                memcpy(self->data, datastr, num);
                        }
			self->flags |= OWNDATA;
			self->base = NULL;
		}
		else {
			self->base = rawdata;
			Py_INCREF(self->base);
		}
	}
	else {
		self->data = PyDataMem_NEW(PyArray_NBYTES(self));
		if (self->data == NULL) { 
			self->nd = 0;
			self->data = PyDataMem_NEW(self->descr->elsize);
			if (self->dimensions) PyDimMem_FREE(self->dimensions);
			return PyErr_NoMemory();
		}
		if (self->descr->hasobject) memset(self->data, 0, PyArray_NBYTES(self));
		self->flags |= OWNDATA;
		self->base = NULL;
		if (_setlist_pkl(self, rawdata) < 0) 
			return NULL;
	}

	PyArray_UpdateFlags(self, UPDATE_ALL);
	
	Py_INCREF(Py_None);
	return Py_None;	
}

/*OBJECT_API*/
static int
PyArray_Dump(PyObject *self, PyObject *file, int protocol)
{
	PyObject *cpick=NULL;
	PyObject *ret;
	if (protocol < 0) protocol = 2;

	cpick = PyImport_ImportModule("cPickle");
	if (cpick==NULL) return -1;

	if PyString_Check(file) {
		file = PyFile_FromString(PyString_AS_STRING(file), "wb");
		if (file==NULL) return -1;
	}
	else Py_INCREF(file);
	ret = PyObject_CallMethod(cpick, "dump", "OOi", self, 
				  file, protocol);
	Py_XDECREF(ret);
	Py_DECREF(file);
	Py_DECREF(cpick);
	if (PyErr_Occurred()) return -1;
	return 0;
}

/*OBJECT_API*/
static PyObject *
PyArray_Dumps(PyObject *self, int protocol)
{
	PyObject *cpick=NULL;
	PyObject *ret;
	if (protocol < 0) protocol = 2;

	cpick = PyImport_ImportModule("cPickle");
	if (cpick==NULL) return NULL;
	ret = PyObject_CallMethod(cpick, "dumps", "Oi", self, protocol);
	Py_DECREF(cpick);
	return ret;
}


static char doc_dump[] = "m.dump(file)";

static PyObject *
array_dump(PyArrayObject *self, PyObject *args)
{
	PyObject *file=NULL;
	int ret;

	if (!PyArg_ParseTuple(args, "O", &file))
		return NULL;
	ret = PyArray_Dump((PyObject *)self, file, 2);
	if (ret < 0) return NULL;
	Py_INCREF(Py_None);
	return Py_None;
}

static char doc_dumps[] = "m.dumps()";

static PyObject *
array_dumps(PyArrayObject *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	return PyArray_Dumps((PyObject *)self, 2);
}


static char doc_transpose[] = "a.transpose(*axes)\n\n"
"Returns a view of `a` with axes transposed. If no axes are given,\n"
"or None is passed, switches the order of the axes (for a 2-d array,\n"
"this is the usual matrix transpose). If axes are given, they\n"
"describe how the axes are permuted.\n\n"
"Example:\n"
">>> a = array([[1,2],[3,4]])\n"
">>> a\n"
"array([[1, 2],\n"
"       [3, 4]])\n"
">>> a.transpose()\n"
"array([[1, 3],\n"
"       [2, 4]])\n"
">>> a.transpose((1,0))\n"
"array([[1, 3],\n"
"       [2, 4]])\n"
">>> a.transpose(1,0)\n"
"array([[1, 3],\n"
"       [2, 4]])\n"
;

static PyObject *
array_transpose(PyArrayObject *self, PyObject *args) 
{
	PyObject *shape=Py_None;
	int n;
	PyArray_Dims permute;
	PyObject *ret;

	n = PyTuple_Size(args);
	if (n > 1) shape = args;
	else if (n == 1) shape = PyTuple_GET_ITEM(args, 0);
	
	if (shape == Py_None)
		ret = PyArray_Transpose(self, NULL);
	else {
		if (!PyArray_IntpConverter(shape, &permute)) return NULL;
		ret = PyArray_Transpose(self, &permute);
		PyDimMem_FREE(permute.ptr);
	}
	
	return _ARET(ret);
}

static char doc_mean[] = "a.mean(axis=None, dtype=None)\n\n"\
  "Average the array over the given axis.  If the axis is None, average\n"\
  "over all dimensions of the array.\n"\
  "\n"\
  "If an integer axis is given, this equals:\n"\
  "    a.sum(axis, dtype) * 1.0 / len(a)\n"\
  "\n"\
  "If axis is None, this equals:\n"\
  "     a.sum(axis, dtype) * 1.0 / product(a.shape)\n"\
  "\n"\
  "The optional dtype argument is the data type for intermediate\n"\
  "calculations in the sum.";

#define _CHKTYPENUM(typ) ((typ) ? (typ)->type_num : PyArray_NOTYPE)

static PyObject *
array_mean(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist,
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;

	return PyArray_Mean(self, axis, _CHKTYPENUM(dtype), out);
}

static char doc_sum[] = "a.sum(axis=None, dtype=None)\n\n"\
  "Sum the array over the given axis.  If the axis is None, sum over all\n"\
  "dimensions of the array.\n"\
  "\n"\
  "The optional dtype argument is the data type for the returned value\n"\
  "and intermediate calculations.  The default is to upcast (promote)\n"\
  "smaller integer types to the platform-dependent int.  For example, on\n"\
  "32-bit platforms:\n"\
  "\n"\
  "    a.dtype                         default sum() dtype\n"\
  "    ---------------------------------------------------\n"\
  "    bool, int8, int16, int32        int32\n"\
  "\n"\
  "Examples:\n"\
  "\n"\
  ">>> array([0.5, 1.5]).sum()\n"\
  "2.0\n"\
  ">>> array([0.5, 1.5]).sum(dtype=int32)\n"\
  "1\n"\
  ">>> array([[0, 1], [0, 5]]).sum(axis=0)\n"\
  "array([0, 6])\n"\
  ">>> array([[0, 1], [0, 5]]).sum(axis=1)\n"\
  "array([1, 5])";

static PyObject *
array_sum(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist, 
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;
	
	return PyArray_Sum(self, axis, _CHKTYPENUM(dtype), out);
}


static char doc_cumsum[] = "a.cumsum(axis=None, dtype=None, out=None)";

static PyObject *
array_cumsum(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist, 
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;
	
	return PyArray_CumSum(self, axis, _CHKTYPENUM(dtype), out);
}

static char doc_prod[] = "a.prod(axis=None, dtype=None)";

static PyObject *
array_prod(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist, 
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;
	
	return PyArray_Prod(self, axis, _CHKTYPENUM(dtype), out);
}


static char doc_cumprod[] = "a.cumprod(axis=None, dtype=None)";

static PyObject *
array_cumprod(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist, 
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;
	
	return PyArray_CumProd(self, axis, _CHKTYPENUM(dtype), out);
}


static char doc_any[] = "a.any(axis=None, out=None)";

static PyObject *
array_any(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	
	
	return PyArray_Any(self, axis, out);
}

static char doc_all[] = "a.all(axis=None)";

static PyObject *
array_all(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&", kwlist, 
					 PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out))
		return NULL;	

	return PyArray_All(self, axis, out);
}

static char doc_stddev[] = "a.std(axis=None, dtype=None, out=None)\n"
"Return the standard deviation, a measure of the spread of a distribution.\n"
"\n"
"The standard deviation is the square root of the average of the squared\n"
"deviations from the mean, i.e. std = sqrt(mean((x - x.mean())**2)).\n"
"\n"
"For multidimensional arrays, std is computed by default along the first axis.\n";

static PyObject *
array_stddev(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist, 
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;
	
	return PyArray_Std(self, axis, _CHKTYPENUM(dtype), out, 0);
}

static char doc_variance[] = "a.var(axis=None, dtype=None)";

static PyObject *
array_variance(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"axis", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O&O&O&", kwlist, 
					 PyArray_AxisConverter, 
					 &axis, PyArray_DescrConverter2,
					 &dtype,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;
	
	return PyArray_Std(self, axis, _CHKTYPENUM(dtype), out, 1);
}

static char doc_compress[] = "a.compress(condition=, axis=None, out=None)";

static PyObject *
array_compress(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis=MAX_DIMS;
	PyObject *condition;	
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"condition", "axis", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O&O&", kwlist, 
					 &condition, PyArray_AxisConverter,
					 &axis,
                                         PyArray_OutputConverter,
                                         &out)) return NULL;

	return _ARET(PyArray_Compress(self, condition, axis, out));
}

static char doc_nonzero[] = \
    "a.nonzero() returns a tuple of arrays, one for each dimension of a,\n"\
    "containing the indices of the non-zero elements in that dimension.\n"\
    "The corresponding non-zero values can be obtained with\n"\
    "    a[a.nonzero()].\n"
    "\n"\
    "To group the indices by element, rather than dimension, use\n"\
    "    transpose(a.nonzero())\n"\
    "instead. The result of this is always a 2d array, with a row for each\n"\
    "non-zero element.";

static PyObject *
array_nonzero(PyArrayObject *self, PyObject *args)
{
	if (!PyArg_ParseTuple(args, "")) return NULL;

	return PyArray_Nonzero(self);
}


static char doc_trace[] = "a.trace(offset=0, axis1=0, axis2=1, dtype=None, out=None)\n"\
	"return the sum along the offset diagonal of the arrays indicated\n" \
	"axis1 and axis2.";

static PyObject *
array_trace(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis1=0, axis2=1, offset=0;
	PyArray_Descr *dtype=NULL;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"offset", "axis1", "axis2", "dtype", "out", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiiO&O&", kwlist, 
					 &offset, &axis1, &axis2,
					 PyArray_DescrConverter2, &dtype,
                                         PyArray_OutputConverter, &out))
		return NULL;
	
	return _ARET(PyArray_Trace(self, offset, axis1, axis2, 
				   _CHKTYPENUM(dtype), out));
}

#undef _CHKTYPENUM


static char doc_clip[] = "a.clip(min=, max=, out=None)";

static PyObject *
array_clip(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	PyObject *min, *max;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"min", "max", "out", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|O&", kwlist,
					 &min, &max, 
                                         PyArray_OutputConverter,
                                         &out)) 
		return NULL;
	
	return _ARET(PyArray_Clip(self, min, max, out));
}

static char doc_conj[] = "a.conj()";

static char doc_conjugate[] = "a.conjugate()";

static PyObject *
array_conjugate(PyArrayObject *self, PyObject *args) 
{

        PyArrayObject *out=NULL;
	if (!PyArg_ParseTuple(args, "|O&",
                              PyArray_OutputConverter,
                              &out)) return NULL;
	
	return PyArray_Conjugate(self, out);
}


static char doc_diagonal[] = "a.diagonal(offset=0, axis1=0, axis2=1)";

static PyObject *
array_diagonal(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int axis1=0, axis2=1, offset=0;
	static char *kwlist[] = {"offset", "axis1", "axis2", NULL};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iii", kwlist, 
					 &offset, &axis1, &axis2))
		return NULL;
	
	return _ARET(PyArray_Diagonal(self, offset, axis1, axis2));
}

static char doc_flatten[] = "a.flatten([fortran]) return a 1-d array (always copy)";

static PyObject *
array_flatten(PyArrayObject *self, PyObject *args)
{
	PyArray_ORDER fortran=PyArray_CORDER;

	if (!PyArg_ParseTuple(args, "|O&", PyArray_OrderConverter, 
			      &fortran)) return NULL;
        
	return PyArray_Flatten(self, fortran);
}

static char doc_ravel[] = "a.ravel([fortran]) return a 1-d array (copy only if needed)";

static PyObject *
array_ravel(PyArrayObject *self, PyObject *args)
{
	PyArray_ORDER fortran=PyArray_CORDER;
	
	if (!PyArg_ParseTuple(args, "|O&", PyArray_OrderConverter, 
			      &fortran)) return NULL;

	return PyArray_Ravel(self, fortran);
}

static char doc_round[] = "a.round(decimals=0, out=None)";

static PyObject *
array_round(PyArrayObject *self, PyObject *args, PyObject *kwds) 
{
	int decimals = 0;
        PyArrayObject *out=NULL;
	static char *kwlist[] = {"decimals", "out", NULL};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iO&", kwlist,
					 &decimals, PyArray_OutputConverter,
                                         &out))
            return NULL;
        	
	return _ARET(PyArray_Round(self, decimals, out));
}


static char doc_setflags[] = "a.setflags(write=None, align=None, uic=None)";

static int _IsAligned(PyArrayObject *);
static Bool _IsWriteable(PyArrayObject *);

static PyObject *
array_setflags(PyArrayObject *self, PyObject *args, PyObject *kwds)
{
	static char *kwlist[] = {"write", "align", "uic", NULL};
	PyObject *write=Py_None;
	PyObject *align=Py_None;
	PyObject *uic=Py_None;
	int flagback = self->flags;
		
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOO", kwlist,
					 &write, &align, &uic))
		return NULL;

	if (align != Py_None) {
		if (PyObject_Not(align)) self->flags &= ~ALIGNED;
		else if (_IsAligned(self)) self->flags |= ALIGNED;
		else {
			PyErr_SetString(PyExc_ValueError, 
					"cannot set aligned flag of mis-"\
					"aligned array to True");
			return NULL;
		}
	}
	
	if (uic != Py_None) {
                if (PyObject_IsTrue(uic)) {
			self->flags = flagback;
                        PyErr_SetString(PyExc_ValueError, 
                                        "cannot set UPDATEIFCOPY"       \
                                        "flag to True");
                        return NULL;
                }
                else {
                        self->flags &= ~UPDATEIFCOPY;
                        Py_XDECREF(self->base);
                        self->base = NULL;
                }
        }
        
        if (write != Py_None) {
                if (PyObject_IsTrue(write)) 
			if (_IsWriteable(self)) {
				self->flags |= WRITEABLE;
			}
			else {
				self->flags = flagback;
				PyErr_SetString(PyExc_ValueError, 
						"cannot set WRITEABLE "	\
						"flag to True of this "	\
						"array");		\
				return NULL;
			}
                else
                        self->flags &= ~WRITEABLE;
        }
        
        Py_INCREF(Py_None);
        return Py_None;
}

static char doc_newbyteorder[] = "a.newbyteorder(<byteorder>) is equivalent\n" \
	" to a.view(a.dtype.newbytorder(<byteorder>))\n";

static PyObject *
array_newbyteorder(PyArrayObject *self, PyObject *args) 
{
	char endian = PyArray_SWAP;
	PyArray_Descr *new;
	
	if (!PyArg_ParseTuple(args, "|O&", PyArray_ByteorderConverter,
			      &endian)) return NULL;

	new = PyArray_DescrNewByteorder(self->descr, endian);
	if (!new) return NULL;
	return PyArray_View(self, new, NULL);

}

static PyMethodDef array_methods[] = {
        {"tolist",	 (PyCFunction)array_tolist,	1, doc_tolist},
        {"item", (PyCFunction)array_toscalar, METH_VARARGS, doc_toscalar},
	{"tofile", (PyCFunction)array_tofile, 
         METH_VARARGS | METH_KEYWORDS, doc_tofile},
        {"tostring", (PyCFunction)array_tostring, 
	 METH_VARARGS | METH_KEYWORDS, doc_tostring},
        {"byteswap",   (PyCFunction)array_byteswap,	1, doc_byteswap},
        {"astype", (PyCFunction)array_cast, 1, doc_cast},
	{"getfield", (PyCFunction)array_getfield, 
	 METH_VARARGS | METH_KEYWORDS, doc_getfield},
	{"setfield", (PyCFunction)array_setfield, 
	 METH_VARARGS | METH_KEYWORDS, doc_setfield},
        {"copy", (PyCFunction)array_copy, 1, doc_copy},  
        {"resize", (PyCFunction)array_resize, 
	 METH_VARARGS | METH_KEYWORDS, doc_resize}, 

	/* for subtypes */
	{"__array__", (PyCFunction)array_getarray, 1, doc_array_getarray},
	{"__array_wrap__", (PyCFunction)array_wraparray, 1, doc_wraparray},
	
	/* for the copy module */
        {"__copy__", (PyCFunction)array_copy, 1, doc_copy},	 
        {"__deepcopy__", (PyCFunction)array_deepcopy, 1, doc_deepcopy},  
	
        /* for Pickling */
        {"__reduce__", (PyCFunction) array_reduce, 1, doc_reduce},	
	{"__setstate__", (PyCFunction) array_setstate, 1, doc_setstate},
	{"dumps", (PyCFunction) array_dumps, 1, doc_dumps},
	{"dump", (PyCFunction) array_dump, 1, doc_dump},

	/* Extended methods added 2005 */
	{"fill", (PyCFunction)array_fill,
	 METH_VARARGS, doc_fill},
	{"transpose",	(PyCFunction)array_transpose, 
	 METH_VARARGS, doc_transpose},
	{"take",	(PyCFunction)array_take, 
	 METH_VARARGS|METH_KEYWORDS, doc_take},
	{"put",	(PyCFunction)array_put, 
	 METH_VARARGS|METH_KEYWORDS, doc_put},
	{"putmask",	(PyCFunction)array_putmask, 
	 METH_VARARGS|METH_KEYWORDS, doc_putmask},
	{"repeat",	(PyCFunction)array_repeat, 
	 METH_VARARGS|METH_KEYWORDS, doc_repeat},
	{"choose",	(PyCFunction)array_choose, 
	 METH_VARARGS|METH_KEYWORDS, doc_choose},	
	{"sort",	(PyCFunction)array_sort, 
	 METH_VARARGS|METH_KEYWORDS, doc_sort},
	{"argsort",	(PyCFunction)array_argsort, 
	 METH_VARARGS|METH_KEYWORDS, doc_argsort},
	{"searchsorted",  (PyCFunction)array_searchsorted, 
	 METH_VARARGS, doc_searchsorted},	
	{"argmax",	(PyCFunction)array_argmax, 
	 METH_VARARGS|METH_KEYWORDS, doc_argmax},
	{"argmin",  (PyCFunction)array_argmin,
	 METH_VARARGS|METH_KEYWORDS, doc_argmin},
	{"reshape",	(PyCFunction)array_reshape, 
	 METH_VARARGS|METH_KEYWORDS, doc_reshape},
	{"squeeze",	(PyCFunction)array_squeeze,
	 METH_VARARGS, doc_squeeze},
	{"view",  (PyCFunction)array_view, 
	 METH_VARARGS, doc_view},
	{"swapaxes", (PyCFunction)array_swapaxes,
	 METH_VARARGS, doc_swapaxes},
	{"max", (PyCFunction)array_max,
	 METH_VARARGS|METH_KEYWORDS, doc_max},
	{"min", (PyCFunction)array_min,
	 METH_VARARGS|METH_KEYWORDS, doc_min},
	{"ptp", (PyCFunction)array_ptp,
	 METH_VARARGS|METH_KEYWORDS, doc_ptp},
	{"mean", (PyCFunction)array_mean,
	 METH_VARARGS|METH_KEYWORDS, doc_mean},
	{"trace", (PyCFunction)array_trace,
	 METH_VARARGS|METH_KEYWORDS, doc_trace},
	{"diagonal", (PyCFunction)array_diagonal,
	 METH_VARARGS|METH_KEYWORDS, doc_diagonal},
	{"clip", (PyCFunction)array_clip,
	 METH_VARARGS|METH_KEYWORDS, doc_clip},
	{"conj", (PyCFunction)array_conjugate,
	 METH_VARARGS, doc_conj},
	{"conjugate", (PyCFunction)array_conjugate,
	 METH_VARARGS, doc_conjugate},
	{"nonzero", (PyCFunction)array_nonzero,
	 METH_VARARGS, doc_nonzero},
	{"std", (PyCFunction)array_stddev,
	 METH_VARARGS|METH_KEYWORDS, doc_stddev},
	{"var", (PyCFunction)array_variance,
	 METH_VARARGS|METH_KEYWORDS, doc_variance},
	{"sum", (PyCFunction)array_sum,
	 METH_VARARGS|METH_KEYWORDS, doc_sum},
	{"cumsum", (PyCFunction)array_cumsum,
	 METH_VARARGS|METH_KEYWORDS, doc_cumsum},
	{"prod", (PyCFunction)array_prod,
	 METH_VARARGS|METH_KEYWORDS, doc_prod},
	{"cumprod", (PyCFunction)array_cumprod,
	 METH_VARARGS|METH_KEYWORDS, doc_cumprod},
	{"all", (PyCFunction)array_all,
	 METH_VARARGS|METH_KEYWORDS, doc_all},
	{"any", (PyCFunction)array_any,
	 METH_VARARGS|METH_KEYWORDS, doc_any},
	{"compress", (PyCFunction)array_compress,
	 METH_VARARGS|METH_KEYWORDS, doc_compress},
	{"flatten", (PyCFunction)array_flatten,
	 METH_VARARGS, doc_flatten},
	{"ravel", (PyCFunction)array_ravel,
	 METH_VARARGS, doc_ravel},
	{"round", (PyCFunction)array_round,
	 METH_VARARGS|METH_KEYWORDS, doc_round},
	{"setflags", (PyCFunction)array_setflags,
	 METH_VARARGS|METH_KEYWORDS, doc_setflags},
	{"newbyteorder", (PyCFunction)array_newbyteorder,
	 METH_VARARGS, doc_newbyteorder},
        {NULL,		NULL}		/* sentinel */
};

#undef _ARET


