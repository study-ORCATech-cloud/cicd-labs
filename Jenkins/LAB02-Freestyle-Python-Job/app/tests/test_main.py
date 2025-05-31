import sys
import os

# Add the parent directory (app) to sys.path to allow importing main
# This assumes the test is run from the 'app/tests/' directory or 'app/' is in PYTHONPATH
# For Jenkins, if workspace is the root, and tests are run from workspace root,
# we might need to adjust imports or how pytest is called.
# For simplicity, let's assume pytest is run with app/ as the current directory or in PYTHONPATH.

# To make this more robust when run by pytest from the lab root (e.g. `pytest Jenkins/LAB02.../app/tests`)
# or when Jenkins checks out and `pytest` is called from workspace root:
# We need to ensure `app` directory is discoverable for `from main import greet`.
# One way is to adjust sys.path relative to this test file's location.

# Corrected path insertion to find `main.py` from `app/` directory
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, APP_DIR)

from main import greet

def test_greet():
    assert greet("TestUser") == "Hello, TestUser from a Jenkins Freestyle job!", "Greeting should match expected format"

def test_greet_another_user():
    assert greet("JenkinsFan") == "Hello, JenkinsFan from a Jenkins Freestyle job!", "Greeting should match for another user"

# To run this test directly (optional):
# if __name__ == "__main__":
#     # This allows running `python test_main.py` from the `tests` directory
#     # For pytest, it will discover tests automatically.
#     print(test_greet())
#     print(test_greet_another_user())
#     print("Tests passed if no assertion errors.") 