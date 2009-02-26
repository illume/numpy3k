# Added Fortran compiler support to config. Currently useful only for
# try_compile call. try_run works but is untested for most of Fortran
# compilers (they must define linker_exe first).
# Pearu Peterson

import os, signal
import warnings
import sys

from distutils.command.config import config as old_config
from distutils.command.config import LANG_EXT
from distutils import log
from distutils.file_util import copy_file
from distutils.ccompiler import CompileError, LinkError
import distutils
from numpy.distutils.exec_command import exec_command
from numpy.distutils.mingw32ccompiler import generate_manifest

LANG_EXT['f77'] = '.f'
LANG_EXT['f90'] = '.f90'

class config(old_config):
    old_config.user_options += [
        ('fcompiler=', None, "specify the Fortran compiler type"),
        ]

    def initialize_options(self):
        self.fcompiler = None
        old_config.initialize_options(self)

    def try_run(self, body, headers=None, include_dirs=None,
                libraries=None, library_dirs=None, lang="c"):
        warnings.warn("\n+++++++++++++++++++++++++++++++++++++++++++++++++\n" \
                      "Usage of try_run is deprecated: please do not \n" \
                      "use it anymore, and avoid configuration checks \n" \
                      "involving running executable on the target machine.\n" \
                      "+++++++++++++++++++++++++++++++++++++++++++++++++\n",
                      DeprecationWarning)
        return old_config.try_run(self, body, headers, include_dirs, libraries,
                                  library_dirs, lang)

    def _check_compiler (self):
        old_config._check_compiler(self)
        from numpy.distutils.fcompiler import FCompiler, new_fcompiler

        if sys.platform == 'win32' and self.compiler.compiler_type == 'msvc':
            # XXX: hack to circumvent a python 2.6 bug with msvc9compiler:
            # initialize call query_vcvarsall, which throws an IOError, and
            # causes an error along the way without much information. We try to
            # catch it here, hoping it is early enough, and print an helpful
            # message instead of Error: None.
            if not self.compiler.initialized:
                try:
                    self.compiler.initialize()
                except IOError, e:
                    msg = """\
Could not initialize compiler instance: do you have Visual Studio
installed ? If you are trying to build with mingw, please use python setup.py
build -c mingw32 instead ). If you have Visual Studio installed, check it is
correctly installed, and the right version (VS 2008 for python 2.6, VS 2003 for
2.5, etc...). Original exception was: %s, and the Compiler
class was %s
============================================================================""" \
                        % (e, self.compiler.__class__.__name__)
                    print """\
============================================================================"""
                    raise distutils.errors.DistutilsPlatformError(msg)

        if not isinstance(self.fcompiler, FCompiler):
            self.fcompiler = new_fcompiler(compiler=self.fcompiler,
                                           dry_run=self.dry_run, force=1,
                                           c_compiler=self.compiler)
            if self.fcompiler is not None:
                self.fcompiler.customize(self.distribution)
                if self.fcompiler.get_version():
                    self.fcompiler.customize_cmd(self)
                    self.fcompiler.show_customization()

    def _wrap_method(self,mth,lang,args):
        from distutils.ccompiler import CompileError
        from distutils.errors import DistutilsExecError
        save_compiler = self.compiler
        if lang in ['f77','f90']:
            self.compiler = self.fcompiler
        try:
            ret = mth(*((self,)+args))
        except (DistutilsExecError,CompileError),msg:
            self.compiler = save_compiler
            raise CompileError
        self.compiler = save_compiler
        return ret

    def _compile (self, body, headers, include_dirs, lang):
        return self._wrap_method(old_config._compile,lang,
                                 (body, headers, include_dirs, lang))

    def _link (self, body,
               headers, include_dirs,
               libraries, library_dirs, lang):
        if self.compiler.compiler_type=='msvc':
            libraries = (libraries or [])[:]
            library_dirs = (library_dirs or [])[:]
            if lang in ['f77','f90']:
                lang = 'c' # always use system linker when using MSVC compiler
                if self.fcompiler:
                    for d in self.fcompiler.library_dirs or []:
                        # correct path when compiling in Cygwin but with
                        # normal Win Python
                        if d.startswith('/usr/lib'):
                            s,o = exec_command(['cygpath', '-w', d],
                                               use_tee=False)
                            if not s: d = o
                        library_dirs.append(d)
                    for libname in self.fcompiler.libraries or []:
                        if libname not in libraries:
                            libraries.append(libname)
            for libname in libraries:
                if libname.startswith('msvc'): continue
                fileexists = False
                for libdir in library_dirs or []:
                    libfile = os.path.join(libdir,'%s.lib' % (libname))
                    if os.path.isfile(libfile):
                        fileexists = True
                        break
                if fileexists: continue
                # make g77-compiled static libs available to MSVC
                fileexists = False
                for libdir in library_dirs:
                    libfile = os.path.join(libdir,'lib%s.a' % (libname))
                    if os.path.isfile(libfile):
                        # copy libname.a file to name.lib so that MSVC linker
                        # can find it
                        libfile2 = os.path.join(libdir,'%s.lib' % (libname))
                        copy_file(libfile, libfile2)
                        self.temp_files.append(libfile2)
                        fileexists = True
                        break
                if fileexists: continue
                log.warn('could not find library %r in directories %s' \
                         % (libname, library_dirs))
        elif self.compiler.compiler_type == 'mingw32':
            generate_manifest(self)
        return self._wrap_method(old_config._link,lang,
                                 (body, headers, include_dirs,
                                  libraries, library_dirs, lang))

    def check_header(self, header, include_dirs=None, library_dirs=None, lang='c'):
        self._check_compiler()
        return self.try_compile(
                "/* we need a dummy line to make distutils happy */", 
                [header], include_dirs)

    def check_decl(self, symbol,
                   headers=None, include_dirs=None):
        self._check_compiler()
        body = """
int main()
{
#ifndef %s
    (void) %s;
#endif
    ;
    return 0;
}""" % (symbol, symbol)

        return self.try_compile(body, headers, include_dirs)

    def check_type_size(self, type_name, headers=None, include_dirs=None, library_dirs=None):
        """Check size of a given type."""
        # XXX: should also implement the cross-compiling version (using binary
        # search + array indexing, see AC_CHECK_SIZEOF).
        self._check_compiler()

        # We declare the functions to avoid warnings with -Wstrict-prototypes
        body = r"""
typedef %(type)s _dist_type_sizeof_;

static long int longval (void)
{
    return (long int) (sizeof (_dist_type_sizeof_));
}
static unsigned long int ulongval (void)
{
    return (long int) (sizeof (_dist_type_sizeof_));
}

#include <stdio.h>
#include <stdlib.h>
int
main (void)
{

    if (((long int) (sizeof (_dist_type_sizeof_))) < 0) {
        long int i = longval ();
        if (i != ((long int) (sizeof (_dist_type_sizeof_))))
            return 1;
        printf("%%ld\n", i);
    } else {
        unsigned long int i = ulongval ();
        if (i != ((long int) (sizeof (_dist_type_sizeof_))))
            return 1;
        printf("%%lu\n", i);
    }

    return 0;
}
""" % {'type': type_name}

        # XXX: this should be refactored (same code as get_output)
        exitcode, output = 255, ''
        size = None
        try:
            src, obj, exe = self._link(body, headers, include_dirs,
                                       [], library_dirs, 'c')
            #exe = os.path.join('.', exe)
            exitstatus, output = exec_command(exe, execute_in='.')
            if hasattr(os, 'WEXITSTATUS'):
                exitcode = os.WEXITSTATUS(exitstatus)
                if os.WIFSIGNALED(exitstatus):
                    sig = os.WTERMSIG(exitstatus)
                    log.error('subprocess exited with signal %d' % (sig,))
                    if sig == signal.SIGINT:
                        # control-C
                        raise KeyboardInterrupt
            else:
                exitcode = exitstatus
            log.info("success!")

            try:
                size = int(output)
            except ValueError:
                log.error("Unexpected output %s" % output)
                log.info("failure")
        except (CompileError, LinkError):
            log.info("failure.")

        self._clean()
        if size is not None:
            return size
        else:
            return -1

    def check_func(self, func,
                   headers=None, include_dirs=None,
                   libraries=None, library_dirs=None,
                   decl=False, call=False, call_args=None):
        # clean up distutils's config a bit: add void to main(), and
        # return a value.
        self._check_compiler()
        body = []
        if decl:
            body.append("int %s (void);" % func)
        # Handle MSVC intrinsics: force MS compiler to make a function call.
        # Useful to test for some functions when built with optimization on, to
        # avoid build error because the intrinsic and our 'fake' test
        # declaration do not match.
        body.append("#ifdef _MSC_VER")
        body.append("#pragma function(%s)" % func)
        body.append("#endif")
        body.append("int main (void) {")
        if call:
            if call_args is None:
                call_args = ''
            body.append("  %s(%s);" % (func, call_args))
        else:
            body.append("  %s;" % func)
        body.append("  return 0;")
        body.append("}")
        body = '\n'.join(body) + "\n"

        return self.try_link(body, headers, include_dirs,
                             libraries, library_dirs)

    def check_funcs_once(self, funcs,
                   headers=None, include_dirs=None,
                   libraries=None, library_dirs=None,
                   decl=False, call=False, call_args=None):
        """Check a list of functions at once.

        This is useful to speed up things, since all the functions in the funcs
        list will be put in one compilation unit.

        Arguments
        ---------
        funcs: seq
            list of functions to test
        include_dirs : seq
            list of header paths
        libraries : seq
            list of libraries to link the code snippet to
        libraru_dirs : seq
            list of library paths
        decl : dict
            for every (key, value), the declaration in the value will be
            used for function in key. If a function is not in the
            dictionay, no declaration will be used.
        call : dict
            for every item (f, value), if the value is True, a call will be
            done to the function f.
        """
        self._check_compiler()
        body = []
        if decl:
            for f, v in decl.items():
                if v:
                    body.append("int %s (void);" % f)

        # Handle MS intrinsics. See check_func for more info.
        body.append("#ifdef _MSC_VER")
        for func in funcs:
            body.append("#pragma function(%s)" % func)
        body.append("#endif")

        body.append("int main (void) {")
        if call:
            for f in funcs:
                if call.has_key(f) and call[f]:
                    if not (call_args and call_args.has_key(f) and call_args[f]):
                        args = ''
                    else:
                        args = call_args[f]
                    body.append("  %s(%s);" % (f, args))
                else:
                    body.append("  %s;" % f)
        else:
            for f in funcs:
                body.append("  %s;" % f)
        body.append("  return 0;")
        body.append("}")
        body = '\n'.join(body) + "\n"

        return self.try_link(body, headers, include_dirs,
                             libraries, library_dirs)

    def get_output(self, body, headers=None, include_dirs=None,
                   libraries=None, library_dirs=None,
                   lang="c"):
        """Try to compile, link to an executable, and run a program
        built from 'body' and 'headers'. Returns the exit status code
        of the program and its output.
        """
        warnings.warn("\n+++++++++++++++++++++++++++++++++++++++++++++++++\n" \
                      "Usage of get_output is deprecated: please do not \n" \
                      "use it anymore, and avoid configuration checks \n" \
                      "involving running executable on the target machine.\n" \
                      "+++++++++++++++++++++++++++++++++++++++++++++++++\n",
                      DeprecationWarning)
        from distutils.ccompiler import CompileError, LinkError
        self._check_compiler()
        exitcode, output = 255, ''
        try:
            src, obj, exe = self._link(body, headers, include_dirs,
                                       libraries, library_dirs, lang)
            exe = os.path.join('.', exe)
            exitstatus, output = exec_command(exe, execute_in='.')
            if hasattr(os, 'WEXITSTATUS'):
                exitcode = os.WEXITSTATUS(exitstatus)
                if os.WIFSIGNALED(exitstatus):
                    sig = os.WTERMSIG(exitstatus)
                    log.error('subprocess exited with signal %d' % (sig,))
                    if sig == signal.SIGINT:
                        # control-C
                        raise KeyboardInterrupt
            else:
                exitcode = exitstatus
            log.info("success!")
        except (CompileError, LinkError):
            log.info("failure.")

        self._clean()
        return exitcode, output
