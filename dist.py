from distutils.dist import *
from distutils.dist import Distribution as OldDistribution
from distutils.errors import DistutilsSetupError

from types import *

class Distribution (OldDistribution):
    def __init__ (self, attrs=None):
        self.fortran_libraries = None
        OldDistribution.__init__(self, attrs)
    
    def has_f_libraries(self):
        print 'has_f_libraries'
        return self.fortran_libraries and len(self.fortran_libraries) > 0

    def check_data_file_list(self):
        """Ensure that the list of data_files (presumably provided as a
           command option 'data_files') is valid, i.e. it is a list of
           2-tuples, where the tuples are (name, list_of_libraries).
           Raise DistutilsSetupError if the structure is invalid anywhere;
           just returns otherwise."""
        print 'check_data_file_list'
        if type(self.data_files) is not ListType:
            raise DistutilsSetupError, \
                  "'data_files' option must be a list of tuples"

        for lib in self.data_files:
            if type(lib) is not TupleType and len(lib) != 2:
                raise DistutilsSetupError, \
                      "each element of 'data_files' must a 2-tuple"

            if type(lib[0]) is not StringType:
                raise DistutilsSetupError, \
                      "first element of each tuple in 'data_files' " + \
                      "must be a string (the package with the data_file)"

            if type(lib[1]) is not ListType:
                raise DistutilsSetupError, \
                      "second element of each tuple in 'data_files' " + \
                      "must be a list of files."
        # for lib

    # check_data_file_list ()
   
    def get_data_files (self):
        print 'get_data_files'
        self.check_data_file_list()
        filenames = []
        
        # Gets data files specified
        for ext in self.data_files:
            filenames.extend(ext[1])

        return filenames
