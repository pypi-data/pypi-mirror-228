from gorp.readfiles import *
import itertools
import unittest


def get_combos():
    """As of this release, gorp tolerates all 1981 possible combinations of
    the options ['-a', '-r', '-l', '-h', '-i', '-c', '-o', '-n', '-v','-f', '-d', '-docx'].
    I haven't tested all permutations, because there are 479,001,600 permutations.
    This has been tested on Python 3.6 - 3.9.
    I also haven't really looked at all the outputs to make sure that every
    possible combination returns the *right* thing.
    """
    os.chdir(os.path.join(gorpdir, "testDir"))
    base_query = " 'yaml|meat|WAF{2}' /."
    gorptags = ["-a", "-r", "-l", "-h", "-i", "-c", "-o", "-n", "-v", "-f", "-d"]
    try:
        import docx

        gorptags.append("-docx")  # only try option if python-docx installed
    except ImportError:
        pass
    tag_combos = (
        c
        for combos in (itertools.combinations(gorptags, ii) for ii in range(9))
        for c in combos
    )
    query_results = {}
    bad_combos = {}
    session = GorpSession(print_output=False)
    try:
        for combo in tag_combos:
            Combo = " ".join(combo)
            try:
                session.receive_query(Combo + base_query)
                out = session.old_queries["prev"].resultset
                query_results[frozenset(re.findall("[a-z]+", Combo))] = out
            except Exception as ex:
                bad_combos[frozenset(re.findall("[a-z]+", Combo))] = repr(ex)
    finally:
        session.close()
        os.chdir("../..")
        return query_results, bad_combos


class OptionComboTester(unittest.TestCase):
    def test_combo_results(self):
        query_results, bad_combos = get_combos()
        self.assertEqual(
            len(bad_combos),
            0,
            "At least one combination of options raised an error under normal circumstances",
        )
        finder_o = lambda x: bool(re.fullmatch(flag + "(?:yaml|meat|WAF{2})", x))
        finder_not_o = lambda x: bool(re.search(flag + "(?:yaml|meat|WAF{2})", x))
        for combo, results in query_results.items():
            flag = "(?i)" if "i" in combo else ""
            v = "v" in combo
            if combo & {"f", "a", "d"}:
                finder = finder_o if "o" in combo else finder_not_o
                for fname in results:
                    basemsg = f"combo = {combo}\nfname = {fname}\nresults = {results}\n"
                    with self.subTest(fname=fname):
                        self.assertTrue(
                            finder(fname) ^ v,
                            basemsg
                            + "a filename in the resultset did not match the given regex",
                        )


if __name__ == "__main__":
    unittest.main()
