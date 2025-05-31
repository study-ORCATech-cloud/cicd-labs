# tests/test_app.py
import pytest
from app import add, subtract

# Test cases for the 'add' function
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(-5, -5) == -10
    assert add(0, 0) == 0
    assert add(100, 200) == 300

# Test cases for the 'subtract' function
def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(2, 5) == -3
    assert subtract(0, 0) == 0
    assert subtract(-5, -2) == -3
    assert subtract(10, -5) == 15

# Example additional tests (students can observe these patterns)
def test_add_positive_numbers():
    assert add(1, 2) == 3

def test_subtract_positive_numbers():
    assert subtract(10, 5) == 5 