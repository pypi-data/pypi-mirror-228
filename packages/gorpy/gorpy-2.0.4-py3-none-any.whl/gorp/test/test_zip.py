from gorp.readfiles import *
from copy import deepcopy
from zipfile import ZipFile
import shutil
import unittest
from functools import wraps
from gorp.test.test_ku_options import setup_tempdir

ogdir = os.getcwd()
original_defaults = deepcopy(DEFAULT_OPTIONS)


def test_files_in_zip_decorator(method, query, correct_files_in_zf):
    @wraps(method)
    def wrapper(self):
        """receive a query, test if the zip file was created, and then test
        to see if the files in the zip file are correct_files_in_zf."""
        self.session.receive_query(query)
        new_listdir = set(os.listdir())
        self.assertEqual(
            new_listdir,
            self.og_listdir | {"zip_test.zip"},
            f"{query} did not correctly create the new zip file 'zip_test.zip'",
        )
        self.zf = ZipFile("zip_test.zip")
        files_in_zf = set(x.filename for x in self.zf.filelist)
        self.assertEqual(files_in_zf, correct_files_in_zf, f"query: {query}")

    return wrapper


def test_files_in_zip(query, correct_files_in_zf):
    def wrapper(method):
        return test_files_in_zip_decorator(method, query, correct_files_in_zf)

    return wrapper


class ZOptionTester(unittest.TestCase):
    zf = None  # placeholder for the ZipFile handle
    session = None

    def setUp(self):
        # run BEFORE EVERY test
        os.chdir(ogdir)
        setup_tempdir()
        os.chdir(os.path.join(gorpdir, "test", "temp"))
        self.og_listdir = set(os.listdir())
        self.session = GorpSession(print_output=False)
        self.session.receive_query("DEFAULTS.PROMPT_Z_OPTION = False")

    def tearDown(self):
        # run AFTER EVERY test
        self.session.close()
        self.zf.close()
        self.zf = None
        if os.path.exists("zip_test.zip"):
            os.unlink("zip_test.zip")
        DEFAULT_OPTIONS = original_defaults

    @test_files_in_zip(
        query="-a 'HUND' -}} -z 'zip_test.zip'",
        correct_files_in_zf={"HUNDENtharst.cpp"},
    )
    def test_one_file(self):
        # one file in same directory
        pass

    @test_files_in_zip(
        query="-a 'dict' /subdir -}} -z 'zip_test.zip'",
        correct_files_in_zf={"dict size vs memory allocated.png"},
    )
    def test_file_diff_dir(self):
        # TEST 2: one file, working from a different directory
        pass

    @test_files_in_zip(
        query="-a -i -r 'dance|dict' /. -}} -z 'zip_test.zip'",
        correct_files_in_zf={
            "The Rolling Stones [ Dance Part 2.py",
            "subdir/dict size vs memory allocated.png",
        },
    )
    def test_multiple_dirs(self):
        # TEST 3: multiple files in multiple directories
        pass

    def test_multi_dirs_from_diff_dir(self):
        # TEST 4: multiple files in multiple directories,
        #   working from a different directory
        query = "-f -r 'subdir_f' /subdir -}} -z 'zip_test.zip'"
        subsubdir = os.path.join("subdir", "subsubdir")
        os.mkdir(subsubdir)
        with open(os.path.join(subsubdir, "subdir_file.txt"), "w") as f:
            f.write("blah")
        self.session.receive_query(query)
        self.zf = ZipFile("zip_test.zip")
        files_in_zf = set(x.filename for x in self.zf.filelist)
        correct_files_in_zf = {
            "subdir_file.txt",
            os.path.join("subsubdir", "subdir_file.txt"),
        }
        other_correct_files_in_zf = {"subdir_file.txt", "subsubdir/subdir_file.txt"}
        # on Windows, it seems that Python sometimes makes the Unix '/' pathsep
        # (which Windows is technically OK with), but the canonical os.path.sep
        # for Windows is '\\', so we wind up having to check both possibilities
        self.assertIn(files_in_zf, [correct_files_in_zf, other_correct_files_in_zf])
        shutil.rmtree(subsubdir)

    @test_files_in_zip(
        query=f"-a 'THARST' /. -}} -z 'zip_test.zip'",
        correct_files_in_zf={
            "BLUTENTHARST.sql",
            "dud(ENTHARST.java",
            "GUT)enTHARST.js",
        },
    )
    def test_multi_files_same_dir(self):
        # uncompressed, multiple same dir
        pass

    @test_files_in_zip(
        query=f"-a 'THARST' /. -}} -zb 'zip_test.zip'",
        correct_files_in_zf={
            "BLUTENTHARST.sql",
            "dud(ENTHARST.java",
            "GUT)enTHARST.js",
        },
    )
    def test_zip_bzip(self):
        # BZIP compression, multiple same dir
        pass

    @test_files_in_zip(
        query=f"-a 'THARST' /. -}} -zl 'zip_test.zip'",
        correct_files_in_zf={
            "BLUTENTHARST.sql",
            "dud(ENTHARST.java",
            "GUT)enTHARST.js",
        },
    )
    def test_zip_lzma(self):
        # LZMA compression, multiple same dir
        pass

    def test_z_overwrites_false(self):
        # TEST 6: Z_OPTION_OVERWRITES is False
        self.session.receive_query("DEFAULTS.Z_OPTION_OVERWRITES = False")
        query = "-f 'js' -}} -zl 'zip_test.zip'"
        correct_files_in_zf1 = {"GUT)enTHARST.js", "RAMMSTEIN 1.json"}
        self.session.receive_query(query)
        query = "-f 'y' -}} -zl 'zip_test.zip'"
        correct_files_in_zf2 = {
            "RAMMSTeIN 10.yaml",
            "The Rolling Stones [ Dance Part 2.py",
        }
        self.session.receive_query(query)
        # run the query twice. The second time you run the query it should
        # create a new zip file, zip_test_0.zip.
        new_listdir = set(os.listdir())
        listdir_diff = new_listdir - self.og_listdir
        correct_listdir_diff = {"zip_test.zip", "zip_test_0.zip"}
        self.assertEqual(
            listdir_diff,
            correct_listdir_diff,
            f"{query} should have created two new zip files, {correct_listdir_diff}, and not {listdir_diff}",
        )
        self.zf = ZipFile("zip_test_0.zip")
        files_in_zf2 = set(x.filename for x in self.zf.filelist)
        self.assertEqual(
            files_in_zf2,
            correct_files_in_zf2,
            f"For query {query}, 'zip_test_0.zip' should have contained only {correct_files_in_zf2}, but instead contained {files_in_zf2}",
        )
        self.zf.close()
        self.zf = ZipFile("zip_test.zip")
        os.unlink("zip_test_0.zip")
        files_in_zf1 = set(x.filename for x in self.zf.filelist)
        self.assertEqual(
            files_in_zf1,
            correct_files_in_zf1,
            f"For query {query}, 'zip_test.zip' should have contained only {correct_files_in_zf1}, but instead contained {files_in_zf1}",
        )

    def test_z_overwrites_true(self):
        self.session.receive_query("DEFAULTS.Z_OPTION_OVERWRITES = True")
        query = "-f 'js' -}} -zl 'zip_test.zip'"
        self.session.receive_query(query)
        query = "-f 'y' -}} -zl 'zip_test.zip'"
        correct_files_in_zf = {
            "RAMMSTeIN 10.yaml",
            "The Rolling Stones [ Dance Part 2.py",
        }
        self.session.receive_query(query)
        # run the query twice. The second time you run the query it should
        # just overwrite the archive
        new_listdir = set(os.listdir())
        listdir_diff = new_listdir - self.og_listdir
        self.assertEqual(
            listdir_diff,
            {"zip_test.zip"},
            f"{query} should have created only one new zip file, 'zip_test.zip', and not {listdir_diff}",
        )
        self.zf = ZipFile("zip_test.zip")
        files_in_zf = set(x.filename for x in self.zf.filelist)
        self.assertEqual(files_in_zf, correct_files_in_zf)


if __name__ == "__main__":
    unittest.main()
