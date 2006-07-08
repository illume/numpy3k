#include "arrayobject.h"

#define REFCOUNT NPY_REFCOUNT
#define MAX_ELSIZE 16

#define PyArray_UNSIGNED_TYPES
#define PyArray_SBYTE PyArray_BYTE
#define PyArray_CopyArray PyArray_CopyInto
#define _PyArray_multiply_list PyArray_MultiplyIntList
#define PyArray_ISSPACESAVER(m) NPY_FALSE
#define PyScalarArray_Check PyArray_CheckScalar

#define CONTIGUOUS NPY_CONTIGUOUS
#define OWN_DIMENSIONS 0
#define OWN_STRIDES 0
#define OWN_DATA NPY_OWNDATA
#define SAVESPACE 0
#define SAVESPACEBIT 0




