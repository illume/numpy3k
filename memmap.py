__all__ = ['memmap']

import mmap
from numeric import uint8, ndarray, dtypedescr
from numerictypes import nbytes

valid_filemodes = ["r", "c", "r+", "w+"]
writeable_filemodes = ["r+","w+"]

mode_equivalents = {
    "readonly":"r",
    "copyonwrite":"c",
    "readwrite":"r+",
    "write":"w+"
    }

_globalvar = 0

class memmap(ndarray):
    def __new__(subtype, name, dtype=uint8, mode='r+', offset=0,
                shape=None, fortran=0):
        global _globalvar

        try:
            mode = mode_equivalents[mode]
        except KeyError:
            if mode not in valid_filemodes:
                raise ValueError("mode must be one of %s" % \
                                 (valid_filemodes + mode_equivalents.keys()))

        fid = file(name, (mode == 'c' and 'r' or mode)+'b')

        if (mode == 'w+') and shape is None:
            raise ValueError, "shape must be given"

        fid.seek(0,2)
        flen = fid.tell()
        descr = dtypedescr(dtype)
        _dbytes = descr.itemsize

        if shape is None:
            bytes = flen-offset
            if (bytes % _dbytes):
                fid.close()
                raise ValueError, "Size of available data is not a "\
                      "multiple of data-type size."
            size = bytes // _dbytes
            shape = (size,)
        else:
            if not isinstance(shape, tuple):
                shape = (shape,)
            size = 1
            for k in shape:
                size *= k

        bytes = offset + size*_dbytes

        if mode == 'w+' or (mode == 'r+' and flen < bytes):  
            fid.seek(bytes-1,0)
            fid.write(chr(0))
            fid.flush()

        if mode == 'c':
            acc = mmap.ACCESS_COPY
        elif mode == 'r':
            acc = mmap.ACCESS_READ
        else:
            acc = mmap.ACCESS_WRITE

        mm = mmap.mmap(fid.fileno(), bytes, access=acc)

        _globalvar = 1
        self = ndarray.__new__(subtype, shape, dtype=descr, buffer=mm,
                               offset=offset, fortran=fortran)
        _globalvar = 0
        self._mmap = mm
        self._offset = offset
        self._mode = mode
        self._size = size
        self._name = name
        fid.close()
        return self

    def __array_finalize__(self, obj):
        if not _globalvar:
            raise ValueError, "Cannot create a memmap array that way"

    def sync(self):
        self._mmap.flush()

    def __del__(self):
        try:
            self._mmap.flush()
            del self._mmap
        except AttributeError:
            pass

