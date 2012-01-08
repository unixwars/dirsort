import os
import tempfile
import shutil
from dirsort import Sorter
from dirsort import Mover
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_almost_equal
from nose.tools import assert_true

FILE1 = 'Battlestar.Galactica.S01E01.avi'
FILE2 = 'Farscape.S01E01.HDTV.avi'
FILE3 = 'Farscape.S01E02.HDTV.avi'
FILES = [FILE1, FILE2, FILE3]

DIR1 = 'Battlestar.Galactica/'
DIR2 = 'FooBar/'
DIR3 = 'Battlestar.Galactica.Merge/'
DIRS = [DIR1, DIR2, DIR3]

class Options:
    def __init__(self):
        self.prefix = ''
        self.dirs = True
        self.factor = 50
        self.ask = False
        self.demo = False

class TestMover(object):
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
        pass

    def test_run(self):
        m = Mover(Options(), TestMover.sorter())
        m()
        path = os.path.join(TestMover.tempdir, DIR3, FILE1)
        assert_true(os.path.isfile(path))

        dirname = FILE2.split('.')[0]
        path = os.path.join(TestMover.tempdir, dirname, FILE2)
        assert_true(os.path.isfile(path))
