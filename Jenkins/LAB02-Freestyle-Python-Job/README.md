# LAB02: Freestyle Job with Python & SCM

This lab guides you through creating a Jenkins Freestyle project that integrates with a Git repository to run a simple Python application and its tests. You'll learn how to configure Source Code Management (SCM) in Jenkins and execute shell commands to manage dependencies, run scripts, and launch tests.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Create a Jenkins Freestyle job that pulls code from a Git repository (your fork).
- Configure SCM settings in Jenkins to specify the repository URL and branch.
- (Optionally) Configure Jenkins to check out repository code to a specific sub-directory within the workspace.
- Add build steps to execute shell commands for:
    - Installing Python package dependencies using `pip` and `requirements.txt`.
    - Running a Python script (`.py`).
    - Executing Python tests using `pytest`.
- Trigger the job manually and inspect the console output to verify SCM checkout, dependency installation, script execution, and test results.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Please follow the **`../../install-and-setup.md`** guide if you haven't done so.
-   **Admin Access to Jenkins:** You need to be able to log in as an admin user.
-   **Python on Jenkins Environment:** The environment where Jenkins build steps execute (the controller for this lab, or an agent in more advanced setups) must have Python 3 and `pip` installed and available in the system's PATH.
-   **Git Client on Jenkins Environment:** The Jenkins controller needs `git` installed to be able to check out code. The `jenkins/jenkins:lts-jdk17` Docker image usually includes this.
-   **GitHub Account and Fork:**
    *   You need a GitHub account.
    *   You must have forked the main `cicd-labs` repository to your own GitHub account (`https://github.com/YOUR_USERNAME/cicd-labs`). This lab requires Jenkins to pull code from **your fork**.
-   **Provided Application Code:** This lab directory (`Jenkins/LAB02-Freestyle-Python-Job/`) contains an `app/` subdirectory with:
    *   `main.py`: A simple Python script.
    *   `requirements.txt`: Lists `pytest` as a dependency.
    *   `tests/test_main.py`: Basic tests for `main.py`.
    This code should be present in your fork when Jenkins tries to check it out.

---

## 🗂️ Folder Structure

```bash
Jenkins/LAB02-Freestyle-Python-Job/
├── README.md         # Overview, objectives, prerequisites, etc. (this file)
├── LAB.md            # Detailed step-by-step instructions to perform the lab
└── app/
    ├── main.py           # Simple Python application
    ├── requirements.txt  # Python dependencies (pytest)
    └── tests/
        └── test_main.py  # Pytest tests for main.py
```

All actions for this lab are performed directly in the Jenkins UI, guided by **`LAB.md`**.

---

## 🚀 Lab Steps

Please refer to the **`LAB.md`** file in this directory for detailed, step-by-step instructions on how to:
1.  Create the Freestyle Jenkins job.
2.  Configure Source Code Management (Git) to point to your repository fork.
3.  Add and configure the necessary "Execute shell" build steps to install dependencies, run the Python script, and execute tests.
4.  Build the job and inspect the console output.

---

## ✅ Validation Checklist

After completing the steps in `LAB.md`:

- [ ] A new Freestyle project (e.g., `python-freestyle-job`) is created in Jenkins.
- [ ] The SCM configuration correctly points to your forked `cicd-labs` GitHub repository and the specified branch.
- [ ] The build steps include commands to install dependencies, run `main.py`, and run `pytest`.
- [ ] The job, when triggered, successfully checks out the code from your repository.
- [ ] The console output shows `pip install` successfully installing `pytest`.
- [ ] The console output includes the message from `app/main.py` (e.g., "Hello, Student from a Jenkins Freestyle job!").
- [ ] The console output shows `pytest` running and all tests passing.
- [ ] The build is marked as "SUCCESS" (e.g., blue or green status icon).

---

## 🧹 Cleanup

To keep your Jenkins instance tidy after completing the lab:

1.  Navigate to the dashboard of your Jenkins instance.
2.  Click on the job name (e.g., `python-freestyle-job`).
3.  In the left-hand menu of the job page, click on **"Delete Project"**.
4.  Confirm by clicking **"Yes"**.

---

## 🧠 Key Concepts

-   **Freestyle Project:** A highly versatile Jenkins job type configurable through the UI.
-   **Source Code Management (SCM):** Jenkins's ability to integrate with version control systems like Git to fetch source code.
    -   **Repository URL:** The address of your Git repository.
    -   **Branch Specifier:** Tells Jenkins which branch(es) to monitor or check out.
    -   **Checkout to a sub-directory:** An SCM option to place checked-out code into a specific folder within the job's workspace, helping to organize files.
-   **Build Steps:** Sequential actions Jenkins performs during a build.
    -   **Execute Shell / Execute Windows Batch Command:** Allows running arbitrary command-line scripts.
-   **Workspace:** A dedicated directory on the Jenkins controller (or agent) where files are checked out and builds are performed for a specific job.
-   **Dependency Management (`pip`, `requirements.txt`):** Standard Python practices for managing package dependencies, usable within Jenkins build steps.
-   **Test Execution (`pytest`):** Integrating automated testing into the CI process.

---

## 🔁 What's Next?

Having successfully run a Python application with tests from SCM in a Freestyle job, you're ready to explore more powerful pipeline definitions.

Proceed to **[../LAB03-Declarative-Pipeline/README.md](../LAB03-Declarative-Pipeline/)** to learn about writing `Jenkinsfile` for creating Declarative Pipelines.

