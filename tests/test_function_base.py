
import sys

from numpy.testing import *
set_package_path()
import numpy.lib;reload(numpy.lib)
from numpy.lib import *
from numpy.core import *
del sys.path[0]

class test_any(ScipyTestCase):
    def check_basic(self):
        y1 = [0,0,1,0]
        y2 = [0,0,0,0]
        y3 = [1,0,1,0]
        assert(any(y1))
        assert(any(y3))
        assert(not any(y2))

    def check_nd(self):
        y1 = [[0,0,0],[0,1,0],[1,1,0]]
        assert(any(y1))
        assert_array_equal(sometrue(y1),[1,1,0])
        assert_array_equal(sometrue(y1,axis=1),[0,1,1])

class test_all(ScipyTestCase):
    def check_basic(self):
        y1 = [0,1,1,0]
        y2 = [0,0,0,0]
        y3 = [1,1,1,1]
        assert(not all(y1))
        assert(all(y3))
        assert(not all(y2))
        assert(all(~array(y2)))

    def check_nd(self):
        y1 = [[0,0,1],[0,1,1],[1,1,1]]
        assert(not all(y1))
        assert_array_equal(alltrue(y1),[0,0,1])
        assert_array_equal(alltrue(y1,axis=1),[0,0,1])

class test_average(ScipyTestCase):
    def check_basic(self):
        y1 = array([1,2,3])
        assert(average(y1) == 2.)
        y2 = array([1.,2.,3.])
        assert(average(y2) == 2.)
        y3 = [0.,0.,0.]
        assert(average(y3) == 0.)

        y4 = ones((4,4))
        y4[0,1] = 0
        y4[1,0] = 2
        assert_array_equal(y4.mean(0), average(y4, 0))
        assert_array_equal(y4.mean(1), average(y4, 1))

        y5 = rand(5,5)
        assert_array_equal(y5.mean(0), average(y5, 0))
        assert_array_equal(y5.mean(1), average(y5, 1))

class test_logspace(ScipyTestCase):
    def check_basic(self):
        y = logspace(0,6)
        assert(len(y)==50)
        y = logspace(0,6,num=100)
        assert(y[-1] == 10**6)
        y = logspace(0,6,endpoint=0)
        assert(y[-1] < 10**6)
        y = logspace(0,6,num=7)
        assert_array_equal(y,[1,10,100,1e3,1e4,1e5,1e6])

class test_linspace(ScipyTestCase):
    def check_basic(self):
        y = linspace(0,10)
        assert(len(y)==50)
        y = linspace(2,10,num=100)
        assert(y[-1] == 10)
        y = linspace(2,10,endpoint=0)
        assert(y[-1] < 10)
        y,st = linspace(2,10,retstep=1)
        assert_almost_equal(st,8/49.0)
        assert_array_almost_equal(y,mgrid[2:10:50j],13)

    def check_corner(self):
        y = list(linspace(0,1,1))
        assert y == [0.0], y
        y = list(linspace(0,1,2.5))
        assert y == [0.0, 1.0]

class test_amax(ScipyTestCase):
    def check_basic(self):
        a = [3,4,5,10,-3,-5,6.0]
        assert_equal(amax(a),10.0)
        b = [[3,6.0, 9.0],
             [4,10.0,5.0],
             [8,3.0,2.0]]
        assert_equal(amax(b,axis=0),[8.0,10.0,9.0])
        assert_equal(amax(b,axis=1),[9.0,10.0,8.0])

class test_amin(ScipyTestCase):
    def check_basic(self):
        a = [3,4,5,10,-3,-5,6.0]
        assert_equal(amin(a),-5.0)
        b = [[3,6.0, 9.0],
             [4,10.0,5.0],
             [8,3.0,2.0]]
        assert_equal(amin(b,axis=0),[3.0,3.0,2.0])
        assert_equal(amin(b,axis=1),[3.0,4.0,2.0])

class test_ptp(ScipyTestCase):
    def check_basic(self):
        a = [3,4,5,10,-3,-5,6.0]
        assert_equal(ptp(a),15.0)
        b = [[3,6.0, 9.0],
             [4,10.0,5.0],
             [8,3.0,2.0]]
        assert_equal(ptp(b,axis=0),[5.0,7.0,7.0])
        assert_equal(ptp(b,axis=-1),[6.0,6.0,6.0])

class test_cumsum(ScipyTestCase):
    def check_basic(self):
        ba = [1,2,10,11,6,5,4]
        ba2 = [[1,2,3,4],[5,6,7,9],[10,3,4,5]]
        for ctype in [int8,uint8,int16,uint16,int32,uint32,
                      float32,float64,complex64,complex128]:
            a = array(ba,ctype)
            a2 = array(ba2,ctype)
            assert_array_equal(cumsum(a), array([1,3,13,24,30,35,39],ctype))
            assert_array_equal(cumsum(a2,axis=0), array([[1,2,3,4],[6,8,10,13],
                                                         [16,11,14,18]],ctype))
            assert_array_equal(cumsum(a2,axis=1),
                               array([[1,3,6,10],
                                      [5,11,18,27],
                                      [10,13,17,22]],ctype))

class test_prod(ScipyTestCase):
    def check_basic(self):
        ba = [1,2,10,11,6,5,4]
        ba2 = [[1,2,3,4],[5,6,7,9],[10,3,4,5]]
        for ctype in [int16,uint16,int32,uint32,
                      float32,float64,complex64,complex128]:
            a = array(ba,ctype)
            a2 = array(ba2,ctype)
            if ctype in ['1', 'b']:
                self.failUnlessRaises(ArithmeticError, prod, a)
                self.failUnlessRaises(ArithmeticError, prod, a2, 1)
                self.failUnlessRaises(ArithmeticError, prod, a)
            else:
                assert_equal(prod(a),26400)
                assert_array_equal(prod(a2,axis=0),
                                   array([50,36,84,180],ctype))
                assert_array_equal(prod(a2,axis=-1),array([24, 1890, 600],ctype))

class test_cumprod(ScipyTestCase):
    def check_basic(self):
        ba = [1,2,10,11,6,5,4]
        ba2 = [[1,2,3,4],[5,6,7,9],[10,3,4,5]]
        for ctype in [int16,uint16,int32,uint32,
                      float32,float64,complex64,complex128]:
            a = array(ba,ctype)
            a2 = array(ba2,ctype)
            if ctype in ['1', 'b']:
                self.failUnlessRaises(ArithmeticError, cumprod, a)
                self.failUnlessRaises(ArithmeticError, cumprod, a2, 1)
                self.failUnlessRaises(ArithmeticError, cumprod, a)
            else:
                assert_array_equal(cumprod(a,axis=-1),
                                   array([1, 2, 20, 220,
                                          1320, 6600, 26400],ctype))
                assert_array_equal(cumprod(a2,axis=0),
                                   array([[ 1,  2,  3,   4],
                                          [ 5, 12, 21,  36],
                                          [50, 36, 84, 180]],ctype))
                assert_array_equal(cumprod(a2,axis=-1),
                                   array([[ 1,  2,   6,   24],
                                          [ 5, 30, 210, 1890],
                                          [10, 30, 120,  600]],ctype))

class test_diff(ScipyTestCase):
    def check_basic(self):
        x = [1,4,6,7,12]
        out = array([3,2,1,5])
        out2 = array([-1,-1,4])
        out3 = array([0,5])
        assert_array_equal(diff(x),out)
        assert_array_equal(diff(x,n=2),out2)
        assert_array_equal(diff(x,n=3),out3)

    def check_nd(self):
        x = 20*rand(10,20,30)
        out1 = x[:,:,1:] - x[:,:,:-1]
        out2 = out1[:,:,1:] - out1[:,:,:-1]
        out3 = x[1:,:,:] - x[:-1,:,:]
        out4 = out3[1:,:,:] - out3[:-1,:,:]
        assert_array_equal(diff(x),out1)
        assert_array_equal(diff(x,n=2),out2)
        assert_array_equal(diff(x,axis=0),out3)
        assert_array_equal(diff(x,n=2,axis=0),out4)

class test_angle(ScipyTestCase):
    def check_basic(self):
        x = [1+3j,sqrt(2)/2.0+1j*sqrt(2)/2,1,1j,-1,-1j,1-3j,-1+3j]
        y = angle(x)
        yo = [arctan(3.0/1.0),arctan(1.0),0,pi/2,pi,-pi/2.0,
              -arctan(3.0/1.0),pi-arctan(3.0/1.0)]
        z = angle(x,deg=1)
        zo = array(yo)*180/pi
        assert_array_almost_equal(y,yo,11)
        assert_array_almost_equal(z,zo,11)

class test_trim_zeros(ScipyTestCase):
    """ only testing for integer splits.
    """
    def check_basic(self):
        a= array([0,0,1,2,3,4,0])
        res = trim_zeros(a)
        assert_array_equal(res,array([1,2,3,4]))
    def check_leading_skip(self):
        a= array([0,0,1,0,2,3,4,0])
        res = trim_zeros(a)
        assert_array_equal(res,array([1,0,2,3,4]))
    def check_trailing_skip(self):
        a= array([0,0,1,0,2,3,0,4,0])
        res = trim_zeros(a)
        assert_array_equal(res,array([1,0,2,3,0,4]))


class test_extins(ScipyTestCase):
    def check_basic(self):
        a = array([1,3,2,1,2,3,3])
        b = extract(a>1,a)
        assert_array_equal(b,[3,2,2,3,3])
    def check_insert(self):
        a = array([1,4,3,2,5,8,7])
        insert(a,[0,1,0,1,0,1,0],[2,4,6])
        assert_array_equal(a,[1,2,3,4,5,6,7])
    def check_both(self):
        a = rand(10)
        mask = a > 0.5
        ac = a.copy()
        c = extract(mask, a)
        insert(a,mask,0)
        insert(a,mask,c)
        assert_array_equal(a,ac)

class test_vectorize(ScipyTestCase):
    def check_simple(self):
        def addsubtract(a,b):
            if a > b:
                return a - b
            else:
                return a + b
        f = vectorize(addsubtract)
        r = f([0,3,6,9],[1,3,5,7])
        assert_array_equal(r,[1,6,1,2])
    def check_scalar(self):
        def addsubtract(a,b):
            if a > b:
                return a - b
            else:
                return a + b
        f = vectorize(addsubtract)
        r = f([0,3,6,9],5)
        assert_array_equal(r,[5,8,1,4])



class test_unwrap(ScipyTestCase):
    def check_simple(self):
                #check that unwrap removes jumps greather that 2*pi
        assert_array_equal(unwrap([1,1+2*pi]),[1,1])
        #check that unwrap maintans continuity
        assert(all(diff(unwrap(rand(10)*100))<pi))


class test_filterwindows(ScipyTestCase):
    def check_hanning(self):
        #check symmetry
        w=hanning(10)
        assert_array_almost_equal(w,flipud(w),7)
        #check known value
        assert_almost_equal(sum(w),4.500,4)

    def check_hamming(self):
        #check symmetry
        w=hamming(10)
        assert_array_almost_equal(w,flipud(w),7)
        #check known value
        assert_almost_equal(sum(w),4.9400,4)

    def check_bartlett(self):
        #check symmetry
        w=bartlett(10)
        assert_array_almost_equal(w,flipud(w),7)
        #check known value
        assert_almost_equal(sum(w),4.4444,4)

    def check_blackman(self):
        #check symmetry
        w=blackman(10)
        assert_array_almost_equal(w,flipud(w),7)
        #check known value
        assert_almost_equal(sum(w),3.7800,4)


class test_trapz(ScipyTestCase):
    def check_simple(self):
        r=trapz(exp(-1.0/2*(arange(-10,10,.1))**2)/sqrt(2*pi),dx=0.1)
        #check integral of normal equals 1
        assert_almost_equal(sum(r),1,7)

class test_sinc(ScipyTestCase):
    def check_simple(self):
        assert(sinc(0)==1)
        w=sinc(linspace(-1,1,100))
        #check symmetry
        assert_array_almost_equal(w,flipud(w),7)

class test_histogram(ScipyTestCase):
    def check_simple(self):
        n=100
        v=rand(n)
        (a,b)=histogram(v)
        #check if the sum of the bins equals the number of samples
        assert(sum(a)==n)
        #check that the bin counts are evenly spaced when the data is from a linear function
        (a,b)=histogram(linspace(0,10,100))
        assert(all(a==10))





def compare_results(res,desired):
    for i in range(len(desired)):
        assert_array_equal(res[i],desired[i])

if __name__ == "__main__":
    ScipyTest('numpy.lib.function_base').run()
