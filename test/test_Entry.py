from dirsort import Entry
from nose.tools import assert_equal

DIR  = '/mnt/downloads/video/'
FILE = 'Future.Boy.Conan.S01E05.HDTV.XviD-LOL.1280x960.avi'
FULL = DIR + FILE
SET1  = set(['future', 'boy', 'conan'])
SET2  = set(['Future', 'Boy', 'Conan'])

class TestEntry(object):
    def test_init_1(self):
        entry = Entry(FULL)
        assert_equal(str(entry), FULL)
        entry = Entry(DIR)
        assert_equal(str(entry), DIR)

    def test_init_2(self):
        entry = Entry(DIR, FILE)
        assert_equal(str(entry), FULL)

    def test_init_3(self):
        entry = Entry(DIR, FILE, False)
        assert_equal(str(entry), FULL)
        entry = Entry(DIR, None, True)
        assert_equal(str(entry), DIR)

    def test_process(self):
        entry = Entry(DIR, FILE, False)
        assert_equal (set(entry.process()), SET1)
