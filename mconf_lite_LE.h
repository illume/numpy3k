/*							mconf_lite.h
 *
 *	Common include file for math routines
 *
 *
 *
 * SYNOPSIS:
 *
 * #include "mconf_lite.h"
 *
 *
 *
 * DESCRIPTION:
 *
 * The file also includes a conditional assembly definition
 * for the type of computer arithmetic (IEEE, DEC, Motorola
 * IEEE, or UNKnown).
 * 
 * For Digital Equipment PDP-11 and VAX computers, certain
 * IBM systems, and others that use numbers with a 56-bit
 * significand, the symbol DEC should be defined.  In this
 * mode, most floating point constants are given as arrays
 * of octal integers to eliminate decimal to binary conversion
 * errors that might be introduced by the compiler.
 *
 * For little-endian computers, such as IBM PC, that follow the
 * IEEE Standard for Binary Floating Point Arithmetic (ANSI/IEEE
 * Std 754-1985), the symbol IBMPC should be defined.  These
 * numbers have 53-bit significands.  In this mode, constants
 * are provided as arrays of hexadecimal 16 bit integers.
 *
 * Big-endian IEEE format is denoted MIEEE.  On some RISC
 * systems such as Sun SPARC, double precision constants
 * must be stored on 8-byte address boundaries.  Since integer
 * arrays may be aligned differently, the MIEEE configuration
 * may fail on such machines.
 *
 * To accommodate other types of computer arithmetic, all
 * constants are also provided in a normal decimal radix
 * which one can hope are correctly converted to a suitable
 * format by the available C language compiler.  To invoke
 * this mode, define the symbol UNK.
 *
 * An important difference among these modes is a predefined
 * set of machine arithmetic constants for each.  The numbers
 * MACHEP (the machine roundoff error), MAXNUM (largest number
 * represented), and several other parameters are preset by
 * the configuration symbol.  Check the file const.c to
 * ensure that these values are correct for your computer.
 *
 * Configurations NANS, INFINITIES, MINUSZERO, and DENORMAL
 * may fail on many systems.  Verify that they are supposed
 * to work on your computer.
 */

/*
Cephes Math Library Release 2.3:  June, 1995
Copyright 1984, 1987, 1989, 1995 by Stephen L. Moshier

Modified to handle just the parts necessary for isnan to work.
*/


/* Type of computer arithmetic */

/* PDP-11, Pro350, VAX:
 */
/* #define DEC 1 */

/* Not sure about these pdp defines */
#if defined(vax) || defined(__vax__) || defined(decvax) || \
    defined(__decvax__) || defined(pro350) || defined(pdp11)
#define DEC 1  

#elif defined(ns32000) || defined(sun386) || \
    defined(i386) || defined(MIPSEL) || defined(_MIPSEL) || \
    defined(BIT_ZERO_ON_RIGHT) || defined(__alpha__) || defined(__alpha) || \
    defined(sequent) || defined(i386) || \
    defined(__ns32000__) || defined(__sun386__) || defined(__i386__)
#define IBMPC 1   /* Intel IEEE, low order words come first */
#define BIGENDIAN 0

#elif defined(sel) || defined(pyr) || defined(mc68000) || defined (m68k) || \
          defined(is68k) || defined(tahoe) || defined(ibm032) || \
          defined(ibm370) || defined(MIPSEB) || defined(_MIPSEB) || \
          defined(__convex__) || defined(DGUX) || defined(hppa) || \
          defined(apollo) || defined(_CRAY) || defined(__hppa) || \
          defined(__hp9000) || defined(__hp9000s300) || \
          defined(__hp9000s700) || defined(__AIX) || defined(_AIX) \
          defined(__pyr__) || defined(__mc68000__) || defined(__sparc) ||\
          defined(_IBMR2) || defined (BIT_ZERO_ON_LEFT) 
#define MIEEE 1     /* Motorola IEEE, high order words come first */
#define BIGENDIAN 1

#else 
#define UNK 1        /* Machine not known
#define BIGENDIAN 0   /* This is a LE file */
#endif


/* Define to ask for infinity support, else undefine. */
#define INFINITIES 1

/* Define to ask for support of numbers that are Not-a-Number,
   else undefine.  This may automatically define INFINITIES in some files. */
#define NANS 1

/* Define to distinguish between -0.0 and +0.0.  */
#define MINUSZERO 1

#if !defined(signbit)
int signbit(double);
#endif
#if !defined(isnan)
int isnan(double);
#endif
#if !defined(isfinite)
int isfinite(double);
#endif
