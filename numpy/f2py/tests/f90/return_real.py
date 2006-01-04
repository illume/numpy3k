__usage__ = """
Run:
  python return_real.py [<f2py options>]
Examples:
  python return_real.py --quiet
"""

import sys
import f2py2e
from Numeric import array

def build(f2py_opts):
    try:
        import f90_ext_return_real
    except ImportError:
        assert not f2py2e.compile('''\
module f90_return_real
  contains
       function t0(value)
         real :: value
         real :: t0
         t0 = value
       end function t0
       function t4(value)
         real(kind=4) :: value
         real(kind=4) :: t4
         t4 = value
       end function t4
       function t8(value)
         real(kind=8) :: value
         real(kind=8) :: t8
         t8 = value
       end function t8
       function td(value)
         double precision :: value
         double precision :: td
         td = value
       end function td

       subroutine s0(t0,value)
         real :: value
         real :: t0
!f2py    intent(out) t0
         t0 = value
       end subroutine s0
       subroutine s4(t4,value)
         real(kind=4) :: value
         real(kind=4) :: t4
!f2py    intent(out) t4
         t4 = value
       end subroutine s4
       subroutine s8(t8,value)
         real(kind=8) :: value
         real(kind=8) :: t8
!f2py    intent(out) t8
         t8 = value
       end subroutine s8
       subroutine sd(td,value)
         double precision :: value
         double precision :: td
!f2py    intent(out) td
         td = value
       end subroutine sd
end module f90_return_real
''','f90_ext_return_real',f2py_opts,source_fn='f90_ret_real.f90')

    from f90_ext_return_real import f90_return_real as m
    test_functions = [m.t0,m.t4,m.t8,m.td,m.s0,m.s4,m.s8,m.sd]
    return test_functions

def runtest(t):
    tname =  t.__doc__.split()[0]
    if tname in ['t0','t4','s0','s4']:
        err = 1e-5
    else:
        err = 0.0
    assert abs(t(234)-234.0)<=err
    assert abs(t(234.6)-234.6)<=err
    assert abs(t(234l)-234.0)<=err
    if sys.version[:3]<='2.2':
        assert abs(t(234.6+3j)-234.6)<=err,`t(234.6+3j)`
    assert abs(t('234')-234)<=err
    assert abs(t('234.6')-234.6)<=err
    assert abs(t(-234)+234)<=err
    assert abs(t([234])-234)<=err
    assert abs(t((234,))-234.)<=err
    assert abs(t(array(234))-234.)<=err
    assert abs(t(array([234]))-234.)<=err
    assert abs(t(array([[234]]))-234.)<=err
    assert abs(t(array([234],'1'))+22)<=err
    assert abs(t(array([234],'s'))-234.)<=err
    assert abs(t(array([234],'i'))-234.)<=err
    assert abs(t(array([234],'l'))-234.)<=err
    assert abs(t(array([234],'b'))-234.)<=err
    assert abs(t(array([234],'f'))-234.)<=err
    assert abs(t(array([234],'d'))-234.)<=err
    if sys.version[:3]<='2.2':
        assert abs(t(array([234+3j],'F'))-234.)<=err,`t(array([234+3j],'F'))`
        assert abs(t(array([234],'D'))-234.)<=err,`t(array([234],'D'))`
    if tname in ['t0','t4','s0','s4']:
        assert t(1e200)==t(1e300) # inf

    try: raise RuntimeError,`t(array([234],'c'))`
    except ValueError: pass
    try: raise RuntimeError,`t('abc')`
    except ValueError: pass

    try: raise RuntimeError,`t([])`
    except IndexError: pass
    try: raise RuntimeError,`t(())`
    except IndexError: pass
    
    try: raise RuntimeError,`t(t)`
    except TypeError: pass
    try: raise RuntimeError,`t({})`
    except TypeError: pass

    try:
        try: raise RuntimeError,`t(10l**400)`
        except OverflowError: pass
    except RuntimeError:
        r = t(10l**400); assert `r` in ['inf','Infinity'],`r`

if __name__=='__main__':
    #import libwadpy
    repeat,f2py_opts = f2py2e.f2py_testing.cmdline()
    test_functions = build(f2py_opts)
    f2py2e.f2py_testing.run(runtest,test_functions,repeat)
    print 'ok'
