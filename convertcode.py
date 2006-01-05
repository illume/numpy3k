
# This module converts code written for Numeric to run with numpy.base

# Makes the following changes:
#  * Converts typecharacters
#  * Changes import statements (warns of use of from Numeric import *)
#  * Changes import statements (using numerix) ...
#  * Makes search and replace changes to:
#    - .typecode()
#    - .iscontiguous()
#    - .byteswapped()
#    - .itemsize()
#  * Converts .flat to .ravel() except for .flat = xxx or .flat[xxx]
#  * Change typecode= to dtype=
#  * Eliminates savespace=xxx
#  * Replace xxx.spacesaver() with True
#  * Convert xx.savespace(?) to pass + ## xx.savespace(?)
#  #### -- not * Convert a.shape = ? to a.reshape(?) 
#  * Prints warning for use of bool, int, float, copmlex, object, and unicode
#

__all__ = ['fromfile', 'fromstr']

import sys
import os
import re
import glob

flatindex_re = re.compile('([.]flat(\s*?[[=]))')

def replacetypechars(astr):
#    astr = astr.replace("'s'","'h'")
#    astr = astr.replace("'c'","'S1'")
    astr = astr.replace("'b'","'B'")
    astr = astr.replace("'1'","'b'")
#    astr = astr.replace("'w'","'H'")
    astr = astr.replace("'u'","'I'")
    return astr

def changeimports(fstr, name, newname):
    importstr = 'import %s' % name
    importasstr = 'import %s as ' % name
    fromstr = 'from %s import ' % name
    fromall=0

    fstr = fstr.replace(importasstr, 'import %s as ' % newname)
    fstr = fstr.replace(importstr, 'import %s as %s' % (newname,name))

    ind = 0
    Nlen = len(fromstr)
    Nlen2 = len("from %s import " % newname)
    while 1:
        found = fstr.find(fromstr,ind)
        if (found < 0):
            break
        ind = found + Nlen
        if fstr[ind] == '*':
            continue
        fstr = "%sfrom %s import %s" % (fstr[:found], newname, fstr[ind:])
        ind += Nlen2 - Nlen
    return fstr, fromall

def replaceattr(astr):
    astr = astr.replace(".typecode()",".dtypechar")
    astr = astr.replace(".iscontiguous()",".flags.contiguous")
    astr = astr.replace(".byteswapped()",".byteswap()")
    astr = astr.replace(".toscalar()", ".item()")
    astr = astr.replace(".itemsize()",".itemsize")
    # preserve uses of flat that should be o.k.
    tmpstr = flatindex_re.sub("@@@@\\2",astr)
    # replace other uses of flat
    tmpstr = tmpstr.replace(".flat",".ravel()")
    # put back .flat where it was valid
    astr = tmpstr.replace("@@@@", ".flat")
    return astr

svspc = re.compile(r'(\S+\s*[(].+),\s*savespace\s*=.+\s*[)]')
svspc2 = re.compile(r'([^,(\s]+[.]spacesaver[(][)])')
svspc3 = re.compile(r'(\S+[.]savespace[(].*[)])')
#shpe = re.compile(r'(\S+\s*)[.]shape\s*=[^=]\s*(.+)')
def replaceother(astr):
    astr = astr.replace("typecode=","dtype=")
    astr = astr.replace("UserArray","ndarray")
    astr = svspc.sub('\\1)',astr)
    astr = svspc2.sub('True',astr)
    astr = svspc3.sub('pass  ## \\1', astr)
    #astr = shpe.sub('\\1=\\1.reshape(\\2)', astr)
    return astr

import datetime
def fromstr(filestr):
    filestr = replacetypechars(filestr)
    filestr, fromall1 = changeimports(filestr, 'Numeric', 'numpy')
    filestr, fromall1 = changeimports(filestr, 'multiarray',
                                      'numpy.core.multiarray')
    filestr, fromall1 = changeimports(filestr, 'umath',
                                          'numpy.core.umath')
    filestr, fromall1 = changeimports(filestr, 'Precision', 'numpy')
    filestr, fromall2 = changeimports(filestr, 'numerix', 'numpy')
    filestr, fromall3 = changeimports(filestr, 'numpy_base', 'numpy')
    filestr, fromall3 = changeimports(filestr, 'MLab', 'numpy.lib.mlab')
    filestr, fromall3 = changeimports(filestr, 'LinearAlgebra', 'numpy.linalg')
    filestr, fromall3 = changeimports(filestr, 'RNG', 'numpy.random')
    filestr, fromall3 = changeimports(filestr, 'RandomArray', 'numpy.random')
    filestr, fromall3 = changeimports(filestr, 'FFT', 'numpy.dft')
    filestr, fromall3 = changeimports(filestr, 'MA', 'numpy.core.ma')
    fromall = fromall1 or fromall2 or fromall3
    filestr = replaceattr(filestr)
    filestr = replaceother(filestr)
    today = datetime.date.today().strftime('%b %d, %Y')
    name = os.path.split(sys.argv[0])[-1]
    filestr = '## Automatically adapted for '\
              'numpy %s by %s\n\n%s' % (today, name, filestr)
    return filestr

def makenewfile(name, filestr):
    fid = file(name, 'w')
    fid.write(filestr)
    fid.close()

def getandcopy(name):
    fid = file(name)
    filestr = fid.read()
    fid.close()
    base, ext = os.path.splitext(name)
    makenewfile(base+'.orig', filestr)
    return filestr

def fromfile(filename):
    filestr = getandcopy(filename)
    filestr = fromstr(filestr)
    makenewfile(filename, filestr)
           
def fromargs(args):
    filename = args[1]
    fromfile(filename)

def convertall(direc=''):
    files = glob.glob(os.path.join(direc,'*.py'))
    for afile in files:
        fromfile(afile)

if __name__ == '__main__':
    fromargs(sys.argv)
    
             

