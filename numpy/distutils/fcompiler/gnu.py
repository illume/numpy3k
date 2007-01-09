import re
import os
import sys
import warnings

from numpy.distutils.cpuinfo import cpu
from numpy.distutils.ccompiler import simple_version_match
from numpy.distutils.fcompiler import FCompiler
from numpy.distutils.exec_command import exec_command, find_executable
from numpy.distutils.misc_util import mingw32, msvc_runtime_library

class GnuFCompiler(FCompiler):

    compiler_type = 'gnu'
    version_match = simple_version_match(start=r'GNU Fortran (?!95)')

    # 'g77 --version' results
    # SunOS: GNU Fortran (GCC 3.2) 3.2 20020814 (release)
    # Debian: GNU Fortran (GCC) 3.3.3 20040110 (prerelease) (Debian)
    #         GNU Fortran (GCC) 3.3.3 (Debian 20040401)
    #         GNU Fortran 0.5.25 20010319 (prerelease)
    # Redhat: GNU Fortran (GCC 3.2.2 20030222 (Red Hat Linux 3.2.2-5)) 3.2.2 20030222 (Red Hat Linux 3.2.2-5)

    for fc_exe in map(find_executable,['g77','f77']):
        if os.path.isfile(fc_exe):
            break
    executables = {
        'version_cmd'  : [fc_exe,"--version"],
        'compiler_f77' : [fc_exe, "-g", "-Wall","-fno-second-underscore"],
        'compiler_f90' : None, # Use --fcompiler=gnu95 for f90 codes
        'compiler_fix' : None,
        'linker_so'    : [fc_exe, "-g", "-Wall"],
        'archiver'     : ["ar", "-cr"],
        'ranlib'       : ["ranlib"],
        'linker_exe'   : [fc_exe, "-g", "-Wall"]
        }
    module_dir_switch = None
    module_include_switch = None

    # Cygwin: f771: warning: -fPIC ignored for target (all code is
    # position independent)
    if os.name != 'nt' and sys.platform!='cygwin':
        pic_flags = ['-fPIC']

    # use -mno-cygwin for g77 when Python is not Cygwin-Python
    if sys.platform == 'win32':
        for key in ['version_cmd', 'compiler_f77', 'linker_so', 'linker_exe']:
            executables[key].append('-mno-cygwin')

    g2c = 'g2c'

    suggested_f90_compiler = 'gnu95'

    #def get_linker_so(self):
    #    # win32 linking should be handled by standard linker
    #    # Darwin g77 cannot be used as a linker.
    #    #if re.match(r'(darwin)', sys.platform):
    #    #    return
    #    return FCompiler.get_linker_so(self)

    def get_flags_linker_so(self):
        opt = self.linker_so[1:]
        if sys.platform=='darwin':
            target = os.environ.get('MACOSX_DEPLOYMENT_TARGET', None)
            if target is None:
                target = '10.3'
            major, minor = target.split('.')
            if int(minor) < 3:
                minor = '3'
                warnings.warn('Environment variable '
                    'MACOSX_DEPLOYMENT_TARGET reset to 10.3')
            os.environ['MACOSX_DEPLOYMENT_TARGET'] = '%s.%s' % (major,
                minor)

            opt.extend(['-undefined', 'dynamic_lookup', '-bundle'])
        else:
            opt.append("-shared")
        if sys.platform[:5]=='sunos':
            # SunOS often has dynamically loaded symbols defined in the
            # static library libg2c.a  The linker doesn't like this.  To
            # ignore the problem, use the -mimpure-text flag.  It isn't
            # the safest thing, but seems to work. 'man gcc' says:
            # ".. Instead of using -mimpure-text, you should compile all
            #  source code with -fpic or -fPIC."
            opt.append('-mimpure-text')
        return opt

    def get_libgcc_dir(self):
        status, output = exec_command(self.compiler_f77 +
                                      ['-print-libgcc-file-name'],
                                      use_tee=0)
        if not status:
            return os.path.dirname(output)
        return None

    def get_library_dirs(self):
        opt = []
        if sys.platform[:5] != 'linux':
            d = self.get_libgcc_dir()
            if d:
                # if windows and not cygwin, libg2c lies in a different folder
                if sys.platform == 'win32' and not d.startswith('/usr/lib'):
                    d = os.path.normpath(d)
                    if not os.path.exists(os.path.join(d, 'libg2c.a')):
                        d2 = os.path.abspath(os.path.join(d,
                                                          '../../../../lib'))
                        if os.path.exists(os.path.join(d2, 'libg2c.a')):
                            opt.append(d2)
                opt.append(d)
        return opt

    def get_libraries(self):
        opt = []
        d = self.get_libgcc_dir()
        if d is not None:
            g2c = self.g2c + '-pic'
            f = self.static_lib_format % (g2c, self.static_lib_extension)
            if not os.path.isfile(os.path.join(d,f)):
                g2c = self.g2c
        else:
            g2c = self.g2c

        if g2c is not None:
            opt.append(g2c)
        if sys.platform == 'win32':
            # in case want to link F77 compiled code with MSVC
            opt.append('gcc')
            runtime_lib = msvc_runtime_library()
            if runtime_lib:
                opt.append(runtime_lib)
        if sys.platform == 'darwin':
            opt.append('cc_dynamic')
        return opt

    def get_flags_debug(self):
        return ['-g']

    def get_flags_opt(self):
        if self.get_version()<='3.3.3':
            # With this compiler version building Fortran BLAS/LAPACK
            # with -O3 caused failures in lib.lapack heevr,syevr tests.
            opt = ['-O2']
        else:
            opt = ['-O3']
        opt.append('-funroll-loops')
        return opt

    def get_flags_arch(self):
        opt = []
        if sys.platform=='darwin':
            if os.name != 'posix':
                # this should presumably correspond to Apple
                if cpu.is_ppc():
                    opt.append('-arch ppc')
                elif cpu.is_i386():
                    opt.append('-arch i386')
            for a in '601 602 603 603e 604 604e 620 630 740 7400 7450 750'\
                    '403 505 801 821 823 860'.split():
                if getattr(cpu,'is_ppc%s'%a)():
                    opt.append('-mcpu='+a)
                    opt.append('-mtune='+a)
                    break
            return opt

        # default march options in case we find nothing better
        if cpu.is_i686():
            march_opt = '-march=i686'
        elif cpu.is_i586():
            march_opt = '-march=i586'
        elif cpu.is_i486():
            march_opt = '-march=i486'
        elif cpu.is_i386():
            march_opt = '-march=i386'
        else:
            march_opt = ''

        gnu_ver =  self.get_version()

        if gnu_ver >= '0.5.26': # gcc 3.0
            if cpu.is_AthlonK6():
                march_opt = '-march=k6'
            elif cpu.is_AthlonK7():
                march_opt = '-march=athlon'

        if gnu_ver >= '3.1.1':
            if cpu.is_AthlonK6_2():
                march_opt = '-march=k6-2'
            elif cpu.is_AthlonK6_3():
                march_opt = '-march=k6-3'
            elif cpu.is_AthlonMP():
                march_opt = '-march=athlon-mp'
                # there's also: athlon-tbird, athlon-4, athlon-xp
            elif cpu.is_Nocona():
                march_opt = '-march=nocona'
            elif cpu.is_Prescott():
                march_opt = '-march=prescott'
            elif cpu.is_PentiumIV():
                march_opt = '-march=pentium4'
            elif cpu.is_PentiumIII():
                march_opt = '-march=pentium3'
            elif cpu.is_PentiumM():
                march_opt = '-march=pentium3'
            elif cpu.is_PentiumII():
                march_opt = '-march=pentium2'

        if gnu_ver >= '3.4':
            if cpu.is_Opteron():
                march_opt = '-march=opteron'
            elif cpu.is_Athlon64():
                march_opt = '-march=athlon64'

        if gnu_ver >= '3.4.4':
            if cpu.is_PentiumM():
                march_opt = '-march=pentium-m'

        # Note: gcc 3.2 on win32 has breakage with -march specified
        if '3.1.1' <= gnu_ver <= '3.4' and sys.platform=='win32':
            march_opt = ''

        if march_opt:
            opt.append(march_opt)

        # other CPU flags
        if gnu_ver >= '3.1.1':
            if cpu.has_mmx(): opt.append('-mmmx')
            if cpu.has_3dnow(): opt.append('-m3dnow')

        if gnu_ver > '3.2.2':
            if cpu.has_sse2(): opt.append('-msse2')
            if cpu.has_sse(): opt.append('-msse')
        if gnu_ver >= '3.4':
            if cpu.has_sse3(): opt.append('-msse3')
        if cpu.is_Intel():
            opt.append('-fomit-frame-pointer')
            if cpu.is_32bit():
                opt.append('-malign-double')
        return opt

class Gnu95FCompiler(GnuFCompiler):

    compiler_type = 'gnu95'
    version_match = simple_version_match(start='GNU Fortran 95')

    # 'gfortran --version' results:
    # Debian: GNU Fortran 95 (GCC 4.0.3 20051023 (prerelease) (Debian 4.0.2-3))
    # OS X: GNU Fortran 95 (GCC) 4.1.0
    #       GNU Fortran 95 (GCC) 4.2.0 20060218 (experimental)

    for fc_exe in map(find_executable,['gfortran','f95']):
        if os.path.isfile(fc_exe):
            break
    executables = {
        'version_cmd'  : [fc_exe,"--version"],
        'compiler_f77' : [fc_exe,"-Wall","-ffixed-form","-fno-second-underscore"],
        'compiler_f90' : [fc_exe,"-Wall","-fno-second-underscore"],
        'compiler_fix' : [fc_exe,"-Wall","-ffixed-form","-fno-second-underscore"],
        'linker_so'    : [fc_exe,"-Wall"],
        'archiver'     : ["ar", "-cr"],
        'ranlib'       : ["ranlib"],
        'linker_exe'   : [fc_exe,"-Wall"]
        }

    # use -mno-cygwin flag for g77 when Python is not Cygwin-Python
    if sys.platform == 'win32':
        for key in ['version_cmd', 'compiler_f77', 'compiler_f90',
                    'compiler_fix', 'linker_so', 'linker_exe']:
            executables[key].append('-mno-cygwin')

    module_dir_switch = '-J'
    module_include_switch = '-I'

    g2c = 'gfortran'

    def get_libraries(self):
        opt = GnuFCompiler.get_libraries(self)
        if sys.platform == 'darwin':
            opt.remove('cc_dynamic')
        return opt

if __name__ == '__main__':
    from distutils import log
    log.set_verbosity(2)
    from numpy.distutils.fcompiler import new_fcompiler
    #compiler = new_fcompiler(compiler='gnu')
    compiler = GnuFCompiler()
    compiler.customize()
    print compiler.get_version()
