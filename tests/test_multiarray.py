
from numpy.testing import *
from numpy.core import *

class test_flags(ScipyTestCase):
    def setUp(self):
        self.a = arange(10)

    def check_writeable(self):
        mydict = locals()
        self.a.flags.writeable = False
        self.assertRaises(RuntimeError, runstring, 'self.a[0] = 3', mydict)
        self.a.flags.writeable = True
        self.a[0] = 5
        self.a[0] = 0

    def check_otherflags(self):
        assert_equal(self.a.flags.carray, True)
        assert_equal(self.a.flags.farray, False)
        assert_equal(self.a.flags.behaved, True)
        assert_equal(self.a.flags.fnc, False)
        assert_equal(self.a.flags.forc, True)
        assert_equal(self.a.flags.owndata, True)
        assert_equal(self.a.flags.writeable, True)
        assert_equal(self.a.flags.aligned, True)
        assert_equal(self.a.flags.updateifcopy, False)
        

class test_attributes(ScipyTestCase):
    def setUp(self):
        self.one = arange(10)
        self.two = arange(20).reshape(4,5)
        self.three = arange(60,dtype=float64).reshape(2,5,6)

    def check_attributes(self):
        assert_equal(self.one.shape, (10,))
        assert_equal(self.two.shape, (4,5))
        assert_equal(self.three.shape, (2,5,6))
        self.three.shape = (10,3,2)
        assert_equal(self.three.shape, (10,3,2))
        self.three.shape = (2,5,6)
        assert_equal(self.one.strides, (self.one.itemsize,))
        num = self.two.itemsize
        assert_equal(self.two.strides, (5*num, num))
        num = self.three.itemsize
        assert_equal(self.three.strides, (30*num, 6*num, num))
        assert_equal(self.one.ndim, 1)
        assert_equal(self.two.ndim, 2)
        assert_equal(self.three.ndim, 3)
        num = self.two.itemsize        
        assert_equal(self.two.size, 20)
        assert_equal(self.two.nbytes, 20*num)
        assert_equal(self.two.itemsize, self.two.dtype.itemsize)
        assert_equal(self.two.base, arange(20))

    def check_dtypeattr(self):
        assert_equal(self.one.dtype, dtype(int_))
        assert_equal(self.three.dtype, dtype(float_))
        assert_equal(self.one.dtype.char, 'l')
        assert_equal(self.three.dtype.char, 'd')
        self.failUnless(self.three.dtype.str[0] in '<>')
        assert_equal(self.one.dtype.str[1], 'i')
        assert_equal(self.three.dtype.str[1], 'f')

    def check_stridesattr(self):
        x = self.one
        def make_array(size, offset, strides):
            return ndarray([size], buffer=x,
                           offset=offset*x.itemsize,
                           strides=strides*x.itemsize)
        assert_equal(make_array(4, 4, -1), array([4, 3, 2, 1]))
        self.failUnlessRaises(ValueError, make_array, 4, 4, -2)
        self.failUnlessRaises(ValueError, make_array, 4, 3, -1)
        self.failUnlessRaises(ValueError, make_array, 8, 3, 1)
        self.failUnlessRaises(ValueError, make_array, 8, 3, 0)
        self.failUnlessRaises(ValueError, lambda: ndarray([1], strides=4))
        

    def check_set_stridesattr(self):
        x = self.one
        def make_array(size, offset, strides):
            try:
                r = ndarray([size], buffer=x, offset=offset*x.itemsize)
            except:
                pass
            r.strides = strides=strides*x.itemsize
            return r
        assert_equal(make_array(4, 4, -1), array([4, 3, 2, 1]))
        self.failUnlessRaises(ValueError, make_array, 4, 4, -2)
        self.failUnlessRaises(ValueError, make_array, 4, 3, -1)
        self.failUnlessRaises(ValueError, make_array, 8, 3, 1)
        self.failUnlessRaises(ValueError, make_array, 8, 3, 0)


class test_dtypedescr(ScipyTestCase):
    def check_construction(self):
        d1 = dtype('i4')
        assert_equal(d1, dtype(int32))
        d2 = dtype('f8')
        assert_equal(d2, dtype(float64))

class test_fromstring(ScipyTestCase):
    def check_binary(self):
        a = fromstring('\x00\x00\x80?\x00\x00\x00@\x00\x00@@\x00\x00\x80@',dtype='<f4')
        assert_array_equal(a, array([1,2,3,4]))

    def check_ascii(self):
        a = fromstring('1 , 2 , 3 , 4',sep=',')
        b = fromstring('1,2,3,4',dtype=float,sep=',')
        assert_array_equal(a,b)
        
class test_zero_rank(ScipyTestCase):
    def setUp(self):
        self.d = array(0), array('x', object)
        
    def check_ellipsis_subscript(self):
        a,b = self.d
        self.failUnlessEqual(a[...], 0)
        self.failUnlessEqual(b[...], 'x')
        self.failUnless(a[...] is a)
        self.failUnless(b[...] is b)
        
    def check_empty_subscript(self):
        a,b = self.d
        self.failUnlessEqual(a[()], 0)
        self.failUnlessEqual(b[()], 'x')
        self.failUnless(type(a[()]) is a.dtype.type)
	self.failUnless(type(b[()]) is str)

    def check_invalid_subscript(self):
        a,b = self.d
        self.failUnlessRaises(IndexError, lambda x: x[0], a)
        self.failUnlessRaises(IndexError, lambda x: x[0], b)
        self.failUnlessRaises(IndexError, lambda x: x[array([], int)], a)
        self.failUnlessRaises(IndexError, lambda x: x[array([], int)], b)

    def check_ellipsis_subscript_assignment(self):
        a,b = self.d
        a[...] = 42
        self.failUnlessEqual(a, 42)
        b[...] = ''
        self.failUnlessEqual(b.item(), '')
        
    def check_empty_subscript_assignment(self):
        a,b = self.d
        a[()] = 42
        self.failUnlessEqual(a, 42)
        b[()] = ''
        self.failUnlessEqual(b.item(), '')

    def check_invalid_subscript_assignment(self):
        a,b = self.d
        def assign(x, i, v):
            x[i] = v
        self.failUnlessRaises(IndexError, assign, a, 0, 42)
        self.failUnlessRaises(IndexError, assign, b, 0, '')
        self.failUnlessRaises(TypeError, assign, a, (), '')

    def check_newaxis(self):
        a,b = self.d
        self.failUnlessEqual(a[newaxis].shape, (1,))
        self.failUnlessEqual(a[..., newaxis].shape, (1,))
        self.failUnlessEqual(a[newaxis, ...].shape, (1,))
        self.failUnlessEqual(a[..., newaxis].shape, (1,))
        self.failUnlessEqual(a[newaxis, ..., newaxis].shape, (1,1))
        self.failUnlessEqual(a[..., newaxis, newaxis].shape, (1,1))
        self.failUnlessEqual(a[newaxis, newaxis, ...].shape, (1,1))
        self.failUnlessEqual(a[(newaxis,)*10].shape, (1,)*10)

    def check_invalid_newaxis(self):
        a,b = self.d
        def subscript(x, i): x[i]
        self.failUnlessRaises(IndexError, subscript, a, (newaxis, 0))
        self.failUnlessRaises(IndexError, subscript, a, (newaxis,)*50)

    def check_constructor(self):
        x = ndarray(())
        x[()] = 5
        self.failUnlessEqual(x[()], 5)
        y = ndarray((),buffer=x)
        y[()] = 6
        self.failUnlessEqual(x[()], 6)
        
class test_creation(ScipyTestCase):
    def check_from_attribute(self):
        class x(object):
            def __array__(self, dtype=None):
                pass
        self.failUnlessRaises(ValueError, array, x())

class test_bool(ScipyTestCase):
    def check_test_interning(self):
        a0 = bool_(0)
        b0 = bool_(False)
        self.failUnless(a0 is b0)
        a1 = bool_(1)
        b1 = bool_(True)
        self.failUnless(a1 is b1)
        self.failUnless(array([True])[0] is a1)
        self.failUnless(array(True)[()] is a1)


class test_methods(ScipyTestCase):
    def check_test_round(self):
        assert_equal(array([1.2,1.5]).round(), [1,2])
        assert_equal(array(1.5).round(), 2)
        assert_equal(array([12.2,15.5]).round(-1), [10,20])
        assert_equal(array([12.15,15.51]).round(1), [12.2,15.5])


class test_subscripting(ScipyTestCase):
    def check_test_zero_rank(self):
        x = array([1,2,3])
        self.failUnless(isinstance(x[0], int))
        self.failUnless(type(x[0, ...]) is ndarray)
            
# Import tests from unicode
set_local_path()
from test_unicode import *
restore_path()

if __name__ == "__main__":
    ScipyTest('numpy.core.multiarray').run()
