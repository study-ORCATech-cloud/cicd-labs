import sys
import os

# Corrected path insertion to find `main.py` from `app/` directory
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, APP_DIR)

from main import greet

def test_greet():
    assert greet("TestUser") == "Hello, TestUser from a Jenkins Declarative Pipeline!", "Greeting should match expected format for Pipeline"

def test_greet_another_user():
    assert greet("PipelineFan") == "Hello, PipelineFan from a Jenkins Declarative Pipeline!", "Greeting should match for another user in Pipeline" 