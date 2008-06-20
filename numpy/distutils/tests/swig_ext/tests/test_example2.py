import sys
from numpy.testing import *
set_package_path()
from swig_ext import example2
restore_path()

class TestExample2(TestCase):

    def test_zoo(self):
        z = example2.Zoo()
        z.shut_up('Tiger')
        z.shut_up('Lion')
        z.display()


if __name__ == "__main__":
    nose.run(argv=['', __file__])
