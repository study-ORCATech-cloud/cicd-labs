# LAB02: Step-by-Step Instructions - Freestyle Python Job

This document provides the detailed steps to complete LAB02. Follow these instructions carefully in your Jenkins User Interface.

---

## 🚀 Setting Up Your Freestyle Python Job

This lab assumes you have forked the main `cicd-labs` repository to your own GitHub account and have cloned it locally. Jenkins will pull the Python application for this lab directly from **your fork**.

1.  **Navigate to the Jenkins Dashboard:**
    *   Open your browser and go to your Jenkins URL (e.g., `http://localhost:8080`).
    *   Log in with the admin user you created during the initial setup.

2.  **Create a New Item (Job):**
    *   On the Jenkins dashboard, click on **"New Item"** in the left-hand navigation menu.
    *   **Enter an item name:** Type `python-freestyle-job` (or a similar descriptive name).
    *   **Select project type:** Click on **"Freestyle project"** from the list of options.
    *   Click the **"OK"** button at the bottom of the page.

3.  **Configure Job Description (Optional):**
    *   On the job configuration page, you can add a **Description** like: "A Freestyle job to run a Python script and tests from a Git repository."

4.  **Configure Source Code Management (SCM):**
    *   Scroll down to the **"Source Code Management"** section.
    *   Select **"Git"**.
    *   In the **"Repository URL"** field, enter the HTTPS URL of **your forked `cicd-labs` repository**. 
        *   Example: `https://github.com/YOUR_USERNAME/cicd-labs.git` (Replace `YOUR_USERNAME` with your actual GitHub username).
    *   **Branch Specifier:** Leave it as `*/main` if your default branch is `main`. If your fork uses a different default branch (e.g., `master`), change it accordingly (e.g., `*/master`).
    *   *(Optional but Recommended for Cleanliness)* **Advanced SCM Configuration:**
        *   Click on **"Add"** next to "Additional Behaviours".
        *   Select **"Check out to a sub-directory"** from the dropdown.
        *   In the **"Local subdirectory for repo"** field, type `lab02_sources`.
            *This will check out your repository into a subdirectory named `lab02_sources` within the Jenkins job's workspace, keeping the workspace root cleaner if you had multiple SCMs or other files.* 
            *If you skip this optional step, your commands in the build step will need to use the full path from the workspace root, e.g., `Jenkins/LAB02-Freestyle-Python-Job/app/...`.*

5.  **Configure Build Steps:**
    *   Scroll down to the **"Build Steps"** section.
    *   Click the **"Add build step"** dropdown button.
    *   Select **"Execute shell"** from the dropdown menu. (If your Jenkins controller is running on Windows, select **"Execute Windows batch command"** and adapt the following commands accordingly, e.g., using `\` for paths and `pip` instead of `python -m pip` if `pip` is directly in PATH).

6.  **Add Shell Commands for Python Execution:**
    A text box will appear for the shell command. Enter the following commands one per line. 

    *   **If you used the "Check out to a sub-directory" (`lab02_sources`) option:**
        ```bash
        echo "--- Setting up Python environment and running script ---"
        
        # Navigate to the app directory within the checked-out sources
        cd lab02_sources/Jenkins/LAB02-Freestyle-Python-Job/app
        
        echo "Current directory: $(pwd)"
        echo "Listing files in app directory:"
        ls -la
        
        echo "Installing dependencies from requirements.txt..."
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
        echo "Running the Python script (main.py)..."
        python main.py
        
        echo "Running tests with pytest..."
        pytest tests/
        
        echo "--- Python script and tests execution complete ---"
        ```

    *   **If you DID NOT use "Check out to a sub-directory":**
        The paths will be relative to the Jenkins workspace root.
        ```bash
        echo "--- Setting up Python environment and running script ---"

        echo "Workspace directory: $(pwd)"
        echo "Listing files in Jenkins/LAB02-Freestyle-Python-Job/app directory:"
        ls -la Jenkins/LAB02-Freestyle-Python-Job/app
        
        echo "Installing dependencies from requirements.txt..."
        python -m pip install --upgrade pip
        pip install -r Jenkins/LAB02-Freestyle-Python-Job/app/requirements.txt
        
        echo "Running the Python script (main.py)..."
        python Jenkins/LAB02-Freestyle-Python-Job/app/main.py
        
        echo "Running tests with pytest..."
        # Pytest usually discovers tests, but specifying the directory is more robust
        pytest Jenkins/LAB02-Freestyle-Python-Job/app/tests/
        
        echo "--- Python script and tests execution complete ---"
        ```
    *Choose ONE set of commands based on your SCM configuration above.*

7.  **Save the Job Configuration:**
    *   Scroll to the bottom of the configuration page.
    *   Click the **"Save"** button.

8.  **Manually Trigger a Build:**
    *   After saving, you'll be taken to the job's main page for `python-freestyle-job`.
    *   In the left-hand navigation menu for this job, click on **"Build Now"**.
    *   A new build will appear in the **"Build History"** section (e.g., `#1`). Click on it.

9.  **Inspect the Console Output:**
    *   Wait for the build to complete. It might take a bit longer this time due to SCM checkout and `pip install`.
    *   A successfully completed build will typically show a blue ball icon 🔵.
    *   On the build-specific page (after clicking the build number), click on **"Console Output"** in the left-hand menu.
    *   Examine the output. You should see:
        *   Logs from the Git checkout.
        *   The `echo` messages you added.
        *   Output from `pip install` installing `pytest`.
        *   The print statements from `main.py` (e.g., "Hello, Student from a Jenkins Freestyle job!").
        *   The output from `pytest`, hopefully showing that tests passed.
        *   A final `Finished: SUCCESS` status.

Congratulations! You've configured Jenkins to fetch code from Git, install dependencies, run a Python script, and execute tests.

---

Refer back to the `README.md` for objectives, validation, cleanup, and key concepts related to this lab. 