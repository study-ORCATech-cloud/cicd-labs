# Service Alpha - app.py

import os

def main():
    python_version = os.getenv("PYTHON_VERSION_INFO", "not specified")
    print(f"Hello from Service Alpha! Running on Python {python_version}.")
    print("Service Alpha dependencies (from requirements.txt) should be installed.")
    # Simulate a simple test
    print("Service Alpha basic test: PASSED")

if __name__ == "__main__":
    main() 