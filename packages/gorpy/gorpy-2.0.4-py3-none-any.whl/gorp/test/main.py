import doctest
from gorp.test import test_jsonpath
from gorp.utils import gorpdir
import os
import subprocess

test_dir = os.path.dirname(__file__)


def main():
    print(
        "WARNING: If you put any files into testDir other than what's in there by default, some of the tests are likely to fail."
    )
    print("======================")
    print("Testing gorp.jsonpath (no output means everything is fine)")
    doctest.testmod(test_jsonpath)
    doctest.testmod(test_jsonpath.aggregate)
    og_dir = os.getcwd()
    os.chdir(os.path.dirname(gorpdir))
    try:
        for mod in os.listdir(test_dir):
            mod = os.path.join(test_dir, mod)
            if (
                mod[-2:] == "py"
                and os.path.isfile(mod)
                and "jsonpath" not in mod
                and os.path.basename(mod) not in ["main.py", "__init__.py"]
            ):
                print("======================")
                print(mod)
                mod_name = os.path.basename(mod)[:-3]
                subprocess.run(f"python -m gorp.test.{mod_name}", shell=True)
    finally:
        os.chdir(og_dir)


if __name__ == "__main__":
    main()
