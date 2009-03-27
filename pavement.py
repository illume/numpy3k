import os
import sys
import subprocess
import re
try:
    from hash import md5
except ImportError:
    import md5

import sphinx

import distutils
import numpy.distutils

try:
    from paver.tasks import VERSION as _PVER
    if not _PVER >= '1.0':
        raise RuntimeError("paver version >= 1.0 required (was %s)" % _PVER)
except ImportError, e:
    raise RuntimeError("paver version >= 1.0 required")

import paver
import paver.doctools
import paver.path
from paver.easy import options, Bunch, task, needs, dry, sh, call_task

from setup import FULLVERSION

# Wine config for win32 builds
WINE_SITE_CFG = ""
WINE_PY25 = "/home/david/.wine/drive_c/Python25/python.exe"
WINE_PY26 = "/home/david/.wine/drive_c/Python26/python.exe"
WINE_PYS = {'2.6' : WINE_PY26, '2.5': WINE_PY25}

PDF_DESTDIR = paver.path.path('build') / 'pdf'
HTML_DESTDIR = paver.path.path('build') / 'html'

RELEASE = 'doc/release/1.3.0-notes.rst'
LOG_START = 'tags/1.2.0'
LOG_END = 'master'
BOOTSTRAP_DIR = "bootstrap"
BOOTSTRAP_PYEXEC = "%s/bin/python" % BOOTSTRAP_DIR
BOOTSTRAP_SCRIPT = "%s/bootstrap.py" % BOOTSTRAP_DIR

options(sphinx=Bunch(builddir="build", sourcedir="source", docroot='doc'),
        virtualenv=Bunch(script_name=BOOTSTRAP_SCRIPT))

# Bootstrap stuff
@task
def bootstrap():
    """create virtualenv in ./install"""
    install = paver.path.path(BOOTSTRAP_DIR)
    if not install.exists():
        install.mkdir()
    call_task('paver.virtual.bootstrap')
    sh('cd %s; %s bootstrap.py' % (BOOTSTRAP_DIR, sys.executable))

@task
def clean():
    """Remove build, dist, egg-info garbage."""
    d = ['build', 'dist', 'numpy.egg-info']
    for i in d:
        paver.path.path(i).rmtree()

    (paver.path.path('doc') / options.sphinx.builddir).rmtree()

@task
def clean_bootstrap():
    paver.path.path('bootstrap').rmtree()

# NOTES/Changelog stuff
def compute_md5():
    released = paver.path.path('installers').listdir()
    checksums = []
    for f in released:
        m = md5.md5(open(f, 'r').read())
        checksums.append('%s  %s' % (m.hexdigest(), f))

    return checksums

def write_release_task(filename='NOTES.txt'):
    source = paver.path.path(RELEASE)
    target = paver.path.path(filename)
    if target.exists():
        target.remove()
    source.copy(target)
    ftarget = open(str(target), 'a')
    ftarget.writelines("""
Checksums
=========

""")
    ftarget.writelines(['%s\n' % c for c in compute_md5()])

def write_log_task(filename='Changelog'):
    st = subprocess.Popen(
            ['git', 'svn', 'log',  '%s..%s' % (LOG_START, LOG_END)],
            stdout=subprocess.PIPE)

    out = st.communicate()[0]
    a = open(filename, 'w')
    a.writelines(out)
    a.close()

@task
def write_release():
    write_release_task()

@task
def write_log():
    write_log_task()

# Doc stuff
@task
@needs('paver.doctools.html')
def html(options):
    """Build numpy documentation and put it into build/docs"""
    builtdocs = paver.path.path("doc") / options.sphinx.builddir / "html"
    HTML_DESTDIR.rmtree()
    builtdocs.copytree(HTML_DESTDIR)

@task
def sdist():
    # To be sure to bypass paver when building sdist... paver + numpy.distutils
    # do not play well together.
    sh('python setup.py sdist --formats=gztar,zip')

@task
@needs('clean')
def bdist_wininst_26():
    _bdist_wininst(pyver='2.6')

@task
@needs('clean')
def bdist_wininst_25():
    _bdist_wininst(pyver='2.5')

@task
@needs('bdist_wininst_25', 'bdist_wininst_26')
def bdist_wininst():
    pass

@task
@needs('clean', 'bdist_wininst')
def winbin():
    pass

def _bdist_wininst(pyver):
    site = paver.path.path('site.cfg')
    exists = site.exists()
    try:
        if exists:
            site.move('site.cfg.bak')
        a = open(str(site), 'w')
        a.writelines(WINE_SITE_CFG)
        a.close()
        sh('%s setup.py build -c mingw32 bdist_wininst' % WINE_PYS[pyver])
    finally:
        site.remove()
        if exists:
            paver.path.path('site.cfg.bak').move(site)

# Mac OS X installer
def macosx_version():
    if not sys.platform == 'darwin':
        raise ValueError("Not darwin ??")
    st = subprocess.Popen(["sw_vers"], stdout=subprocess.PIPE)
    out = st.stdout.readlines()
    ver = re.compile("ProductVersion:\s+([0-9]+)\.([0-9]+)\.([0-9]+)")
    for i in out:
        m = ver.match(i)
        if m:
            return m.groups()

def mpkg_name():
    maj, min = macosx_version()[:2]
    pyver = ".".join([str(i) for i in sys.version_info[:2]])
    return "numpy-%s-py%s-macosx%s.%s.mpkg" % \
            (FULLVERSION, pyver, maj, min)

@task
@needs("setuptools.bdist_mpkg", "doc")
def dmg():
    pyver = ".".join([str(i) for i in sys.version_info[:2]])
    builddir = paver.path.path("build") / "dmg"
    builddir.rmtree()
    builddir.mkdir()

    # Copy mpkg into image source
    mpkg_n = mpkg_name()
    mpkg = paver.path.path("dist") / mpkg_n
    mpkg.copytree(builddir / mpkg_n)
    tmpkg = builddir / mpkg_n
    tmpkg.rename(builddir / ("numpy-%s-py%s.mpkg" % (FULLVERSION, pyver)))

    # Copy docs into image source
    doc_root = paver.path.path(builddir) / "docs"
    html_docs = paver.path.path("docs") / "html"
    #pdf_docs = paver.path.path("docs") / "pdf" / "numpy.pdf"
    html_docs.copytree(doc_root / "html")
    #pdf_docs.copy(doc_root / "numpy.pdf")

    # Build the dmg
    image_name = "numpy-%s.dmg" % FULLVERSION
    image = paver.path.path(image_name)
    image.remove()
    cmd = ["hdiutil", "create", image_name, "-srcdir", str(builddir)]
    sh(" ".join(cmd))
