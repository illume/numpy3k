import numpy 
import types, time
from numpy.core.ma import *
from numpy.testing import ScipyTestCase, ScipyTest
def eq(v,w):
    result = allclose(v,w)
    if not result:
        print """Not eq:
%s
----
%s"""% (str(v), str(w))
    return result

class test_ma(ScipyTestCase):
    def __init__(self, *args, **kwds):
        ScipyTestCase.__init__(self, *args, **kwds)
        self.setUp()
    
    def setUp (self):
        x=numpy.array([1.,1.,1.,-2., pi/2.0, 4., 5., -10., 10., 1., 2., 3.])
        y=numpy.array([5.,0.,3., 2., -1., -4., 0., -10., 10., 1., 0., 3.])
        a10 = 10.
        m1 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        m2 = [0, 0, 1, 0, 0, 1, 1, 0, 0, 0 ,0, 1]
        xm = array(x, mask=m1)
        ym = array(y, mask=m2)
        z = numpy.array([-.5, 0., .5, .8])
        zm = array(z, mask=[0,1,0,0])
        xf = numpy.where(m1, 1.e+20, x)
        s = x.shape
        xm.set_fill_value(1.e+20)
        self.d = (x, y, a10, m1, m2, xm, ym, z, zm, xf, s)

    def check_testBasic1d(self):
        "Test of basic array creation and properties in 1 dimension."
        (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
        self.failIf(isMaskedArray(x))
        self.failUnless(isMaskedArray(xm))
        self.assertEqual(shape(xm), s)
        self.assertEqual(xm.shape, s)
        self.assertEqual(xm.dtype, x.dtype)
        self.assertEqual(xm.dtypechar, x.dtypechar)
        self.assertEqual( xm.size , reduce(lambda x,y:x*y, s))
        self.assertEqual(count(xm) , len(m1) - reduce(lambda x,y:x+y, m1))
        self.failUnless(eq(xm, xf))
        self.failUnless(eq(filled(xm, 1.e20), xf))
        self.failUnless(eq(x, xm))

    def check_testBasic2d(self):
        "Test of basic array creation and properties in 2 dimensions."
        for s in [(4,3), (6,2)]: 
            (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
            x.shape = s
            y.shape = s
            xm.shape = s
            ym.shape = s
            xf.shape = s
    
            self.failIf(isMaskedArray(x))
            self.failUnless(isMaskedArray(xm))
            self.assertEqual(shape(xm), s)
            self.assertEqual(xm.shape, s)
            self.assertEqual( xm.size , reduce(lambda x,y:x*y, s))
            self.assertEqual( count(xm) , len(m1) - reduce(lambda x,y:x+y, m1))
            self.failUnless(eq(xm, xf))
            self.failUnless(eq(filled(xm, 1.e20), xf))
            self.failUnless(eq(x, xm))
            self.setUp()

    def check_testArithmetic (self):
        "Test of basic arithmetic."
        (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
        a2d = array([[1,2],[0,4]])
        a2dm = masked_array(a2d, [[0,0],[1,0]])
        self.failUnless(eq (a2d * a2d, a2d * a2dm))
        self.failUnless(eq (a2d + a2d, a2d + a2dm))
        self.failUnless(eq (a2d - a2d, a2d - a2dm))
        for s in [(12,), (4,3), (2,6)]: 
            x = x.reshape(s)
            y = y.reshape(s)
            xm = xm.reshape(s)
            ym = ym.reshape(s)
            xf = xf.reshape(s)
            self.failUnless(eq(-x, -xm))
            self.failUnless(eq(x + y, xm + ym))
            self.failUnless(eq(x - y, xm - ym))
            self.failUnless(eq(x * y, xm * ym))
            self.failUnless(eq(x / y, xm / ym))
            self.failUnless(eq(a10 + y, a10 + ym))
            self.failUnless(eq(a10 - y, a10 - ym))
            self.failUnless(eq(a10 * y, a10 * ym))
            self.failUnless(eq(a10 / y, a10 / ym))
            self.failUnless(eq(x + a10, xm + a10))
            self.failUnless(eq(x - a10, xm - a10))
            self.failUnless(eq(x * a10, xm * a10))
            self.failUnless(eq(x / a10, xm / a10))
            self.failUnless(eq(x**2, xm**2))
            self.failUnless(eq(abs(x)**2.5, abs(xm) **2.5))
            self.failUnless(eq(x**y, xm**ym))
            self.failUnless(eq(numpy.add(x,y), add(xm, ym)))
            self.failUnless(eq(numpy.subtract(x,y), subtract(xm, ym)))
            self.failUnless(eq(numpy.multiply(x,y), multiply(xm, ym)))
            self.failUnless(eq(numpy.divide(x,y), divide(xm, ym)))


    def check_testUfuncs1 (self):
        "Test various functions such as sin, cos."
        (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
        self.failUnless (eq(numpy.cos(x), cos(xm)))
        self.failUnless (eq(numpy.cosh(x), cosh(xm)))
        self.failUnless (eq(numpy.sin(x), sin(xm)))
        self.failUnless (eq(numpy.sinh(x), sinh(xm)))
        self.failUnless (eq(numpy.tan(x), tan(xm)))
        self.failUnless (eq(numpy.tanh(x), tanh(xm)))
        self.failUnless (eq(numpy.sqrt(abs(x)), sqrt(xm)))
        self.failUnless (eq(numpy.log(abs(x)), log(xm)))
        self.failUnless (eq(numpy.log10(abs(x)), log10(xm)))
        self.failUnless (eq(numpy.exp(x), exp(xm)))
        self.failUnless (eq(numpy.arcsin(z), arcsin(zm)))
        self.failUnless (eq(numpy.arccos(z), arccos(zm)))
        self.failUnless (eq(numpy.arctan(z), arctan(zm)))
        self.failUnless (eq(numpy.arctan2(x, y), arctan2(xm, ym)))
        self.failUnless (eq(numpy.absolute(x), absolute(xm)))
        self.failUnless (eq(numpy.equal(x,y), equal(xm, ym)))
        self.failUnless (eq(numpy.not_equal(x,y), not_equal(xm, ym)))
        self.failUnless (eq(numpy.less(x,y), less(xm, ym)))
        self.failUnless (eq(numpy.greater(x,y), greater(xm, ym)))
        self.failUnless (eq(numpy.less_equal(x,y), less_equal(xm, ym)))
        self.failUnless (eq(numpy.greater_equal(x,y), greater_equal(xm, ym)))
        self.failUnless (eq(numpy.conjugate(x), conjugate(xm)))
        self.failUnless (eq(numpy.concatenate((x,y)), concatenate((xm,ym))))
        self.failUnless (eq(numpy.concatenate((x,y)), concatenate((x,y))))
        self.failUnless (eq(numpy.concatenate((x,y)), concatenate((xm,y))))
        self.failUnless (eq(numpy.concatenate((x,y,x)), concatenate((x,ym,x))))
    
    def check_xtestCount (self):
        "Test count"
        ott = array([0.,1.,2.,3.], mask=[1,0,0,0])
        self.failUnless( isinstance(count(ott), types.IntType))
        self.assertEqual(3, count(ott))
        self.assertEqual(1, count(1))
        self.failUnless (eq(0, array(1,mask=[1])))
        ott=ott.reshape((2,2))
        assert isMaskedArray(count(ott,0))
        assert isinstance(count(ott), types.IntType)
        self.failUnless (eq(3, count(ott)))
        assert getmask(count(ott,0)) is None
        self.failUnless (eq([1,2],count(ott,0)))
   
    def check_testMinMax (self):
        "Test minimum and maximum." 
        (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
        xr = numpy.ravel(x) #max doesn't work if shaped
        xmr = ravel(xm)
        self.failUnless (eq(max(xr), maximum(xmr))) #true because of careful selection of data
        self.failUnless (eq(min(xr), minimum(xmr))) #true because of careful selection of data

    def check_testAddSumProd (self):
        "Test add, sum, product."
        (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
        self.failUnless (eq(numpy.add.reduce(x), add.reduce(x)))
        self.failUnless (eq(numpy.add.accumulate(x), add.accumulate(x)))
        self.failUnless (eq(4, sum(array(4))))
        self.failUnless (eq(4, sum(array(4), axis=0)))
        self.failUnless (eq(numpy.sum(x), sum(x)))
        self.failUnless (eq(numpy.sum(filled(xm,0)), sum(xm)))
        self.failUnless (eq(numpy.sum(x,0), sum(x,0)))
        self.failUnless (eq(numpy.product(x), product(x)))
        self.failUnless (eq(numpy.product(x,0), product(x,0)))
        self.failUnless (eq(numpy.product(filled(xm,1)), product(xm)))
        if len(s) > 1:
            self.failUnless (eq(numpy.concatenate((x,y),1), concatenate((xm,ym),1)))
            self.failUnless (eq(numpy.add.reduce(x,1), add.reduce(x,1)))
            self.failUnless (eq(numpy.sum(x,1), sum(x,1)))
            self.failUnless (eq(numpy.product(x,1), product(x,1)))
    
    
    def check_testCI(self):
        "Test of conversions and indexing"
        x1 = numpy.array([1,2,4,3])
        x2 = array(x1, mask = [1,0,0,0])
        x3 = array(x1, mask = [0,1,0,1])
        x4 = array(x1)
    # test conversion to strings
        junk, garbage = str(x2), repr(x2)
        assert eq(numpy.sort(x1),sort(x2, fill_value=0))
    # tests of indexing
        assert type(x2[1]) is type(x1[1])
        assert x1[1] == x2[1]
        assert x2[0] is masked
        assert eq(x1[2],x2[2])
        assert eq(x1[2:5],x2[2:5])
        assert eq(x1[:],x2[:])
        assert eq(x1[1:], x3[1:])
        x1[2]=9
        x2[2]=9
        assert eq(x1,x2)
        x1[1:3] = 99
        x2[1:3] = 99
        assert eq(x1,x2)
        x2[1] = masked
        assert eq(x1,x2)
        x2[1:3]=masked
        assert eq(x1,x2)
        x2[:] = x1
        x2[1] = masked
        assert allequal(getmask(x2),array([0,1,0,0]))
        x3[:] = masked_array([1,2,3,4],[0,1,1,0])
        assert allequal(getmask(x3), array([0,1,1,0]))
        x4[:] = masked_array([1,2,3,4],[0,1,1,0])
        assert allequal(getmask(x4), array([0,1,1,0]))
        assert allequal(x4, array([1,2,3,4]))
        x1 = numpy.arange(5)*1.0
        x2 = masked_values(x1, 3.0)
        assert eq(x1,x2)
        assert allequal(array([0,0,0,1,0],MaskType), x2.mask)
        assert eq(3.0, x2.fill_value())
        x1 = array([1,'hello',2,3],object)
        x2 = numpy.array([1,'hello',2,3],object)
        s1 = x1[1].item()
        s2 = x2[1].item()
        self.assertEqual(type(s2), str)
        self.assertEqual(type(s1), str)
        self.assertEqual(s1, s2)
        assert x1[1:1].shape == (0,)
    
    def check_testCopySize(self):
        "Tests of some subtle points of copying and sizing."
        n = [0,0,1,0,0]
        m = make_mask(n)
        m2 = make_mask(m)
        self.failUnless(m is m2)
        m3 = make_mask(m, copy=1)
        self.failUnless(m is not m3)
        
        x1 = numpy.arange(5)
        y1 = array(x1, mask=m)
        self.failUnless( y1.raw_data() is not x1)
        self.failUnless( allequal(x1,y1.raw_data()))
        self.failUnless( y1.mask is m)
    
        y1a = array(y1, copy=0)
        self.failUnless( y1a.raw_data() is y1.raw_data())
        self.failUnless( y1a.mask is y1.mask)
        
        y2 = array(x1, mask=m, copy=0)
        self.failUnless( y2.raw_data() is x1)
        self.failUnless( y2.mask is m)
        self.failUnless( y2[2] is masked)
        y2[2]=9
        self.failUnless( y2[2] is not masked)
        self.failUnless( y2.mask is not m)
        self.failUnless( allequal(y2.mask, 0))
    
        y3 = array(x1*1.0, mask=m)
        self.failUnless(filled(y3).dtype is (x1*1.0).dtype)
    
        x4 = arange(4)
        x4[2] = masked
        y4 = resize(x4, (8,))
        self.failUnless( eq(concatenate([x4,x4]), y4))
        self.failUnless( eq(getmask(y4),[0,0,1,0,0,0,1,0]))
        y5 = repeat(x4, (2,2,2,2))
        self.failUnless( eq(y5, [0,0,1,1,2,2,3,3]))
        y6 = repeat(x4, 2)
        self.failUnless( eq(y5, y6))
    
    def check_testPut(self):
        "Test of put"
        d = arange(5)
        n = [0,0,0,1,1]
        m = make_mask(n)
        x = array(d, mask = m)
        self.failUnless( x[3] is masked)
        self.failUnless( x[4] is masked)
        x[[1,4]] = [10,40]
        self.failUnless( x.mask is not m)
        self.failUnless( x[3] is masked)
        self.failUnless( x[4] is not masked)
        self.failUnless( eq(x, [0,10,2,-1,40]))
    
        x = array(d, mask = m) 
        x.put([-1,100,200])
        self.failUnless( eq(x, [-1,100,200,0,0]))
        self.failUnless( x[3] is masked)
        self.failUnless( x[4] is masked)
    
        x = array(d, mask = m) 
        x.putmask([30,40])
        self.failUnless( eq(x, [0,1,2,30,40]))
        self.failUnless( x.mask is None)
    
        x = array(d, mask = m) 
        y = x.compressed()
        z = array(x, mask = m)
        z.put(y)
        assert eq (x, z)
    
    def check_testMaPut(self):
        (x, y, a10, m1, m2, xm, ym, z, zm, xf, s) = self.d
        m = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
        i = numpy.nonzero(m)
        putmask(xm, m, z)
        assert take(xm, i) == z
        put(ym, i, zm)
        assert take(ym, i) == zm
        
    def check_testOddFeatures(self):
        "Test of other odd features"
        x = arange(20); x=x.reshape(4,5)
        x.flat[5] = 12
        assert x[1,0] == 12
        z = x + 10j * x
        assert eq(z.real, x)
        assert eq(z.imag, 10*x)
        assert eq((z*conjugate(z)).real, 101*x*x)
        z.imag[...] = 0.0
    
        x = arange(10)
        x[3] = masked
        assert str(x[3]) == str(masked)
        c = x >= 8
        assert count(where(c,masked,masked)) == 0
        assert shape(where(c,masked,masked)) == c.shape
        z = where(c , x, masked)
        assert z.dtype is x.dtype
        assert z[3] is masked
        assert z[4] is masked
        assert z[7] is masked
        assert z[8] is not masked
        assert z[9] is not masked
        assert eq(x,z)
        z = where(c , masked, x)
        assert z.dtype is x.dtype
        assert z[3] is masked
        assert z[4] is not masked
        assert z[7] is not masked
        assert z[8] is masked
        assert z[9] is masked
        z = masked_where(c, x)
        assert z.dtype is x.dtype
        assert z[3] is masked
        assert z[4] is not masked
        assert z[7] is not masked
        assert z[8] is masked
        assert z[9] is masked
        assert eq(x,z)
        x = array([1.,2.,3.,4.,5.])
        c = array([1,1,1,0,0])
        x[2] = masked
        z = where(c, x, -x)
        assert eq(z, [1.,2.,0., -4., -5])
        c[0] = masked
        z = where(c, x, -x)
        assert eq(z, [1.,2.,0., -4., -5])
        assert z[0] is masked
        assert z[1] is not masked
        assert z[2] is masked
        assert eq(masked_where(greater(x, 2), x), masked_greater(x,2))
        assert eq(masked_where(greater_equal(x, 2), x), masked_greater_equal(x,2))
        assert eq(masked_where(less(x, 2), x), masked_less(x,2))
        assert eq(masked_where(less_equal(x, 2), x), masked_less_equal(x,2))
        assert eq(masked_where(not_equal(x, 2), x), masked_not_equal(x,2))
        assert eq(masked_where(equal(x, 2), x), masked_equal(x,2))
        assert eq(masked_where(not_equal(x,2), x), masked_not_equal(x,2))
        assert eq(masked_inside(range(5), 1, 3), [0, 199, 199, 199, 4])
        assert eq(masked_outside(range(5), 1, 3),[199,1,2,3,199])
        assert eq(masked_inside(array(range(5), mask=[1,0,0,0,0]), 1, 3).mask, [1,1,1,1,0])
        assert eq(masked_outside(array(range(5), mask=[0,1,0,0,0]), 1, 3).mask, [1,1,0,0,1])
        assert eq(masked_equal(array(range(5), mask=[1,0,0,0,0]), 2).mask, [1,0,1,0,0])
        assert eq(masked_not_equal(array([2,2,1,2,1], mask=[1,0,0,0,0]), 2).mask, [1,0,1,0,1])
        assert eq(masked_where([1,1,0,0,0], [1,2,3,4,5]), [99,99,3,4,5])
        atest = ones((10,10,10), dtype=float32)
        btest = zeros(atest.shape, MaskType)
        ctest = masked_where(btest,atest)
        assert eq(atest,ctest)
        z = choose(c, (-x, x))
        assert eq(z, [1.,2.,0., -4., -5])
        assert z[0] is masked
        assert z[1] is not masked
        assert z[2] is masked
        x = arange(6)
        x[5] = masked
        y = arange(6)*10
        y[2]= masked
        c = array([1,1,1,0,0,0], mask=[1,0,0,0,0,0])
        cm = c.filled(1)
        z = where(c,x,y)
        zm = where(cm,x,y)
        assert eq(z, zm)
        assert getmask(zm) is None
        assert eq(zm, [0,1,2,30,40,50])
        z = where(c, masked, 1)
        assert eq(z, [99,99,99,1,1,1])
        z = where(c, 1, masked)
        assert eq(z, [99, 1, 1, 99, 99, 99])
    
    def check_testMinMax(self):
        "Test of minumum, maximum."    
        assert eq(minimum([1,2,3],[4,0,9]), [1,0,3])
        assert eq(maximum([1,2,3],[4,0,9]), [4,2,9])
        x = arange(5)
        y = arange(5) - 2
        x[3] = masked
        y[0] = masked
        assert eq(minimum(x,y), where(less(x,y), x, y))
        assert eq(maximum(x,y), where(greater(x,y), x, y))
        assert minimum(x) == 0
        assert maximum(x) == 4
    
    def check_testTakeTransposeInnerOuter(self):
        "Test of take, transpose, inner, outer products"
        x = arange(24)
        y = numpy.arange(24)
        x[5:6] = masked
        x=x.reshape(2,3,4)
        y=y.reshape(2,3,4)
        assert eq(numpy.transpose(y,(2,0,1)), transpose(x,(2,0,1)))
        assert eq(numpy.take(y, (2,0,1), 1), take(x, (2,0,1), 1))
        assert eq(numpy.innerproduct(filled(x,0),filled(y,0)),
                                innerproduct(x, y))
        assert eq(numpy.outerproduct(filled(x,0),filled(y,0)),
                                outerproduct(x, y))
        y = array(['abc', 1, 'def', 2, 3], object)
        y[2] = masked
        t = take(y,[0,3,4])
        assert t[0].item() == 'abc'
        assert t[1].item() == 2
        assert t[2].item() == 3
    
    def check_testInplace(self):
        """Test of inplace operations and rich comparisons"""
        y = arange(10)
    
        x = arange(10)
        xm = arange(10)
        xm[2] = masked
        x += 1
        assert eq(x, y+1)
        xm += 1
        assert eq(x, y+1)
    
        x = arange(10)
        xm = arange(10)
        xm[2] = masked
        x -= 1
        assert eq(x, y-1)
        xm -= 1
        assert eq(xm, y-1)
    
        x = arange(10)*1.0
        xm = arange(10)*1.0
        xm[2] = masked
        x *= 2.0
        assert eq(x, y*2)
        xm *= 2.0
        assert eq(xm, y*2)
    
        x = arange(10)*2
        xm = arange(10)
        xm[2] = masked
        x /= 2
        assert eq(x, y)
        xm /= 2
        assert eq(x, y)
    
        x = arange(10)*1.0
        xm = arange(10)*1.0
        xm[2] = masked
        x /= 2.0
        assert eq(x, y/2.0)
        xm /= arange(10)
        assert eq(xm, ones((10,)))
    
        x = arange(10).astype(float32)
        xm = arange(10)
        xm[2] = masked
        id1 = id(x.raw_data())
        x += 1.
        assert id1 == id(x.raw_data())
        assert eq(x, y+1.)
      
    def check_testPickle(self):
        "Test of pickling"
        x = arange(12)
        x[4:10:2] = masked
        x=x.reshape(4,3)
        f = open('test9.pik','wb')
        import pickle
        pickle.dump(x, f)
        f.close()
        f = open('test9.pik', 'rb')
        y = pickle.load(f)
        assert eq(x,y) 
    
    def check_testMasked(self):
        "Test of masked element"
        xx=arange(6)
        xx[1] = masked
        self.failUnless(xx[1] is masked)
        self.failUnlessRaises(Exception, lambda x,y: x+y, masked, masked)
        self.failUnlessRaises(Exception, lambda x,y: x+y, masked, 2)
        self.failUnlessRaises(Exception, lambda x,y: x+y, masked, xx)
        self.failUnlessRaises(Exception, lambda x,y: x+y, xx, masked)
    
    def check_testAverage1(self):
        "Test of average."
        ott = array([0.,1.,2.,3.], mask=[1,0,0,0])
        self.failUnless(eq(2.0, average(ott)))
        self.failUnless(eq(2.0, average(ott, weights=[1., 1., 2., 1.])))
        result, wts = average(ott, weights=[1.,1.,2.,1.], returned=1)
        self.failUnless(eq(2.0, result))
        self.failUnless(wts == 4.0)
        ott[:] = masked
        self.failUnless(average(ott) is masked)
        ott = array([0.,1.,2.,3.], mask=[1,0,0,0])
        ott=ott.reshape(2,2)
        ott[:,1] = masked
        self.failUnless(eq(average(ott), [2.0, 0.0]))
        self.failUnless(average(ott,axis=1)[0] is masked)
        self.failUnless(eq([2.,0.], average(ott)))
        result, wts = average(ott, returned=1)
        self.failUnless(eq(wts, [1., 0.]))

    def check_testAverage2(self):
        "More tests of average."
        w1 = [0,1,1,1,1,0]
        w2 = [[0,1,1,1,1,0],[1,0,0,0,0,1]]
        x=arange(6)
        self.failUnless(allclose(average(x), 2.5))
        self.failUnless(allclose(average(x, weights=w1), 2.5))
        y=array([arange(6), 2.0*arange(6)])
        self.failUnless(allclose(average(y, None), numpy.add.reduce(numpy.arange(6))*3./12.))
        self.failUnless(allclose(average(y, axis=0), numpy.arange(6) * 3./2.))
        self.failUnless(allclose(average(y, axis=1), [average(x), average(x) * 2.0]))
        self.failUnless(allclose(average(y, None, weights=w2), 20./6.))
        self.failUnless(allclose(average(y, axis=0, weights=w2), [0.,1.,2.,3.,4.,10.]))
        self.failUnless(allclose(average(y, axis=1), [average(x), average(x) * 2.0]))
        m1 = zeros(6)
        m2 = [0,0,1,1,0,0]
        m3 = [[0,0,1,1,0,0],[0,1,1,1,1,0]]
        m4 = ones(6)
        m5 = [0, 1, 1, 1, 1, 1]
        self.failUnless(allclose(average(masked_array(x, m1)), 2.5))
        self.failUnless(allclose(average(masked_array(x, m2)), 2.5))
        self.failUnless(average(masked_array(x, m4)) is masked)
        self.assertEqual(average(masked_array(x, m5)), 0.0)
        self.assertEqual(count(average(masked_array(x, m4))), 0)
        z = masked_array(y, m3)
        self.failUnless(allclose(average(z, None), 20./6.))
        self.failUnless(allclose(average(z, axis=0), [0.,1.,99.,99.,4.0, 7.5]))
        self.failUnless(allclose(average(z, axis=1), [2.5, 5.0]))
        self.failUnless(allclose( average(z,weights=w2), [0.,1., 99., 99., 4.0, 10.0]))
    
        a = arange(6)
        b = arange(6) * 3
        r1, w1 = average([[a,b],[b,a]], axis=1, returned=1)
        self.assertEqual(shape(r1) , shape(w1))
        self.assertEqual(r1.shape , w1.shape)
        r2, w2 = average(ones((2,2,3)), axis=0, weights=[3,1], returned=1)
        self.assertEqual(shape(w2) , shape(r2))
        r2, w2 = average(ones((2,2,3)), returned=1)
        self.assertEqual(shape(w2) , shape(r2))
        r2, w2 = average(ones((2,2,3)), weights=ones((2,2,3)), returned=1)
        self.failUnless(shape(w2) == shape(r2))
        a2d = array([[1,2],[0,4]], float)
        a2dm = masked_array(a2d, [[0,0],[1,0]])
        a2da = average(a2d)
        self.failUnless(eq (a2da, [0.5, 3.0]))
        a2dma = average(a2dm)
        self.failUnless(eq( a2dma, [1.0, 3.0]))
        a2dma = average(a2dm, axis=None)
        self.failUnless(eq(a2dma, 7./3.))
        a2dma = average(a2dm, axis=1)
        self.failUnless(eq(a2dma, [1.5, 4.0]))

    def check_testToPython(self):
        self.assertEqual(1, int(array(1)))
        self.assertEqual(1.0, float(array(1)))
        self.assertEqual(1, int(array([[[1]]])))
        self.assertEqual(1.0, float(array([[1]])))
        self.failUnlessRaises(ValueError, float, array([1,1]))
        self.failUnlessRaises(MAError, float, array([1],mask=[1]))
        self.failUnless(bool(array([0,1])))
        self.failUnless(bool(array([0,0],mask=[0,1])))
        self.failIf(bool(array([0,0])))
        self.failIf(bool(array([0,0],mask=[0,0])))

    def check_testScalarArithmetic(self):
        xm = array(0, mask=1)
        self.failUnless((1/array(0)).mask)
        self.failUnless((1 + xm).mask)
        self.failUnless((-xm).mask)
        self.failUnless((-xm).mask)
        self.failUnless(maximum(xm, xm).mask)
        self.failUnless(minimum(xm, xm).mask)
                
def timingTest():
    for f in [testf, testinplace]:
        for n in [1000,10000,50000]:
            t = testta(n, f)
            t1 = testtb(n, f)
            t2 = testtc(n, f)
            print f.test_name
            print """\
n = %7d 
numpy time (ms) %6.1f 
MA maskless ratio %6.1f
MA masked ratio %6.1f
""" % (n, t*1000.0, t1/t, t2/t)

def testta(n, f):
    x=numpy.arange(n) + 1.0
    tn0 = time.time()
    z = f(x)
    return time.time() - tn0

def testtb(n, f):
    x=arange(n) + 1.0
    tn0 = time.time()
    z = f(x)
    return time.time() - tn0

def testtc(n, f):
    x=arange(n) + 1.0
    x[0] = masked
    tn0 = time.time()
    z = f(x)
    return time.time() - tn0

def testf(x):
    for i in range(25):
        y = x **2 +  2.0 * x - 1.0
        w = x **2 +  1.0
        z = (y / w) ** 2
    return z
testf.test_name = 'Simple arithmetic'

def testinplace(x):
    for i in range(25):
        y = x**2
        y += 2.0*x
        y -= 1.0
        y /= x
    return y
testinplace.test_name = 'Inplace operations'

if __name__ == "__main__":
    ScipyTest('numpy.core.ma').run()    
    #timingTest()
