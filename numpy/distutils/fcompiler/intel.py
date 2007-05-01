# -*- encoding: iso-8859-1 -*-
# above encoding b/c there's a non-ASCII character in the sample output
# of intele
# http://developer.intel.com/software/products/compilers/flin/

import os
import sys

from numpy.distutils.cpuinfo import cpu
from numpy.distutils.ccompiler import simple_version_match
from numpy.distutils.fcompiler import FCompiler, dummy_fortran_file
from numpy.distutils.exec_command import find_executable

def intel_version_match(type):
    # Match against the important stuff in the version string
    return simple_version_match(start=r'Intel.*?Fortran.*?%s.*?Version' % (type,))

class IntelFCompiler(FCompiler):

    compiler_type = 'intel'
    version_match = intel_version_match('32-bit')

    for fc_exe in map(find_executable,['ifort','ifc']):
        if os.path.isfile(fc_exe):
            break

    executables = {
        'version_cmd'  : [fc_exe, "-FI -V -c %(fname)s.f -o %(fname)s.o" \
                          % {'fname':dummy_fortran_file()}],
        'compiler_f77' : [fc_exe,"-72","-w90","-w95"],
        'compiler_fix' : [fc_exe,"-FI"],
        'compiler_f90' : [fc_exe],
        'linker_so'    : [fc_exe,"-shared"],
        'archiver'     : ["ar", "-cr"],
        'ranlib'       : ["ranlib"]
        }

    pic_flags = ['-KPIC']
    module_dir_switch = '-module ' # Don't remove ending space!
    module_include_switch = '-I'

    def get_flags(self):
        opt = self.pic_flags + ["-cm"]
        return opt

    def get_flags_free(self):
        return ["-FR"]

    def get_flags_opt(self):
        return ['-O3','-unroll']

    def get_flags_arch(self):
        opt = []
        if cpu.has_fdiv_bug():
            opt.append('-fdiv_check')
        if cpu.has_f00f_bug():
            opt.append('-0f_check')
        if cpu.is_PentiumPro() or cpu.is_PentiumII() or cpu.is_PentiumIII():
            opt.extend(['-tpp6'])
        elif cpu.is_PentiumM():
            opt.extend(['-tpp7','-xB'])
        elif cpu.is_Pentium():
            opt.append('-tpp5')
        elif cpu.is_PentiumIV() or cpu.is_Xeon():
            opt.extend(['-tpp7','-xW'])
        if cpu.has_mmx() and not cpu.is_Xeon():
            opt.append('-xM')
        if cpu.has_sse2():
            opt.append('-arch SSE2')
        elif cpu.has_sse():
            opt.append('-arch SSE')
        return opt

    def get_flags_linker_so(self):
        opt = FCompiler.get_flags_linker_so(self)
        v = self.get_version()
        if v and v >= '8.0':
            opt.append('-nofor_main')
        opt.extend(self.get_flags_arch())
        return opt

class IntelItaniumFCompiler(IntelFCompiler):
    compiler_type = 'intele'

    version_match = intel_version_match('Itanium')

#Intel(R) Fortran Itanium(R) Compiler for Itanium(R)-based applications
#Version 9.1� � Build 20060928 Package ID: l_fc_c_9.1.039
#Copyright (C) 1985-2006 Intel Corporation.� All rights reserved.
#30 DAY EVALUATION LICENSE

    for fc_exe in map(find_executable,['ifort','efort','efc']):
        if os.path.isfile(fc_exe):
            break

    executables = {
        'version_cmd'  : [fc_exe, "-FI -V -c %(fname)s.f -o %(fname)s.o" \
                          % {'fname':dummy_fortran_file()}],
        'compiler_f77' : [fc_exe,"-FI","-w90","-w95"],
        'compiler_fix' : [fc_exe,"-FI"],
        'compiler_f90' : [fc_exe],
        'linker_so'    : [fc_exe,"-shared"],
        'archiver'     : ["ar", "-cr"],
        'ranlib'       : ["ranlib"]
        }

class IntelEM64TFCompiler(IntelFCompiler):
    compiler_type = 'intelem'

    version_match = intel_version_match('EM64T-based')

    for fc_exe in map(find_executable,['ifort','efort','efc']):
        if os.path.isfile(fc_exe):
            break

    executables = {
        'version_cmd'  : [fc_exe, "-FI -V -c %(fname)s.f -o %(fname)s.o" \
                          % {'fname':dummy_fortran_file()}],
        'compiler_f77' : [fc_exe,"-FI","-w90","-w95"],
        'compiler_fix' : [fc_exe,"-FI"],
        'compiler_f90' : [fc_exe],
        'linker_so'    : [fc_exe,"-shared"],
        'archiver'     : ["ar", "-cr"],
        'ranlib'       : ["ranlib"]
        }

    def get_flags_arch(self):
        opt = []
        if cpu.is_PentiumIV() or cpu.is_Xeon():
            opt.extend(['-tpp7', '-xW'])
        return opt

# Is there no difference in the version string between the above compilers
# and the Visual compilers?

class IntelVisualFCompiler(FCompiler):

    compiler_type = 'intelv'
    version_match = intel_version_match('32-bit')

    ar_exe = 'lib.exe'
    fc_exe = 'ifl'

    executables = {
        'version_cmd'  : [fc_exe, "-FI -V -c %(fname)s.f -o %(fname)s.o" \
                          % {'fname':dummy_fortran_file()}],
        'compiler_f77' : [fc_exe,"-FI","-w90","-w95"],
        'compiler_fix' : [fc_exe,"-FI","-4L72","-w"],
        'compiler_f90' : [fc_exe],
        'linker_so'    : [fc_exe,"-shared"],
        'archiver'     : [ar_exe, "/verbose", "/OUT:"],
        'ranlib'       : None
        }

    compile_switch = '/c '
    object_switch = '/Fo'     #No space after /Fo!
    library_switch = '/OUT:'  #No space after /OUT:!
    module_dir_switch = '/module:' #No space after /module:
    module_include_switch = '/I'

    def get_flags(self):
        opt = ['/nologo','/MD','/nbs','/Qlowercase','/us']
        return opt

    def get_flags_free(self):
        return ["-FR"]

    def get_flags_debug(self):
        return ['/4Yb','/d2']

    def get_flags_opt(self):
        return ['/O3','/Qip','/Qipo','/Qipo_obj']

    def get_flags_arch(self):
        opt = []
        if cpu.is_PentiumPro() or cpu.is_PentiumII():
            opt.extend(['/G6','/Qaxi'])
        elif cpu.is_PentiumIII():
            opt.extend(['/G6','/QaxK'])
        elif cpu.is_Pentium():
            opt.append('/G5')
        elif cpu.is_PentiumIV():
            opt.extend(['/G7','/QaxW'])
        if cpu.has_mmx():
            opt.append('/QaxM')
        return opt

class IntelItaniumVisualFCompiler(IntelVisualFCompiler):

    compiler_type = 'intelev'
    version_match = intel_version_match('Itanium')

    fc_exe = 'efl' # XXX this is a wild guess
    ar_exe = IntelVisualFCompiler.ar_exe

    executables = {
        'version_cmd'  : [fc_exe, "-FI -V -c %(fname)s.f -o %(fname)s.o" \
                          % {'fname':dummy_fortran_file()}],
        'compiler_f77' : [fc_exe,"-FI","-w90","-w95"],
        'compiler_fix' : [fc_exe,"-FI","-4L72","-w"],
        'compiler_f90' : [fc_exe],
        'linker_so'    : [fc_exe,"-shared"],
        'archiver'     : [ar_exe, "/verbose", "/OUT:"],
        'ranlib'       : None
        }

if __name__ == '__main__':
    from distutils import log
    log.set_verbosity(2)
    from numpy.distutils.fcompiler import new_fcompiler
    compiler = new_fcompiler(compiler='intel')
    compiler.customize()
    print compiler.get_version()
