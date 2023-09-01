from gorp.readfiles import *
from gorp.test.test_ku_options import setup_tempdir
from datetime import datetime, date
import re
from copy import deepcopy
import unittest
from functools import wraps

now = str(datetime.now())
today = str(date.today())
og_dir = os.getcwd()
setup_tempdir()
newdirname = os.path.join(gorpdir, "test", "temp")
os.chdir(newdirname)


def test_len_results_decorator(method, query, correct_len):
    @wraps(method)
    def wrapper(self):
        """receive a query, save the query and results to the TestCase object,
        and test if len(results) == correct_len."""
        self.query = query
        self.session.receive_query(query)
        self.results = deepcopy(self.session.resultset)
        self.assertEqual(len(self.results), correct_len)

    return wrapper


def test_len_results(query, correct_len):
    def wrapper(method):
        return test_len_results_decorator(method, query, correct_len)

    return wrapper


class SMOptionsTester(unittest.TestCase):
    session = GorpSession(print_output=False)

    @test_len_results(query="-s -a -r ''", correct_len=11)
    def test_s_option_simple(self):
        self.assertTrue(
            all(
                (isinstance(v, str) and ("b" in v.lower()))
                for v in self.results.values()
            ),
            f"For query {self.query}, expected a dict mapping fnames to file size strings, got {self.results}",
        )

    @test_len_results(query="-r -a -s<0.5kb ''", correct_len=10)
    def test_s_option_lt_filter(self):
        self.assertFalse(
            any(("dict size vs" in x) for x in results),
            f"Expected results not to contain the 29kb png file, but it contained {self.results}",
        )

    @test_len_results(query="-r -a -s>=50,000MB ''", correct_len=0)
    def test_s_option_ge_filter(self):
        pass

    @test_len_results(query="-m -a -r ''", correct_len=11)
    def test_m_option_simple(self):
        self.assertTrue(
            all(
                isinstance(v, str) and (v[:10] == today) for v in self.results.values()
            ),
            f"For query {self.query}, expected a dict mapping fnames to date strings, got {self.results}",
        )

    @test_len_results(f"-m>={today} -a -r ''", 11)
    def test_m_option_ge_filter(self):
        pass

    @test_len_results(f"-m<{today} -a -r ''", 0)
    def test_m_option_lt_filter(self):
        pass

    @test_len_results("-m -r -s -a ''", 11)
    def test_s_AND_m_simple(self):
        self.assertTrue(
            all(
                isinstance(v, tuple) and (v[0][:10] == today and ("b" in v[1].lower()))
                for v in self.results.values()
            ),
            f"For query {self.query}, expected a dict mapping fnames to (date string, file size string), got {self.results}",
        )

    @test_len_results(f"-m>={today} -r -s>1kb -a ''", 1)
    def test_s_gt_AND_m_ge(self):
        self.assertIn(
            "dict size vs",
            results[0][0],
            f"For query {self.query}, expected results to contain only the 29kb png file, but it contained {results}",
        )

    @test_len_results(f"-m>={today} -r -s>1kb -5 -a ''", 1)
    def test_s_gt_AND_m_ge_AND_num(self):
        # Filtering for >1kb and today or later, and at most 5 files.
        # The num option had a problem with the s and m filters at one point.
        self.assertIn(
            "dict size vs",
            results[0][0],
            f"Expected results to contain only the 29kb png file, but it contained {results}",
        )

    def zzzz_cleanup(self):
        # give it this name so it's guaranteed to be last lexicographically.
        # unittest.TestCase methods are run in alpha order.
        os.chdir(og_dir)
        self.session.close()


if __name__ == "__main__":
    unittest.main()
