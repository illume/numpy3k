"""\
SciPy Core
==========

You can support the development of SciPy by purchasing documentation
at

  http://www.trelgol.com

It is being distributed for a fee for a limited time to try and raise
money for development.

Documentation is also available in the docstrings.

Available subpackages
---------------------
"""

import os, sys
NO_SCIPY_IMPORT = os.environ.get('NO_SCIPY_IMPORT',None)
SCIPY_IMPORT_VERBOSE = int(os.environ.get('SCIPY_IMPORT_VERBOSE','0'))

try:
    from __core_config__ import show as show_core_config
except ImportError:
    show_core_config = None

class PackageLoader:
    def __init__(self):
        """ Manages loading SciPy packages.
        """

        self.parent_frame = frame = sys._getframe(1)
        self.parent_name = eval('__name__',frame.f_globals,frame.f_locals)
        self.parent_path = eval('__path__',frame.f_globals,frame.f_locals)
        if not frame.f_locals.has_key('__all__'):
            exec('__all__ = []',frame.f_globals,frame.f_locals)
        self.parent_export_names = eval('__all__',frame.f_globals,frame.f_locals)

        self.info_modules = None
        self.imported_packages = []
        self.verbose = None

    def _get_info_files(self, package_dir, parent_path, parent_package=None):
        """ Return list of (package name,info.py file) from parent_path subdirectories.
        """
        from glob import glob
        files = glob(os.path.join(parent_path,package_dir,'info.py'))
        for info_file in glob(os.path.join(parent_path,package_dir,'info.pyc')):
            if info_file[:-1] not in files:
                files.append(info_file)
        info_files = []
        for info_file in files:
            package_name = os.path.dirname(info_file[len(parent_path)+1:])\
                           .replace(os.sep,'.')
            if parent_package:
                package_name = parent_package + '.' + package_name
            info_files.append((package_name,info_file))
            info_files.extend(self._get_info_files('*',
                                                   os.path.dirname(info_file),
                                                   package_name))
        return info_files

    def _init_info_modules(self, packages=None):
        """Initialize info_modules = {<package_name>: <package info.py module>}.
        """
        import imp
        info_files = []
        if packages is None:
            for path in self.parent_path:
                info_files.extend(self._get_info_files('*',path))
        else:
            for package_name in packages:
                package_dir = os.path.join(*package_name.split('.'))
                for path in self.parent_path:
                    names_files = self._get_info_files(package_dir, path)
                    if names_files:
                        info_files.extend(names_files)
                        break
                else:
                    self.warn('Package %r does not have info.py file. Ignoring.'\
                              % package_name)

        info_modules = self.info_modules
        for package_name,info_file in info_files:
            if info_modules.has_key(package_name):
                continue
            fullname = self.parent_name +'.'+ package_name
            if info_file[-1]=='c':
                filedescriptor = ('.pyc','rb',2)
            else:
                filedescriptor = ('.py','U',1)

            try:
                info_module = imp.load_module(fullname+'.info',
                                              open(info_file,filedescriptor[1]),
                                              info_file,
                                              filedescriptor)
            except Exception,msg:
                self.error(msg)
                info_module = None

            if info_module is None or getattr(info_module,'ignore',False):
                info_modules.pop(package_name,None)
            else:
                self._init_info_modules(getattr(info_module,'depends',[]))
                info_modules[package_name] = info_module

        return

    def _get_sorted_names(self):
        """ Return package names sorted in the order as they should be
        imported due to dependence relations between packages. 
        """

        depend_dict = {}
        for name,info_module in self.info_modules.items():
            depend_dict[name] = getattr(info_module,'depends',[])
        package_names = []

        for name in depend_dict.keys():
            if not depend_dict[name]:
                package_names.append(name)
                del depend_dict[name]

        while depend_dict:
            for name, lst in depend_dict.items():
                new_lst = [n for n in lst if depend_dict.has_key(n)]
                if not new_lst:
                    package_names.append(name)
                    del depend_dict[name]
                else:
                    depend_dict[name] = new_lst

        return package_names

    def __call__(self,*packages, **options):
        """Load one or more packages into scipy's top-level namespace.

    Usage:

       This function is intended to shorten the need to import many of scipy's
       submodules constantly with statements such as

       import scipy.linalg, scipy.fft, scipy.etc...

       Instead, you can say:

         import scipy
         scipy.pkgload('linalg','fft',...)

       or

         scipy.pkgload()

       to load all of them in one call.

       If a name which doesn't exist in scipy's namespace is
       given, an exception [[WHAT? ImportError, probably?]] is raised.
       [NotImplemented]

     Inputs:

       - the names (one or more strings) of all the scipy modules one wishes to
       load into the top-level namespace.

     Optional keyword inputs:

       - verbose - integer specifying verbosity level [default: 0].
       - force   - when True, force reloading loaded packages [default: False].
       - postpone - when True, don't load packages [default: False]

     If no input arguments are given, then all of scipy's subpackages are
     imported.


     Outputs:

       The function returns a tuple with all the names of the modules which
       were actually imported. [NotImplemented]

     """
        frame = self.parent_frame
        self.info_modules = {}
        if options.get('force',False):
            self.imported_packages = []
        self.verbose = verbose = options.get('verbose',False)
        postpone = options.get('postpone',False)

        self._init_info_modules(packages or None)

        self.log('Imports to %r namespace\n----------------------------'\
                 % self.parent_name)

        for package_name in self._get_sorted_names():
            if package_name in self.imported_packages:
                continue
            info_module = self.info_modules[package_name]
            global_symbols = getattr(info_module,'global_symbols',[])            
            if postpone and not global_symbols:
                self.log('__all__.append(%r)' % (package_name))
                if '.' not in package_name:
                    self.parent_export_names.append(package_name)
                continue
            
            old_object = frame.f_locals.get(package_name,None)

            cmdstr = 'import '+package_name
            if self._execcmd(cmdstr):
                continue
            self.imported_packages.append(package_name)
    
            if verbose!=-1:
                new_object = frame.f_locals.get(package_name)
                if old_object is not None and old_object is not new_object:
                    self.warn('Overwriting %s=%s (was %s)' \
                              % (package_name,self._obj2str(new_object),
                                 self._obj2str(old_object)))

            if '.' not in package_name:
                self.parent_export_names.append(package_name)

            for symbol in global_symbols:
                if symbol=='*':
                    symbols = eval('getattr(%s,"__all__",None)'\
                                   % (package_name),
                                   frame.f_globals,frame.f_locals)
                    if symbols is None:
                        symbols = eval('dir(%s)' % (package_name),
                                       frame.f_globals,frame.f_locals)
                        symbols = filter(lambda s:not s.startswith('_'),symbols)
                else:
                    symbols = [symbol]

                if verbose!=-1:
                    old_objects = {}
                    for s in symbols:
                        if frame.f_locals.has_key(s):
                            old_objects[s] = frame.f_locals[s]

                cmdstr = 'from '+package_name+' import '+symbol
                if self._execcmd(cmdstr):
                    continue

                if verbose!=-1:
                    for s,old_object in old_objects.items():
                        new_object = frame.f_locals[s]
                        if new_object is not old_object:
                            self.warn('Overwriting %s=%s (was %s)' \
                                      % (s,self._obj2repr(new_object),
                                         self._obj2repr(old_object)))

                if symbol=='*':
                    self.parent_export_names.extend(symbols)
                else:
                    self.parent_export_names.append(symbol)

        return

    def _execcmd(self,cmdstr):
        """ Execute command in parent_frame."""
        frame = self.parent_frame
        try:
            exec (cmdstr, frame.f_globals,frame.f_locals)
        except Exception,msg:
            self.error('%s -> failed: %s' % (cmdstr,msg))
            return True
        else:
            self.log('%s -> success' % (cmdstr))                            
        return

    def _obj2repr(self,obj):
        """ Return repr(obj) with"""
        module = getattr(obj,'__module__',None)
        file = getattr(obj,'__file__',None)
        if module is not None:
            return repr(obj) + ' from ' + module
        if file is not None:
            return repr(obj) + ' from ' + file
        return repr(obj)

    def log(self,mess):
        if self.verbose>1:
            print >> sys.stderr, str(mess)
    def warn(self,mess):
        if self.verbose>=0:
            print >> sys.stderr, str(mess)
    def error(self,mess):
        if self.verbose!=-1:
            print >> sys.stderr, str(mess)

try:
    import pkg_resources # activate namespace packages (manipulates __path__)
except ImportError:
    pass

pkgload = PackageLoader()

if show_core_config is None:
    print >> sys.stderr, 'Running from scipy core source directory.'
else:
    from core_version import version as __core_version__

    pkgload('testing','base','corefft','corelinalg','random',
            verbose=SCIPY_IMPORT_VERBOSE)


    test = ScipyTest('scipy').test
    __all__.append('test')

__scipy_doc__ = """

SciPy: A scientific computing package for Python
================================================

Available subpackages
---------------------
"""

if NO_SCIPY_IMPORT is not None:
    print >> sys.stderr, 'Skip importing scipy packages (NO_SCIPY_IMPORT=%s)' % (NO_SCIPY_IMPORT)
    show_scipy_config = None
elif show_core_config is None:
    show_scipy_config = None
else:
    try:
        from __scipy_config__ import show as show_scipy_config
    except ImportError:
        show_scipy_config = None


if show_scipy_config is not None:
    from scipy_version import scipy_version as __scipy_version__
    __doc__ += __scipy_doc__
    pkgload(verbose=SCIPY_IMPORT_VERBOSE,postpone=True)
