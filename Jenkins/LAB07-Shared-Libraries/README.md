# LAB07: Using Jenkins Shared Libraries

This lab introduces a powerful feature of Jenkins: **Shared Libraries**. Shared Libraries allow you to define reusable Groovy code (functions, classes) that can be used across multiple Jenkinsfiles. This promotes DRY (Don't Repeat Yourself) principles, simplifies individual Jenkinsfiles, and helps maintain consistency in your CI/CD processes.

In this lab, you will:
1.  Examine a pre-created simple shared library located within this lab's directory.
2.  Configure Jenkins to recognize and load this shared library.
3.  Modify a `Jenkinsfile` to call custom functions from the shared library to perform tasks like installing dependencies and running tests for a sample Python application.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the purpose and basic structure of a Jenkins Shared Library (specifically `vars/` scripts).
- Configure a Global Pipeline Library in Jenkins to load a shared library from a specific path within your SCM (your forked `cicd-labs` repository).
- Use the `@Library` annotation in a `Jenkinsfile` to import a configured shared library.
- Call custom global functions defined in a shared library (`vars` script) from your pipeline steps.
- Appreciate how shared libraries can encapsulate common pipeline logic for reuse.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Refer to **`../../install-and-setup.md`**.
    *   You need **administrator access** to Jenkins to configure Global Pipeline Libraries.
-   **Python & Git on Jenkins Environment:** The Jenkins execution environment (agent or controller) needs Python 3, `pip`, and `git` for the example pipeline to run fully.
-   **GitHub Account and Fork:** Your forked `cicd-labs` repository. The shared library code and the `Jenkinsfile` for this lab are within `Jenkins/LAB07-Shared-Libraries/`.
-   **Basic Groovy Syntax Understanding (Helpful but not strictly required):** Shared libraries are written in Groovy.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB07-Shared-Libraries/
├── README.md                     # Lab overview, objectives, setup, TODOs (this file)
├── Jenkinsfile                   # Declarative Pipeline script that will use the shared library (contains TODOs)
├── solutions.md                  # Contains the completed Jenkinsfile and setup recap
├── example-shared-library/       # Directory containing our simple shared library code
│   └── vars/
│       └── customSteps.groovy    # Groovy script defining custom pipeline steps (provided, complete)
└── app/                          # Sample Python application (reused from Lab 06)
    ├── main.py
    ├── requirements.txt
    └── tests/
        └── test_main.py
```

---

## ✨ Understanding the Provided Shared Library: `example-shared-library`

Located in `Jenkins/LAB07-Shared-Libraries/example-shared-library/`, this simple library demonstrates the `vars/` script pattern.

-   **`vars/customSteps.groovy`**: This file defines global functions that can be called directly in your `Jenkinsfile` once the library is loaded. The filename (`customSteps`) becomes the name of a global variable in your pipeline script, through which you access its functions.
    *   `printMessage(String message)`: A simple function that echoes a formatted message to the console.
    *   `installPythonDependencies(Map config)`: A function to install Python dependencies using `pip` and `requirements.txt` from a given application path (`config.appPath`).
    *   `runPyTests(Map config)`: A function to run `pytest` for a given application path (`config.appPath`).

Your task is **not** to modify this shared library code, but to configure Jenkins to use it and then call its functions from the main `Jenkinsfile` for this lab.

---

## 🔧 Jenkins Configuration: Setting up the Global Pipeline Library

For your `Jenkinsfile` to use the `example-shared-library`, you first need to tell Jenkins where to find it. You'll do this by configuring a "Global Pipeline Library".

1.  **Navigate to Jenkins System Configuration:**
    *   Go to your Jenkins Dashboard.
    *   Click **Manage Jenkins** -> **Configure System**.

2.  **Scroll to "Global Pipeline Libraries":**
    *   Find this section on the page (it might be towards the bottom).

3.  **Add a New Library:**
    *   Click the **"Add"** button under Global Pipeline Libraries.
    *   A set of fields will appear. Configure them as follows:
        *   **Name:** `cicd-lab-library` (You will use this name in your `@Library` annotation. You can choose another name, but be consistent.)
        *   **Default version:** `main` (Or the name of your primary branch in your forked `cicd-labs` repository if it's different, e.g., `master`).
        *   **Retrieval method:** Select **Modern SCM**.
        *   **Source Code Management:** Select **Git**.
        *   **Project Repository:** Enter the HTTPS URL of **your forked `cicd-labs` repository** (e.g., `https://github.com/YOUR_USERNAME/cicd-labs.git`).
        *   **Behaviors (Optional but Recommended):**
            *   Click **"Add"** next to Behaviors.
            *   Select **"Discover branches"** if you want Jenkins to be aware of all branches (though for this lab, `main` is primary).
            *   You might see other options like "Advanced clone behaviours" - for this lab, default clone settings are usually fine.
        *   **Library Path (Optional):** This is **CRUCIAL**. You must specify the path *within your repository* where the shared library code (the directory containing `vars/` and/or `src/`) is located.
            *   Set this to: `Jenkins/LAB07-Shared-Libraries/example-shared-library`
            *   Ensure this path is accurate and points to the directory that directly contains the `vars/` folder.

4.  **Save Jenkins Configuration:**
    *   Click **"Save"** at the bottom of the Configure System page.

Jenkins is now aware of your shared library. Any pipeline can now attempt to load it using `@Library('cicd-lab-library') _` (or whatever name you chose).

---

## 🚀 Lab Steps: Using the Shared Library in `Jenkinsfile`

Your primary task is to complete the `Jenkins/LAB07-Shared-Libraries/Jenkinsfile`.

**1. Locate and Open `Jenkinsfile`:**
   Open `Jenkins/LAB07-Shared-Libraries/Jenkinsfile` in your local clone of your forked repository.

**2. Complete the `TODO` items in `Jenkinsfile`:**

   *   **`TODO_LOAD_LIBRARY` (Line 1-4):**
        *   **Goal:** Tell your pipeline to load the shared library you configured in Jenkins.
        *   **Action:** At the very top of your `Jenkinsfile` (before the `pipeline { ... }` block), add the `@Library()` annotation.
            *   Use the name you gave the library in Jenkins Global Configuration (e.g., `cicd-lab-library`).
            *   Specify the branch using `@branchName` (e.g., `@main`).
            *   The line must end with `_` (an underscore followed by a space).
            *   Example: `@Library('cicd-lab-library@main') _`

   *   **`TODO_CALL_PRINT_MESSAGE` (Line 20-23):**
        *   **Goal:** Call the `printMessage` function from your `customSteps.groovy` shared library script.
        *   **Action:** Since your Groovy script is named `customSteps.groovy`, its functions are available via a global variable named `customSteps`.
            *   Call it like: `customSteps.printMessage("Your custom message for Lab 07 here!")`

   *   **`TODO_CALL_INSTALL_DEPS` (Line 25-26):**
        *   **Goal:** Call the `installPythonDependencies` function from your shared library to install dependencies for the sample Python app.
        *   **Action:** Call `customSteps.installPythonDependencies(...)`. This function accepts a map. You need to pass the `appPath` key with the value of `env.APP_PATH` (which is already defined in the `environment` block).
            *   Example: `customSteps.installPythonDependencies(appPath: env.APP_PATH)`

   *   **`TODO_CALL_RUN_PY_TESTS` (Line 28-29):**
        *   **Goal:** Call the `runPyTests` function from your shared library to run tests for the sample Python app.
        *   **Action:** Call `customSteps.runPyTests(...)`. This also accepts a map where you pass the `appPath`.
            *   Example: `customSteps.runPyTests(appPath: env.APP_PATH)`

**3. Commit and Push `Jenkinsfile` Changes:**
   Save your completed `Jenkinsfile`, then commit and push it to your forked GitHub repository.

**4. Configure and Run Jenkins Pipeline Job:**
   *   In Jenkins, create a new "Pipeline" job (e.g., `lab07-shared-library-pipeline`).
   *   Configure it to use "Pipeline script from SCM," pointing to your forked repository and the `Jenkins/LAB07-Shared-Libraries/Jenkinsfile` script path.
   *   Ensure the branch is correct (e.g., `*/main`).
   *   Save and click "Build Now."
   *   Observe the console output. You should see messages from your shared library functions and see the tests run.

---

## ✅ Validation Checklist

- [ ] The Global Pipeline Library is configured correctly in Jenkins system settings, pointing to your fork and the `Jenkins/LAB07-Shared-Libraries/example-shared-library` path.
- [ ] The `Jenkinsfile` correctly uses `@Library('your-library-name@main') _` at the top.
- [ ] The pipeline job successfully loads the shared library (check console output for any library loading errors).
- [ ] The `customSteps.printMessage()` call executes and its output is visible in the Jenkins console log.
- [ ] The `customSteps.installPythonDependencies()` call executes, and Python dependencies are installed (check logs).
- [ ] The `customSteps.runPyTests()` call executes, and `pytest` runs for the sample application (check logs for test results).
- [ ] The pipeline completes successfully.

---

## 🧹 Cleanup

1.  **Jenkins Job:** Delete the `lab07-shared-library-pipeline` job in Jenkins if no longer needed.
2.  **Global Pipeline Library (Optional):** If you don't plan to reuse it immediately, you can remove the "cicd-lab-library" configuration from **Manage Jenkins** -> **Configure System** -> **Global Pipeline Libraries**.

---

## 🧠 Key Concepts

-   **Shared Library:** A collection of Groovy scripts stored in a specific SCM (Git) repository structure, which can be used by multiple Jenkins pipelines.
-   **`vars/` directory:** Scripts in this directory define global variables/functions accessible in pipelines. If a script is named `foo.groovy`, its methods are available as `foo.bar()`.
-   **`src/` directory (not used in this lab):** Used for more complex, POGO (Plain Old Groovy Object) style classes, often organized into Java-like package structures. Methods here are typically called with explicit imports.
-   **Global Pipeline Libraries Configuration:** A section in Jenkins system configuration (`Manage Jenkins` -> `Configure System`) where you define named shared libraries and point Jenkins to their SCM locations.
-   **`@Library('library-name@version') _` annotation:** Used at the top of a `Jenkinsfile` to explicitly load a configured shared library. The `_` at the end is significant.
-   **Reusability & Maintainability:** Shared libraries help centralize common pipeline logic, reducing code duplication in Jenkinsfiles and making updates easier to manage.

---

## 🔁 What's Next?

Having learned how to create and use shared libraries, you'll next explore how to securely manage secrets and credentials within your Jenkins pipelines.

Proceed to **[../LAB08-Secure-Credentials/README.md](../LAB08-Secure-Credentials/)**.

