
/* This expects the following variables to be defined (besides
   the usual ones from pyconfig.h

   SIZEOF_LONG_DOUBLE -- sizeof(long double) or sizeof(double) if no
                         long double is present on platform.
   CHAR_BIT       --     number of bits in a char (usually 8)
                         (should be in limits.h)
*/

#ifndef Py_ARRAYOBJECT_H
#define Py_ARRAYOBJECT_H
#ifdef __cplusplus
extern "C" {
#endif

#include "config.h"

#ifdef PY_ARRAY_TYPES_PREFIX
#  define CAT2(x,y)   x ## y
#  define CAT(x,y)    CAT2(x,y)
#  define NS(name)    CAT(PY_ARRAY_TYPES_PREFIX, name)
#  define longlong    NS(longlong)
#  define ulonglong   NS(ulonglong)
#  define Bool        NS(Bool)
#  define longdouble  NS(longdouble)
#  define byte        NS(byte)
#  define ubyte       NS(ubyte)
#  define ushort      NS(ushort)
#  define uint        NS(uint)
#  define ulong       NS(ulong)
#  define cfloat      NS(cfloat)
#  define cdouble     NS(cdouble)
#  define clongdouble NS(clongdouble)
#  define Int8        NS(Int8)
#  define UInt8       NS(UInt8)
#  define Int16       NS(Int16)
#  define UInt16      NS(UInt16)
#  define Int32       NS(Int32)
#  define UInt32      NS(UInt32)
#  define Int64       NS(Int64)
#  define UInt64      NS(UInt64)
#  define Int128      NS(Int128)
#  define UInt128     NS(UInt128)
#  define Int256      NS(Int256)
#  define UInt256     NS(UInt256)
#  define Float16     NS(Float16)
#  define Complex32   NS(Complex32)
#  define Float32     NS(Float32)
#  define Complex64   NS(Complex64)
#  define Float64     NS(Float64)
#  define Complex128  NS(Complex128)
#  define Float80     NS(Float80)
#  define Complex160  NS(Complex160)
#  define Float96     NS(Float96)
#  define Complex192  NS(Complex192)
#  define Float128    NS(Float128)
#  define Complex256  NS(Complex256)
#  define intp        NS(intp)
#  define uintp       NS(uintp)
#endif

/* There are several places in the code where an array of dimensions is */
/* allocated statically.  This is the size of that static allocation. */

#define MAX_DIMS 40

/* Used for Converter Functions "O&" code in ParseTuple */
#define PY_FAIL 0
#define PY_SUCCEED 1

	/* Helpful to distinguish what is installed */
#define NDARRAY_VERSION 0x0432

	/* Some platforms don't define bool, long long, or long double.
	   Handle that here.
	 */

#ifdef PY_LONG_LONG
typedef PY_LONG_LONG longlong;
typedef unsigned PY_LONG_LONG ulonglong;
#  ifdef _MSC_VER
#    define LONGLONG_FMT         "I64d"
#    define ULONGLONG_FMT        "I64u"
#    define LONGLONG_SUFFIX(x)   (x##i64)
#    define ULONGLONG_SUFFIX(x)  (x##Ui64)
#  else
	/* #define LONGLONG_FMT   "lld"      Another possible variant
           #define ULONGLONG_FMT  "llu"

	   #define LONGLONG_FMT   "qd"   -- BSD perhaps?
	   #define ULONGLONG_FMT   "qu"
	*/
#    define LONGLONG_FMT         "Ld"
#    define ULONGLONG_FMT        "Lu"
#    define LONGLONG_SUFFIX(x)   (x##LL)
#    define ULONGLONG_SUFFIX(x)  (x##ULL)
#  endif
#else
typedef long longlong;
typedef unsigned long ulonglong;
#  define LONGLONG_SUFFIX(x)  (x##L)
#  define ULONGLONG_SUFFIX(x) (x##UL)
#endif

typedef unsigned char Bool;
#ifndef FALSE
#define FALSE 0
#endif
#ifndef TRUE
#define TRUE 1
#endif

#if SIZEOF_LONG_DOUBLE==SIZEOF_DOUBLE
	typedef double longdouble;
        #define LONGDOUBLE_FMT "g"
#else
	typedef long double longdouble;
        #define LONGDOUBLE_FMT "Lg"
#endif

#ifndef Py_USING_UNICODE
#define Py_UNICODE char
#endif


typedef signed char byte;
typedef unsigned char ubyte;
#ifndef _BSD_SOURCE
typedef unsigned short ushort;
typedef unsigned int uint;
typedef unsigned long ulong;
#endif

typedef struct { float real, imag; } cfloat;
typedef struct { double real, imag; } cdouble;
typedef struct {longdouble real, imag;} clongdouble;

enum PyArray_TYPES {    PyArray_BOOL=0,
                        PyArray_BYTE, PyArray_UBYTE,
		        PyArray_SHORT, PyArray_USHORT,
		        PyArray_INT, PyArray_UINT,
			PyArray_LONG, PyArray_ULONG,
                        PyArray_LONGLONG, PyArray_ULONGLONG,
			PyArray_FLOAT, PyArray_DOUBLE, PyArray_LONGDOUBLE,
			PyArray_CFLOAT, PyArray_CDOUBLE, PyArray_CLONGDOUBLE,
			PyArray_OBJECT=17,
                        PyArray_STRING, PyArray_UNICODE,
			PyArray_VOID,
			PyArray_NTYPES,
			PyArray_NOTYPE,
			PyArray_USERDEF=256  /* leave room for characters */
};

	/* basetype array priority */
#define PyArray_PRIORITY 0.0
#define PyArray_BIG_PRIORITY 0.1
	/* default subtype priority */
#define PyArray_SUBTYPE_PRIORITY 1.0

	/* How many floating point types are there */
#define PyArray_NUM_FLOATTYPE 3


	/* We need to match intp to a signed integer of the same size as
	   a pointer variable. uintp to the equivalent unsigned integer
	*/


	/* These characters correspond to the array type and the
	   struct module */

	/*  except 'p' -- signed integer for pointer type */

enum PyArray_TYPECHAR { PyArray_BOOLLTR = '?',
			PyArray_BYTELTR = 'b',
			PyArray_UBYTELTR = 'B',
			PyArray_SHORTLTR = 'h',
			PyArray_USHORTLTR = 'H',
			PyArray_INTLTR = 'i',
			PyArray_UINTLTR = 'I',
			PyArray_LONGLTR = 'l',
			PyArray_ULONGLTR = 'L',  
			PyArray_LONGLONGLTR = 'q',   
			PyArray_ULONGLONGLTR = 'Q',
			PyArray_FLOATLTR = 'f',
			PyArray_DOUBLELTR = 'd',
			PyArray_LONGDOUBLELTR = 'g',
			PyArray_CFLOATLTR = 'F',
			PyArray_CDOUBLELTR = 'D',
			PyArray_CLONGDOUBLELTR = 'G',
			PyArray_OBJECTLTR = 'O',
			PyArray_STRINGLTR = 'S',
			PyArray_UNICODELTR = 'U',
		        PyArray_VOIDLTR = 'V',

			/* No Descriptor, just a define -- this let's
			 Python users specify an array of integers
			 large enough to hold a pointer on the platform*/
			PyArray_INTPLTR = 'p',
			PyArray_UINTPLTR = 'P',

			PyArray_GENBOOLLTR ='b',
			PyArray_SIGNEDLTR = 'i',
			PyArray_UNSIGNEDLTR = 'u',
			PyArray_FLOATINGLTR = 'f',
			PyArray_COMPLEXLTR = 'c'
};

	/* Define bit-width array types and typedefs */

#define MAX_INT8 127
#define MIN_INT8 -128
#define MAX_UINT8 255
#define MAX_INT16 32767
#define MIN_INT16 -32768
#define MAX_UINT16 65535
#define MAX_INT32 2147483647
#define MIN_INT32 (-MAX_INT32 - 1)
#define MAX_UINT32 4294967295U
#define MAX_INT64 LONGLONG_SUFFIX(9223372036854775807)
#define MIN_INT64 (-MAX_INT64 - LONGLONG_SUFFIX(1))
#define MAX_UINT64 ULONGLONG_SUFFIX(18446744073709551615)
#define MAX_INT128 LONGLONG_SUFFIX(85070591730234615865843651857942052864)
#define MIN_INT128 (-MAX_INT128 - LONGLONG_SUFFIX(1))
#define MAX_UINT128 ULONGLONG_SUFFIX(170141183460469231731687303715884105728)
#define MAX_INT256 LONGLONG_SUFFIX(57896044618658097711785492504343953926634992332820282019728792003956564819967)
#define MIN_INT256 (-MAX_INT256 - LONGLONG_SUFFIX(1))
#define MAX_UINT256 ULONGLONG_SUFFIX(115792089237316195423570985008687907853269984665640564039457584007913129639935)

	/* Need to find the number of bits for each type and 
	   make definitions accordingly. 

	   C states that sizeof(char) == 1 by definition 
	   
	   So, just using the sizeof keyword won't help.  

	   It also looks like Python itself uses sizeof(char) quite a
	   bit, which by definition should be 1 all the time.

	   Idea: Make Use of CHAR_BIT which should tell us how many
	   BITS per CHARACTER
	*/

	/* Include platform definitions -- These are in the C89/90 standard */
#include <limits.h>  
#define MAX_BYTE SCHAR_MAX
#define MIN_BYTE SCHAR_MIN
#define MAX_UBYTE UCHAR_MAX
#define MAX_SHORT SHRT_MAX
#define MIN_SHORT SHRT_MIN
#define MAX_USHORT USHRT_MAX
#define MAX_INT   INT_MAX
#ifndef INT_MIN
#define INT_MIN (-INT_MAX - 1)
#endif
#define MIN_INT   INT_MIN
#define MAX_UINT  UINT_MAX
#define MAX_LONG  LONG_MAX
#define MIN_LONG  LONG_MIN
#define MAX_ULONG  ULONG_MAX

#define SIZEOF_LONGDOUBLE SIZEOF_LONG_DOUBLE
#define SIZEOF_LONGLONG SIZEOF_LONG_LONG
#define BITSOF_BOOL sizeof(Bool)*CHAR_BIT
#define BITSOF_CHAR CHAR_BIT
#define BITSOF_SHORT (SIZEOF_SHORT*CHAR_BIT)
#define BITSOF_INT (SIZEOF_INT*CHAR_BIT)
#define BITSOF_LONG (SIZEOF_LONG*CHAR_BIT)
#define BITSOF_LONGLONG (SIZEOF_LONGLONG*CHAR_BIT)
#define BITSOF_FLOAT (SIZEOF_FLOAT*CHAR_BIT)
#define BITSOF_DOUBLE (SIZEOF_DOUBLE*CHAR_BIT)
#define BITSOF_LONGDOUBLE (SIZEOF_LONGDOUBLE*CHAR_BIT)


#if BITSOF_LONG == 8
#define PyArray_INT8 PyArray_LONG
#define PyArray_UINT8 PyArray_ULONG
	typedef long Int8;
	typedef unsigned long UInt8;
#define STRBITSOF_LONG "8"
#elif BITSOF_LONG == 16
#define PyArray_INT16 PyArray_LONG
#define PyArray_UINT16 PyArray_ULONG
	typedef long Int16;
	typedef unsigned long UInt16;
#define STRBITSOF_LONG "16"
#elif BITSOF_LONG == 32
#define PyArray_INT32 PyArray_LONG
#define PyArray_UINT32 PyArray_ULONG
	typedef long Int32;
	typedef unsigned long UInt32;
#define STRBITSOF_LONG "32"
#elif BITSOF_LONG == 64
#define PyArray_INT64 PyArray_LONG
#define PyArray_UINT64 PyArray_ULONG
	typedef long Int64;
	typedef unsigned long UInt64;
#define STRBITSOF_LONG "64"
#elif BITSOF_LONG == 128
#define PyArray_INT128 PyArray_LONG
#define PyArray_UINT128 PyArray_ULONG
	typedef long Int128;
	typedef unsigned long UInt128;
#define STRBITSOF_LONG "128"
#endif

#if BITSOF_LONGLONG == 8
#  ifndef PyArray_INT8
#    define PyArray_INT8 PyArray_LONGLONG
#    define PyArray_UINT8 PyArray_ULONGLONG
	typedef longlong Int8;
	typedef ulonglong UInt8;
#  endif
#  define MAX_LONGLONG MAX_INT8
#  define MIN_LONGLONG MIN_INT8
#  define MAX_ULONGLONG MAX_UINT8
#define STRBITSOF_LONGLONG "8"
#elif BITSOF_LONGLONG == 16
#  ifndef PyArray_INT16
#    define PyArray_INT16 PyArray_LONGLONG
#    define PyArray_UINT16 PyArray_ULONGLONG
	typedef longlong Int16;
	typedef ulonglong UInt16;
#  endif
#  define MAX_LONGLONG MAX_INT16
#  define MIN_LONGLONG MIN_INT16
#  define MAX_ULONGLONG MAX_UINT16
#define STRBITSOF_LONGLONG "16"
#elif BITSOF_LONGLONG == 32
#  ifndef PyArray_INT32
#    define PyArray_INT32 PyArray_LONGLONG
#    define PyArray_UINT32 PyArray_ULONGLONG
	typedef longlong Int32;
	typedef ulonglong UInt32;
#  endif
#  define MAX_LONGLONG MAX_INT32
#  define MIN_LONGLONG MIN_INT32
#  define MAX_ULONGLONG MAX_UINT32
#define STRBITSOF_LONGLONG "32"
#elif BITSOF_LONGLONG == 64
#  ifndef PyArray_INT64
#    define PyArray_INT64 PyArray_LONGLONG
#    define PyArray_UINT64 PyArray_ULONGLONG
	typedef longlong Int64;
	typedef ulonglong UInt64;
#  endif
#  define MAX_LONGLONG MAX_INT64
#  define MIN_LONGLONG MIN_INT64
#  define MAX_ULONGLONG MAX_UINT64
#define STRBITSOF_LONGLONG "64"
#elif BITSOF_LONGLONG == 128
#  ifndef PyArray_INT128
#    define PyArray_INT128 PyArray_LONGLONG
#    define PyArray_UINT128 PyArray_ULONGLONG
	typedef longlong Int128;
	typedef ulonglong UInt128;
#  endif
#  define MAX_LONGLONG MAX_INT128
#  define MIN_LONGLONG MIN_INT128
#  define MAX_ULONGLONG MAX_UINT128
#define STRBITSOF_LONGLONG "128"
#elif BITSOF_LONGLONG == 256
#  define PyArray_INT256 PyArray_LONGLONG
#  define PyArray_UINT256 PyArray_ULONGLONG
	typedef longlong Int256;
	typedef ulonglong UInt256;
#  define MAX_LONGLONG MAX_INT256
#  define MIN_LONGLONG MIN_INT256
#  define MAX_ULONGLONG MAX_UINT256
#define STRBITSOF_LONGLONG "256"
#endif

#if BITSOF_INT == 8
#ifndef PyArray_INT8
#define PyArray_INT8 PyArray_INT
#define PyArray_UINT8 PyArray_UINT
	typedef int Int8;
	typedef unsigned int UInt8;
#endif
#define STRBITSOF_INT "8"
#elif BITSOF_INT == 16
#ifndef PyArray_INT16
#define PyArray_INT16 PyArray_INT
#define PyArray_UINT16 PyArray_UINT
	typedef int Int16;
	typedef unsigned int UInt16;
#endif
#define STRBITSOF_INT "16"
#elif BITSOF_INT == 32
#ifndef PyArray_INT32
#define PyArray_INT32 PyArray_INT
#define PyArray_UINT32 PyArray_UINT
	typedef int Int32;
	typedef unsigned int UInt32;
#endif
#define STRBITSOF_INT "32"
#elif BITSOF_INT == 64
#ifndef PyArray_INT64
#define PyArray_INT64 PyArray_INT
#define PyArray_UINT64 PyArray_UINT
	typedef int Int64;
	typedef unsigned int UInt64;
#endif
#define STRBITSOF_INT "64"
#elif BITSOF_INT == 128
#ifndef PyArray_INT128
#define PyArray_INT128 PyArray_INT
#define PyArray_UINT128 PyArray_UINT
	typedef int Int128;
	typedef unsigned int UInt128;
#endif
#define STRBITSOF_INT "128"
#endif

#if BITSOF_SHORT == 8
#ifndef PyArray_INT8
#define PyArray_INT8 PyArray_SHORT
#define PyArray_UINT8 PyArray_USHORT
	typedef short Int8;
	typedef unsigned short UInt8;
#endif
#define STRBITSOF_SHORT "8"
#elif BITSOF_SHORT == 16
#ifndef PyArray_INT16
#define PyArray_INT16 PyArray_SHORT
#define PyArray_UINT16 PyArray_USHORT
	typedef short Int16;
	typedef unsigned short UInt16;
#endif
#define STRBITSOF_SHORT "16"
#elif BITSOF_SHORT == 32
#ifndef PyArray_INT32
#define PyArray_INT32 PyArray_SHORT
#define PyArray_UINT32 PyArray_USHORT
	typedef short Int32;
	typedef unsigned short UInt32;
#endif
#define STRBITSOF_SHORT "32"
#elif BITSOF_SHORT == 64
#ifndef PyArray_INT64
#define PyArray_INT64 PyArray_SHORT
#define PyArray_UINT64 PyArray_USHORT
	typedef short Int64;
	typedef unsigned short UInt64;
#endif
#define STRBITSOF_SHORT "64"
#elif BITSOF_SHORT == 128
#ifndef PyArray_INT128
#define PyArray_INT128 PyArray_SHORT
#define PyArray_UINT128 PyArray_USHORT
	typedef short Int128;
	typedef unsigned short UInt128;
#endif
#define STRBITSOF_SHORT "128"
#endif


#if BITSOF_CHAR == 8
#ifndef PyArray_INT8
#define PyArray_INT8 PyArray_BYTE
#define PyArray_UINT8 PyArray_UBYTE
	typedef signed char Int8;
	typedef unsigned char UInt8;
#endif
#define STRBITSOF_CHAR "8"
#elif BITSOF_CHAR == 16
#ifndef PyArray_INT16
#define PyArray_INT16 PyArray_BYTE
#define PyArray_UINT16 PyArray_UBYTE
	typedef signed char Int16;
	typedef unsigned char UInt16;
#endif
#define STRBITSOF_CHAR "16"
#elif BITSOF_CHAR == 32
#ifndef PyArray_INT32
#define PyArray_INT32 PyArray_BYTE
#define PyArray_UINT32 PyArray_UBYTE
	typedef signed char Int32;
	typedef unsigned char UInt32;
#endif
#define STRBITSOF_CHAR "32"
#elif BITSOF_CHAR == 64
#ifndef PyArray_INT64
#define PyArray_INT64 PyArray_BYTE
#define PyArray_UINT64 PyArray_UBYTE
	typedef signed char Int64;
	typedef unsigned char UInt64;
#endif
#define STRBITSOF_CHAR "64"
#elif BITSOF_CHAR == 128
#ifndef PyArray_INT128
#define PyArray_INT128 PyArray_BYTE
#define PyArray_UINT128 PyArray_UBYTE
	typedef signed char Int128;
	typedef unsigned char UInt128;
#endif
#define STRBITSOF_CHAR "128"
#endif



#if BITSOF_DOUBLE == 16
#define STRBITSOF_DOUBLE "16"
#define STRBITSOF_CDOUBLE "32"
#ifndef PyArray_FLOAT16
#define PyArray_FLOAT16 PyArray_DOUBLE
#define PyArray_COMPLEX32 PyArray_CDOUBLE
	typedef  double Float16;
	typedef cdouble Complex32;
#endif
#elif BITSOF_DOUBLE == 32
#define STRBITSOF_DOUBLE "32"
#define STRBITSOF_CDOUBLE "64"
#ifndef PyArray_FLOAT32
#define PyArray_FLOAT32 PyArray_DOUBLE
#define PyArray_COMPLEX64 PyArray_CDOUBLE
	typedef double Float32;
	typedef cdouble Complex64;
#endif
#elif BITSOF_DOUBLE == 64
#define STRBITSOF_DOUBLE "64"
#define STRBITSOF_CDOUBLE "128"
#ifndef PyArray_FLOAT64
#define PyArray_FLOAT64 PyArray_DOUBLE
#define PyArray_COMPLEX128 PyArray_CDOUBLE
	typedef double Float64;
	typedef cdouble Complex128;
#endif
#elif BITSOF_DOUBLE == 80
#define STRBITSOF_DOUBLE "80"
#define STRBITSOF_CDOUBLE "160"
#ifndef PyArray_FLOAT80
#define PyArray_FLOAT80 PyArray_DOUBLE
#define PyArray_COMPLEX160 PyArray_CDOUBLE
	typedef double Float80;
	typedef cdouble Complex160;
#endif
#elif BITSOF_DOUBLE == 96
#define STRBITSOF_DOUBLE "96"
#define STRBITSOF_CDOUBLE "192"
#ifndef PyArray_FLOAT96
#define PyArray_FLOAT96 PyArray_DOUBLE
#define PyArray_COMPLEX192 PyArray_CDOUBLE
	typedef double Float96;
	typedef cdouble Complex192;
#endif
#elif BITSOF_DOUBLE == 128
#define STRBITSOF_DOUBLE "128"
#define STRBITSOF_CDOUBLE "256"
#ifndef PyArray_FLOAT128
#define PyArray_FLOAT128 PyArray_DOUBLE
#define PyArray_COMPLEX256 PyArray_CDOUBLE
	typedef double Float128;
	typedef cdouble Complex256;
#endif
#endif



#if BITSOF_FLOAT == 16
#define STRBITSOF_FLOAT "16"
#define STRBITSOF_CFLOAT "32"
#ifndef PyArray_FLOAT16
#define PyArray_FLOAT16 PyArray_FLOAT
#define PyArray_COMPLEX32 PyArray_CFLOAT
	typedef float Float16;
	typedef cfloat Complex32;
#endif
#elif BITSOF_FLOAT == 32
#define STRBITSOF_FLOAT "32"
#define STRBITSOF_CFLOAT "64"
#ifndef PyArray_FLOAT32
#define PyArray_FLOAT32 PyArray_FLOAT
#define PyArray_COMPLEX64 PyArray_CFLOAT
	typedef float Float32;
	typedef cfloat Complex64;
#endif
#elif BITSOF_FLOAT == 64
#define STRBITSOF_FLOAT "64"
#define STRBITSOF_CFLOAT "128"
#ifndef PyArray_FLOAT64
#define PyArray_FLOAT64 PyArray_FLOAT
#define PyArray_COMPLEX128 PyArray_CFLOAT
	typedef float Float64;
	typedef cfloat Complex128;
#endif
#elif BITSOF_FLOAT == 80
#define STRBITSOF_FLOAT "80"
#define STRBITSOF_CFLOAT "160"
#ifndef PyArray_FLOAT80
#define PyArray_FLOAT80 PyArray_FLOAT
#define PyArray_COMPLEX160 PyArray_CFLOAT
	typedef float Float80;
	typedef cfloat Complex160;
#endif
#elif BITSOF_FLOAT == 96
#define STRBITSOF_FLOAT "96"
#define STRBITSOF_CFLOAT "192"
#ifndef PyArray_FLOAT96
#define PyArray_FLOAT96 PyArray_FLOAT
#define PyArray_COMPLEX192 PyArray_CFLOAT
	typedef float Float96;
	typedef cfloat Complex192;
#endif
#elif BITSOF_FLOAT == 128
#define STRBITSOF_FLOAT "128"
#define STRBITSOF_CFLOAT "256"
#ifndef PyArray_FLOAT128
#define PyArray_FLOAT128 PyArray_FLOAT
#define PyArray_COMPLEX256 PyArray_CFLOAT
	typedef float Float128;
	typedef cfloat Complex256;
#endif
#endif


#if BITSOF_LONGDOUBLE == 16
#define STRBITSOF_LONGDOUBLE "16"
#define STRBITSOF_CLONGDOUBLE "32"
#ifndef PyArray_FLOAT16
#define PyArray_FLOAT16 PyArray_LONGDOUBLE
#define PyArray_COMPLEX32 PyArray_CLONGDOUBLE
	typedef  longdouble Float16;
	typedef clongdouble Complex32;
#endif
#elif BITSOF_LONGDOUBLE == 32
#define STRBITSOF_LONGDOUBLE "32"
#define STRBITSOF_CLONGDOUBLE "64"
#ifndef PyArray_FLOAT32
#define PyArray_FLOAT32 PyArray_LONGDOUBLE
#define PyArray_COMPLEX64 PyArray_CLONGDOUBLE
	typedef longdouble Float32;
	typedef clongdouble Complex64;
#endif
#elif BITSOF_LONGDOUBLE == 64
#define STRBITSOF_LONGDOUBLE "64"
#define STRBITSOF_CLONGDOUBLE "128"
#ifndef PyArray_FLOAT64
#define PyArray_FLOAT64 PyArray_LONGDOUBLE
#define PyArray_COMPLEX128 PyArray_CLONGDOUBLE
	typedef longdouble Float64;
	typedef clongdouble Complex128;
#endif
#elif BITSOF_LONGDOUBLE == 80
#define STRBITSOF_LONGDOUBLE "80"
#define STRBITSOF_CLONGDOUBLE "160" 
#ifndef PyArray_FLOAT80
#define PyArray_FLOAT80 PyArray_LONGDOUBLE
#define PyArray_COMPLEX160 PyArray_CLONGDOUBLE
	typedef longdouble Float80;
	typedef clongdouble Complex160;
#endif
#elif BITSOF_LONGDOUBLE == 96
#define STRBITSOF_LONGDOUBLE "96"
#define STRBITSOF_CLONGDOUBLE "192"
#ifndef PyArray_FLOAT96
#define PyArray_FLOAT96 PyArray_LONGDOUBLE
#define PyArray_COMPLEX192 PyArray_CLONGDOUBLE
	typedef longdouble Float96;
	typedef clongdouble Complex192;
#endif
#elif BITSOF_LONGDOUBLE == 128
#define STRBITSOF_LONGDOUBLE "128"
#define STRBITSOF_CLONGDOUBLE "256"
#ifndef PyArray_FLOAT128
#define PyArray_FLOAT128 PyArray_LONGDOUBLE
#define PyArray_COMPLEX256 PyArray_CLONGDOUBLE
	typedef longdouble Float128;
	typedef clongdouble Complex256;
#endif
#elif BITSOF_LONGDOUBLE == 256
#define STRBITSOF_LONGDOUBLE "256"
#define STRBITSOF_CLONGDOUBLE "512"
#define PyArray_FLOAT256 PyArray_LONGDOUBLE
#define PyArray_COMPLEX512 PyArray_CLONGDOUBLE
	typedef longdouble Float256;
	typedef clongdouble Complex512;
#endif


	/* End of typedefs for numarray style bit-width names */

/* This is to typedef Intp to the appropriate pointer size for this platform.
 * Py_intptr_t, Py_uintptr_t are defined in pyport.h. */
typedef Py_intptr_t intp;
typedef Py_uintptr_t uintp;

#define INTP_FMT "d"

#if SIZEOF_PY_INTPTR_T == SIZEOF_INT  
	#define PyArray_INTP PyArray_INT
	#define PyArray_UINTP PyArray_UINT
        #define PyIntpArrType_Type PyIntArrType_Type
        #define PyUIntpArrType_Type PyUIntArrType_Type
	#define MAX_INTP MAX_INT
	#define MIN_INTP MIN_INT
	#define MAX_UINTP MAX_UINT
#elif SIZEOF_PY_INTPTR_T == SIZEOF_LONG
	#define PyArray_INTP PyArray_LONG
	#define PyArray_UINTP PyArray_ULONG
        #define PyIntpArrType_Type PyLongArrType_Type
        #define PyUIntpArrType_Type PyULongArrType_Type
	#define MAX_INTP MAX_LONG
	#define MIN_INTP MIN_LONG
	#define MAX_UINTP MAX_ULONG
        #undef INTP_FMT
        #define INTP_FMT "ld"
#elif defined(PY_LONG_LONG) && (SIZEOF_PY_INTPTR_T == SIZEOF_LONG_LONG)
	#define PyArray_INTP PyArray_LONGLONG
	#define PyArray_UINTP PyArray_ULONGLONG
        #define PyIntpArrType_Type PyLongLongArrType_Type
        #define PyUIntpArrType_Type PyULongLongArrType_Type
	#define MAX_INTP MAX_LONGLONG
	#define MIN_INTP MIN_LONGLONG
	#define MAX_UINTP MAX_ULONGLONG
        #undef INTP_FMT
        #define INTP_FMT "Ld"
#endif

#define ERR(str) fprintf(stderr, #str); fflush(stderr);
#define ERR2(str) fprintf(stderr, str); fflush(stderr);

  /* Macros to define how array, and dimension/strides data is
     allocated. 
  */

  /* Data buffer */
#define PyDataMem_NEW(size) ((char *)malloc(size))
  /* #define PyArrayMem_NEW(size) PyMem_NEW(char, size)*/
#define PyDataMem_FREE(ptr)  free(ptr)
  /* #define PyArrayMem_FREE(ptr) PyMem_Free(ptr) */
#define PyDataMem_RENEW(ptr,size) ((char *)realloc(ptr,size))

  /* Dimensions and strides */
#define PyDimMem_NEW(size) ((intp *)malloc(size*sizeof(intp)))
#define PyDimMem_FREE(ptr) free(ptr)
#define PyDimMem_RENEW(ptr,size) ((intp *)realloc(ptr,size*sizeof(intp)))


  /* These must deal with unaligned and swapped data if necessary */
typedef PyObject * (PyArray_GetItemFunc) (void *, void *);
typedef int (PyArray_SetItemFunc)(PyObject *, void *, void *);

typedef void (PyArray_CopySwapNFunc)(void *, void *, intp, int, int);
typedef void (PyArray_CopySwapFunc)(void *, void *, int, int);
typedef Bool (PyArray_NonzeroFunc)(void *, void *);


  /* These assume aligned and notswapped data -- a buffer will be
      used before or contiguous data will be obtained
  */
typedef int (PyArray_CompareFunc)(const void *, const void *, void *);
typedef int (PyArray_ArgFunc)(void*, intp, intp*, void *);
typedef void (PyArray_DotFunc)(void *, intp, void *, intp, void *, intp, 
			       void *);
typedef void (PyArray_VectorUnaryFunc)(void *, void *, intp, void *, void *);
typedef int (PyArray_ScanFunc)(FILE *, void *, void *, void *);


typedef struct {
 	PyTypeObject *typeobj;  /* the type object for this type */
	char kind;              /* kind for this type */
	char type;              /* character representing this type */
	int type_num;           /* number representing this type */
	int elsize;             /* element size for this type -- 
				   or 0 if variable */
       	int alignment;          /* alignment needed for this type */

	/* Functions to cast to all other standard types*/
	PyArray_VectorUnaryFunc *cast[PyArray_NTYPES];

	/* Functions to get and set items with standard
	   Python types -- not array scalars */
	PyArray_GetItemFunc *getitem;
	PyArray_SetItemFunc *setitem;

	/* Function to compare items */
	PyArray_CompareFunc *compare;

  	/* Function to select largest */
	PyArray_ArgFunc *argmax;

	/* Function to compute dot product */
	PyArray_DotFunc	*dotfunc;	   
	
	/* Function to scan an ASCII file and 
	   place a single value plus possible separator */
	PyArray_ScanFunc *scanfunc;

	/* Copy and/or swap data.  Memory areas may not overlap */
	/*  Use memmove first if they might */
	PyArray_CopySwapNFunc *copyswapn;
        PyArray_CopySwapFunc *copyswap;
	
	/* Function to determine if data is zero or not */
	PyArray_NonzeroFunc *nonzero;

} PyArray_Descr;


typedef struct PyArrayObject {
	PyObject_HEAD
	char *data;             /* pointer to raw data buffer */
	int nd;                 /* number of dimensions, also called ndim */ 
	intp *dimensions;       /* size in each dimension */
        intp *strides;          /* bytes to jump to get to the 
				   next element in each dimension */
	PyObject *base;         /* This object should be decref'd
				   upon deletion of array */
	                        /* For views it points to the original array */
	                        /* For creation from buffer object it points 
				   to an object that shold be decref'd on 
				   deletion */
	                        /* For UPDATEIFCOPY flag this is an array 
				   to-be-updated upon deletion of this one */
	PyArray_Descr *descr;   /* Pointer to type structure */
	int flags;              /* Flags describing array -- see below*/
	int itemsize;           /* needed for Flexible size arrays:
                                   CHAR, UNICODE, and VOID arrays
 			         */ 
	PyObject *weakreflist;  /* For weakreferences */

} PyArrayObject;

#define fortran fortran_  /* For some compilers */

typedef struct {   /* Just the type_num and itemsize variables 
		      for use in the TypeNum Converter function */
	int type_num; /* The enumerated type number */
	int itemsize; /* The itemsize desired (for flexible types) */
	int fortran;  /* Set to 1 if fortran-defined strides is desired */
} PyArray_Typecode;

typedef struct {
        intp *ptr;
        int len;
} PyArray_Dims;


/* Mirrors buffer object to ptr */

typedef struct {
        PyObject_HEAD
        PyObject *base;
        void *ptr;
        intp len;
        int flags;        
} PyArray_Chunk;

/* Array flags */
#define CONTIGUOUS     1      /* means c-style contiguous (last index
			       varies the fastest) data elements right
			      after each other. */

	                      /* All 0-d arrays are CONTIGUOUS and FORTRAN
				 contiguous.  If a 1-d array is CONTIGUOUS
				 it is also FORTRAN contiguous 
			      */

#define FORTRAN    2    /* set if array is a contiguous Fortran array */
                       /*  first index varies the fastest in memory
                           (strides array is reverse of C-contiguous
			           array)*/

#define OWNDATA        4
#define OWN_DATA       OWNDATA

	/* array never has these three set -- FromAny flags only */
#define FORCECAST     0x010    
#define ENSURECOPY    0x020
#define ENSUREARRAY   0x040

#define ALIGNED       0x100
#define NOTSWAPPED    0x200
#define WRITEABLE     0x400


	/* If this flags is set, then base contains a pointer to 
	   an array of the same size that should be updated with the 
	   current contents of this array when this array is deallocated
	*/
#define UPDATEIFCOPY  0x1000


/* Size of internal buffers used for alignment */
#define PyArray_BUFSIZE 10000
#define PyArray_MIN_BUFSIZE 5
#define PyArray_MAX_BUFSIZE 100000000

#define BEHAVED_FLAGS ALIGNED | NOTSWAPPED | WRITEABLE
#define BEHAVED_FLAGS_RO ALIGNED | NOTSWAPPED
#define CARRAY_FLAGS CONTIGUOUS | BEHAVED_FLAGS
#define FARRAY_FLAGS FORTRAN | BEHAVED_FLAGS
#define DEFAULT_FLAGS CARRAY_FLAGS

#define UPDATE_ALL_FLAGS CONTIGUOUS | FORTRAN | ALIGNED


/*
 * C API:  consists of Macros and functions.  The MACROS are defined here. 
 */


#define PyArray_CHKFLAGS(m, FLAGS) \
	((((PyArrayObject *)(m))->flags & (FLAGS)) == (FLAGS))
#define PyArray_ISCONTIGUOUS(m) PyArray_CHKFLAGS(m, CONTIGUOUS)
#define PyArray_ISWRITEABLE(m) PyArray_CHKFLAGS(m, WRITEABLE)
#define PyArray_ISALIGNED(m) PyArray_CHKFLAGS(m, ALIGNED)

#define PyArray_ISCARRAY(m) PyArray_CHKFLAGS(m, CARRAY_FLAGS)
#define PyArray_ISFARRAY(m) PyArray_CHKFLAGS(m, FARRAY_FLAGS)
#define PyArray_ISBEHAVED(m) PyArray_CHKFLAGS(m, BEHAVED_FLAGS)
#define PyArray_ISBEHAVED_RO(m) PyArray_CHKFLAGS(m, BEHAVED_FLAGS_RO)


#ifndef MAX
#define MAX(a,b) (((a)>(b))?(a):(b))
#endif
#ifndef MIN
#define MIN(a,b) (((a)<(b))?(a):(b))
#endif

        /* Useful if a and b have to be evaluated.  */

#define tMAX(a,b,typ) {typ _x_=(a); typ _y_=(b); _x_>_y_ ? _x_ : _y_}
#define tMIN(a,b,typ) {typ _x_=(a); typ _y_=(b); _x_<_y_ ? _x_ : _y_}

#if defined(ALLOW_THREADS)
#define BEGIN_THREADS_DEF PyThreadState *_save;
#define BEGIN_THREADS _save = PyEval_SaveThread();
#define END_THREADS   PyEval_RestoreThread(_save);
#define ALLOW_C_API_DEF  PyGILState_STATE __save__;
#define ALLOW_C_API      __save__ = PyGILState_Ensure();
#define DISABLE_C_API    PyGILState_Release(__save__);
#else
#define BEGIN_THREADS_DEF
#define BEGIN_THREADS
#define END_THREADS
#define ALLOW_C_API_DEF
#define	ALLOW_C_API    
#define	DISABLE_C_API  
#endif

typedef struct {
        PyObject_HEAD
	int               nd_m1;            /* number of dimensions - 1 */
        intp		  index, size;
	intp              coordinates[MAX_DIMS];/* N-dimensional loop */
        intp              dims_m1[MAX_DIMS];    /* ao->dimensions - 1 */
	intp              strides[MAX_DIMS];    /* ao->strides or fake */
	intp              backstrides[MAX_DIMS];/* how far to jump back */
	intp              factors[MAX_DIMS];     /* shape factors */
	PyArrayObject     *ao;
	char              *dataptr;        /* pointer to current item*/
        Bool              contiguous;
} PyArrayIterObject;


/* Iterator API */ 
#define PyArrayIter_Check(op) PyObject_TypeCheck(op, &PyArrayIter_Type)
	
#define PyArray_ITER_RESET(it) {					\
	it->index = 0;						        \
	it->dataptr = it->ao->data;					\
	memset(it->coordinates, 0, (it->nd_m1+1)*sizeof(intp));		\
}


#define PyArray_ITER_NEXT(it) {				\
	it->index++;					\
	if (it->contiguous)  it->dataptr += it->ao->itemsize;	       \
	else {								\
		int _i_;						\
		for (_i_ = it->nd_m1; _i_ >= 0; _i_--) {		\
			if (it->coordinates[_i_] <			\
			    it->dims_m1[_i_]) {				\
				it->coordinates[_i_]++;			\
				it->dataptr += it->strides[_i_];	\
				break;					\
			}						\
			else {						\
				it->coordinates[_i_] = 0;		\
				it->dataptr -= it->backstrides[_i_];	\
			}						\
		}							\
	}								\
}

#define PyArray_ITER_GOTO(it, destination) {				\
		int _i_;						\
		it->index = 0;						\
		it->dataptr = it->ao->data;				\
		for (_i_ = it->nd_m1; _i_>=0; _i_--) {			\
			it->dataptr += destination[_i_] *		\
				it->strides[_i_];			\
			it->coordinates[_i_] = destination[_i_];	\
			it->index += destination[_i_] *			\
				( _i_==it->nd_m1 ? 1 :			\
				  it->dims_m1[i+1]+1) ;	  	        \
		}							\
	} 

#define PyArray_ITER_GOTO1D(it, ind) {                                  \
		int _i_;						\
		intp _lind_ = (intp) (ind);				\
		it->index = _lind_;					\
		if (it->contiguous)					\
			it->dataptr = it->ao->data + (ind) *		\
				it->ao->itemsize;			\
		else {							\
			it->dataptr = it->ao->data;			\
			for (_i_ = 0; _i_<=it->nd_m1; _i_++) {		\
				it->dataptr += (_lind_ / it->factors[_i_]) \
					* it->strides[_i_];		\
				_lind_ %= it->factors[_i_];		\
			}						\
		}							\
}

/* Not constructed anywhere.  Just serves as a standard type that
   PyArray_Broadcast expects.

   Any object passed to PyArray_Broadcast must be binary compatible with 
   this structure.    
*/


typedef struct {
	PyObject_HEAD

	int                     numiter;               /* number of iters */
	intp                    size;                  /* broadcasted size */
	intp                    index;                 /* current index */
	int                     nd;                    /* number of dims */
	intp                    dimensions[MAX_DIMS];  /* dimensions */
	PyArrayIterObject       *iters[MAX_DIMS];      /* iterators */
} PyArrayMultiIterObject;  
	

/* Store the information needed for fancy-indexing over an array */

typedef struct {
	PyObject_HEAD
	/* Multi-iterator portion --- needs to be present in this order to 
	   work with PyArray_Broadcast */

	int                     numiter;               /* number of index-array
							  iterators */
	intp                    size;                  /* size of broadcasted 
							  result */
	intp                    index;                 /* current index */
	int                     nd;                    /* number of dims */
	intp                    dimensions[MAX_DIMS];  /* dimensions */
	PyArrayIterObject       *iters[MAX_DIMS];      /* index object 
							  iterators */
	PyArrayIterObject       *ait;                   /* flat Iterator for 
							  underlying array */

	/* flat iterator for subspace (when numiter < nd) */
	PyArrayIterObject       *subspace;

	/* if subspace iteration, then this is the array of 
	   axes in the underlying array represented by the
	   index objects */
	int                     iteraxes[MAX_DIMS];
	/* if subspace iteration, the these are the coordinates
	   to the start of the subspace.
	*/
	intp                    bscoord[MAX_DIMS];

	
	PyObject                *indexobj;             /* reference to 
							  creating obj */
	int                     view;
	int                     consec;
	char                    *dataptr;

} PyArrayMapIterObject;


/* Map Iterator API */ 
#define PyArrayMapIter_Check(op) PyObject_TypeCheck(op, &PyArrayMapIter_Type)


#define PyArray_NDIM(obj) (((PyArrayObject *)(obj))->nd)
#define PyArray_ISONESEGMENT(m) (PyArray_NDIM(m) == 0 || PyArray_CHKFLAGS(m, CONTIGUOUS) || \
				 PyArray_CHKFLAGS(m, FORTRAN))
#define PyArray_ISFORTRAN(m) (PyArray_CHKFLAGS(m, FORTRAN) && (PyArray_NDIM(m) > 1))
#define PyArray_DATA(obj) (((PyArrayObject *)(obj))->data)
#define PyArray_DIMS(obj) (((PyArrayObject *)(obj))->dimensions)
#define PyArray_STRIDES(obj) (((PyArrayObject *)(obj))->strides)
#define PyArray_DIM(obj,n) (((PyArrayObject *)(obj))->dimensions[n])
#define PyArray_STRIDE(obj,n) (((PyArrayObject *)(obj))->strides[n])
#define PyArray_BASE(obj) (((PyArrayObject *)(obj))->base)
#define PyArray_DESCR(obj) (((PyArrayObject *)(obj))->descr)
#define PyArray_FLAGS(obj) (((PyArrayObject *)(obj))->flags)
#define PyArray_ITEMSIZE(obj) (((PyArrayObject *)(obj))->itemsize)
#define PyArray_TYPE(obj) (((PyArrayObject *)(obj))->descr->type_num)
#define PyArray_GETITEM(obj,itemptr)			\
	((PyArrayObject *)(obj))->descr->getitem((char *)itemptr,	\
						 (PyArrayObject *)obj);
#define PyArray_SETITEM(obj,itemptr,v)					\
	(obj)->descr->setitem((PyObject *)v,(char *)(itemptr),		\
			      (PyArrayObject *)(obj));


#define PyTypeNum_ISBOOL(type) (type == PyArray_BOOL)
#define PyTypeNum_ISUNSIGNED(type) ((type == PyArray_UBYTE) || \
				 (type == PyArray_USHORT) || \
				 (type == PyArray_UINT) ||	\
				 (type == PyArray_ULONG) || \
				 (type == PyArray_ULONGLONG))

#define PyTypeNum_ISSIGNED(type) ((type == PyArray_BYTE) ||	\
			       (type == PyArray_SHORT) ||	\
			       (type == PyArray_INT) ||	\
			       (type == PyArray_LONG) ||	\
			       (type == PyArray_LONGLONG))

#define PyTypeNum_ISINTEGER(type) ((type >= PyArray_BYTE) &&	\
				(type <= PyArray_ULONGLONG))
       
#define PyTypeNum_ISFLOAT(type) ((type >= PyArray_FLOAT) &&  \
			      (type <= PyArray_LONGDOUBLE))

#define PyTypeNum_ISNUMBER(type) (type <= PyArray_CLONGDOUBLE)

#define PyTypeNum_ISSTRING(type) ((type == PyArray_UCHAR) || \
			       (type == PyArray_UNICODE))

#define PyTypeNum_ISCOMPLEX(type) ((type >= PyArray_CFLOAT) && \
				(type <= PyArray_CLONGDOUBLE))
	
#define PyTypeNum_ISPYTHON(type) ((type == PyArray_LONG) || \
				  (type == PyArray_DOUBLE) ||	\
				  (type == PyArray_CDOUBLE) ||	\
		                  (type == PyArray_BOOL) || \
				  (type == PyArray_OBJECT ))

#define PyTypeNum_ISFLEXIBLE(type) ((type==PyArray_STRING) || \
				    (type==PyArray_UNICODE) ||	\
				    (type==PyArray_VOID))

#define PyTypeNum_ISUSERDEF(type) ((type >= PyArray_USERDEF) && \
				   (type < PyArray_USERDEF+\
				    PyArray_NUMUSERTYPES))

#define PyTypeNum_ISEXTENDED(type) (PyTypeNum_ISFLEXIBLE(type) ||  \
                                    PyTypeNum_ISUSERDEF(type))
				    
#define PyTypeNum_ISOBJECT(type) ((type) == PyArray_OBJECT)

#define PyArray_ISBOOL(obj) PyTypeNum_ISBOOL(PyArray_TYPE(obj))
#define PyArray_ISUNSIGNED(obj) PyTypeNum_ISUNSIGNED(PyArray_TYPE(obj))
#define PyArray_ISSIGNED(obj) PyTypeNum_ISSIGNED(PyArray_TYPE(obj))
#define PyArray_ISINTEGER(obj) PyTypeNum_ISINTEGER(PyArray_TYPE(obj))
#define PyArray_ISFLOAT(obj) PyTypeNum_ISFLOAT(PyArray_TYPE(obj))
#define PyArray_ISNUMBER(obj) PyTypeNum_ISNUMBER(PyArray_TYPE(obj))
#define PyArray_ISSTRING(obj) PyTypeNum_ISSTRING(PyArray_TYPE(obj))
#define PyArray_ISCOMPLEX(obj) PyTypeNum_ISCOMPLEX(PyArray_TYPE(obj))
#define PyArray_ISPYTHON(obj) PyTypeNum_ISPYTHON(PyArray_TYPE(obj))
#define PyArray_ISFLEXIBLE(obj) PyTypeNum_ISFLEXIBLE(PyArray_TYPE(obj))
#define PyArray_ISUSERDEF(obj) PyTypeNum_ISUSERDEF(PyArray_TYPE(obj))
#define PyArray_ISEXTENDED(obj) PyTypeNum_ISEXTENDED(PyArray_TYPE(obj))
#define PyArray_ISOBJECT(obj) PyTypeNum_ISOBJECT(PyArray_TYPE(obj))

/* Object arrays ignore notswapped flag */
#define PyArray_ISNOTSWAPPED(m) (PyArray_CHKFLAGS(m, NOTSWAPPED) || \
				 PyArray_ISOBJECT(m))


typedef struct {
        int version;          /* contains the integer 2 as a sanity check */
        int nd;               /* number of dimensions */
        char typekind;        /* kind in array --- character code of typestr */
        int itemsize;         /* size of each element */
        int flags;            /* how should be data interpreted */
        intp *shape;          /* A length-nd array of shape information */
        intp *strides;        /* A length-nd array of stride information */
        void *data;           /* A pointer to the first element of the array */
} PyArrayInterface;



  /*  Often, rather than always convert to an array, 
      we may want to delegate behavior for other objects passed in
  */

	/* 

#define Py_DELEGATE(op, name)                                     \
	if (PyObject_HasAttrString(op, #name)) {                  \
		PyObject *ret=NULL;				  \
		PyObject *meth=PyObject_GetAttrString(op, #name); \
		if (PyCallable_Check(meth)) {			  \
			ret = PyObject_CallObject(meth, NULL);	  \
		}						  \
		Py_XDECREF(meth);				  \
		return ret;					  \
	}

#define Py_DELEGATE_ARGS(op, name, args)			  \
	if (PyObject_HasAttrString(op, #name)) {                  \
		PyObject *ret=NULL;				  \
		PyObject *meth=PyObject_GetAttrString(op, #name); \
		if (PyCallable_Check(meth)) {			  \
			ret = PyObject_CallObject(meth, args);	  \
		}						  \
                Py_XDECREF(args);                                 \
		Py_XDECREF(meth);				  \
		return ret;					  \
	}

#define Py_DELEGATE_ARGS_KWDS(op, name, args, kwds)	          \
	if (PyObject_HasAttrString(op, #name)) {                  \
		PyObject *ret=NULL;				  \
		PyObject *meth=PyObject_GetAttrString(op, #name); \
		if (PyCallable_Check(meth)) {			  \
			ret = PyObject_Call(meth, args, kwds);	  \
		}						  \
                Py_XDECREF(args);                                 \
		Py_XDECREF(meth);				  \
		return ret;					  \
	}
	*/


        /* Includes the "function" C-API -- these are all stored in a 
	   list of pointers --- one for each file
	   The two lists are concatenated into one in multiarray.
	   
	   They are available as import_array()
         */

#include "__multiarray_api.h"


        /* C-API that requries previous API to be defined */

#define PyArray_Check(op) (PyObject_TypeCheck((op), &PyBigArray_Type))
#define PyBigArray_CheckExact(op) ((op)->ob_type == &PyBigArray_Type)
#define PyArray_CheckExact(op) ((op)->ob_type == &PyArray_Type)

#define PyArray_IsZeroDim(op) (PyArray_Check(op) && (PyArray_NDIM(op) == 0))
#define PyArray_IsScalar(obj, cls)				\
	(PyObject_TypeCheck((obj), &Py##cls##ArrType_Type))
#define PyArray_CheckScalar(m) (PyArray_IsScalar(m, Generic) || \
                                PyArray_IsZeroDim(m))
#define PyArray_IsPythonScalar(obj) \
	(PyInt_Check(obj) || PyFloat_Check(obj) || PyComplex_Check(obj) || \
	 PyLong_Check(obj) || PyBool_Check(obj) || PyString_Check(obj) || \
	 PyUnicode_Check(obj))
#define PyArray_IsAnyScalar(obj) \
	(PyArray_IsScalar(obj, Generic) || PyArray_IsPythonScalar(obj))

#define PyArray_GETCONTIGUOUS(m) (PyArray_ISCONTIGUOUS(m) ? Py_INCREF(m), m : \
                                  (PyArrayObject *)(PyArray_Copy(m)))

#define PyArray_SIZE(m) PyArray_MultiplyList(PyArray_DIMS(m), PyArray_NDIM(m))
#define PyArray_NBYTES(m) (PyArray_ITEMSIZE(m) * PyArray_SIZE(m))
#define PyArray_FROM_O(m) PyArray_FromAny(m, NULL, 0, 0, 0)
#define PyArray_FROM_OF(m,flags) PyArray_FromAny(m, NULL, 0, 0, flags)

#define PyArray_FILLWBYTE(obj, val) memset(PyArray_DATA(obj), (val), PyArray_NBYTES(obj))

#define REFCOUNT(obj) (((PyObject *)(obj))->ob_refcnt)
#define MAX_ELSIZE 2*SIZEOF_LONGDOUBLE

#define PyArray_SimpleNew(nd, dims, typenum) \
	PyArray_New(&PyArray_Type, nd, dims, typenum, NULL, NULL, 0, 0, NULL)
#define PyArray_SimpleNewFromData(nd, dims, typenum, data) \
        PyArray_New(&PyArray_Type, nd, dims, typenum, NULL, data, 0, CARRAY_FLAGS, NULL)

        /*Compatibility with old Numeric stuff -- don't use in new code */

#define PyArray_UNSIGNED_TYPES
#define PyArray_SBYTE PyArray_BYTE
#define PyArray_CHAR PyArray_BYTE
#define PyArray_CopyArray PyArray_CopyInto
#define _PyArray_multiply_list PyArray_MultiplyIntList
#define PyArray_ISSPACESAVER(m) FALSE
#define PyScalarArray_Check PyArray_CheckScalar

#ifdef PY_ARRAY_TYPES_PREFIX
#  undef CAT
#  undef CAT2
#  undef NS
#  undef longlong
#  undef ulonglong
#  undef Bool
#  undef longdouble
#  undef byte
#  undef ubyte
#  undef ushort
#  undef uint
#  undef ulong
#  undef cfloat
#  undef cdouble
#  undef clongdouble
#  undef Int8
#  undef UInt8
#  undef Int16
#  undef UInt16
#  undef Int32
#  undef UInt32
#  undef Int64
#  undef UInt64
#  undef Int128
#  undef UInt128
#  undef Int256
#  undef UInt256
#  undef Float16
#  undef Complex32
#  undef Float32
#  undef Complex64
#  undef Float64
#  undef Complex128
#  undef Float80
#  undef Complex160
#  undef Float96
#  undef Complex192
#  undef Float128
#  undef Complex256
#  undef intp
#  undef uintp
#endif

#ifdef __cplusplus
}
#endif

#endif /* !Py_ARRAYOBJECT_H */
