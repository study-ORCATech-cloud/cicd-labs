# LAB02 - Python Test Workflow (GitHub Actions)

In this lab, you'll configure a GitHub Actions workflow to automatically run tests for a Python project using `pytest`. You will work with an existing Python application and its tests, focusing on completing the CI workflow. You'll also learn to use a matrix strategy to test across multiple Python versions.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand how to use a GitHub Actions matrix strategy to test against multiple Python versions (e.g., 3.8, 3.9, 3.10).
- Configure a workflow to automatically install project dependencies using `pip` and `requirements.txt`.
- Integrate `pytest` into a GitHub Actions workflow to execute Python tests.
- Locate and interpret test logs and results within the GitHub Actions UI.
- Examine a `pytest` test suite and understand how it tests a Python application.

---

## 🧰 Prerequisites

- Basic understanding of Python and `pytest`.
- Familiarity with GitHub Actions workflow syntax (as covered in LAB01).
- A GitHub account and a repository for this lab (can be the same one used for LAB01, or a new one).
- Python 3.8+ installed locally (optional, for running tests outside of Actions).

---

## 🗂️ Folder Structure

Your lab directory is already set up with the following structure:

```bash
GitHub-Actions/LAB02-Python-Test-Workflow/
├── .github/
│   └── workflows/
│       └── python-tests.yml  # Your partially completed workflow file with TODOs
├── app.py                   # A simple Python application
├── requirements.txt         # Python dependencies (contains pytest)
├── tests/
│   └── test_app.py          # Python tests for app.py (no TODOs here)
├── README.md                # Lab instructions (this file)
└── solutions.md             # Solutions for python-tests.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB02-Python-Test-Workflow/` directory.

2.  **Examine the Python Application (`app.py`):**
    Open `app.py`. It contains simple `add` and `subtract` functions. You don't need to modify this file, but understanding its functionality will help you understand the tests.

3.  **Examine the Python Tests (`tests/test_app.py`):**
    Open `tests/test_app.py`. This file uses `pytest` to test the functions in `app.py`.
    *   Review the existing test cases for the `add` and `subtract` functions to understand how they verify the application's behavior.
    *   Note: There are no `TODO`s in this Python file for you to complete. The focus is on the GitHub Actions workflow.

4.  **Examine the Dependencies (`requirements.txt`):**
    Open `requirements.txt`. It lists `pytest`, which is required to run the tests.

5.  **Complete the GitHub Actions Workflow (`.github/workflows/python-tests.yml`):**
    Open `.github/workflows/python-tests.yml`. This file contains a partially completed workflow with `TODO` comments.
    Your tasks are to complete the `TODO` sections in this YAML file only.
    *   Configure the `on` section to trigger the workflow on pushes to `main` and pull requests targeting `main`.
    *   Set the `runs-on` key to use `ubuntu-latest`.
    *   Define the `strategy.matrix.python-version` to include Python versions `3.8`, `3.9`, and `3.10`.
    *   Use the `actions/checkout@v3` action in the first step.
    *   Use the `actions/setup-python@v4` action in the second step, ensuring it uses the Python version from the matrix.
    *   In the "Install dependencies" step, write the shell commands to upgrade `pip` and install packages from `requirements.txt`.
    *   In the "Run tests" step, write the command to execute `pytest`.
    Refer to the hints in the `TODO` comments and the concepts learned in LAB01.

6.  **Commit and Push Your Changes:**
    Once you have completed all the `TODO`s in `.github/workflows/python-tests.yml`:
    ```bash
    git add .github/workflows/python-tests.yml
    git commit -m "feat: Complete Python test workflow for LAB02"
    git push origin main
    ```

7.  **Verify Workflow Execution:**
    *   Go to your GitHub repository in your web browser and open the "Actions" tab.
    *   You should see your "Python CI" workflow listed. Click on it.
    *   Observe that the workflow runs jobs for each Python version specified in your matrix (3.8, 3.9, 3.10).
    *   Inspect the logs for each job. Verify that dependencies were installed and `pytest` executed successfully.
    *   If any tests fail, review your `tests/test_app.py` and the workflow logs to debug.

---

## ✅ Validation Checklist

- [ ] The Python test file `tests/test_app.py` has been reviewed and understood.
- [ ] The `.github/workflows/python-tests.yml` file is correctly completed (all `TODO`s addressed).
- [ ] Pushing changes to `main` (or creating a PR to `main`) triggers the "Python CI" workflow.
- [ ] The workflow successfully runs three separate jobs, one for each Python version (3.8, 3.9, 3.10).
- [ ] Each job installs dependencies and executes `pytest`.
- [ ] All provided tests in `tests/test_app.py` pass in all Python versions.
- [ ] You can view the test execution logs in the GitHub Actions tab.
- [ ] You understand where to find the `solutions.md` file for this lab.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for `python-tests.yml` with explanations.

---

## 🧹 Cleanup

To remove the workflow and Python files if desired:
```bash
rm .github/workflows/python-tests.yml
rm app.py
rm requirements.txt
rm -rf tests/
# Optionally, remove solutions.md as well
# rm solutions.md
```
Commit and push the deletions.

---

## 🧠 Key Concepts

-   **Matrix Strategy (`strategy: matrix`):** Allows you to run a job multiple times with different configurations (e.g., different Python versions, operating systems).
-   **`actions/checkout`:** A standard GitHub Action to check out your repository's code into the runner.
-   **`actions/setup-python`:** A standard GitHub Action to set up a specific version of Python on the runner.
-   **`requirements.txt`:** A standard file for listing Python project dependencies, installable with `pip install -r requirements.txt`.
-   **`pytest`:** A popular Python testing framework that makes it easy to write and run tests.
-   **Workflow Triggers (`on: push:`, `on: pull_request:`):** Defining multiple events that can trigger a workflow.

---

## 🌟 Well Done!

You've successfully configured a CI pipeline to test a Python application across multiple Python versions! This is a common and powerful pattern in CI/CD.

---

## 🔁 What's Next?
Continue to [LAB03 - Docker Build and Push](../LAB03-Docker-Build-And-Push/) to learn how to build and publish Docker images using GitHub Actions.

Test early. Test often. CI for the win! 🧪🐍