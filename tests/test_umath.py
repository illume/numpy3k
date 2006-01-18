
from numpy.testing import *
set_package_path()
from numpy.core.umath import minimum, maximum, exp
import numpy.core.umath as ncu
from numpy import zeros, ndarray
restore_path()

class test_log1p(ScipyTestCase):
    def check_log1p(self):
        assert_almost_equal(ncu.log1p(0.2), ncu.log(1.2))
        assert_almost_equal(ncu.log1p(1e-6), ncu.log(1+1e-6))

class test_expm1(ScipyTestCase):
    def check_expm1(self):
        assert_almost_equal(ncu.expm1(0.2), ncu.exp(0.2)-1)
        assert_almost_equal(ncu.expm1(1e-6), ncu.exp(1e-6)-1)

class test_maximum(ScipyTestCase):
    def check_reduce_complex(self):
        assert_equal(maximum.reduce([1,2j]),1)
        assert_equal(maximum.reduce([1+3j,2j]),1+3j)

class test_minimum(ScipyTestCase):
    def check_reduce_complex(self):
        assert_equal(minimum.reduce([1,2j]),2j)

class test_floating_point(ScipyTestCase):
    def check_floating_point(self):
        assert_equal(ncu.FLOATING_POINT_SUPPORT, 1)

class test_special_methods(ScipyTestCase):
    def test_wrap(self):
        class with_wrap(object):
            def __array__(self):
                return zeros(1)
            def __array_wrap__(self, arr, context):
                r = with_wrap()
                r.arr = arr
                r.context = context
                return r 
        a = with_wrap()
        x = minimum(a, a)
        assert_equal(x.arr, zeros(1))
        func, args, i = x.context
        self.failUnless(func is minimum)
        self.failUnlessEqual(len(args), 2)
        assert_equal(args[0], a)
        assert_equal(args[1], a)
        self.failUnlessEqual(i, 0)

    def test_old_wrap(self):
        class with_wrap(object):
            def __array__(self):
                return zeros(1)
            def __array_wrap__(self, arr):
                r = with_wrap()
                r.arr = arr
                return r 
        a = with_wrap()
        x = minimum(a, a)
        assert_equal(x.arr, zeros(1))

    def test_priority(self):
        class A(object):
            def __array__(self):
                return zeros(1)
            def __array_wrap__(self, arr, context):
                r = type(self)()
                r.arr = arr
                r.context = context
                return r
        class B(A):
            __array_priority__ = 20.
        class C(A):
            __array_priority__ = 40.
        x = zeros(1)
        a = A()
        b = B()
        c = C()
        f = minimum
        self.failUnless(type(f(x,x)) is ndarray)
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

        self.failUnless(type(exp(a) is A))
        self.failUnless(type(exp(b) is B))
        self.failUnless(type(exp(c) is C))

    def test_failing_wrap(self):
        class A(object):
            def __array__(self):
                return zeros(1)
            def __array_wrap__(self, arr, context):
                raise RuntimeError
        a = A()
        self.failUnlessRaises(RuntimeError, maximum, a, a)

    def test_array_with_context(self):
        class A(object):
            def __array__(self, dtype=None, context=None):
                func, args, i = context
                self.func = func
                self.args = args
                self.i = i
                return zeros(1)
        class B(object):
            def __array__(self, dtype=None):
                return zeros(1, dtype)
        class C(object):
            def __array__(self):
                return zeros(1)
        a = A()
        maximum(zeros(1), a)
        self.failUnless(a.func is maximum)
        assert_equal(a.args[0], 0)
        self.failUnless(a.args[1] is a)
        self.failUnless(a.i == 1)
        assert_equal(maximum(a, B()), 0)
        assert_equal(maximum(a, C()), 0)

        
if __name__ == "__main__":
    ScipyTest().run()
