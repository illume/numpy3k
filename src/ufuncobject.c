
/*
  Python Universal Functions Object -- Math for all types, plus fast 
  arrays math
  
  Full description
  
  This supports mathematical (and Boolean) functions on arrays and other python
  objects.  Math on large arrays of basic C types is rather efficient.

  Travis E. Oliphant  (2005)
  Assistant Professor
  Brigham Young University

  based on the 

  Original Implementation:  
  Copyright (c) 1995, 1996, 1997 Jim Hugunin, hugunin@mit.edu

  with inspiration and code from
  Numarray
  Space Science Telescope Institute
  J. Todd Miller
  Perry Greenfield
  Rick White
 
*/


typedef double (DoubleBinaryFunc)(double x, double y);
typedef float (FloatBinaryFunc)(float x, float y);
typedef longdouble (LongdoubleBinaryFunc)(longdouble x, longdouble y);

typedef void (CdoubleBinaryFunc)(cdouble *x, cdouble *y, cdouble *res);
typedef void (CfloatBinaryFunc)(cfloat *x, cfloat *y, cfloat *res);
typedef void (ClongdoubleBinaryFunc)(clongdouble *x, clongdouble *y, \
				     clongdouble *res);

/*UFUNC_API*/
static void
PyUFunc_ff_f_As_dd_d(char **args, intp *dimensions, intp *steps, void *func)
{
	register intp i, n=dimensions[0];
	register intp is1=steps[0],is2=steps[1],os=steps[2];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		*(float *)op = (float)((DoubleBinaryFunc *)func) \
			((double)*(float *)ip1, (double)*(float *)ip2);
	}
}

/*UFUNC_API*/
static void 
PyUFunc_ff_f(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, n=dimensions[0];
	register intp is1=steps[0],is2=steps[1],os=steps[2];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		*(float *)op = ((FloatBinaryFunc *)func)(*(float *)ip1, 
							 *(float *)ip2);
	}
} 

/*UFUNC_API*/
static void 
PyUFunc_dd_d(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, n=dimensions[0];
	register intp is1=steps[0],is2=steps[1],os=steps[2];
	char *ip1=args[0], *ip2=args[1], *op=args[2];

	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		*(double *)op = ((DoubleBinaryFunc *)func)\
			(*(double *)ip1, *(double *)ip2);
	}
}

/*UFUNC_API*/
static void 
PyUFunc_gg_g(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, n=dimensions[0];
	register intp is1=steps[0],is2=steps[1],os=steps[2];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		*(longdouble *)op = \
			((LongdoubleBinaryFunc *)func)(*(longdouble *)ip1, 
						       *(longdouble *)ip2);
	}
}


/*UFUNC_API*/
static void 
PyUFunc_FF_F_As_DD_D(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i,n=dimensions[0],is1=steps[0],is2=steps[1],os=steps[2];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	cdouble x, y, r;
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		x.real = ((float *)ip1)[0]; x.imag = ((float *)ip1)[1];
		y.real = ((float *)ip2)[0]; y.imag = ((float *)ip2)[1];
		((CdoubleBinaryFunc *)func)(&x, &y, &r);
		((float *)op)[0] = (float)r.real;
		((float *)op)[1] = (float)r.imag;
	}
}

/*UFUNC_API*/
static void 
PyUFunc_DD_D(char **args, intp *dimensions, intp *steps, void *func)
{
	register intp i, is1=steps[0],is2=steps[1],os=steps[2],n=dimensions[0];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	cdouble x,y,r;
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		x.real = ((double *)ip1)[0]; x.imag = ((double *)ip1)[1];
		y.real = ((double *)ip2)[0]; y.imag = ((double *)ip2)[1];
		((CdoubleBinaryFunc *)func)(&x, &y, &r);
		((double *)op)[0] = r.real;
		((double *)op)[1] = r.imag;
	}
}

/*UFUNC_API*/
static void 
PyUFunc_FF_F(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, is1=steps[0],is2=steps[1],os=steps[2],n=dimensions[0];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	cfloat x,y,r;
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		x.real = ((float *)ip1)[0]; x.imag = ((float *)ip1)[1];
		y.real = ((float *)ip2)[0]; y.imag = ((float *)ip2)[1];
		((CfloatBinaryFunc *)func)(&x, &y, &r);
		((float *)op)[0] = r.real;
		((float *)op)[1] = r.imag;
	}
}

/*UFUNC_API*/
static void 
PyUFunc_GG_G(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, is1=steps[0],is2=steps[1],os=steps[2],n=dimensions[0];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	clongdouble x,y,r;
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		x.real = ((longdouble *)ip1)[0]; 
		x.imag = ((longdouble *)ip1)[1];
		y.real = ((longdouble *)ip2)[0]; 
		y.imag = ((longdouble *)ip2)[1];
		((ClongdoubleBinaryFunc *)func)(&x, &y, &r);
		((longdouble *)op)[0] = r.real;
		((longdouble *)op)[1] = r.imag;
	}
}

/*UFUNC_API*/
static void 
PyUFunc_OO_O(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, is1=steps[0],is2=steps[1],os=steps[2], \
		n=dimensions[0];
	char *ip1=args[0], *ip2=args[1], *op=args[2];
	PyObject *tmp;
	PyObject *x1, *x2;
	
	for(i=0; i<n; i++, ip1+=is1, ip2+=is2, op+=os) {
		x1 = *((PyObject **)ip1);
		x2 = *((PyObject **)ip2);
		if ((x1 == NULL) || (x2 == NULL)) goto done;
		if ( (void *) func == (void *) PyNumber_Power)
			tmp = ((ternaryfunc)func)(x1, x2, Py_None);
		else
			tmp = ((binaryfunc)func)(x1, x2);
		if (PyErr_Occurred()) goto done;
                Py_XDECREF(*((PyObject **)op));
		*((PyObject **)op) = tmp;
	}
 done:
        return;
}


typedef double DoubleUnaryFunc(double x);
typedef float FloatUnaryFunc(float x);
typedef longdouble LongdoubleUnaryFunc(longdouble x);
typedef void CdoubleUnaryFunc(cdouble *x, cdouble *res);
typedef void CfloatUnaryFunc(cfloat *x, cfloat *res);
typedef void ClongdoubleUnaryFunc(clongdouble *x, clongdouble *res);

/*UFUNC_API*/
static void 
PyUFunc_f_f_As_d_d(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i, n=dimensions[0];
	char *ip1=args[0], *op=args[1];
	for(i=0; i<n; i++, ip1+=steps[0], op+=steps[1]) {
		*(float *)op = (float)((DoubleUnaryFunc *)func)((double)*(float *)ip1);
	}
}

/*UFUNC_API*/
static void 
PyUFunc_d_d(char **args, intp *dimensions, intp *steps, void *func) 
{
	intp i;
	char *ip1=args[0], *op=args[1];
	for(i=0; i<*dimensions; i++, ip1+=steps[0], op+=steps[1]) {
		*(double *)op = ((DoubleUnaryFunc *)func)(*(double *)ip1);
	}
}

/*UFUNC_API*/
static void 
PyUFunc_f_f(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i;
	intp n=dimensions[0];
	char *ip1=args[0], *op=args[1];
	for(i=0; i<n; i++, ip1+=steps[0], op+=steps[1]) {
		*(float *)op = ((FloatUnaryFunc *)func)(*(float *)ip1);
	}
}

/*UFUNC_API*/
static void 
PyUFunc_g_g(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i;
	intp n=dimensions[0];
	char *ip1=args[0], *op=args[1];
	for(i=0; i<n; i++, ip1+=steps[0], op+=steps[1]) {
		*(longdouble *)op = ((LongdoubleUnaryFunc *)func)\
                        (*(longdouble *)ip1);
	}
}


/*UFUNC_API*/
static void 
PyUFunc_F_F_As_D_D(char **args, intp *dimensions, intp *steps, void *func) 
{
	register intp i; cdouble x, res;
	intp n=dimensions[0];
	char *ip1=args[0], *op=args[1];
	for(i=0; i<n; i++, ip1+=steps[0], op+=steps[1]) {
		x.real = ((float *)ip1)[0]; x.imag = ((float *)ip1)[1];
		((CdoubleUnaryFunc *)func)(&x, &res);
		((float *)op)[0] = (float)res.real;
		((float *)op)[1] = (float)res.imag;
	}
}

/*UFUNC_API*/
static void 
PyUFunc_F_F(char **args, intp *dimensions, intp *steps, void *func) 
{
	intp i; cfloat x, res;
	char *ip1=args[0], *op=args[1];
	for(i=0; i<*dimensions; i++, ip1+=steps[0], op+=steps[1]) {
		x.real = ((float *)ip1)[0]; 
		x.imag = ((float *)ip1)[1];
		((CfloatUnaryFunc *)func)(&x, &res);
		((float *)op)[0] = res.real;
		((float *)op)[1] = res.imag;
	}
}


/*UFUNC_API*/
static void 
PyUFunc_D_D(char **args, intp *dimensions, intp *steps, void *func) 
{
	intp i; cdouble x, res;
	char *ip1=args[0], *op=args[1];
	for(i=0; i<*dimensions; i++, ip1+=steps[0], op+=steps[1]) {
		x.real = ((double *)ip1)[0]; 
		x.imag = ((double *)ip1)[1];
		((CdoubleUnaryFunc *)func)(&x, &res);
		((double *)op)[0] = res.real;
		((double *)op)[1] = res.imag;
	}
}


/*UFUNC_API*/
static void 
PyUFunc_G_G(char **args, intp *dimensions, intp *steps, void *func) 
{
	intp i; clongdouble x, res;
	char *ip1=args[0], *op=args[1];
	for(i=0; i<*dimensions; i++, ip1+=steps[0], op+=steps[1]) {
		x.real = ((longdouble *)ip1)[0]; 
		x.imag = ((longdouble *)ip1)[1];
		((ClongdoubleUnaryFunc *)func)(&x, &res);
		((double *)op)[0] = res.real;
		((double *)op)[1] = res.imag;
	}
}

/*UFUNC_API*/
static void 
PyUFunc_O_O(char **args, intp *dimensions, intp *steps, void *func) 
{
	intp i; PyObject *tmp, *x1;
	char *ip1=args[0], *op=args[1];

	for(i=0; i<*dimensions; i++, ip1+=steps[0], op+=steps[1]) {
		x1 = *(PyObject **)ip1;
		if (x1 == NULL) goto done;
		tmp = ((unaryfunc)func)(x1);
		if ((tmp==NULL) || PyErr_Occurred()) goto done;
                Py_XDECREF(*((PyObject **)op));
		*((PyObject **)op) = tmp;
	}
 done:
        return;
}

/*UFUNC_API*/
static void 
PyUFunc_O_O_method(char **args, intp *dimensions, intp *steps, void *func) 
{
	intp i; PyObject *tmp, *meth, *arglist, *x1;
	char *ip1=args[0], *op=args[1];

	for(i=0; i<*dimensions; i++, ip1+=steps[0], op+=steps[1]) {
		x1 = *(PyObject **)ip1;
		if (x1 == NULL) goto done;
		meth = PyObject_GetAttrString(x1, (char *)func);
		if (meth != NULL) {
			arglist = PyTuple_New(0);
			tmp = PyEval_CallObject(meth, arglist);
			Py_DECREF(arglist);
			Py_DECREF(meth);
                        if ((tmp==NULL) || PyErr_Occurred()) goto done;
                        Py_XDECREF(*((PyObject **)op));
			*((PyObject **)op) = tmp;
		}
	}
 done:
        return;

}



/* a general-purpose ufunc that deals with general-purpose Python callable.
   func is a structure with nin, nout, and a Python callable function
*/

/*UFUNC_API*/
static void
PyUFunc_On_Om(char **args, intp *dimensions, intp *steps, void *func)
{
	intp i, j;
	intp n=dimensions[0];
        PyUFunc_PyFuncData *data = (PyUFunc_PyFuncData *)func;
        int nin = data->nin, nout=data->nout;
        int ntot;
        PyObject *tocall = data->callable;        
        char *ptrs[MAX_ARGS];
        PyObject *arglist, *result;
        PyObject *in, **op;

        ntot = nin+nout;

        for (j=0; j < ntot; j++) ptrs[j] = args[j];
	for(i=0; i<n; i++) {
		arglist = PyTuple_New(nin);
		if (arglist == NULL) return;
                for (j=0; j < nin; j++) {
                        in = *((PyObject **)ptrs[j]);
                        if (in == NULL) {Py_DECREF(arglist); return;}
                        PyTuple_SET_ITEM(arglist, j, in);
                        Py_INCREF(in);
                }                
                result = PyEval_CallObject(tocall, arglist);
		Py_DECREF(arglist);
                if (result == NULL) return;
                if PyTuple_Check(result) {
                        if (nout != PyTuple_Size(result)) {
                                Py_DECREF(result);
				return;
			}
                        for (j=0; j < nout; j++) {
                                op = (PyObject **)ptrs[j+nin];
				Py_XDECREF(*op);
                                *op = PyTuple_GET_ITEM(result, j);
                                Py_INCREF(*op);
                        }
                        Py_DECREF(result);
                }
                else {
                        op = (PyObject **)ptrs[nin];
			Py_XDECREF(*op);
                        *op = result;
		}
                for (j=0; j < ntot; j++) ptrs[j] += steps[j];
	}
	return;
}




/* ---------------------------------------------------------------- */


/* fpstatus is the ufunc_formatted hardware status 
   errmask is the handling mask specified by the user.
   errobj is a Python object with (string, callable object or None)
   or NULL
*/

/*
  2. for each of the flags 
     determine whether to ignore, warn, raise error, or call Python function.
     If ignore, do nothing
     If warn, print a warning and continue
     If raise return an error
     If call, call a user-defined function with string
*/	   

static int
_error_handler(int method, PyObject *errobj, char *errtype, int retstatus)
{
	PyObject *pyfunc, *ret, *args;
	char *name=PyString_AS_STRING(PyTuple_GET_ITEM(errobj,0));
	char msg[100];

	ALLOW_C_API_DEF

	ALLOW_C_API

	switch(method) {
	case UFUNC_ERR_WARN:
		snprintf(msg, 100, "%s encountered in %s", errtype, name);
		if (PyErr_Warn(PyExc_RuntimeWarning, msg) < 0) goto fail;
		break;
	case UFUNC_ERR_RAISE:
		PyErr_Format(PyExc_FloatingPointError, 
			     "%s encountered in %s",
			     errtype, name);
		goto fail;
	case UFUNC_ERR_CALL:
		pyfunc = PyTuple_GET_ITEM(errobj, 1);

		if (pyfunc == Py_None) {
			PyErr_Format(PyExc_NameError, 
				     "python callback specified for %s (in " \
				     " %s) but no function found.", 
				     errtype, name);
			goto fail;
		}
		args = Py_BuildValue("NN", PyString_FromString(errtype), 
                                     PyInt_FromLong((long) retstatus));
		if (args == NULL) goto fail;
		ret = PyObject_CallObject(pyfunc, args);
		Py_DECREF(args);
		if (ret == NULL) goto fail;
		Py_DECREF(ret);

		break;
	}
	DISABLE_C_API
	return 0;

 fail:	
	DISABLE_C_API
	return -1;	
}


/*UFUNC_API*/
static int
PyUFunc_checkfperr(int errmask, PyObject *errobj)
{
	int retstatus;
	int handle;

	/* 1. check hardware flag --- this is platform dependent code */

	UFUNC_CHECK_STATUS(retstatus)  /* no semicolon */
	
	/* End platform dependent code */

#define HANDLEIT(NAME, str) {if (retstatus & UFUNC_FPE_##NAME) { \
			handle = errmask & UFUNC_MASK_##NAME;\
			if (handle && \
			    _error_handler(handle >> UFUNC_SHIFT_##NAME, \
					   errobj, str, retstatus) < 0)  \
				return -1;		      \
			}}

	if (errmask && retstatus) {
		HANDLEIT(DIVIDEBYZERO, "divide by zero");
		HANDLEIT(OVERFLOW, "overflow");
		HANDLEIT(UNDERFLOW, "underflow");
		HANDLEIT(INVALID, "invalid");
	}

#undef HANDLEIT

	return 0;
}


/* Checking the status flag clears it */
/*UFUNC_API*/
static void
PyUFunc_clearfperr()
{
	int retstatus;

	UFUNC_CHECK_STATUS(retstatus)
}


#define UFUNC_NOSCALAR         0
#define UFUNC_BOOL_SCALAR      1
#define UFUNC_INTPOS_SCALAR    2
#define UFUNC_INTNEG_SCALAR    3
#define UFUNC_FLOAT_SCALAR     4
#define UFUNC_COMPLEX_SCALAR   5
#define UFUNC_OBJECT_SCALAR    6

#define NO_UFUNCLOOP        0
#define ZERODIM_REDUCELOOP  0
#define ONE_UFUNCLOOP       1
#define ONEDIM_REDUCELOOP   1
#define NOBUFFER_UFUNCLOOP  2
#define NOBUFFER_REDUCELOOP 2
#define BUFFER_UFUNCLOOP  3
#define BUFFER_REDUCELOOP 3


static char
_lowest_type(char intype)
{
        switch(intype) {
	/* case PyArray_BYTE */
	case PyArray_SHORT:
        case PyArray_INT:
        case PyArray_LONG:
	case PyArray_LONGLONG:
		return PyArray_BYTE;
	/* case PyArray_UBYTE */
        case PyArray_USHORT:
        case PyArray_UINT:
	case PyArray_ULONG:
	case PyArray_ULONGLONG:
		return PyArray_UBYTE;
	/* case PyArray_FLOAT:*/
        case PyArray_DOUBLE:
	case PyArray_LONGDOUBLE:
		return PyArray_FLOAT;
	/* case PyArray_CFLOAT:*/
        case PyArray_CDOUBLE:
	case PyArray_CLONGDOUBLE:
		return PyArray_CFLOAT;
        default:
                return intype;
        }
}

/* Called to determine coercion
 */

static int 
_cancoerce(char thistype, char neededtype, char scalar) 
{

	switch(scalar) {
	case UFUNC_NOSCALAR:
	case UFUNC_BOOL_SCALAR:
	case UFUNC_OBJECT_SCALAR:
		return PyArray_CanCastSafely(thistype, neededtype);
	case UFUNC_INTPOS_SCALAR:
		return (neededtype >= PyArray_UBYTE);
	case UFUNC_INTNEG_SCALAR:
		return (neededtype >= PyArray_BYTE) &&		\
			!(PyTypeNum_ISUNSIGNED(neededtype));
	case UFUNC_FLOAT_SCALAR:
		return (neededtype >= PyArray_FLOAT);
	case UFUNC_COMPLEX_SCALAR:
		return (neededtype >= PyArray_CFLOAT);
	}
	fprintf(stderr, "\n**Error** coerce fall through: %d %d %d\n\n", 
		thistype, neededtype, scalar);
	return 1; /* should never get here... */   
}


static int 
select_types(PyUFuncObject *self, int *arg_types, 
             PyUFuncGenericFunction *function, void **data,
	     char *scalars)
{

	int i=0, j;
	char start_type;
	
	if (PyTypeNum_ISUSERDEF((arg_types[0]))) {
		PyObject *key, *obj;
		for (i=0; i<self->nin; i++) {
			if (arg_types[i] != arg_types[0]) {
				PyErr_SetString(PyExc_TypeError,
						"ufuncs on user defined" \
						" types don't support "\
						"coercion");
				return -1;
			}
		}
		for (i=self->nin; i<self->nargs; i++) {
			arg_types[i] = arg_types[0];
		}

		obj = NULL;
		if (self->userloops) {
			key = PyInt_FromLong((long) arg_types[0]);
			if (key == NULL) return -1;
			obj = PyDict_GetItem(self->userloops, key);
			Py_DECREF(key);
		}
		if (obj == NULL) {
			PyErr_SetString(PyExc_TypeError, 
					"no registered loop for this "	\
					"user-defined type");
			return -1;			
		}
		if PyTuple_Check(obj) {
			*function = (PyUFuncGenericFunction) \
				PyCObject_AsVoidPtr(PyTuple_GET_ITEM(obj, 0));
			*data = PyCObject_AsVoidPtr(PyTuple_GET_ITEM(obj, 1));
		}
		else {
			*function = (PyUFuncGenericFunction)	\
				PyCObject_AsVoidPtr(obj);
			*data = NULL;
		}
                Py_DECREF(obj);
		return 0;
	}
	

	start_type = arg_types[0];
	/* If the first argument is a scalar we need to place 
	   the start type as the lowest type in the class
	*/
	if (scalars[0] != UFUNC_NOSCALAR) {
		start_type = _lowest_type(start_type);
	}

	while (i<self->ntypes && start_type > self->types[i*self->nargs]) 
		i++;

	for(;i<self->ntypes; i++) {
		for(j=0; j<self->nin; j++) {
			if (!_cancoerce(arg_types[j], 
					self->types[i*self->nargs+j],
					scalars[j]))
				break;
		}
		if (j == self->nin) break;
	}
	if(i>=self->ntypes) {
		PyErr_SetString(PyExc_TypeError, 
				"function not supported for these types, "\
				"and can't coerce safely to supported types");
		return -1;
	}
	for(j=0; j<self->nargs; j++) 
		arg_types[j] = self->types[i*self->nargs+j];

        if (self->data)
                *data = self->data[i];
        else 
                *data = NULL;
	*function = self->functions[i];

	return 0;
}

static int PyUFunc_USEDEFAULTS=0;

/*UFUNC_API*/
static int
PyUFunc_GetPyValues(char *name, int *bufsize, int *errmask, PyObject **errobj)
{
        PyObject *thedict;
        PyObject *ref=NULL;
	PyObject *retval;
	static PyObject *thestring=NULL;

	if (!PyUFunc_USEDEFAULTS) {
		if (thestring == NULL) {
			thestring = PyString_InternFromString(UFUNC_PYVALS_NAME);
		}
		thedict = PyEval_GetLocals();
		ref = PyDict_GetItem(thedict, thestring);
		if (ref == NULL) {
			thedict = PyEval_GetGlobals();
			ref = PyDict_GetItem(thedict, thestring);
		}
		if (ref == NULL) {
			thedict = PyEval_GetBuiltins();
			ref = PyDict_GetItem(thedict, thestring);
		}
	}
	if (ref == NULL) {
		*errmask = UFUNC_ERR_DEFAULT;
		*errobj = Py_BuildValue("NO",
					PyString_FromString(name),
					Py_None);
		*bufsize = PyArray_BUFSIZE;
		return 0;
	}
	*errobj = NULL;
	if (!PyList_Check(ref) || (PyList_GET_SIZE(ref)!=3)) {
		PyErr_Format(PyExc_TypeError, "%s must be a length 3 list.",
			     UFUNC_PYVALS_NAME);
		return -1;
	}

	*bufsize = PyInt_AsLong(PyList_GET_ITEM(ref, 0));
	if ((*bufsize == -1) && PyErr_Occurred()) return -1;
	if ((*bufsize < PyArray_MIN_BUFSIZE) ||	\
	    (*bufsize > PyArray_MAX_BUFSIZE) || \
	    (*bufsize % 16 != 0)) {
		PyErr_Format(PyExc_ValueError,  
			     "buffer size (%d) is not "	\
			     "in range (%d - %d) or not a multiple of 16", 
			     *bufsize, PyArray_MIN_BUFSIZE, 
			     PyArray_MAX_BUFSIZE);
		return -1;
	}

	*errmask = PyInt_AsLong(PyList_GET_ITEM(ref, 1));
	if (*errmask < 0) {
		if (PyErr_Occurred()) return -1;
		PyErr_Format(PyExc_ValueError,		\
			     "invalid error mask (%d)", 
			     *errmask);
		return -1;
	}
	
	retval = PyList_GET_ITEM(ref, 2);
	if (retval != Py_None && !PyCallable_Check(retval)) {
		PyErr_SetString(PyExc_TypeError, 
				"callback function must be callable");
		return -1;
	}

	*errobj = Py_BuildValue("NO", 
				PyString_FromString(name),
				retval);
	if (*errobj == NULL) return -1;
	
	return 0;
}


static char
_scalar_kind(int typenum, PyArrayObject **arr) 
{
	if (PyTypeNum_ISSIGNED(typenum)) return UFUNC_INTNEG_SCALAR;
	if (PyTypeNum_ISFLOAT(typenum)) return UFUNC_FLOAT_SCALAR;
	if (PyTypeNum_ISCOMPLEX(typenum)) return UFUNC_COMPLEX_SCALAR;
	if (PyTypeNum_ISUNSIGNED(typenum)) return UFUNC_INTPOS_SCALAR;
	if (PyTypeNum_ISBOOL(typenum)) return UFUNC_BOOL_SCALAR;
	return UFUNC_OBJECT_SCALAR;
}


/* Create copies for any arrays that are less than loop->bufsize
   in total size and are mis-behaved or in need
   of casting.
*/

static int
_create_copies(PyUFuncLoopObject *loop, int *arg_types, PyArrayObject **mps)
{
	int nin = loop->ufunc->nin;
	int i;
	intp size;
	PyObject *new;
	PyArray_Descr *ntype; 
	PyArray_Descr *atype;

	for (i=0; i<nin; i++) {
		size = PyArray_SIZE(mps[i]);
		/* if the type of mps[i] is equivalent to arg_types[i] */
		/* then set arg_types[i] equal to type of
		   mps[i] for later checking....
		*/
		if (PyArray_TYPE(mps[i]) != arg_types[i]) {
			ntype = mps[i]->descr;
			atype = PyArray_DescrFromType(arg_types[i]);
			if (PyArray_EquivTypes(atype, ntype)) {
				arg_types[i] = ntype->type_num;
			}
			Py_DECREF(atype);
		}
		if (size < loop->bufsize) {
			if (!(PyArray_ISBEHAVED_RO(mps[i])) ||		\
			    PyArray_TYPE(mps[i]) != arg_types[i]) {
				ntype = PyArray_DescrFromType(arg_types[i]);
				new = PyArray_FromAny((PyObject *)mps[i], 
						      ntype, 0, 0,
						      FORCECAST | ALIGNED);
				if (new == NULL) return -1;
				Py_DECREF(mps[i]);
				mps[i] = (PyArrayObject *)new;
			}
		}
	}
	
	return 0;
}

#define _GETATTR_(str, rstr) if (strcmp(name, #str) == 0) { \
                return PyObject_HasAttrString(op, "__" #rstr "__");}

static int
_has_reflected_op(PyObject *op, char *name)
{
        _GETATTR_(add, radd)
        _GETATTR_(subtract, rsub)
        _GETATTR_(multiply, rmul)
        _GETATTR_(divide, rdiv)
        _GETATTR_(true_divide, rtruediv)
        _GETATTR_(floor_divide, rfloordiv)
        _GETATTR_(remainder, rmod)
        _GETATTR_(power, rpow)
        _GETATTR_(left_shift, rrlshift)
        _GETATTR_(right_shift, rrshift)
        _GETATTR_(bitwise_and, rand)
        _GETATTR_(bitwise_xor, rxor)
        _GETATTR_(bitwise_or, ror)
        return 0;
}

#undef _GETATTR_


static int
construct_matrices(PyUFuncLoopObject *loop, PyObject *args, PyArrayObject **mps)
{
        int nargs, i, maxsize;
        int arg_types[MAX_ARGS];
	char scalars[MAX_ARGS];
	PyUFuncObject *self=loop->ufunc;
	Bool allscalars=TRUE;
	PyTypeObject *subtype=&PyArray_Type;

        /* Check number of arguments */
        nargs = PyTuple_Size(args);
        if ((nargs != self->nin) && (nargs != self->nargs)) {
                PyErr_SetString(PyExc_ValueError, 
				"invalid number of arguments");
                return -1;
        }


        /* Get each input argument */
        for (i=0; i<self->nin; i++) {
                mps[i] = (PyArrayObject *)\
			PyArray_FromAny(PyTuple_GET_ITEM(args,i), 
					NULL, 0, 0, 0);
                if (mps[i] == NULL) return -1;
                arg_types[i] = PyArray_TYPE(mps[i]);
                if (PyTypeNum_ISFLEXIBLE(arg_types[i])) {
			loop->notimplemented = 1;
			return nargs;
                }
		/*
		fprintf(stderr, "array %d has reference %d\n", i, 
		                (mps[i])->ob_refcnt);
		*/

		/* Scalars are 0-dimensional arrays
		   at this point
		*/
		if (mps[i]->nd > 0) {
			scalars[i] = UFUNC_NOSCALAR;
			allscalars=FALSE;
		}
		else scalars[i] = _scalar_kind(arg_types[i], &(mps[i]));

		/* If any input is a big-array */
		if (!PyType_IsSubtype(mps[i]->ob_type, &PyArray_Type)) {
			subtype = &PyBigArray_Type;
		}
        }

	/* If everything is a scalar, then use normal coercion rules */
	if (allscalars) {
		for (i=0; i<self->nin; i++) {
			scalars[i] = UFUNC_NOSCALAR;
		}
	}
       
        /* Select an appropriate function for these argument types. */
        if (select_types(loop->ufunc, arg_types, &(loop->function), 
                         &(loop->funcdata), scalars) == -1)
		return -1;

        /* FAIL with NotImplemented if the other object has 
	   the __r<op>__ method and has __array_priority__ as 
	   an attribute (signalling it can handle ndarray's) 
	   and is not already an ndarray or bigndarray
	*/
        if ((arg_types[1] == PyArray_OBJECT) &&				\
            (loop->ufunc->nin==2) && (loop->ufunc->nout == 1)) {
		PyObject *_obj = PyTuple_GET_ITEM(args, 1);
                if (!PyArray_CheckExact(_obj) &&			\
		    !PyBigArray_CheckExact(_obj) &&			\
		    PyObject_HasAttrString(_obj, "__array_priority__") && \
		    _has_reflected_op(_obj, loop->ufunc->name)) {
                        loop->notimplemented = 1;
                        return nargs;
                }
        }
        loop->notimplemented=0;
        
	/* Create copies for some of the arrays if appropriate */
	if (_create_copies(loop, arg_types, mps) < 0) return -1;
	
	/* Create Iterators for the Inputs */
	for (i=0; i<self->nin; i++) {
                loop->iters[i] = (PyArrayIterObject *)		\
			PyArray_IterNew((PyObject *)mps[i]);
                if (loop->iters[i] == NULL) return -1;
	}
        
        /* Broadcast the result */
        loop->numiter = self->nin;
        if (PyArray_Broadcast((PyArrayMultiIterObject *)loop) < 0)
		return -1;
	
        /* Get any return arguments */
        for (i=self->nin; i<nargs; i++) {
                mps[i] = (PyArrayObject *)PyTuple_GET_ITEM(args, i);
                if (((PyObject *)mps[i])==Py_None) {
                        mps[i] = NULL;
                        continue;
                }
                Py_INCREF(mps[i]);
                if (!PyArray_Check((PyObject *)mps[i])) {
			PyObject *new;
			if (PyArrayIter_Check(mps[i])) {
				new = PyObject_CallMethod((PyObject *)mps[i],
							  "__array__", NULL);
				Py_DECREF(mps[i]);
				mps[i] = (PyArrayObject *)new;
			}
			else {
				PyErr_SetString(PyExc_TypeError, 
						"return arrays must be "\
						"of ArrayType");
				Py_DECREF(mps[i]);
                                mps[i] = NULL;
				return -1;
			}
                }
                if (!PyArray_CompareLists(mps[i]->dimensions, 
					  loop->dimensions, loop->nd)) {
                        PyErr_SetString(PyExc_ValueError, 
                                        "invalid return array shape");
			Py_DECREF(mps[i]);
                        mps[i] = NULL;
                        return -1;
                }
                if (!PyArray_ISWRITEABLE(mps[i])) {
                        PyErr_SetString(PyExc_ValueError, 
                                        "return array is not writeable");
			Py_DECREF(mps[i]);
                        mps[i] = NULL;
                        return -1;
                }
        }

        /* construct any missing return arrays and make output iterators */
        
        for (i=self->nin; i<self->nargs; i++) {
		PyArray_Descr *ntype;

                if (mps[i] == NULL) {
                        mps[i] = (PyArrayObject *)PyArray_New(subtype,
                                                              loop->nd, 
                                                              loop->dimensions,
                                                              arg_types[i], 
                                                              NULL, NULL,
                                                              0, 0, NULL);
                        if (mps[i] == NULL) return -1;
                }

		/* reset types for outputs that are equivalent 
		    -- no sense casting uselessly
		*/
		else {
  		  if (mps[i]->descr->type_num != arg_types[i]) {
			  PyArray_Descr *atype;
			  ntype = mps[i]->descr;
			  atype = PyArray_DescrFromType(arg_types[i]);
			  if (PyArray_EquivTypes(atype, ntype)) {
				  arg_types[i] = ntype->type_num;
			  }
			  Py_DECREF(atype);
		  }
		  
		/* still not the same -- or will we have to use buffers?*/
		  if (mps[i]->descr->type_num != arg_types[i] ||
		      !PyArray_ISBEHAVED_RO(mps[i])) {
			  if (loop->size < loop->bufsize) {
				  PyObject *new;
				  /* Copy the array to a temporary copy 
				     and set the UPDATEIFCOPY flag
				  */
				  ntype = PyArray_DescrFromType(arg_types[i]);
				  new = PyArray_FromAny((PyObject *)mps[i],
							ntype, 0, 0,
							FORCECAST | ALIGNED |
							UPDATEIFCOPY);
				  if (new == NULL) return -1;
				  Py_DECREF(mps[i]);
				  mps[i] = (PyArrayObject *)new;
			  }
		  }
		}
		
                loop->iters[i] = (PyArrayIterObject *)		\
			PyArray_IterNew((PyObject *)mps[i]);
                if (loop->iters[i] == NULL) return -1;
        }


        /*  If any of different type, or misaligned or swapped
            then must use buffers */

        loop->bufcnt = 0;

        loop->obj = 0;

        /* Determine looping method needed */
        loop->meth = NO_UFUNCLOOP;

	maxsize = 0;
        for (i=0; i<self->nargs; i++) {
		loop->needbuffer[i] = 0;
                if (arg_types[i] != mps[i]->descr->type_num || 
		    !PyArray_ISBEHAVED_RO(mps[i])) {
                        loop->meth = BUFFER_UFUNCLOOP;
			loop->needbuffer[i] = 1;
                }
                if (!loop->obj && mps[i]->descr->type_num == PyArray_OBJECT) {
			loop->obj = 1;
		}
        }
        
        if (loop->meth == NO_UFUNCLOOP) {
                
                loop->meth = ONE_UFUNCLOOP;

                /* All correct type and BEHAVED */
                /* Check for non-uniform stridedness */

                for (i=0; i<self->nargs; i++) {
                        if (!(loop->iters[i]->contiguous)) {
				/* may still have uniform stride
				   if (broadcated result) <= 1-d */
				if (mps[i]->nd != 0 &&			\
				    (loop->iters[i]->nd_m1 > 0)) {
					loop->meth = NOBUFFER_UFUNCLOOP;
					break;
				}
			}
                }
		if (loop->meth == ONE_UFUNCLOOP) {
			for (i=0; i<self->nargs; i++) {
				loop->bufptr[i] = mps[i]->data;
			}
		}
        }

        loop->numiter = self->nargs;

        /* Fill in steps */
        if (loop->meth != ONE_UFUNCLOOP) {
		int ldim = 0;
		intp maxdim=-1;
		PyArrayIterObject *it;

                /* Fix iterators */

                /* Find the **largest** dimension */
                
		maxdim = -1;
		for (i=loop->nd - 1; i>=0; i--) {
			if (loop->dimensions[i] > maxdim) {
				ldim = i;
				maxdim = loop->dimensions[i];
			}
		}

		loop->size /= maxdim;
                loop->bufcnt = maxdim;
		loop->lastdim = ldim;

                /* Fix the iterators so the inner loop occurs over the 
		   largest dimensions -- This can be done by 
		   setting the size to 1 in that dimension 
		   (just in the iterators)
                 */

		for (i=0; i<loop->numiter; i++) {
			it = loop->iters[i];
                        it->contiguous = 0;
			it->size /= (it->dims_m1[ldim]+1);
			it->dims_m1[ldim] = 0;
			it->backstrides[ldim] = 0;

			/* (won't fix factors because we
			   don't use PyArray_ITER_GOTO1D 
			   so don't change them) */

			/* Set the steps to the strides in that dimension */
                        loop->steps[i] = it->strides[ldim];
		}

		/* fix up steps where we will be copying data to 
		   buffers and calculate the ninnerloops and leftover
		   values -- if step size is already zero that is not changed... 
		*/
		if (loop->meth == BUFFER_UFUNCLOOP) {
			loop->leftover = maxdim % loop->bufsize;
			loop->ninnerloops = (maxdim / loop->bufsize) + 1;
			for (i=0; i<self->nargs; i++) {
				if (loop->needbuffer[i] && loop->steps[i]) {
					loop->steps[i] = mps[i]->descr->elsize;
				}
				/* These are changed later if casting is needed */
			}
		}
        }
        else { /* uniformly-strided case ONE_UFUNCLOOP */
		for (i=0; i<self->nargs; i++) {
			if (PyArray_SIZE(mps[i]) == 1)
				loop->steps[i] = 0;
			else
				loop->steps[i] = mps[i]->strides[mps[i]->nd-1];
		}
	}
        

	/* Finally, create memory for buffers if we need them */
	
	/* buffers for scalars are specially made small -- scalars are
	   not copied multiple times */
	if (loop->meth == BUFFER_UFUNCLOOP) {
		int cnt = 0, cntcast = 0; /* keeps track of bytes to allocate */
		int scnt = 0, scntcast = 0;
		char *castptr;
		char *bufptr;
		int last_was_scalar=0;
		int last_cast_was_scalar=0;
		int oldbufsize=0;
		int oldsize=0;
		int scbufsize = 4*sizeof(double);
		int memsize;
                PyArray_Descr *descr;

		/* compute the element size */
		for (i=0; i<self->nargs;i++) {
			if (!loop->needbuffer) continue;
			if (arg_types[i] != mps[i]->descr->type_num) {
				descr = PyArray_DescrFromType(arg_types[i]);
				if (loop->steps[i])
					cntcast += descr->elsize;
				else
					scntcast += descr->elsize;
				if (i < self->nin) {
					loop->cast[i] =			\
						mps[i]->descr->f->cast[arg_types[i]];
				}
				else {
					loop->cast[i] = descr->f->	\
						cast[mps[i]->descr->type_num];
				}
				Py_DECREF(descr);
			}
			loop->swap[i] = !(PyArray_ISNOTSWAPPED(mps[i]));
			if (loop->steps[i])
				cnt += mps[i]->descr->elsize;
			else
				scnt += mps[i]->descr->elsize;
		}
		memsize = loop->bufsize*(cnt+cntcast) + scbufsize*(scnt+scntcast);
 		loop->buffer[0] = PyDataMem_NEW(memsize);

		/* fprintf(stderr, "Allocated buffer at %p of size %d, cnt=%d, cntcast=%d\n", loop->buffer[0], loop->bufsize * (cnt + cntcast), cnt, cntcast); */

		if (loop->buffer[0] == NULL) {PyErr_NoMemory(); return -1;}
		castptr = loop->buffer[0] + loop->bufsize*cnt + scbufsize*scnt;
		bufptr = loop->buffer[0];
		for (i=0; i<self->nargs; i++) {
			if (!loop->needbuffer[i]) continue;
			loop->buffer[i] = bufptr + (last_was_scalar ? scbufsize : \
						    loop->bufsize)*oldbufsize;
			last_was_scalar = (loop->steps[i] == 0);
			bufptr = loop->buffer[i];
			oldbufsize = mps[i]->descr->elsize;
			/* fprintf(stderr, "buffer[%d] = %p\n", i, loop->buffer[i]); */
			if (loop->cast[i]) {
				PyArray_Descr *descr;
				loop->castbuf[i] = castptr + (last_cast_was_scalar ? scbufsize : \
							      loop->bufsize)*oldsize;
				last_cast_was_scalar = last_was_scalar;
				/* fprintf(stderr, "castbuf[%d] = %p\n", i, loop->castbuf[i]); */
				descr = PyArray_DescrFromType(arg_types[i]);
				oldsize = descr->elsize;
				Py_DECREF(descr);
				loop->bufptr[i] = loop->castbuf[i];
				castptr = loop->castbuf[i];
				if (loop->steps[i])
					loop->steps[i] = oldsize;
			}
			else {
				loop->bufptr[i] = loop->buffer[i];
			}
		}
	}
        return nargs;
}

static void
ufuncreduce_dealloc(PyUFuncReduceObject *self)
{
        if (self->ufunc) {
                Py_XDECREF(self->it);
		Py_XDECREF(self->rit);
                Py_XDECREF(self->ret);
		Py_XDECREF(self->errobj);
		Py_XDECREF(self->decref);
                if (self->buffer) PyDataMem_FREE(self->buffer);
                Py_DECREF(self->ufunc);
        }
        _pya_free(self);
}

static void
ufuncloop_dealloc(PyUFuncLoopObject *self)
{
	int i;
	
	if (self->ufunc != NULL) {
		for (i=0; i<self->ufunc->nargs; i++)
			Py_XDECREF(self->iters[i]);
		if (self->buffer[0]) PyDataMem_FREE(self->buffer[0]);
		Py_XDECREF(self->errobj);
		Py_DECREF(self->ufunc);
	}
        _pya_free(self);
}

static PyUFuncLoopObject *
construct_loop(PyUFuncObject *self, PyObject *args, PyArrayObject **mps)
{
	PyUFuncLoopObject *loop;
	int i;
	
	if (self == NULL) {
		PyErr_SetString(PyExc_ValueError, "function not supported");
		return NULL;
	}
        if ((loop = _pya_malloc(sizeof(PyUFuncLoopObject)))==NULL) {
                PyErr_NoMemory(); return loop;
        }
	
	loop->index = 0;
	loop->ufunc = self;
        Py_INCREF(self);
	loop->buffer[0] = NULL;
        for (i=0; i<self->nargs; i++) {
                loop->iters[i] = NULL;
                loop->cast[i] = NULL;
        }
	loop->errobj = NULL;

	if (PyUFunc_GetPyValues((self->name ? self->name : ""),
				&(loop->bufsize), &(loop->errormask), 
				&(loop->errobj)) < 0) goto fail;
        
	/* Setup the matrices */
	if (construct_matrices(loop, args, mps) < 0) goto fail;

	PyUFunc_clearfperr();

	return loop;

 fail:
        ufuncloop_dealloc(loop);
	return NULL;
}


/* 
static void
_printbytebuf(PyUFuncLoopObject *loop, int bufnum) 
{        
	int i;
	
 	fprintf(stderr, "Printing byte buffer %d\n", bufnum);
        for (i=0; i<loop->bufcnt; i++) {
	 	fprintf(stderr, "  %d\n", *(((byte *)(loop->buffer[bufnum]))+i));
	} 
}

static void
_printlongbuf(PyUFuncLoopObject *loop, int bufnum) 
{        
	int i;
	
 	fprintf(stderr, "Printing long buffer %d\n", bufnum);
        for (i=0; i<loop->bufcnt; i++) {
	 	fprintf(stderr, "  %ld\n", *(((long *)(loop->buffer[bufnum]))+i));
	} 
}

static void
_printlongbufptr(PyUFuncLoopObject *loop, int bufnum) 
{        
	int i;
	
 	fprintf(stderr, "Printing long buffer %d\n", bufnum);
        for (i=0; i<loop->bufcnt; i++) {
	 	fprintf(stderr, "  %ld\n", *(((long *)(loop->bufptr[bufnum]))+i));
	} 
}


 
static void
_printcastbuf(PyUFuncLoopObject *loop, int bufnum) 
{        
	int i;
	
 	fprintf(stderr, "Printing long buffer %d\n", bufnum);
        for (i=0; i<loop->bufcnt; i++) {
	 	fprintf(stderr, "  %ld\n", *(((long *)(loop->castbuf[bufnum]))+i));
	} 
}

*/




/* currently generic ufuncs cannot be built for use on flexible arrays.

   The cast functions in the generic loop would need to be fixed to pass 
   in something besides NULL, NULL.

   Also the underlying ufunc loops would not know the element-size unless
   that was passed in as data (which could be arranged).

*/

/* This generic function is called with the ufunc object, the arguments to it,
   and an array of (pointers to) PyArrayObjects which are NULL.  The 
   arguments are parsed and placed in mps in construct_loop (construct_matrices)
*/

/*UFUNC_API*/
static int 
PyUFunc_GenericFunction(PyUFuncObject *self, PyObject *args, 
			PyArrayObject **mps) 
{
	PyUFuncLoopObject *loop;
	int i;
        BEGIN_THREADS_DEF

	if (!(loop = construct_loop(self, args, mps))) return -1;
        if (loop->notimplemented) {ufuncloop_dealloc(loop); return -2;}

	LOOP_BEGIN_THREADS

	switch(loop->meth) {
	case ONE_UFUNCLOOP:
		/* Everything is contiguous, notswapped, aligned,
		   and of the right type.  -- Fastest.
		   Or if not contiguous, then a single-stride
		   increment moves through the entire array. 
		*/
                /*fprintf(stderr, "ONE...%d\n", loop->size);*/
		loop->function((char **)loop->bufptr, &(loop->size), 
			       loop->steps, loop->funcdata);
		UFUNC_CHECK_ERROR(loop);
		break;
	case NOBUFFER_UFUNCLOOP:
		/* Everything is notswapped, aligned and of the 
		   right type but not contiguous. -- Almost as fast.
		*/
                /*fprintf(stderr, "NOBUFFER...%d\n", loop->size);*/
		while (loop->index < loop->size) {
			for (i=0; i<self->nargs; i++) 
				loop->bufptr[i] = loop->iters[i]->dataptr;

			loop->function((char **)loop->bufptr, &(loop->bufcnt),
				       loop->steps, loop->funcdata);
			UFUNC_CHECK_ERROR(loop);

			for (i=0; i<self->nargs; i++) {
				PyArray_ITER_NEXT(loop->iters[i]);
			}
			loop->index++;
		}
		break;
	case BUFFER_UFUNCLOOP: {
		PyArray_CopySwapNFunc *copyswapn[MAX_ARGS];
		PyArrayIterObject **iters=loop->iters;
		int *swap=loop->swap;
		void **dptr=loop->dptr;
		int mpselsize[MAX_ARGS];
		intp laststrides[MAX_ARGS];
		int fastmemcpy[MAX_ARGS];
		int *needbuffer=loop->needbuffer;
		intp index=loop->index, size=loop->size;
		int bufsize;
		intp bufcnt;
		int copysizes[MAX_ARGS];
		void **bufptr = loop->bufptr;
		void **buffer = loop->buffer;
		void **castbuf = loop->castbuf;
		intp *steps = loop->steps;
		char *tptr[MAX_ARGS];
		int ninnerloops = loop->ninnerloops;
		Bool pyobject[MAX_ARGS];
		int datasize[MAX_ARGS];
                int i, j, k, stopcondition;
		char *myptr1, *myptr2;

		
		for (i=0; i<self->nargs; i++) {
			copyswapn[i] = mps[i]->descr->f->copyswapn;
			mpselsize[i] = mps[i]->descr->elsize;
			pyobject[i] = (loop->obj && \
                                       (mps[i]->descr->type_num == PyArray_OBJECT));
			laststrides[i] = iters[i]->strides[loop->lastdim];
			if (steps[i] && laststrides[i] != mpselsize[i]) fastmemcpy[i] = 0;
			else fastmemcpy[i] = 1;
		}
		/* Do generic buffered looping here (works for any kind of
		   arrays -- some need buffers, some don't. 
		*/
		
		/* New algorithm: N is the largest dimension.  B is the buffer-size.
		   quotient is loop->ninnerloops-1
		   remainder is loop->leftover

		Compute N = quotient * B + remainder.   
		quotient = N / B  # integer math    
		(store quotient + 1) as the number of innerloops
		remainder = N % B # integer remainder
		
		On the inner-dimension we will have (quotient + 1) loops where 
		the size of the inner function is B for all but the last when the niter size is
		remainder. 
		
		So, the code looks very similar to NOBUFFER_LOOP except the inner-most loop is 
		replaced with...
		
		for(i=0; i<quotient+1; i++) {
		     if (i==quotient+1) make itersize remainder size
		     copy only needed items to buffer.
		     swap input buffers if needed
		     cast input buffers if needed
		     call loop_function()
		     cast outputs in buffers if needed
		     swap outputs in buffers if needed
		     copy only needed items back to output arrays.	 
		     update all data-pointers by strides*niter
		     }		
		*/


		/* fprintf(stderr, "BUFFER...%d,%d,%d\n", loop->size, 
		           loop->ninnerloops, loop->leftover);
		*/
		/*
		for (i=0; i<self->nargs; i++) {
		         fprintf(stderr, "iters[%d]->dataptr = %p, %p of size %d\n", i, 
			 iters[i], iters[i]->ao->data, PyArray_NBYTES(iters[i]->ao));
		}
		*/

		stopcondition = ninnerloops;
		if (loop->leftover == 0) stopcondition--;
		while (index < size) {
			bufsize=loop->bufsize;
			for (i=0; i<self->nargs; i++) {
				tptr[i] = loop->iters[i]->dataptr;
				if (needbuffer[i]) {
					dptr[i] = bufptr[i];
					datasize[i] = (steps[i] ? bufsize : 1);
					copysizes[i] = datasize[i] * mpselsize[i];
				}
				else {
					dptr[i] = tptr[i];
				}
			}

			/* This is the inner function over the last dimension */
			for (k=1; k<=stopcondition; k++) {
				if (k==ninnerloops) {
                                        bufsize = loop->leftover;
                                        for (i=0; i<self->nargs;i++) {
						if (!needbuffer[i]) continue;
                                                datasize[i] = (steps[i] ? bufsize : 1);
						copysizes[i] = datasize[i] * mpselsize[i];
                                        }
                                }
                                        
				for (i=0; i<self->nin; i++) {
					if (!needbuffer[i]) continue;
					if (fastmemcpy[i]) 
						memcpy(buffer[i], tptr[i],
						       copysizes[i]);
					else {
						myptr1 = buffer[i];
						myptr2 = tptr[i];
						for (j=0; j<bufsize; j++) {
							memcpy(myptr1, myptr2, mpselsize[i]);
							myptr1 += mpselsize[i];
							myptr2 += laststrides[i];
						}
					}
					
					/* swap the buffer if necessary */
					if (swap[i]) {
						/* fprintf(stderr, "swapping...\n");*/
						copyswapn[i](buffer[i], NULL,
							     (intp) datasize[i], 1,
							     mpselsize[i]);
					}
					/* cast to the other buffer if necessary */
					if (loop->cast[i]) {
						loop->cast[i](buffer[i],
							      castbuf[i],
							      (intp) datasize[i],
							      NULL, NULL);
					}
				}
				
				bufcnt = (intp) bufsize;
				loop->function((char **)dptr, &bufcnt, steps, loop->funcdata);
				
				for (i=self->nin; i<self->nargs; i++) {
					if (!needbuffer[i]) continue;
					if (loop->cast[i]) {
						loop->cast[i](castbuf[i],
							      buffer[i],
							      (intp) datasize[i],
							      NULL, NULL);
					}
					if (swap[i]) {
						copyswapn[i](buffer[i], NULL,
							     (intp) datasize[i], 1, 
							     mpselsize[i]);
					}
					/* copy back to output arrays */
					/* decref what's already there for object arrays */
					if (pyobject[i]) {
						myptr1 = tptr[i];
						for (j=0; j<datasize[i]; j++) {
							Py_XDECREF(*((PyObject **)myptr1));
							myptr1 += laststrides[i];
						}
					}
					if (fastmemcpy[i]) 
						memcpy(tptr[i], buffer[i], copysizes[i]);
					else {
						myptr2 = buffer[i];
						myptr1 = tptr[i];
						for (j=0; j<bufsize; j++) {
							memcpy(myptr1, myptr2, 
							       mpselsize[i]);
							myptr1 += laststrides[i];
							myptr2 += mpselsize[i];
						}
					}
                                }
				if (k == stopcondition) continue;
				for (i=0; i<self->nargs; i++) {
					tptr[i] += bufsize * laststrides[i];
					if (!needbuffer[i]) dptr[i] = tptr[i];
				}
			}

			if (loop->obj) { /* DECREF castbuf for object arrays */
				for (i=0; i<self->nargs; i++) {
					if (pyobject[i]) {
						if (steps[i] == 0) {
							Py_XDECREF(*((PyObject **)castbuf[i]));
						}
						else {
							int size = loop->bufsize;
							PyObject **objptr = castbuf[i];
							/* size is loop->bufsize unless there
							   was only one loop */
							if (ninnerloops == 1) \
								size = loop->leftover;
							
							for (j=0; j<size; j++) {
								Py_XDECREF(*objptr);
								objptr += 1;
							}
						}
					}
				}
				
			}
			
			UFUNC_CHECK_ERROR(loop);
			
			for (i=0; i<self->nargs; i++) {
				PyArray_ITER_NEXT(loop->iters[i]);
			}
			index++;
                }
        }
        }
                
        LOOP_END_THREADS
                
        ufuncloop_dealloc(loop);
	return 0;

 fail:
        LOOP_END_THREADS

	if (loop) ufuncloop_dealloc(loop);
	return -1;
}

static PyArrayObject *
_getidentity(PyUFuncObject *self, int otype, char *str)
{
        PyObject *obj, *arr;
        PyArray_Descr *typecode;
	
        if (self->identity == PyUFunc_None) {
                PyErr_Format(PyExc_ValueError, 
                             "zero-size array to ufunc.%s "      \
                             "without identity", str);
                return NULL;
        }
        if (self->identity == PyUFunc_One) {
                obj = PyInt_FromLong((long) 1);
        } else {
                obj = PyInt_FromLong((long) 0);
        }

	typecode = PyArray_DescrFromType(otype); 
        arr = PyArray_FromAny(obj, typecode, 0, 0, CARRAY_FLAGS);
        Py_DECREF(obj);
        return (PyArrayObject *)arr;
}

static int
_create_reduce_copy(PyUFuncReduceObject *loop, PyArrayObject **arr, int rtype)
{
	intp maxsize;
	PyObject *new;
	PyArray_Descr *ntype;
	
	maxsize = PyArray_SIZE(*arr);
	
	if (maxsize < loop->bufsize) {
		if (!(PyArray_ISBEHAVED_RO(*arr)) ||	\
		    PyArray_TYPE(*arr) != rtype) {
			ntype = PyArray_DescrFromType(rtype);
			new = PyArray_FromAny((PyObject *)(*arr), 
					      ntype, 0, 0,
					      FORCECAST | ALIGNED);
			if (new == NULL) return -1;
			*arr = (PyArrayObject *)new;
			loop->decref = new;
		}
	}

	/* Don't decref *arr before re-assigning
	   because it was not going to be DECREF'd anyway.
	   
	   If a copy is made, then the copy will be removed
	   on deallocation of the loop structure by setting 
	   loop->decref.
	*/
	
	return 0;
}

static PyUFuncReduceObject *
construct_reduce(PyUFuncObject *self, PyArrayObject **arr, int axis, 
		 int otype, int operation, intp ind_size, char *str)
{
        PyUFuncReduceObject *loop;
        PyArrayObject *idarr;
	PyArrayObject *aar;
        intp loop_i[MAX_DIMS];
        int arg_types[3] = {otype, otype, otype};
	char scalars[3] = {UFUNC_NOSCALAR, UFUNC_NOSCALAR, UFUNC_NOSCALAR};
	int i, j;
	int nd = (*arr)->nd;
	/* Reduce type is the type requested of the input 
	   during reduction */
        
        if ((loop = _pya_malloc(sizeof(PyUFuncReduceObject)))==NULL) {
                PyErr_NoMemory(); return loop;
        }
        
        loop->swap = 0;
	loop->index = 0;
	loop->ufunc = self;
        Py_INCREF(self);
        loop->cast = NULL;
        loop->buffer = NULL;
        loop->ret = NULL;
	loop->it = NULL;
	loop->rit = NULL;
	loop->errobj = NULL;
	loop->decref=NULL;    
        loop->N = (*arr)->dimensions[axis];
	loop->instrides = (*arr)->strides[axis];

	if (select_types(loop->ufunc, arg_types, &(loop->function), 
			 &(loop->funcdata), scalars) == -1) goto fail;   
	
	/* output type may change -- if it does 
	 reduction is forced into that type 
	 and we need to select the reduction function again
	*/
	if (otype != arg_types[2]) {
		otype = arg_types[2];
		arg_types[0] = otype;
		arg_types[1] = otype;
		if (select_types(loop->ufunc, arg_types, &(loop->function), 
				 &(loop->funcdata), scalars) == -1) 
			goto fail;   		
	}
	
	/* get looping parameters from Python */
	if (PyUFunc_GetPyValues(str, &(loop->bufsize), &(loop->errormask), 
				&(loop->errobj)) < 0) goto fail;
	
	/* Make copy if misbehaved or not otype for small arrays */
	if (_create_reduce_copy(loop, arr, otype) < 0) goto fail; 
	aar = *arr;
	
        if (loop->N == 0) {
                loop->meth = ZERODIM_REDUCELOOP;
        }
        else if (PyArray_ISBEHAVED_RO(aar) &&		\
                 otype == (aar)->descr->type_num) {
		if (loop->N == 1) {
			loop->meth = ONEDIM_REDUCELOOP;
		}
		else {
			loop->meth = NOBUFFER_UFUNCLOOP;
			loop->steps[0] = (aar)->strides[axis];
			loop->N -= 1;
		}
        }
        else {
                loop->meth = BUFFER_UFUNCLOOP;
                loop->swap = !(PyArray_ISNOTSWAPPED(aar));
        }

        /* Determine if object arrays are involved */
        if (otype == PyArray_OBJECT || aar->descr->type_num == PyArray_OBJECT)
                loop->obj = 1;
        else
                loop->obj = 0;

        if (loop->meth == ZERODIM_REDUCELOOP) {
                idarr = _getidentity(self, otype, str);
                if (idarr == NULL) goto fail;
                if (idarr->descr->elsize > UFUNC_MAXIDENTITY) {
                        PyErr_Format(PyExc_RuntimeError, 
				     "UFUNC_MAXIDENTITY (%d)"		\
                                     " is too small (needs to be at least %d)",
                                     UFUNC_MAXIDENTITY, idarr->descr->elsize);
                        Py_DECREF(idarr);
                        goto fail;
                }
                memcpy(loop->idptr, idarr->data, idarr->descr->elsize);
                Py_DECREF(idarr);
        }
	
        /* Construct return array */
	switch(operation) {
	case UFUNC_REDUCE:
		for (j=0, i=0; i<nd; i++) {
			if (i != axis) 
				loop_i[j++] = (aar)->dimensions[i];
			
		}
		loop->ret = (PyArrayObject *)				\
			PyArray_New(aar->ob_type, aar->nd-1, loop_i, otype, 
				    NULL, NULL, 0, 0, (PyObject *)aar);
		break;
	case UFUNC_ACCUMULATE:
		loop->ret = (PyArrayObject *)				\
			PyArray_New(aar->ob_type, aar->nd, aar->dimensions, 
				    otype, NULL, NULL, 0, 0, (PyObject *)aar);
		break;
	case UFUNC_REDUCEAT:
		memcpy(loop_i, aar->dimensions, nd*sizeof(intp));
		/* Index is 1-d array */
		loop_i[axis] = ind_size; 
		loop->ret = (PyArrayObject *)\
			PyArray_New(aar->ob_type, aar->nd, loop_i, otype,
				    NULL, NULL, 0, 0, (PyObject *)aar);
		if (loop->ret == NULL) goto fail;
		if (ind_size == 0) {
			loop->meth = ZERODIM_REDUCELOOP;
			return loop;
		}
		if (loop->meth == ONEDIM_REDUCELOOP)
			loop->meth = NOBUFFER_REDUCELOOP;
		break;
	}
        if (loop->ret == NULL) goto fail;
        loop->insize = aar->descr->elsize;
        loop->outsize = loop->ret->descr->elsize;
        loop->bufptr[1] = loop->ret->data;

	if (loop->meth == ZERODIM_REDUCELOOP) {
		loop->size = PyArray_SIZE(loop->ret);
		return loop;
	}

	loop->it = (PyArrayIterObject *)PyArray_IterNew((PyObject *)aar);
        if (loop->it == NULL) return NULL;

	if (loop->meth == ONEDIM_REDUCELOOP) {
		loop->size = loop->it->size;		
		return loop;
	}

        /* Fix iterator to loop over correct dimension */
	/* Set size in axis dimension to 1 */
        
        loop->it->contiguous = 0;
        loop->it->size /= (loop->it->dims_m1[axis]+1);
        loop->it->dims_m1[axis] = 0;
        loop->it->backstrides[axis] = 0;


        loop->size = loop->it->size;

	if (operation == UFUNC_REDUCE) {
		loop->steps[1] = 0;
	}
	else {
		loop->rit = (PyArrayIterObject *)			\
			PyArray_IterNew((PyObject *)(loop->ret));
		if (loop->rit == NULL) return NULL;		

		/* Fix iterator to loop over correct dimension */
		/* Set size in axis dimension to 1 */
		
		loop->rit->contiguous = 0;
		loop->rit->size /= (loop->rit->dims_m1[axis]+1);
		loop->rit->dims_m1[axis] = 0;
		loop->rit->backstrides[axis] = 0;

		if (operation == UFUNC_ACCUMULATE)
			loop->steps[1] = loop->ret->strides[axis];
		else 
			loop->steps[1] = 0;
	}
	loop->steps[2] = loop->steps[1];
	loop->bufptr[2] = loop->bufptr[1] + loop->steps[2];

	
	if (loop->meth == BUFFER_UFUNCLOOP) {
		int _size;
		loop->steps[0] = loop->outsize;
                if (otype != aar->descr->type_num) {
			_size=loop->bufsize*(loop->outsize +		\
					     aar->descr->elsize);
                        loop->buffer = PyDataMem_NEW(_size);
                        if (loop->buffer == NULL) goto fail;
			if (loop->obj) memset(loop->buffer, 0, _size);
                        loop->castbuf = loop->buffer + \
                                loop->bufsize*aar->descr->elsize;
                        loop->bufptr[0] = loop->castbuf;     
                        loop->cast = aar->descr->f->cast[otype];
                }
                else {
			_size = loop->bufsize * loop->outsize;
                        loop->buffer = PyDataMem_NEW(_size);
                        if (loop->buffer == NULL) goto fail;
			if (loop->obj) memset(loop->buffer, 0, _size);
                        loop->bufptr[0] = loop->buffer;
                }
	}


	PyUFunc_clearfperr();
	return loop;

 fail:
        ufuncreduce_dealloc(loop);
	return NULL;	
}


/* We have two basic kinds of loops */
/*  One is used when arr is not-swapped and aligned and output type
    is the same as input type.
    and another using buffers when one of these is not satisfied.

    Zero-length and one-length axes-to-be-reduced are handled separately.
*/

static PyObject *
PyUFunc_Reduce(PyUFuncObject *self, PyArrayObject *arr, int axis, int otype)
{
        PyArrayObject *ret=NULL;
        PyUFuncReduceObject *loop;
        intp i, n;
        char *dptr;
        BEGIN_THREADS_DEF
        	
        /* Construct loop object */
        loop = construct_reduce(self, &arr, axis, otype, UFUNC_REDUCE, 0,
				"reduce");
	if (!loop) return NULL;

        LOOP_BEGIN_THREADS
        switch(loop->meth) {
        case ZERODIM_REDUCELOOP:
		/* fprintf(stderr, "ZERO..%d\n", loop->size); */
		for(i=0; i<loop->size; i++) {
			if (loop->obj) Py_INCREF(*((PyObject **)loop->idptr));
			memmove(loop->bufptr[1], loop->idptr, loop->outsize);
			loop->bufptr[1] += loop->outsize;
		}
                break;
        case ONEDIM_REDUCELOOP:
		/*fprintf(stderr, "ONEDIM..%d\n", loop->size); */
                while(loop->index < loop->size) {
			if (loop->obj) Py_INCREF(*((PyObject **)loop->it->dataptr));
                        memmove(loop->bufptr[1], loop->it->dataptr, 
                               loop->outsize);
			PyArray_ITER_NEXT(loop->it);
			loop->bufptr[1] += loop->outsize;
			loop->index++;
		}		
		break;
        case NOBUFFER_UFUNCLOOP:
		/*fprintf(stderr, "NOBUFFER..%d\n", loop->size); */
                while(loop->index < loop->size) {
			/* Copy first element to output */
			if (loop->obj) 
				Py_INCREF(*((PyObject **)loop->it->dataptr));
                        memmove(loop->bufptr[1], loop->it->dataptr, 
                               loop->outsize);
			/* Adjust input pointer */
                        loop->bufptr[0] = loop->it->dataptr+loop->steps[0];
                        loop->function((char **)loop->bufptr, 
				       &(loop->N),
                                       loop->steps, loop->funcdata);
			UFUNC_CHECK_ERROR(loop);

                        PyArray_ITER_NEXT(loop->it)
                        loop->bufptr[1] += loop->outsize;
                        loop->bufptr[2] = loop->bufptr[1];
                        loop->index++; 
                }
                break;
        case BUFFER_UFUNCLOOP: 
                /* use buffer for arr */
                /* 
                   For each row to reduce
                   1. copy first item over to output (casting if necessary)
                   2. Fill inner buffer 
                   3. When buffer is filled or end of row
                      a. Cast input buffers if needed
                      b. Call inner function.
                   4. Repeat 2 until row is done.
                */
		/* fprintf(stderr, "BUFFERED..%d %d\n", loop->size, 
		   loop->swap); */
                while(loop->index < loop->size) {
                        loop->inptr = loop->it->dataptr;			
			/* Copy (cast) First term over to output */
			if (loop->cast) {
				/* A little tricky because we need to
				   cast it first */
				arr->descr->f->copyswap(loop->buffer,
						     loop->inptr,
						     loop->swap,
						     loop->insize);
				loop->cast(loop->buffer, loop->castbuf,
					   1, NULL, NULL);
				if (loop->obj) 
					Py_INCREF(*((PyObject **)loop->castbuf));
				memcpy(loop->bufptr[1], loop->castbuf,
				       loop->outsize);
			}
			else { /* Simple copy */
				arr->descr->f->copyswap(loop->bufptr[1], 
						     loop->inptr,
						     loop->swap,
						     loop->insize);
			}
			loop->inptr += loop->instrides;
                        n = 1;
                        while(n < loop->N) {
                                /* Copy up to loop->bufsize elements to 
                                   buffer */
                                dptr = loop->buffer;
                                for (i=0; i<loop->bufsize; i++, n++) {
                                        if (n == loop->N) break;
                                        arr->descr->f->copyswap(dptr,
                                                             loop->inptr,
                                                             loop->swap,
                                                             loop->insize);
                                        loop->inptr += loop->instrides;
                                        dptr += loop->insize;
                                }
                                if (loop->cast)
                                        loop->cast(loop->buffer,
                                                   loop->castbuf,
                                                   i, NULL, NULL);
                                loop->function((char **)loop->bufptr,
                                               &i, 
					       loop->steps, loop->funcdata);
				UFUNC_CHECK_ERROR(loop);
                        }                       
                        PyArray_ITER_NEXT(loop->it);
                        loop->bufptr[1] += loop->outsize;
                        loop->bufptr[2] = loop->bufptr[1]; 
                        loop->index++;
                }
        }

        LOOP_END_THREADS

        ret = loop->ret;
	/* Hang on to this reference -- will be decref'd with loop */
        Py_INCREF(ret);
        ufuncreduce_dealloc(loop);
        return (PyObject *)ret;

 fail:
        LOOP_END_THREADS

        if (loop) ufuncreduce_dealloc(loop);
        return NULL;
}


static PyObject *
PyUFunc_Accumulate(PyUFuncObject *self, PyArrayObject *arr, int axis, 
		   int otype)
{
        PyArrayObject *ret=NULL;
        PyUFuncReduceObject *loop;
        intp i, n;
        char *dptr;
        
        /* Construct loop object */
        loop = construct_reduce(self, &arr, axis, otype, UFUNC_ACCUMULATE, 0,
				"accumulate");
	if (!loop) return NULL;

	LOOP_BEGIN_THREADS
        switch(loop->meth) {
        case ZERODIM_REDUCELOOP: /* Accumulate */
		/* fprintf(stderr, "ZERO..%d\n", loop->size); */
		for(i=0; i<loop->size; i++) {
			if (loop->obj) 
				Py_INCREF(*((PyObject **)loop->idptr));
			memcpy(loop->bufptr[1], loop->idptr, loop->outsize);
			loop->bufptr[1] += loop->outsize;
		}               
                break;
        case ONEDIM_REDUCELOOP: /* Accumulate */
		/* fprintf(stderr, "ONEDIM..%d\n", loop->size); */
                while(loop->index < loop->size) {
			if (loop->obj) 
				Py_INCREF(*((PyObject **)loop->it->dataptr));
                        memcpy(loop->bufptr[1], loop->it->dataptr, 
                               loop->outsize);
			PyArray_ITER_NEXT(loop->it);
			loop->bufptr[1] += loop->outsize;
			loop->index++;
		}		
		break;
        case NOBUFFER_UFUNCLOOP: /* Accumulate */
		/* fprintf(stderr, "NOBUFFER..%d\n", loop->size); */
                while(loop->index < loop->size) {
			/* Copy first element to output */
			if (loop->obj) 
				Py_INCREF(*((PyObject **)loop->it->dataptr));
                        memcpy(loop->bufptr[1], loop->it->dataptr, 
                               loop->outsize);
			/* Adjust input pointer */
                        loop->bufptr[0] = loop->it->dataptr+loop->steps[0];
                        loop->function((char **)loop->bufptr, 
				       &(loop->N),
                                       loop->steps, loop->funcdata);
			UFUNC_CHECK_ERROR(loop);

                        PyArray_ITER_NEXT(loop->it);
			PyArray_ITER_NEXT(loop->rit);
                        loop->bufptr[1] = loop->rit->dataptr;
			loop->bufptr[2] = loop->bufptr[1] + loop->steps[1];
                        loop->index++;
                }
                break;
        case BUFFER_UFUNCLOOP:  /* Accumulate */
                /* use buffer for arr */
                /* 
                   For each row to reduce
                   1. copy identity over to output (casting if necessary)
                   2. Fill inner buffer 
                   3. When buffer is filled or end of row
                      a. Cast input buffers if needed
                      b. Call inner function.
                   4. Repeat 2 until row is done.
                */
		/* fprintf(stderr, "BUFFERED..%d %p\n", loop->size, 
		   loop->cast); */
                while(loop->index < loop->size) {
                        loop->inptr = loop->it->dataptr;			
			/* Copy (cast) First term over to output */
			if (loop->cast) {
				/* A little tricky because we need to
				   cast it first */
				arr->descr->f->copyswap(loop->buffer,
						     loop->inptr,
						     loop->swap,
						     loop->insize);
				loop->cast(loop->buffer, loop->castbuf,
					   1, NULL, NULL);
				if (loop->obj) 
					Py_INCREF(*((PyObject **)loop->castbuf));
				memcpy(loop->bufptr[1], loop->castbuf,
				       loop->outsize);
			}
			else { /* Simple copy */
				arr->descr->f->copyswap(loop->bufptr[1], 
						     loop->inptr,
						     loop->swap,
						     loop->insize);
			}
			loop->inptr += loop->instrides;
                        n = 1;
                        while(n < loop->N) {
                                /* Copy up to loop->bufsize elements to 
                                   buffer */
                                dptr = loop->buffer;
                                for (i=0; i<loop->bufsize; i++, n++) {
                                        if (n == loop->N) break;
                                        arr->descr->f->copyswap(dptr,
                                                             loop->inptr,
                                                             loop->swap,
                                                             loop->insize);
                                        loop->inptr += loop->instrides;
                                        dptr += loop->insize;
                                }
                                if (loop->cast)
                                        loop->cast(loop->buffer,
                                                   loop->castbuf,
                                                   i, NULL, NULL);
                                loop->function((char **)loop->bufptr,
                                               &i, 
					       loop->steps, loop->funcdata);
				UFUNC_CHECK_ERROR(loop);
                        }                       
                        PyArray_ITER_NEXT(loop->it);
			PyArray_ITER_NEXT(loop->rit);
                        loop->bufptr[1] = loop->rit->dataptr;
			loop->bufptr[2] = loop->bufptr[1] + loop->steps[1];
                        loop->index++;
                }
        }

	LOOP_END_THREADS
        ret = loop->ret;
	/* Hang on to this reference -- will be decref'd with loop */
        Py_INCREF(ret);
        ufuncreduce_dealloc(loop);
        return (PyObject *)ret;

 fail:
	LOOP_END_THREADS

        if (loop) ufuncreduce_dealloc(loop);
        return NULL;
}

/* Reduceat performs a reduce over an axis using the indices as a guide

op.reduceat(array,indices)  computes
op.reduce(array[indices[i]:indices[i+1]]  
   for i=0..end with an implicit indices[i+1]=len(array)
    assumed when i=end-1

if indices[i+1] <= indices[i]+1  
   then the result is array[indices[i]] for that value

op.accumulate(array) is the same as
op.reduceat(array,indices)[::2]
where indices is range(len(array)-1) with a zero placed in every other sample
  indices = zeros(len(array)*2-1)
  indices[1::2] = range(1,len(array))

output shape is based on the size of indices
 */

static PyObject *
PyUFunc_Reduceat(PyUFuncObject *self, PyArrayObject *arr, PyArrayObject *ind, 
                 int axis, int otype)
{	
	PyArrayObject *ret;
        PyUFuncReduceObject *loop;
	intp *ptr=(intp *)ind->data;
	intp nn=ind->dimensions[0];		
	intp mm=arr->dimensions[axis]-1;
	intp n, i, j;
	char *dptr;

	/* Check for out-of-bounds values in indices array */		
	for (i=0; i<nn; i++) {
		if ((*ptr < 0) || (*ptr > mm)) {
			PyErr_Format(PyExc_IndexError, 
				     "index out-of-bounds (0, %d)", (int) mm);
			return NULL;
		}
		ptr++;
	}
	
	ptr = (intp *)ind->data;
        /* Construct loop object */
        loop = construct_reduce(self, &arr, axis, otype, UFUNC_REDUCEAT, nn,
				"reduceat");
	if (!loop) return NULL;

	LOOP_BEGIN_THREADS
	switch(loop->meth) {
	/* zero-length index -- return array immediately */
	case ZERODIM_REDUCELOOP:
		/* fprintf(stderr, "ZERO..\n"); */
		break;
	/* NOBUFFER -- behaved array and same type */
	case NOBUFFER_UFUNCLOOP: 	                /* Reduceat */
		/* fprintf(stderr, "NOBUFFER..%d\n", loop->size); */
		while(loop->index < loop->size) {
			ptr = (intp *)ind->data;
			for (i=0; i<nn; i++) {
				loop->bufptr[0] = loop->it->dataptr +	\
					(*ptr)*loop->instrides;
				if (loop->obj) 
					Py_INCREF(*((PyObject **)loop->bufptr[0]));
				memcpy(loop->bufptr[1], loop->bufptr[0],
				       loop->outsize);
				mm = (i==nn-1 ? arr->dimensions[axis]-*ptr : \
				      *(ptr+1) - *ptr) - 1;
				if (mm > 0) {
					loop->bufptr[0] += loop->instrides;
					loop->bufptr[2] = loop->bufptr[1];
					loop->function((char **)loop->bufptr,
						       &mm, loop->steps,
						       loop->funcdata);
					UFUNC_CHECK_ERROR(loop);
				}	
				loop->bufptr[1] += loop->ret->strides[axis];
				ptr++;
			}
			PyArray_ITER_NEXT(loop->it);
			PyArray_ITER_NEXT(loop->rit);
			loop->bufptr[1] = loop->rit->dataptr;
			loop->index++;
		}
		break;

	/* BUFFER -- misbehaved array or different types */ 
	case BUFFER_UFUNCLOOP:                               /* Reduceat */
		/* fprintf(stderr, "BUFFERED..%d\n", loop->size); */
		while(loop->index < loop->size) {
			ptr = (intp *)ind->data;
			for (i=0; i<nn; i++) {
				if (loop->obj) 
					Py_INCREF(*((PyObject **)loop->idptr));
				memcpy(loop->bufptr[1], loop->idptr, 
				       loop->outsize);
				n = 0;
				mm = (i==nn-1 ? arr->dimensions[axis] - *ptr :\
				      *(ptr+1) - *ptr);
				if (mm < 1) mm = 1;
				loop->inptr = loop->it->dataptr + \
					(*ptr)*loop->instrides;
				while (n < mm) {
					/* Copy up to loop->bufsize elements
					   to buffer */
					dptr = loop->buffer;
					for (j=0; j<loop->bufsize; j++, n++) {
						if (n == mm) break;
						arr->descr->f->copyswap\
							(dptr,
							 loop->inptr,
							 loop->swap,
							 loop->insize);
						loop->inptr += loop->instrides;
						dptr += loop->insize;
					}
					if (loop->cast)
						loop->cast(loop->buffer,
							   loop->castbuf,
							   j, NULL, NULL);
					loop->bufptr[2] = loop->bufptr[1];
					loop->function((char **)loop->bufptr,
						       &j, loop->steps,
						       loop->funcdata);
					UFUNC_CHECK_ERROR(loop);
				} 
				loop->bufptr[1] += loop->ret->strides[axis];
				ptr++;
			}
			PyArray_ITER_NEXT(loop->it);
			PyArray_ITER_NEXT(loop->rit);
			loop->bufptr[1] = loop->rit->dataptr;
			loop->index++;
		}
		break;
	}

	LOOP_END_THREADS
	
        ret = loop->ret;
	/* Hang on to this reference -- will be decref'd with loop */
        Py_INCREF(ret);
        ufuncreduce_dealloc(loop);
        return (PyObject *)ret;
	
 fail:
	LOOP_END_THREADS

        if (loop) ufuncreduce_dealloc(loop);
	return NULL;
}


/* This code handles reduce, reduceat, and accumulate 
   (accumulate and reduce are special cases of the more general reduceat       
    but they are handled separately for speed) 
*/

static PyObject * 
PyUFunc_GenericReduction(PyUFuncObject *self, PyObject *args, 
                         PyObject *kwds, int operation) 
{
	int axis=0;
	PyArrayObject *mp, *ret = NULL;
	PyObject *op, *res=NULL;
	PyObject *obj_ind;        
	PyArrayObject *indices = NULL;
	PyArray_Descr *otype=NULL;
	static char *kwlist1[] = {"array", "axis", "rtype", NULL};
	static char *kwlist2[] = {"array", "indices", "axis", "rtype", NULL}; 
        static char *_reduce_type[] = {"reduce", "accumulate", \
				       "reduceat", NULL};
	if (self == NULL) {
		PyErr_SetString(PyExc_ValueError, "function not supported");
		return NULL;
	}	

	if (self->nin != 2) {
		PyErr_Format(PyExc_ValueError, 
                             "%s only supported for binary functions",
                             _reduce_type[operation]);
		return NULL;
	}
	if (self->nout != 1) {
		PyErr_Format(PyExc_ValueError,
                             "%s only supported for functions " \
                             "returning a single value",
                             _reduce_type[operation]);
		return NULL;
	}

	if (operation == UFUNC_REDUCEAT) {
		PyArray_Descr *indtype;
		indtype = PyArray_DescrFromType(PyArray_INTP);
		if(!PyArg_ParseTupleAndKeywords(args, kwds, "OO|iO&", kwlist2, 
						&op, &obj_ind, &axis, 
						PyArray_DescrConverter, 
						&otype)) return NULL;
                indices = (PyArrayObject *)PyArray_FromAny(obj_ind, indtype, 
							   1, 1, CARRAY_FLAGS);
                if (indices == NULL) return NULL;
		Py_DECREF(indtype);		
	}
	else {
		if(!PyArg_ParseTupleAndKeywords(args, kwds, "O|iO&", kwlist1,
						&op, &axis, 
						PyArray_DescrConverter, 
						&otype)) return NULL;
	}
	
	/* Ensure input is an array */	
	mp = (PyArrayObject *)PyArray_FromAny(op, NULL, 0, 0, 0);
	if (mp == NULL) return NULL;

        /* Check to see if input is zero-dimensional */
        if (mp->nd == 0) {
                PyErr_Format(PyExc_TypeError, "cannot %s on a scalar",
                             _reduce_type[operation]);
                Py_DECREF(mp);
                return NULL;        
        }

        /* Check to see that type (and otype) is not FLEXIBLE */
	if (PyArray_ISFLEXIBLE(mp) || (otype && PyTypeNum_ISFLEXIBLE(otype->type_num))) {
                PyErr_Format(PyExc_TypeError, 
			     "cannot perform %s with flexible type",
                             _reduce_type[operation]);
                Py_DECREF(mp);
                return NULL;
        }

	if (axis < 0) axis += mp->nd;
	if (axis < 0 || axis >= mp->nd) {
		PyErr_SetString(PyExc_ValueError, "axis not in array");
                Py_DECREF(mp);
		return NULL;
	}

	/* Get default type to reduce over if not given */
        if (otype == NULL) {
		/* For integer types --- makes sure at 
		   least a long is used */
		int typenum = PyArray_TYPE(mp);
		if (PyTypeNum_ISINTEGER(typenum) &&	\
		    (mp->descr->elsize < sizeof(long))) {
			if (PyTypeNum_ISUNSIGNED(typenum))
				typenum = PyArray_ULONG;
			else
				typenum = PyArray_LONG;
		}
		else if (PyTypeNum_ISBOOL(typenum) && \
			 ((strcmp(self->name,"add")==0) ||	\
			  (strcmp(self->name,"multiply")==0))) {
			typenum = PyArray_LONG;
		}
		otype = PyArray_DescrFromType(typenum);
	}

        switch(operation) {
        case UFUNC_REDUCE:
                ret = (PyArrayObject *)PyUFunc_Reduce(self, mp, axis, 
                                                      otype->type_num);
		break;
        case UFUNC_ACCUMULATE:
                ret = (PyArrayObject *)PyUFunc_Accumulate(self, mp, axis, 
                                                          otype->type_num);
		break;
        case UFUNC_REDUCEAT:
                ret = (PyArrayObject *)PyUFunc_Reduceat(self, mp, indices, 
                                                        axis, otype->type_num);
                Py_DECREF(indices);
		break;
        }
        Py_DECREF(mp);
	Py_DECREF(otype);
	if (ret==NULL) return NULL;
	if (op->ob_type != ret->ob_type) {
		res = PyObject_CallMethod(op, "__array_wrap__", "O", ret);
		if (res == NULL) PyErr_Clear();
		else if (res == Py_None) Py_DECREF(res);
		else {
			Py_DECREF(ret);
			return res;
		}	
	}
	return PyArray_Return(ret);
	
}



/* ---------- */

static PyObject *
_find_array_wrap(PyObject *args)
{
	int nargs, i;
	int np = 0;
	int argmax = 0;
	int val;
	double priority[MAX_ARGS];
	double maxpriority = PyArray_SUBTYPE_PRIORITY;
	PyObject *with_wrap[MAX_ARGS];
	PyObject *attr;
	PyObject *obj;

	nargs = PyTuple_Size(args);
	for (i=0; i<nargs; i++) {
		obj = PyTuple_GET_ITEM(args, i);
		if (PyArray_CheckExact(obj) || PyBigArray_CheckExact(obj) || \
		    PyArray_IsAnyScalar(obj))
			continue;
		attr = PyObject_GetAttrString(obj, "__array_wrap__");
		if (attr != NULL) {
			val = PyCallable_Check(attr);
			Py_DECREF(attr);
			if (val) {
				attr = PyObject_GetAttrString(obj,
						     "__array_priority__");
				if (attr == NULL)
					priority[np] = \
						PyArray_SUBTYPE_PRIORITY;
				else {
					priority[np] = PyFloat_AsDouble(attr);
					if (PyErr_Occurred()) {
						PyErr_Clear();
						priority[np] = PyArray_SUBTYPE_PRIORITY;
					}
                                        Py_DECREF(attr);
				}
				with_wrap[np] = obj;
				np += 1;
			}
		}
                PyErr_Clear();
	}

	if (np == 0) return NULL;

	for (i=0; i<np; i++) {
		if (priority[i] > maxpriority) {
			maxpriority = priority[i];
			argmax = i;
		}
	}

	return with_wrap[argmax];
}

static PyObject *
ufunc_generic_call(PyUFuncObject *self, PyObject *args) 
{
	int i;
	PyTupleObject *ret;
	PyArrayObject *mps[MAX_ARGS];
	PyObject *retobj[MAX_ARGS];
	PyObject *res;
	PyObject *obj;
        int errval;
        
	/* Initialize all array objects to NULL to make cleanup easier 
	   if something goes wrong. */
	for(i=0; i<self->nargs; i++) mps[i] = NULL;
	
        errval = PyUFunc_GenericFunction(self, args, mps);
        if (errval < 0) {
		for(i=0; i<self->nargs; i++) Py_XDECREF(mps[i]);
		if (errval == -1)
			return NULL;
		else {
			Py_INCREF(Py_NotImplemented);
			return Py_NotImplemented;
		}
        }
	
	for(i=0; i<self->nin; i++) Py_DECREF(mps[i]);

	/*  Use __array_wrap__ on all outputs 
	        if present on one of the input arguments.
	    If present for multiple inputs:
	        use __array_wrap__ of input object with largest 
		__array_priority__ (default = 0.0)
	 */
	obj = _find_array_wrap(args);
	
	/* wrap outputs */
	for (i=0; i<self->nout; i++) {
		int j=self->nin+i;
		/* check to see if any UPDATEIFCOPY flags are set 
		   which meant that a temporary output was generated 
		*/
		if (mps[j]->flags & UPDATEIFCOPY) {
			PyObject *old = mps[j]->base;
			Py_INCREF(old);   /* we want to hang on to this */
			Py_DECREF(mps[j]); /* should trigger the copy 
					      back into old */
			mps[j] = (PyArrayObject *)old;
		}
		if (obj != NULL) {
			res = PyObject_CallMethod(obj, "__array_wrap__",
						  "O", mps[j]);
			if (res == NULL) PyErr_Clear();
			else if (res == Py_None) Py_DECREF(res);
			else {
				Py_DECREF(mps[j]);
				retobj[i] = res;
				continue;
			}
		}
		retobj[i] = PyArray_Return(mps[j]);
	}
	
	if (self->nout == 1) { 
		return retobj[0];
	} else {  
		ret = (PyTupleObject *)PyTuple_New(self->nout);
		for(i=0; i<self->nout; i++) {
			PyTuple_SET_ITEM(ret, i, retobj[i]);
		}
		return (PyObject *)ret;
	}	

}

static PyObject *
ufunc_update_use_defaults(PyObject *dummy, PyObject *args)
{
	PyObject *errobj;
	int errmask, bufsize;

	if (!PyArg_ParseTuple(args, "")) return NULL;
	
	PyUFunc_USEDEFAULTS = 0;
	if (PyUFunc_GetPyValues("test", &bufsize, &errmask, &errobj) < 0) return NULL;
	
	if ((errmask == UFUNC_ERR_DEFAULT) &&		\
	    (bufsize == PyArray_BUFSIZE) &&		\
	    (PyTuple_GET_ITEM(errobj, 1) == Py_None)) {
		PyUFunc_USEDEFAULTS = 1;
	}
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyUFuncGenericFunction pyfunc_functions[] = {PyUFunc_On_Om};

static char 
doc_frompyfunc[] = "frompyfunc(func, nin, nout) take an arbitrary python function that takes nin objects as input and returns nout objects and return a universal function (ufunc).  This ufunc always returns PyObject arrays";

static PyObject *
ufunc_frompyfunc(PyObject *dummy, PyObject *args, PyObject *kwds) {
        /* Keywords are ignored for now */
        
        PyObject *function, *pyname=NULL;
        int nin, nout, i;
        PyUFunc_PyFuncData *fdata;
        PyUFuncObject *self;
        char *fname, *str;
        int fname_len=-1;
	int offset[2];

        if (!PyArg_ParseTuple(args, "Oii", &function, &nin, &nout)) return NULL;

        if (!PyCallable_Check(function)) {
                PyErr_SetString(PyExc_TypeError, "function must be callable");
                return NULL;
        }
	
        self = _pya_malloc(sizeof(PyUFuncObject));
        if (self == NULL) return NULL;
        PyObject_Init((PyObject *)self, &PyUFunc_Type);

	self->userloops = NULL;
	self->nin = nin;
	self->nout = nout;
	self->nargs = nin+nout;
	self->identity = PyUFunc_None;	
	self->functions = pyfunc_functions;

	self->ntypes = 1;
	self->check_return = 0;

        pyname = PyObject_GetAttrString(function, "__name__");
        if (pyname)
                (void) PyString_AsStringAndSize(pyname, &fname, &fname_len);
        
        if (PyErr_Occurred()) {
                fname = "?";
                fname_len = 1;
                PyErr_Clear();
        }        
        Py_XDECREF(pyname);



	/* self->ptr holds a pointer for enough memory for
	   self->data[0] (fdata)
	   self->data
	   self->name
	   self->types

	   To be safest, all of these need their memory aligned on void * pointers
	   Therefore, we may need to allocate extra space.
	*/
	offset[0] = sizeof(PyUFunc_PyFuncData);
	i = (sizeof(PyUFunc_PyFuncData) % sizeof(void *));
	if (i) offset[0] += (sizeof(void *) - i);
	offset[1] = self->nargs;
	i = (self->nargs % sizeof(void *));
	if (i) offset[1] += (sizeof(void *)-i);

        self->ptr = _pya_malloc(offset[0] + offset[1] + sizeof(void *) + \
			   (fname_len+14));

	if (self->ptr == NULL) return PyErr_NoMemory();
        Py_INCREF(function);
        self->obj = function;
	fdata = (PyUFunc_PyFuncData *)(self->ptr);
        fdata->nin = nin;
        fdata->nout = nout;
        fdata->callable = function;
        
        self->data = (void **)(self->ptr + offset[0]);
        self->data[0] = (void *)fdata;
	
	self->types = (char *)self->data + sizeof(void *);
        for (i=0; i<self->nargs; i++) self->types[i] = PyArray_OBJECT;

        str = self->types + offset[1];
        memcpy(str, fname, fname_len);
        memcpy(str+fname_len, " (vectorized)", 14);
        
        self->name = str;

        /* Do a better job someday */
        self->doc = "dynamic ufunc based on a python function";
        
	
	return (PyObject *)self;
}


/*UFUNC_API*/
static PyObject *
PyUFunc_FromFuncAndData(PyUFuncGenericFunction *func, void **data, 
			char *types, int ntypes,
			int nin, int nout, int identity, 
			char *name, char *doc, int check_return) 
{
	PyUFuncObject *self;

        self = _pya_malloc(sizeof(PyUFuncObject));
        if (self == NULL) return NULL;
        PyObject_Init((PyObject *)self, &PyUFunc_Type);
	
	self->nin = nin;
	self->nout = nout;
	self->nargs = nin+nout;
	self->identity = identity;
	
	self->functions = func;
	self->data = data;
	self->types = types;
	self->ntypes = ntypes;
	self->check_return = check_return;
        self->ptr = NULL;
        self->obj = NULL;
	self->userloops=NULL;
	
	if (name == NULL) self->name = "?";
	else self->name = name;
	
        if (doc == NULL) self->doc = "NULL";
	else self->doc = doc;
	
	return (PyObject *)self;
}

/*UFUNC_API*/
static int
PyUFunc_RegisterLoopForType(PyUFuncObject *ufunc, 
			    int usertype,
			    PyUFuncGenericFunction function,
			    void *data)
{
	PyArray_Descr *descr;
    	PyObject *key, *cobj;
	int ret;	
	
	descr=PyArray_DescrFromType(usertype);
	if ((usertype < PyArray_USERDEF) || (descr==NULL)) {
		PyErr_SetString(PyExc_TypeError, 
				"unknown type");
		return -1;
	}
	Py_DECREF(descr);
	
	if (ufunc->userloops == NULL) {
		ufunc->userloops = PyDict_New();
	}
	key = PyInt_FromLong((long) usertype);
	if (key == NULL) return -1;
	cobj = PyCObject_FromVoidPtr((void *)function, NULL);
	if (cobj == NULL) {Py_DECREF(key); return -1;}
	if (data == NULL) {
		ret = PyDict_SetItem(ufunc->userloops, key, cobj);
		Py_DECREF(cobj);
		Py_DECREF(key);
		return ret;
	}
	else {
		PyObject *cobj2, *tmp;
		cobj2 = PyCObject_FromVoidPtr(data, NULL);
		if (cobj2 == NULL) {
			Py_DECREF(cobj); 
			Py_DECREF(key);
			return -1;
		}
		tmp=Py_BuildValue("NN", cobj, cobj2);
		ret = PyDict_SetItem(ufunc->userloops, key, tmp);
		Py_DECREF(tmp);
		Py_DECREF(key);
		return ret;
	}
}

static void
ufunc_dealloc(PyUFuncObject *self)
{
        if (self->ptr) _pya_free(self->ptr);
	Py_XDECREF(self->userloops);
        Py_XDECREF(self->obj);
        _pya_free(self);
}

static PyObject *
ufunc_repr(PyUFuncObject *self)
{
	char buf[100];
	
	sprintf(buf, "<ufunc '%.50s'>", self->name);
	
	return PyString_FromString(buf);
}


/* -------------------------------------------------------- */

/* op.outer(a,b) is equivalent to op(a[:,NewAxis,NewAxis,etc.],b)
   where a has b.ndim NewAxis terms appended.

   The result has dimensions a.ndim + b.ndim
 */

static PyObject *
ufunc_outer(PyUFuncObject *self, PyObject *args) 
{
	int i;
	PyObject *ret;
	PyArrayObject *ap1=NULL, *ap2=NULL, *ap_new=NULL;
	PyObject *new_args, *tmp;
	PyObject *shape1, *shape2, *newshape;

	if(self->nin != 2) {
		PyErr_SetString(PyExc_ValueError,
				"outer product only supported "\
				"for binary functions");
		return NULL;
	}
	
	if (PySequence_Length(args) != 2) {
		PyErr_SetString(PyExc_TypeError,
				"exactly two arguments expected");
		return NULL;
	}
	
	tmp = PySequence_GetItem(args, 0);
	if (tmp == NULL) return NULL;
	ap1 = (PyArrayObject *)					\
		PyArray_FromObject(tmp, PyArray_NOTYPE, 0, 0);
	Py_DECREF(tmp);
	if (ap1 == NULL) return NULL;
	
	tmp = PySequence_GetItem(args, 1);
	if (tmp == NULL) return NULL;
	ap2 = (PyArrayObject *)PyArray_FromObject(tmp, PyArray_NOTYPE, 0, 0);
	Py_DECREF(tmp);
	if (ap2 == NULL) {Py_DECREF(ap1); return NULL;}

	/* Construct new shape tuple */
	shape1 = PyTuple_New(ap1->nd);
	if (shape1 == NULL) goto fail;
	for (i=0; i<ap1->nd; i++) 
		PyTuple_SET_ITEM(shape1, i, 
				 PyLong_FromLongLong((longlong)ap1->	\
						     dimensions[i]));
	
	shape2 = PyTuple_New(ap2->nd);
	for (i=0; i<ap2->nd; i++) 
		PyTuple_SET_ITEM(shape2, i, PyInt_FromLong((long) 1));
	if (shape2 == NULL) {Py_DECREF(shape1); goto fail;}
	newshape = PyNumber_Add(shape1, shape2);
	Py_DECREF(shape1);
	Py_DECREF(shape2);
	if (newshape == NULL) goto fail;
	
	ap_new = (PyArrayObject *)PyArray_Reshape(ap1, newshape);
	Py_DECREF(newshape);
	if (ap_new == NULL) goto fail;
	
	new_args = Py_BuildValue("(OO)", ap_new, ap2);
	Py_DECREF(ap1);
	Py_DECREF(ap2);
	Py_DECREF(ap_new);	
	ret = ufunc_generic_call(self, new_args);
	Py_DECREF(new_args);
	return ret;

 fail:
	Py_XDECREF(ap1);
	Py_XDECREF(ap2);
	Py_XDECREF(ap_new);
	return NULL;

}


static PyObject *
ufunc_reduce(PyUFuncObject *self, PyObject *args, PyObject *kwds) 
{
	
	return PyUFunc_GenericReduction(self, args, kwds, UFUNC_REDUCE);
}

static PyObject *
ufunc_accumulate(PyUFuncObject *self, PyObject *args, PyObject *kwds) 
{
	
	return PyUFunc_GenericReduction(self, args, kwds, UFUNC_ACCUMULATE);
}

static PyObject *
ufunc_reduceat(PyUFuncObject *self, PyObject *args, PyObject *kwds) 
{	
	return PyUFunc_GenericReduction(self, args, kwds, UFUNC_REDUCEAT);
}


static struct PyMethodDef ufunc_methods[] = {
	{"reduce",  (PyCFunction)ufunc_reduce, METH_VARARGS | METH_KEYWORDS},
	{"accumulate",  (PyCFunction)ufunc_accumulate, 
	 METH_VARARGS | METH_KEYWORDS},
	{"reduceat",  (PyCFunction)ufunc_reduceat, 
	 METH_VARARGS | METH_KEYWORDS},	
	{"outer", (PyCFunction)ufunc_outer, METH_VARARGS},
	{NULL,		NULL}		/* sentinel */
};



/* construct the string
 y1,y2,...,yn
*/

static void
_makeargs(int num, char ltr, char *str) 
{
	int ind=0;
	int k;
	static char *digits="123456789ABCDE";

	if (num == 1) {
		str[0] = ltr;
		ind = 1;
	}
	else {
		for (k=0; k<num; k++) {
			str[3*k] = ltr;
			str[3*k+1] = digits[k];
			str[3*k+2] = ',';
		}
		/* overwrite last comma */
		ind = 3*k-1;
	}

	str[ind] = '\0';
	return;
}

static char
_typecharfromnum(int num) {
	PyArray_Descr *descr;
	char ret;
	
	descr = PyArray_DescrFromType(num);
	ret = descr->type;
	Py_DECREF(descr);
	return ret;
} 

static PyObject *
ufunc_getattr(PyUFuncObject *self, char *name)
{
	PyObject *obj;
	/* Put docstring first or FindMethod finds it...*/
	/* could so some introspection on name and nin + nout */
	/* to automate the first part of it */
	/* the doc string shouldn't need the calling convention */
	if (strcmp(name, "__doc__") == 0) {
		static char doc[256];
		static char tmp1[3*MAX_ARGS+2];
		static char tmp2[3*MAX_ARGS+2];
		/* construct 
		   y1,y2,,... = name(x1,x2,...) __doc__
		*/		
		_makeargs(self->nout, 'y', tmp1);
		_makeargs(self->nin, 'x', tmp2);
		snprintf(doc, 256, "%s = %s(%s) %s", tmp1, self->name, 
			 tmp2, self->doc);
		return PyString_FromString(doc);
	}
	obj = Py_FindMethod(ufunc_methods, (PyObject *)self, name);
	if (obj != NULL) return obj;
	PyErr_Clear();
	if (strcmp(name, "nin") == 0) {
		return PyInt_FromLong(self->nin);
	}
	else if (strcmp(name, "nout") == 0) {
		return PyInt_FromLong(self->nout);
	}
	else if (strcmp(name, "nargs") == 0) {
		return PyInt_FromLong(self->nargs);
	}
	else if (strcmp(name, "ntypes") == 0) {
		return PyInt_FromLong(self->ntypes);
	}
	else if (strcmp(name, "types") == 0) {
		/* return a list with types grouped
		 input->output */
		PyObject *list;
		PyObject *str;
		int k, j, n, nt=self->ntypes;
		int ni = self->nin;
		int no = self->nout;
		char *t;
		list = PyList_New(nt);
		if (list == NULL) return NULL;
		t = _pya_malloc(no+ni+2);
		n = 0;
		for (k=0; k<nt; k++) {
			for (j=0; j<ni; j++) {
				t[j] = _typecharfromnum(self->types[n]);
				n++;
			}
			t[ni] = '-';
			t[ni+1] = '>';
			for (j=0; j<no; j++) {
				t[ni+2+j] =				\
					_typecharfromnum(self->types[n]);
				n++;
			}
			str = PyString_FromStringAndSize(t, no+ni+2);
			PyList_SET_ITEM(list, k, str);
		}
		_pya_free(t);
		return list;
		
	}
	else if (strcmp(name, "__name__") == 0) {
		return PyString_FromString(self->name);
	}
	else if (strcmp(name, "identity") == 0) {
		switch(self->identity) {
		case PyUFunc_One:
			return PyInt_FromLong(1);
		case PyUFunc_Zero:
			return PyInt_FromLong(0);
		default:
			Py_INCREF(Py_None);
			return Py_None;
		}
	}
	PyErr_SetString(PyExc_AttributeError, name);
	return NULL;
}

#undef _typecharfromnum

static int
ufunc_setattr(PyUFuncObject *self, char *name, PyObject *v) 
{
	return -1;
}

static char Ufunctype__doc__[] = 
	"Optimized functions make it possible to implement arithmetic "\
	"with arrays efficiently";

static PyTypeObject PyUFunc_Type = {
	PyObject_HEAD_INIT(0)
	0,				/*ob_size*/
	"scipy.ufunc",			/*tp_name*/
	sizeof(PyUFuncObject),		/*tp_basicsize*/
	0,				/*tp_itemsize*/
	/* methods */
	(destructor)ufunc_dealloc,	/*tp_dealloc*/
	(printfunc)0,		        /*tp_print*/
	(getattrfunc)ufunc_getattr,	/*tp_getattr*/
	(setattrfunc)ufunc_setattr,	/*tp_setattr*/
	(cmpfunc)0,	          	/*tp_compare*/
	(reprfunc)ufunc_repr,		/*tp_repr*/
	0,			       /*tp_as_number*/
	0,		               /*tp_as_sequence*/
	0,		               /*tp_as_mapping*/
	(hashfunc)0,		/*tp_hash*/
	(ternaryfunc)ufunc_generic_call,		/*tp_call*/
	(reprfunc)ufunc_repr,		/*tp_str*/
		
	/* Space for future expansion */
	0L,0L,0L,0L,
	Ufunctype__doc__ /* Documentation string */
};

/* End of code for ufunc objects */
/* -------------------------------------------------------- */
