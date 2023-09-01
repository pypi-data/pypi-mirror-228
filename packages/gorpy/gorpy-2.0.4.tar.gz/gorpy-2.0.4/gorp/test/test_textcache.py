from gorp.textcache import TextCache
from gorp.utils import gorpdir
from gorp.test.test_ku_options import setup_tempdir
import json
import os
import time
import unittest

ogdir = os.getcwd()
testdir = os.path.join(gorpdir, "test")
os.chdir(testdir)
tempdir = os.path.join(testdir, "temp")
db_fname = os.path.join(testdir, "temp_textcache.sqlite")
if os.path.exists(db_fname):
    os.unlink(db_fname)
guten_fname = os.path.join(tempdir, "GUT)enTHARST.js")


def populate_cache(tc):
    ogdir = os.getcwd()
    os.chdir(tempdir)
    try:
        for fname in os.listdir(tempdir):
            fname = os.path.join(tempdir, fname)
            if os.path.isfile(fname):
                with open(fname) as f:
                    tc[fname] = f.read().split("\n")
    finally:
        os.chdir(ogdir)


class TextCacheTester(unittest.TestCase):
    tc = TextCache(db_fname)

    # tests are run in alphabetical order, so we can enforce an order by
    # putting numbers before all of their names
    def test_1_db_created(self):
        # check that database was created
        self.assertTrue(os.path.exists("temp_textcache.sqlite"))

    def test_2_populate_cache(self):
        # make temp files, populate cache, check that rows were added
        setup_tempdir()
        populate_cache(self.tc)
        files = self.tc.files
        self.assertEqual(
            len(files),
            9,
            f"TextCache from tempdir should have 9 keys, got {len(files)}",
        )

    def test_3_CRUD(self):
        guten = self.tc.get_all_data(guten_fname)
        self.assertTrue(
            len(guten) == 1 and len(guten[0]) == 5,
            f"self.tc.get_all_data({guten_fname}) has wrong # of elements",
        )
        # test that text is fine
        fname, text, modtime, insert_time, size = guten[0]
        with open(guten_fname) as f:
            true_guten_text = f.read().split("\n")
        self.assertEqual(
            text,
            json.dumps(true_guten_text),
            f"Expected self.tc's text to be {repr(true_guten_text)}, got {repr(text)}",
        )

        # test that insertion when no record exists does not do anything
        self.tc[guten_fname] = true_guten_text
        guten2 = self.tc.get_all_data(guten_fname)
        self.assertEqual(
            guten2,
            guten,
            f"Attempted insertion of unmodified file perturbed the database to make row {guten2}, but it should be unmodified ({guten})",
        )

        # test that self.tc overwrites old record when a file already in the
        # database is changed.
        new_guten_text = ["new guten text", "blah"]
        with open(guten_fname, "w") as f:
            f.write("\n".join(new_guten_text))
        self.tc[guten_fname] = new_guten_text
        guten3 = self.tc.get_all_data(guten_fname)
        self.assertEqual(
            len(guten3),
            1,
            "Insertion of (filename, text) pair where filename already in database should replace the old record, not add a new one.",
        )
        self.assertNotEqual(
            guten3,
            guten,
            f"Attempted insertion of modified file should perturb the database, but it didn't",
        )

        # test that deletion works
        self.tc.pop(guten_fname)
        self.assertNotIn(
            guten_fname, self.tc, f"self.tc.pop should remove {guten_fname}"
        )
        self.assertEqual(
            self.tc.get(guten_fname, 3),
            3,
            "self.tc.get should return default if key doesn't exist",
        )

        # re-add file, make sure it's added correctly
        time.sleep(1)
        with open(guten_fname, "w") as f:
            f.write("\n".join(new_guten_text))
        self.tc[guten_fname] = new_guten_text
        self.assertIn(guten_fname, self.tc, "File deleted should be re-added")

    def test_4_smallest(self):
        smallest = self.tc.smallest_files(9)
        self.assertEqual(len(smallest), 9)
        self.assertEqual(guten_fname, smallest[0][0])

    def test_5_largest(self):
        largest = self.tc.largest_files(9)
        self.assertEqual(len(largest), 9)
        self.assertEqual(guten_fname, largest[8][0])

    def test_6_newest(self):
        newest = self.tc.newest_files()
        self.assertEqual(len(newest), 1)
        self.assertEqual(guten_fname, newest[0][0])

    def test_7_oldest(self):
        oldest = self.tc.oldest_files(9)
        self.assertEqual(guten_fname, oldest[8][0])

    def test_zzzz_teardown(self):
        os.unlink("temp_textcache.sqlite")
        os.chdir(ogdir)


if __name__ == "__main__":
    unittest.main()
