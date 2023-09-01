from gorp.readfiles import GorpSession, gorpdir
from gorp.readfiles import warn_first_import_error
import os
import random
import unittest

try:
    import gorp.pdf_utils  # just importing to get any ImportErrors out of the way
    from gorp.textcache import TextCache
except ImportError as ex:
    warn_first_import_error("pdfminer")
    raise ex
# tested on Python 3.6 - 3.11


ogdir = os.getcwd()


class PDFOptionTester(unittest.TestCase):
    def setUp(self):
        os.chdir(gorpdir)

    def tearDown(self):
        os.chdir(ogdir)

    def test_with_c_i_n_options(self):
        base_query = "-r -a 'pdf$' /testDir -}} "
        regex_dirname = " -i -pdf 'WORLD|html'"
        opt_combos = [("-c", "-n"), ("-n",), ("-c",)]
        bad_combos = {}
        query_results = {}
        with GorpSession(print_output=False) as session:
            for combo in opt_combos:
                with self.subTest(combo=combo):
                    Combo = " ".join(combo)
                    comboset = frozenset(combo)
                    query = base_query + Combo + regex_dirname
                    session.receive_query(query)
                    query_results[comboset] = session.resultset
                    self.assertTrue(
                        query_results[comboset],
                        f"Resultset for query {query} should not be empty, but it is.",
                    )

    def test_no_error_on_nonexistent_file(self):
        nonexistent = ''.join(random.choices('abcdef', k=20)) + '.pdf'
        while os.path.exists(nonexistent):
            nonexistent = ''.join(random.choices('abcdef', k=20)) + '.pdf'
        with GorpSession(print_output=False) as session:
            session.receive_query("-pdf '' /" + nonexistent)

    def test_not_redundant_entries_from_same_file_different_relpath(self):
        with GorpSession(False) as session:
            session.receive_query("-r -pdf 'world' /testDir")
            with self.subTest(resultset=session.resultset):
                self.assertTrue(bool(session.resultset))
            # now change to a different dir and  query the same files again
            session.receive_query('cd testDir')
            session.receive_query("-pdf 'world' /silly_html_example.pdf")
            with self.subTest(session=session):
                self.assertTrue(bool(session.resultset))
        tc = TextCache(os.path.join(gorpdir, 'pdf_textcache.sqlite'))
        # now check if the database contains two entries for the same file
        fnames = tc.files
        silly_html_examples = [f for f in fnames if 'silly_html' in f]
        with self.subTest(silly_html_examples=silly_html_examples):
            self.assertEqual(len(silly_html_examples), 1)
        


if __name__ == "__main__":
    unittest.main()
