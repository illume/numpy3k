"""distutils.command.run_f2py

Implements the Distutils 'run_f2py' command.
"""

# created 2002/01/09, Pearu Peterson 

__revision__ = "$Id$"

from distutils.dep_util import newer
from scipy_distutils.core import Command

import re,os

module_name_re = re.compile(r'\s*python\s*module\s*(?P<name>[\w_]+)',re.I).match
user_module_name_re = re.compile(r'\s*python\s*module\s*(?P<name>[\w_]*?__user__[\w_]*)',re.I).match
fortran_ext_re = re.compile(r'.*[.](f90|f95|f77|for|ftn|f)\Z',re.I).match

class run_f2py(Command):

    description = "\"run_f2py\" runs f2py that builds Fortran wrapper sources"\
                  "(C and occasionally Fortran)."

    user_options = [('build-dir=', 'b',
                     "directory to build fortran wrappers to"),
                    ('debug-capi', None,
                     "generate C/API extensions with debugging code"),
                    ('no-wrap-functions', None,
                     "do not generate wrappers for Fortran functions,etc."),
                    ('force', 'f',
                     "forcibly build everything (ignore file timestamps)"),
                   ]

    def initialize_options (self):
        self.build_dir = None
        self.debug_capi = None
        self.force = None
        self.no_wrap_functions = None
        self.f2py_options = []
    # initialize_options()


    def finalize_options (self):
        self.set_undefined_options('build',
                                   ('build_temp', 'build_dir'),
                                   ('force', 'force'))

        self.f2py_options.extend(['--build-dir',self.build_dir])

        if self.debug_capi is not None:
            self.f2py_options.append('--debug-capi')
        if self.no_wrap_functions is not None:
            self.f2py_options.append('--no-wrap-functions')

    # finalize_options()

    def run (self):
        if self.distribution.has_ext_modules():
            # XXX: might need also
            #  build_flib = self.get_finalized_command('build_flib')
            #  ...
            # for getting extra f2py_options that are specific to
            # a given fortran compiler.
            for ext in self.distribution.ext_modules:
                ext.sources = self.f2py_sources(ext.sources,ext)
                self.fortran_sources_to_flib(ext)
    # run()

    def f2py_sources (self, sources, ext):

        """Walk the list of source files in 'sources', looking for f2py
        interface (.pyf) files.  Run f2py on all that are found, and
        return a modified 'sources' list with f2py source files replaced
        by the generated C (or C++) and Fortran files.
        If 'sources' contains not .pyf files, then create a temporary
        one from the Fortran files in 'sources'.
        """
        import string
        import f2py2e
        # f2py generates the following files for an extension module
        # with a name <modulename>:
        #   <modulename>module.c
        #   <modulename>-f2pywrappers.f  [occasionally]
        # In addition, <f2py2e-dir>/src/fortranobject.{c,h} are needed
        # for building f2py generated extension modules.
        # It is assumed that one pyf file contains defintions for exactly
        # one extension module.

        target_dir = self.build_dir

        new_sources = []
        f2py_sources = []
        fortran_sources = []
        f2py_targets = {}
        f2py_fortran_targets = {}
        target_ext = 'module.c'
        fortran_target_ext = '-f2pywrappers.f'

        for source in sources:
            (base, source_ext) = os.path.splitext(source)
            (source_dir, base) = os.path.split(base)
            if source_ext == ".pyf":                  # f2py interface file
                # get extension module name
                f = open(source)
                for line in f.xreadlines():
                    m = module_name_re(line)
                    if m:
                        if user_module_name_re(line): # skip *__user__* names
                            continue
                        base = m.group('name')
                        break
                f.close()
                if base != ext.name:
                    # XXX: Should we do here more than just warn?
                    self.warn('%s provides %s but this extension is %s' \
                              % (source,`base`,`ext.name`))
                target_file = os.path.join(target_dir,base+target_ext)
                fortran_target_file = os.path.join(target_dir,base+fortran_target_ext)
                f2py_sources.append(source)
                f2py_targets[source] = target_file
                f2py_fortran_targets[source] = fortran_target_file
            elif fortran_ext_re(source_ext):
                fortran_sources.append(source)                
            else:
                new_sources.append(source)

        if not (f2py_sources or fortran_sources):
            return new_sources

        if not f2py_sources:
            # creating a temporary pyf file from fortran sources
            pyf_target = os.path.join(target_dir,ext.name+'.pyf')
            pyf_target_file = os.path.join(target_dir,ext.name+target_ext)
            pyf_fortran_target_file = os.path.join(target_dir,ext.name+fortran_target_ext)
            f2py_opts2 = ['-m',ext.name,'-h',pyf_target,'--overwrite-signature']
            for source in fortran_sources:
                if newer(source,pyf_target) or self.force:
                    self.announce("f2py-ing a new %s" % (pyf_target))
                    self.announce("f2py-opts: %s" % string.join(f2py_opts2,' '))
                    f2py2e.run_main(fortran_sources + f2py_opts2)
                    break
            f2py_sources.append(pyf_target)
            f2py_targets[pyf_target] = pyf_target_file
            f2py_fortran_targets[pyf_target] = pyf_fortran_target_file

        new_sources.extend(fortran_sources)

        if len(f2py_sources) > 1:
            self.warn('Only one .pyf file can be used per Extension but got %s.'\
                      % (len(f2py_sources)))

        # a bit of a hack, but I think it'll work.  Just include one of
        # the fortranobject.c files that was copied into most 
        d = os.path.dirname(f2py2e.__file__)
        new_sources.append(os.path.join(d,'src','fortranobject.c'))
        ext.include_dirs.append(os.path.join(d,'src'))

        f2py_options = ext.f2py_options + self.f2py_options

        # make sure the target dir exists
        from distutils.dir_util import mkpath
        mkpath(target_dir)

        for source in f2py_sources:
            target = f2py_targets[source]
            fortran_target = f2py_fortran_targets[source]
            if newer(source,target) or self.force:
                self.announce("f2py-ing %s to %s" % (source, target))
                self.announce("f2py-opts: %s" % string.join(f2py_options,' '))
                f2py2e.run_main(f2py_options + [source])
            new_sources.append(target)
            if os.path.exists(fortran_target):
                new_sources.append(fortran_target)

        return new_sources

    # f2py_sources ()

    def fortran_sources_to_flib(self, ext):
        """
        Extract fortran files from ext.sources and append them to
        fortran_libraries item having the same name as ext.
        """
        sources = []
        f_files = []

        for file in ext.sources:
            if fortran_ext_re(file):
                f_files.append(file)
            else:
                sources.append(file)
        if not f_files:
            return

        ext.sources = sources

        if self.distribution.fortran_libraries is None:
            self.distribution.fortran_libraries = []
        fortran_libraries = self.distribution.fortran_libraries

        name = ext.name
        flib = None
        for n,d in fortran_libraries:
            if n == name:
                flib = d
                break
        if flib is None:
            flib = {'sources':[]}
            fortran_libraries.append((name,flib))

        flib['sources'].extend(f_files)
        
# class run_f2py
