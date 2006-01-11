"""
Set operations for 1D numeric arrays based on sort() function.

Contains:
  ediff1d,
  unique1d,
  intersect1d,
  intersect1d_nu,
  setxor1d,
  setmember1d,
  union1d,
  setdiff1d

Concerning the speed, test_unique1d_speed() reveals that up to 10000000
elements unique1d() is about 10 times faster than the standard dictionary-based
numpy.unique().

Limitations: Except unique1d, union1d and intersect1d_nu, all functions expect
inputs with unique elements. Speed could be gained in some operations by an
implementaion of sort(), that can provide directly the permutation vectors,
avoiding thus calls to argsort().

To do: Optionally return indices analogously to unique1d for all functions.

Author: Robert Cimrman
"""
__all__ = ['unique1d', 'intersect1d', 'intersect1d_nu', 'setxor1d',
           'setmember1d', 'union1d', 'setdiff1d']


# 02.11.2005, c
import time
import numpy

##
# 03.11.2005, c
def ediff1d( ar1, to_end = None, to_begin = None ):
    """Array difference with prefixed and/or appended value."""
    dar1 = ar1[1:] - ar1[:-1]
    if to_end and to_begin:
        shape = (ar1.shape[0] + 1,) + ar1.shape[1:]
        ed = numpy.empty( shape, dtype = ar1.dtype )
        ed[0], ed[-1] = to_begin, to_end
        ed[1:-1] = dar1
    elif to_end:
        ed = numpy.empty( ar1.shape, dtype = ar1.dtype )
        ed[-1] = to_end
        ed[:-1] = dar1
    elif to_begin:
        ed = numpy.empty( ar1.shape, dtype = ar1.dtype )
        ed[0] = to_begin
        ed[1:] = dar1
    else:
        ed = dar1

    return ed


##
# 01.11.2005, c
# 02.11.2005
def unique1d( ar1, retindx = False ):
    """Unique elements of 1D array. When ret_indx is True, return also the
    indices indx such that ar1.flat[indx] is the resulting array of unique
    elements."""
    ar = numpy.array( ar1 ).ravel()
    if retindx:
        perm = numpy.argsort( ar )
        aux = numpy.take( ar, perm )
        flag = ediff1d( aux, 1 ) != 0
        return numpy.compress( flag, perm ), numpy.compress( flag, aux )
    else:
        aux = numpy.sort( ar )
        return numpy.compress( ediff1d( aux, 1 ) != 0, aux ) 

##
# 01.11.2005, c
def intersect1d( ar1, ar2 ):
    """Intersection of 1D arrays with unique elements."""
    aux = numpy.sort( numpy.concatenate( (ar1, ar2 ) ) )
    return numpy.compress( (aux[1:] - aux[:-1]) == 0, aux )

##
# 01.11.2005, c
def intersect1d_nu( ar1, ar2 ):
    """Intersection of 1D arrays with any elements."""
    # Might be faster then unique1d( intersect1d( ar1, ar2 ) )?
    aux = numpy.sort( numpy.concatenate( (unique1d( ar1 ),
                                          unique1d( ar2  )) ) )
    return numpy.compress( (aux[1:] - aux[:-1]) == 0, aux )

##
# 01.11.2005, c
def setxor1d( ar1, ar2 ):
    """Set exclusive-or of 1D arrays with unique elements."""
    aux = numpy.sort( numpy.concatenate( (ar1, ar2 ) ) )
    flag = ediff1d( aux, to_end = 1, to_begin = 1 ) == 0
    flag2 = ediff1d( flag, 0 ) == 0
    return numpy.compress( flag2, aux )

##
# 03.11.2005, c
# 05.01.2006
def setmember1d( ar1, ar2 ):
    """Return an array of shape of ar1 containing 1 where the elements of
    ar1 are in ar2 and 0 otherwise."""
    ar = numpy.concatenate( (ar1, ar2 ) )
    tt = numpy.concatenate( (numpy.zeros_like( ar1 ),
                             numpy.zeros_like( ar2 ) + 1) )
    perm = numpy.argsort( ar )
    aux = numpy.take( ar, perm )
    aux2 = numpy.take( tt, perm )
    flag = ediff1d( aux, 1 ) == 0

    ii = numpy.where( flag * aux2 )
    aux = perm[ii+1]
    perm[ii+1] = perm[ii]
    perm[ii] = aux

    indx = numpy.argsort( perm )[:len( ar1 )]

    return numpy.take( flag, indx )

##
# 03.11.2005, c
def union1d( ar1, ar2 ):
    """Union of 1D arrays with unique elements."""
    return unique1d( numpy.concatenate( (ar1, ar2) ) )

##
# 03.11.2005, c
def setdiff1d( ar1, ar2 ):
    """Set difference of 1D arrays with unique elements."""
    aux = setmember1d( ar1, ar2 )
    return numpy.compress( aux == 0, ar1 )

##
# 02.11.2005, c
def test_unique1d_speed( plot_results = False ):
#    exponents = numpy.linspace( 2, 7, 9 )
    exponents = numpy.linspace( 2, 6, 9 )
    ratios = []
    nItems = []
    dt1s = []
    dt2s = []
    for ii in exponents:

        nItem = 10 ** ii
        print 'using %d items:' % nItem
        a = numpy.fix( nItem / 10 * numpy.random.random( nItem ) )

        print 'dictionary:'
        tt = time.clock() 
        b = numpy.unique( a )
        dt1 = time.clock() - tt
        print dt1

        print 'array:'
        tt = time.clock() 
        c = unique1d( a )
        dt2 = time.clock() - tt
        print dt2


        if dt1 < 1e-8:
            ratio = 'ND'
        else:
            ratio = dt2 / dt1
        print 'ratio:', ratio
        print 'nUnique: %d == %d\n' % (len( b ), len( c ))

        nItems.append( nItem )
        ratios.append( ratio )
        dt1s.append( dt1 )
        dt2s.append( dt2 )

        assert numpy.alltrue( b == c )


    print nItems
    print dt1s
    print dt2s
    print ratios

    if plot_results:
        import pylab

        def plotMe( fig, fun, nItems, dt1s, dt2s ):
            pylab.figure( fig )
            fun( nItems, dt1s, 'g-o', linewidth = 2, markersize = 8 )
            fun( nItems, dt2s, 'b-x', linewidth = 2, markersize = 8 )
            pylab.legend( ('dictionary', 'array' ) )
            pylab.xlabel( 'nItem' )
            pylab.ylabel( 'time [s]' )

        plotMe( 1, pylab.loglog, nItems, dt1s, dt2s )
        plotMe( 2, pylab.plot, nItems, dt1s, dt2s )
        pylab.show()

if (__name__ == '__main__'):
    test_unique1d_speed( plot_results = True )
