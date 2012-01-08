import os
import tempfile
import shutil
from dirsort import Entry
from dirsort import Sorter
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_almost_equal
from nose.tools import assert_true

FILE1 = 'Battlestar.Galactica.S01E01.avi'
FILE2 = 'Farscape.S03E03.HDTV.avi'
FILES = [FILE1, FILE2]

DIR1 = 'Battlestar.Galactica/'
DIR2 = 'FooBar/'
DIRS = [DIR1, DIR2]

class Options:
    def __init__(self):
        self.prefix = None
        self.dirs = False

class TestSorter(object):
    @classmethod
    def setup_class(klass):
        klass.tempdir = tempfile.mkdtemp()
        for f in FILES:
            open(os.path.join(klass.tempdir, f), 'w').close()

        for d in DIRS:
            os.mkdir(os.path.join(klass.tempdir, d))

        klass.sorter = Sorter(Options(), [klass.tempdir])

    @classmethod
    def teardown_class(klass):
        shutil.rmtree(klass.tempdir)

    def test_compare(self):
        e1 = Entry(os.path.join(TestSorter.tempdir, FILE1))
        e2 = Entry(os.path.join(TestSorter.tempdir, FILE2))
        e3 = Entry(os.path.join(TestSorter.tempdir, DIR1))

        f1vs3 = TestSorter.sorter._compare(e1,e3)
        assert_almost_equal(f1vs3, 100)

        f2vs3 = TestSorter.sorter._compare(e2,e3)
        assert_almost_equal(f2vs3, 0)

    def test_run(self):
        result = TestSorter.sorter()
        for r in result:
            if r['factor'] > 99.999:
                assert_true(r['x']['name'] in r['y']['name'] or r['y']['name'] in r['x']['name'])
            elif r['factor'] < 0.001:
                assert_not_equal(r['x']['name'], r['y']['name'])
