"""
Support code for building Python extensions on Windows.

    # NT stuff
    # 1. Make sure libpython<version>.a exists for gcc.  If not, build it.
    # 2. Force windows to use gcc (we're struggling with MSVC and g77 support)
    # 3. Force windows to use g77

"""

import os
import sys
import log

# Overwrite certain distutils.ccompiler functions:
import numpy.distutils.ccompiler

# NT stuff
# 1. Make sure libpython<version>.a exists for gcc.  If not, build it.
# 2. Force windows to use gcc (we're struggling with MSVC and g77 support)
#    --> this is done in numpy/distutils/ccompiler.py
# 3. Force windows to use g77

import distutils.cygwinccompiler
from distutils.version import StrictVersion
from numpy.distutils.ccompiler import gen_preprocess_options, gen_lib_options
from distutils.errors import DistutilsExecError, CompileError, UnknownFileError

from distutils.unixccompiler import UnixCCompiler
from distutils.msvccompiler import get_build_version as get_build_msvc_version
from numpy.distutils.misc_util import msvc_runtime_library

# the same as cygwin plus some additional parameters
class Mingw32CCompiler(distutils.cygwinccompiler.CygwinCCompiler):
    """ A modified MingW32 compiler compatible with an MSVC built Python.

    """

    compiler_type = 'mingw32'

    def __init__ (self,
                  verbose=0,
                  dry_run=0,
                  force=0):

        distutils.cygwinccompiler.CygwinCCompiler.__init__ (self,
                                                       verbose,dry_run, force)

        # we need to support 3.2 which doesn't match the standard
        # get_versions methods regex
        if self.gcc_version is None:
            import re
            out = os.popen('gcc -dumpversion','r')
            out_string = out.read()
            out.close()
            result = re.search('(\d+\.\d+)',out_string)
            if result:
                self.gcc_version = StrictVersion(result.group(1))

        # A real mingw32 doesn't need to specify a different entry point,
        # but cygwin 2.91.57 in no-cygwin-mode needs it.
        if self.gcc_version <= "2.91.57":
            entry_point = '--entry _DllMain@12'
        else:
            entry_point = ''

        if self.linker_dll == 'dllwrap':
            # Commented out '--driver-name g++' part that fixes weird
            #   g++.exe: g++: No such file or directory
            # error (mingw 1.0 in Enthon24 tree, gcc-3.4.5).
            # If the --driver-name part is required for some environment
            # then make the inclusion of this part specific to that environment.
            self.linker = 'dllwrap' #  --driver-name g++'
        elif self.linker_dll == 'gcc':
            self.linker = 'g++'

        # **changes: eric jones 4/11/01
        # 1. Check for import library on Windows.  Build if it doesn't exist.

        build_import_library()

        # **changes: eric jones 4/11/01
        # 2. increased optimization and turned off all warnings
        # 3. also added --driver-name g++
        #self.set_executables(compiler='gcc -mno-cygwin -O2 -w',
        #                     compiler_so='gcc -mno-cygwin -mdll -O2 -w',
        #                     linker_exe='gcc -mno-cygwin',
        #                     linker_so='%s --driver-name g++ -mno-cygwin -mdll -static %s'
        #                                % (self.linker, entry_point))
        if self.gcc_version <= "3.0.0":
            self.set_executables(compiler='gcc -mno-cygwin -O2 -w',
                                 compiler_so='gcc -mno-cygwin -mdll -O2 -w -Wstrict-prototypes',
                                 linker_exe='g++ -mno-cygwin',
                                 linker_so='%s -mno-cygwin -mdll -static %s'
                                 % (self.linker, entry_point))
        else:
            self.set_executables(compiler='gcc -mno-cygwin -O2 -Wall',
                                 compiler_so='gcc -mno-cygwin -O2 -Wall -Wstrict-prototypes',
                                 linker_exe='g++ -mno-cygwin',
                                 linker_so='g++ -mno-cygwin -shared')
        # added for python2.3 support
        # we can't pass it through set_executables because pre 2.2 would fail
        self.compiler_cxx = ['g++']

        # Maybe we should also append -mthreads, but then the finished
        # dlls need another dll (mingwm10.dll see Mingw32 docs)
        # (-mthreads: Support thread-safe exception handling on `Mingw32')

        # no additional libraries needed
        #self.dll_libraries=[]
        return

    # __init__ ()

    def link(self,
             target_desc,
             objects,
             output_filename,
             output_dir,
             libraries,
             library_dirs,
             runtime_library_dirs,
             export_symbols = None,
             debug=0,
             extra_preargs=None,
             extra_postargs=None,
             build_temp=None,
             target_lang=None):
        # Include the appropiate MSVC runtime library if Python was built
        # with MSVC >= 7.0 (MinGW standard is msvcrt)
        runtime_library = msvc_runtime_library()
        if runtime_library:
            if not libraries:
                libraries = []
            libraries.append(runtime_library)
        args = (self,
                target_desc,
                objects,
                output_filename,
                output_dir,
                libraries,
                library_dirs,
                runtime_library_dirs,
                None, #export_symbols, we do this in our def-file
                debug,
                extra_preargs,
                extra_postargs,
                build_temp,
                target_lang)
        if self.gcc_version < "3.0.0":
            func = distutils.cygwinccompiler.CygwinCCompiler.link
        else:
            func = UnixCCompiler.link
        func(*args[:func.im_func.func_code.co_argcount])
        return

    def object_filenames (self,
                          source_filenames,
                          strip_dir=0,
                          output_dir=''):
        if output_dir is None: output_dir = ''
        obj_names = []
        for src_name in source_filenames:
            # use normcase to make sure '.rc' is really '.rc' and not '.RC'
            (base, ext) = os.path.splitext (os.path.normcase(src_name))

            # added these lines to strip off windows drive letters
            # without it, .o files are placed next to .c files
            # instead of the build directory
            drv,base = os.path.splitdrive(base)
            if drv:
                base = base[1:]

            if ext not in (self.src_extensions + ['.rc','.res']):
                raise UnknownFileError, \
                      "unknown file type '%s' (from '%s')" % \
                      (ext, src_name)
            if strip_dir:
                base = os.path.basename (base)
            if ext == '.res' or ext == '.rc':
                # these need to be compiled to object files
                obj_names.append (os.path.join (output_dir,
                                                base + ext + self.obj_extension))
            else:
                obj_names.append (os.path.join (output_dir,
                                                base + self.obj_extension))
        return obj_names

    # object_filenames ()


def build_import_library():
    """ Build the import libraries for Mingw32-gcc on Windows
    """
    if os.name != 'nt':
        return
    lib_name = "python%d%d.lib" % tuple(sys.version_info[:2])
    lib_file = os.path.join(sys.prefix,'libs',lib_name)
    out_name = "libpython%d%d.a" % tuple(sys.version_info[:2])
    out_file = os.path.join(sys.prefix,'libs',out_name)
    if not os.path.isfile(lib_file):
        log.warn('Cannot build import library: "%s" not found' % (lib_file))
        return
    if os.path.isfile(out_file):
        log.debug('Skip building import library: "%s" exists' % (out_file))
        return
    log.info('Building import library: "%s"' % (out_file))

    from numpy.distutils import lib2def

    def_name = "python%d%d.def" % tuple(sys.version_info[:2])
    def_file = os.path.join(sys.prefix,'libs',def_name)
    nm_cmd = '%s %s' % (lib2def.DEFAULT_NM, lib_file)
    nm_output = lib2def.getnm(nm_cmd)
    dlist, flist = lib2def.parse_nm(nm_output)
    lib2def.output_def(dlist, flist, lib2def.DEF_HEADER, open(def_file, 'w'))

    dll_name = "python%d%d.dll" % tuple(sys.version_info[:2])
    args = (dll_name,def_file,out_file)
    cmd = 'dlltool --dllname %s --def %s --output-lib %s' % args
    status = os.system(cmd)
    # for now, fail silently
    if status:
        log.warn('Failed to build import library for gcc. Linking will fail.')
    #if not success:
    #    msg = "Couldn't find import library, and failed to build it."
    #    raise DistutilsPlatformError, msg
    return

# Functions to deal with visual studio manifests. Manifest are a mechanism to
# enforce strong DLL versioning on windows, and has nothing to do with
# distutils MANIFEST. manifests are XML files with version info, and used by
# the OS loader; they are necessary when linking against a DLL no in the system
# path; in particular, python 2.6 is built against the MS runtime 9 (the one
# from VS 2008), which is not available on most windows systems; python 2.6
# installer does install it in the Win SxS (Side by side) directory, but this
# requires the manifest too. This is a big mess, thanks MS for a wonderful
# system.

# XXX: ideally, we should use exactly the same version as used by python, but I
# have no idea how to obtain the exact version from python. We could use the
# strings utility on python.exe, maybe ?
_MSVCRVER_TO_FULLVER = {'90': "9.0.21022.8"}

def msvc_manifest_xml(maj, min):
    """Given a major and minor version of the MSVCR, returns the
    corresponding XML file."""
    try:
        fullver = _MSVCRVER_TO_FULLVER[str(maj * 10 + min)]
    except KeyError:
        raise ValueError("Version %d,%d of MSVCRT not supported yet" \
                         % (maj, min))
    # Don't be fooled, it looks like an XML, but it is not. In particular, it
    # should not have any space before starting, and its size should be
    # divisible by 4, most likely for alignement constraints when the xml is
    # embedded in the binary...
    # This template was copied directly from the python 2.6 binary (using
    # strings.exe from mingw on python.exe).
    template = """\
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false"></requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity type="win32" name="Microsoft.VC%(maj)d%(min)d.CRT" version="%(fullver)s" processorArchitecture="*" publicKeyToken="1fc8b3b9a1e18e3b"></assemblyIdentity>
    </dependentAssembly>
  </dependency>
</assembly>"""

    return template % {'fullver': fullver, 'maj': maj, 'min': min}

def manifest_rc(name, type='dll'):
    """Return the rc file used to generate the res file which will be embedded
    as manifest for given manifest file name, of given type ('dll' or
    'exe').

    Parameters
    ---------- name: str
            name of the manifest file to embed
        type: str ('dll', 'exe')
            type of the binary which will embed the manifest"""
    if type == 'dll':
        rctype = 2
    elif type == 'exe':
        rctype = 1
    else:
        raise ValueError("Type %s not supported" % type)

    return """\
#include "winuser.h"
%d RT_MANIFEST %s""" % (rctype, name)

def check_embedded_msvcr_match_linked(msver):
    """msver is the ms runtime version used for the MANIFEST."""
    # check msvcr major version are the same for linking and
    # embedding
    msvcv = msvc_runtime_library()
    if msvcv:
        maj = int(msvcv[5:6])
        if not maj == int(msver):
            raise ValueError, \
                  "Discrepancy between linked msvcr " \
                  "(%d) and the one about to be embedded " \
                  "(%d)" % (int(msver), maj)

def configtest_name(config):
    base = os.path.basename(config._gen_temp_sourcefile("yo", [], "c"))
    return os.path.splitext(base)[0]
       
def manifest_name(config):
    # Get configest name (including suffix)  
    root = configtest_name(config)
    exext = config.compiler.exe_extension
    return root + exext + ".manifest"

def rc_name(config):
    # Get configest name (including suffix)  
    root = configtest_name(config)
    return root + ".rc"

def generate_manifest(config):
    msver = get_build_msvc_version()
    if msver is not None:
        if msver >= 8:
            check_embedded_msvcr_match_linked(msver)
            ma = int(msver)
            mi = int((msver - ma) * 10)
            # Write the manifest file
            manxml = msvc_manifest_xml(ma, mi)
            man = open(manifest_name(config), "w")
            config.temp_files.append(manifest_name(config))
            man.write(manxml)
            man.close()
            # # Write the rc file
            # manrc = manifest_rc(manifest_name(self), "exe")
            # rc = open(rc_name(self), "w")
            # self.temp_files.append(manrc)
            # rc.write(manrc)
            # rc.close()
