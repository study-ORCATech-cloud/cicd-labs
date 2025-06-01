import sys
import os

# Corrected path insertion to find `main.py` from `app/` directory
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, APP_DIR)

from main import greet # greet function now from Lab 06 main.py

def test_greet_lab06():
    assert greet("TestUserLab06") == "Hello, TestUserLab06 from Lab 06 (Parallel & Conditional)!", "Greeting should match Lab 06 format"

def test_greet_another_user_lab06():
    assert greet("ConditionalFan") == "Hello, ConditionalFan from Lab 06 (Parallel & Conditional)!", "Greeting should match Lab 06 for another user" 