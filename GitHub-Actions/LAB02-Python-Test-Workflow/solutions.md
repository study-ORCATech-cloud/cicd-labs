# Solutions for LAB02 - Python Test Workflow

This file contains the solutions for the `TODO` items in the `.github/workflows/python-tests.yml` workflow file.

---

## `python-tests.yml` Solutions

```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"] # Note: "3.10" needs quotes in YAML for some parsers if not at the end of a list

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

### Explanation (`python-tests.yml`):

1.  **Trigger Configuration (`on`):**
    *   The workflow triggers on `push` events to the `main` branch and `pull_request` events targeting the `main` branch.

2.  **Runner OS (`runs-on`):**
    *   `runs-on: ubuntu-latest`: The job will run on the latest Ubuntu runner.

3.  **Strategy Matrix (`strategy.matrix.python-version`):**
    *   `python-version: [3.8, 3.9, "3.10"]`: This creates a build matrix, running the job three times, once for each specified Python version.

4.  **Checkout Code (`uses: actions/checkout@v3`):**
    *   This step uses the official `checkout` action (version 3) to download the repository code into the runner environment.

5.  **Set up Python (`uses: actions/setup-python@v4`):**
    *   This step uses the official `setup-python` action (version 4).
    *   `with: python-version: ${{ matrix.python-version }}`: It configures the Python version for the current job run based on the matrix value.

6.  **Install Dependencies (`run`):**
    *   `python -m pip install --upgrade pip`: Upgrades pip to the latest version.
    *   `pip install -r requirements.txt`: Installs the packages listed in `requirements.txt` (which is `pytest` in this lab).

7.  **Run Tests (`run: pytest`):**
    *   This command executes `pytest`, which will automatically discover and run tests in the `tests/` directory.

--- 