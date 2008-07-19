from numpy.testing import *
import numpy.core.umath as ncu
import numpy as np

class TestDivision(TestCase):
    def test_division_int(self):
        # int division should return the floor of the result, a la Python
        x = np.array([5, 10, 90, 100, -5, -10, -90, -100, -120])
        assert_equal(x / 100, [0, 0, 0, 1, -1, -1, -1, -1, -2])
        assert_equal(x // 100, [0, 0, 0, 1, -1, -1, -1, -1, -2])
        assert_equal(x % 100, [5, 10, 90, 0, 95, 90, 10, 0, 80])

class TestPower(TestCase):
    def test_power_float(self):
        x = np.array([1., 2., 3.])
        assert_equal(x**0, [1., 1., 1.])
        assert_equal(x**1, x)
        assert_equal(x**2, [1., 4., 9.])
        y = x.copy()
        y **= 2
        assert_equal(y, [1., 4., 9.])
        assert_almost_equal(x**(-1), [1., 0.5, 1./3])
        assert_almost_equal(x**(0.5), [1., ncu.sqrt(2), ncu.sqrt(3)])

    def test_power_complex(self):
        x = np.array([1+2j, 2+3j, 3+4j])
        assert_equal(x**0, [1., 1., 1.])
        assert_equal(x**1, x)
        assert_equal(x**2, [-3+4j, -5+12j, -7+24j])
        assert_almost_equal(x**(-1), [1/(1+2j), 1/(2+3j), 1/(3+4j)])
        assert_almost_equal(x**(-3), [(-11+2j)/125, (-46-9j)/2197,
                                      (-117-44j)/15625])
        assert_almost_equal(x**(0.5), [ncu.sqrt(1+2j), ncu.sqrt(2+3j),
                                       ncu.sqrt(3+4j)])
        assert_almost_equal(x**14, [-76443+16124j, 23161315+58317492j,
                                    5583548873 +  2465133864j])


class TestLog1p(TestCase):
    def test_log1p(self):
        assert_almost_equal(ncu.log1p(0.2), ncu.log(1.2))
        assert_almost_equal(ncu.log1p(1e-6), ncu.log(1+1e-6))

class TestExpm1(TestCase):
    def test_expm1(self):
        assert_almost_equal(ncu.expm1(0.2), ncu.exp(0.2)-1)
        assert_almost_equal(ncu.expm1(1e-6), ncu.exp(1e-6)-1)

class TestMaximum(TestCase):
    def test_reduce_complex(self):
        assert_equal(ncu.maximum.reduce([1,2j]),1)
        assert_equal(ncu.maximum.reduce([1+3j,2j]),1+3j)

class TestMinimum(TestCase):
    def test_reduce_complex(self):
        assert_equal(ncu.minimum.reduce([1,2j]),2j)

class TestFloatingPoint(TestCase):
    def test_floating_point(self):
        assert_equal(ncu.FLOATING_POINT_SUPPORT, 1)

class TestDegrees(TestCase):
    def test_degrees(self):
        assert_almost_equal(ncu.degrees(np.pi), 180.0)
        assert_almost_equal(ncu.degrees(-0.5*np.pi), -90.0)

class TestRadians(TestCase):
    def test_radians(self):
        assert_almost_equal(ncu.radians(180.0), np.pi)
        assert_almost_equal(ncu.radians(-90.0), -0.5*np.pi)

class TestSpecialMethods(TestCase):
    def test_wrap(self):
        class with_wrap(object):
            def __array__(self):
                return np.zeros(1)
            def __array_wrap__(self, arr, context):
                r = with_wrap()
                r.arr = arr
                r.context = context
                return r
        a = with_wrap()
        x = ncu.minimum(a, a)
        assert_equal(x.arr, np.zeros(1))
        func, args, i = x.context
        self.failUnless(func is ncu.minimum)
        self.failUnlessEqual(len(args), 2)
        assert_equal(args[0], a)
        assert_equal(args[1], a)
        self.failUnlessEqual(i, 0)

    def test_old_wrap(self):
        class with_wrap(object):
            def __array__(self):
                return np.zeros(1)
            def __array_wrap__(self, arr):
                r = with_wrap()
                r.arr = arr
                return r
        a = with_wrap()
        x = ncu.minimum(a, a)
        assert_equal(x.arr, np.zeros(1))

    def test_priority(self):
        class A(object):
            def __array__(self):
                return np.zeros(1)
            def __array_wrap__(self, arr, context):
                r = type(self)()
                r.arr = arr
                r.context = context
                return r
        class B(A):
            __array_priority__ = 20.
        class C(A):
            __array_priority__ = 40.
        x = np.zeros(1)
        a = A()
        b = B()
        c = C()
        f = ncu.minimum
        self.failUnless(type(f(x,x)) is np.ndarray)
        self.failUnless(type(f(x,a)) is A)
        self.failUnless(type(f(x,b)) is B)
        self.failUnless(type(f(x,c)) is C)
        self.failUnless(type(f(a,x)) is A)
        self.failUnless(type(f(b,x)) is B)
        self.failUnless(type(f(c,x)) is C)

        self.failUnless(type(f(a,a)) is A)
        self.failUnless(type(f(a,b)) is B)
        self.failUnless(type(f(b,a)) is B)
        self.failUnless(type(f(b,b)) is B)
        self.failUnless(type(f(b,c)) is C)
        self.failUnless(type(f(c,b)) is C)
        self.failUnless(type(f(c,c)) is C)

        self.failUnless(type(ncu.exp(a) is A))
        self.failUnless(type(ncu.exp(b) is B))
        self.failUnless(type(ncu.exp(c) is C))

    def test_failing_wrap(self):
        class A(object):
            def __array__(self):
                return np.zeros(1)
            def __array_wrap__(self, arr, context):
                raise RuntimeError
        a = A()
        self.failUnlessRaises(RuntimeError, ncu.maximum, a, a)

    def test_array_with_context(self):
        class A(object):
            def __array__(self, dtype=None, context=None):
                func, args, i = context
                self.func = func
                self.args = args
                self.i = i
                return np.zeros(1)
        class B(object):
            def __array__(self, dtype=None):
                return np.zeros(1, dtype)
        class C(object):
            def __array__(self):
                return np.zeros(1)
        a = A()
        ncu.maximum(np.zeros(1), a)
        self.failUnless(a.func is ncu.maximum)
        assert_equal(a.args[0], 0)
        self.failUnless(a.args[1] is a)
        self.failUnless(a.i == 1)
        assert_equal(ncu.maximum(a, B()), 0)
        assert_equal(ncu.maximum(a, C()), 0)


class TestChoose(TestCase):
    def test_mixed(self):
        c = np.array([True,True])
        a = np.array([True,True])
        assert_equal(np.choose(c, (a, 1)), np.array([1,1]))


class TestComplexFunctions(TestCase):
    funcs = [np.arcsin , np.arccos , np.arctan, np.arcsinh, np.arccosh,
             np.arctanh, np.sin    , np.cos   , np.tan    , np.exp,
             np.log    , np.sqrt   , np.log10]

    def test_it(self):
        for f in self.funcs:
            if f is np.arccosh :
                x = 1.5
            else :
                x = .5
            fr = f(x)
            fz = f(np.complex(x))
            assert_almost_equal(fz.real, fr, err_msg='real part %s'%f)
            assert_almost_equal(fz.imag, 0., err_msg='imag part %s'%f)

    def test_precisions_consistent(self) :
        z = 1 + 1j
        for f in self.funcs :
            fcf = f(np.csingle(z))
            fcd  = f(np.cdouble(z))
            fcl = f(np.clongdouble(z))
            assert_almost_equal(fcf, fcd, decimal=6, err_msg='fch-fcd %s'%f)
            assert_almost_equal(fcl, fcd, decimal=15, err_msg='fch-fcl %s'%f)


class TestAttributes(TestCase):
    def test_attributes(self):
        add = ncu.add
        assert_equal(add.__name__, 'add')
        assert add.__doc__.startswith('y = add(x1,x2)\n\n')
        self.failUnless(add.ntypes >= 18) # don't fail if types added
        self.failUnless('ii->i' in add.types)
        assert_equal(add.nin, 2)
        assert_equal(add.nout, 1)
        assert_equal(add.identity, 0)


if __name__ == "__main__":
    run_module_suite()