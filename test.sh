PREFIX=/usr/media/src/src/dsp/numpy/numpy.scons/
rm -rf $PREFIX/build
rm -rf $PREFIX/tmp
python setup.py scons --jobs=4
python setup.py build
python setup.py install --prefix=$PREFIX/tmp
(cd $PREFIX/tmp && PYTHONPATH=$PREFIX/tmp/lib/python2.5/site-packages python -c "import numpy; print numpy; numpy.test(level = 9999)")