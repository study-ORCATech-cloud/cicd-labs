# Service Beta - app.py

import os

def main():
    python_version = os.getenv("PYTHON_VERSION_INFO", "not specified")
    print(f"Hello from Service Beta! Running with Python {python_version}.")
    print("Service Beta specific dependencies (from its requirements.txt) should be available.")
    # Simulate a simple test for beta
    print("Service Beta basic test: PASSED")

if __name__ == "__main__":
    main() 