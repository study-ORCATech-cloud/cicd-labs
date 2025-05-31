# LAB03: Declarative Pipeline with Jenkinsfile

Welcome to your first lab on Jenkins Pipelines! In this lab, you'll transition from UI-configured Freestyle jobs to defining your build, test, and (eventually) deployment logic as code using a `Jenkinsfile`. We will use the Declarative Pipeline syntax, which provides a structured and simpler way to define pipelines.

This lab will teach you how to create a `Jenkinsfile` to automate the process of checking out code, installing dependencies, running a Python script, and executing tests—all orchestrated by Jenkins based on the `Jenkinsfile` in your repository.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the basic structure and syntax of a Declarative `Jenkinsfile` (`pipeline`, `agent`, `stages`, `stage`, `steps`).
- Create a `Jenkinsfile` with stages for checking out code, installing dependencies, running a Python application, and executing tests.
- Configure a Jenkins "Pipeline" job to use a `Jenkinsfile` from Source Code Management (SCM) (your Git fork).
- Observe the execution of your pipeline in Jenkins, including its stages and console output.
- Appreciate the benefits of pipeline-as-code for versioning, reusability, and collaboration.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Please follow the **`../../install-and-setup.md`** guide.
-   **Admin Access to Jenkins:** You need to be able to log in as an admin user.
-   **Python & Git on Jenkins Environment:** As in Lab 02, the Jenkins execution environment needs Python 3, `pip`, and `git`.
-   **GitHub Account and Fork:**
    *   You must have forked the main `cicd-labs` repository (`https://github.com/ORCA-TECH/cicd-labs.git`) to your own GitHub account.
    *   This lab requires you to commit the `Jenkinsfile` (that you will complete) to **your fork** at the path `Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile`.
-   **Application Code:** The `Jenkins/LAB03-Declarative-Pipeline/app/` directory contains the Python application and tests, which should also be in your fork.

---

## 🗂️ Folder Structure for This Lab

```bash
Jenkins/LAB03-Declarative-Pipeline/
├── README.md         # Lab instructions, TODOs, and explanations (this file)
├── Jenkinsfile       # The Declarative Pipeline script you will complete (with TODOs)
├── solutions.md      # Contains the completed Jenkinsfile and explanations
└── app/
    ├── main.py           # Simple Python application (from Lab 02, slightly modified)
    ├── requirements.txt  # Python dependencies (pytest)
    └── tests/
        └── test_main.py  # Pytest tests for main.py (from Lab 02, slightly modified)
```

---

## Understanding Declarative Jenkinsfile Syntax

A `Jenkinsfile` is a text file that contains the definition of a Jenkins Pipeline and is checked into source control. Declarative Pipeline is a more recent and simplified way to write these files.

Key components:

-   `pipeline { ... }`: The main block that defines the entire pipeline.
-   `agent <agent_details>`: Specifies where the entire Pipeline, or a specific stage, will execute. 
    *   `agent any`: Runs on any available agent (including the Jenkins controller if it allows builds).
    *   `agent none`: Used at the top level if you want to specify agents per stage.
    *   `agent { docker 'maven:3.9.5-eclipse-temurin-17' }`: Runs steps within a Docker container.
-   `stages { ... }`: Contains one or more `stage` directives.
-   `stage('Stage Name') { ... }`: Defines a distinct part of your pipeline (e.g., 'Build', 'Test', 'Deploy'). Stages are visualized in the Jenkins UI.
-   `steps { ... }`: Contains one or more steps to be executed within a `stage`.
    *   `sh 'your_shell_command'`: Executes a shell command (on Linux/macOS).
    *   `bat 'your_batch_command'`: Executes a Windows batch command.
    *   Other steps: `echo`, `git`, `junit`, etc.
-   `post { ... }`: Defines actions to be run at the end of the Pipeline's or a stage's execution (e.g., `always`, `success`, `failure`).

---

## 🚀 Lab Steps: Creating Your Jenkinsfile

Your primary task in this lab is to complete the `Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile` in your forked repository. This file has `TODO:` markers indicating where you need to add or modify code.

**1. Locate and Open `Jenkinsfile`:**
   Open the `Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile` in your local clone of your forked repository using your code editor.

**2. Complete the `TODO` items in `Jenkinsfile`:**

   *   **`TODO_AGENT` (Line 2-4):**
       *   The pipeline needs an agent to run on. For this lab, `agent any` is appropriate as it allows Jenkins to pick any available executor. This line is mostly complete, but review its purpose.

   *   **`TODO_CHECKOUT` (Line 12-20):**
       *   While Jenkins often handles an initial checkout automatically when using "Pipeline script from SCM," explicitly adding `checkout scm` is good practice. This `TODO` is more of an informational one for this basic lab, as `checkout scm` itself is usually sufficient if your job is configured correctly in the UI to point to your repo and this `Jenkinsfile`.
       *   The `script { sh 'ls -la' }` block is there to help you verify what was checked out and where. No direct code change is required for `checkout scm` itself unless you need specific SCM behaviors not covered by the job's SCM UI configuration.

   *   **`TODO_INSTALL_DEPS` (Line 30-33):**
       *   In the "Install Dependencies" stage, you need to provide the shell command to install the Python packages listed in `app/requirements.txt`.
       *   The `Jenkinsfile` comment for this `TODO` provides guiding questions to help you figure out the command(s).
       *   **Action:** Replace `sh ''` with the correct `sh` command(s).

   *   **`TODO_RUN_SCRIPT` (Line 37-40):**
       *   In the "Run Python Script" stage, provide the shell command to execute the `app/main.py` script.
       *   The `Jenkinsfile` comment for this `TODO` provides guiding questions.
       *   **Action:** Replace `sh ''` with the correct `sh` command.

   *   **`TODO_RUN_TESTS` (Line 44-47):**
       *   In the "Run Tests" stage, provide the shell command to execute `pytest` against the tests in `app/tests/`.
       *   The `Jenkinsfile` comment for this `TODO` provides guiding questions.
       *   **Action:** Replace `sh ''` with the correct `sh` command.

   *   **`TODO_CLEANUP_WORKSPACE` (Optional) (Line 53-55):**
       *   In the `post` section, there's an optional `TODO` to add a workspace cleanup step. For now, you can leave this as is or explore the `cleanWs()` step if you wish.

**3. Commit and Push `Jenkinsfile` Changes:**
   Once you have completed all the `TODO`s, commit the modified `Jenkinsfile` to your forked GitHub repository and push the changes.
   ```bash
   git add Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile
   git commit -m "Complete Jenkinsfile for Lab03 Declarative Pipeline"
   git push
   ```

**4. Configure Jenkins Pipeline Job:**

   *   Navigate to your Jenkins Dashboard.
   *   Click **"New Item"**.
   *   Enter an item name (e.g., `python-declarative-pipeline`).
   *   Select **"Pipeline"** as the project type.
   *   Click **"OK"**.
   *   On the configuration page, scroll down to the **"Pipeline"** section.
   *   For **"Definition"**, select **"Pipeline script from SCM"** from the dropdown.
   *   For **"SCM"**, select **"Git"** from the dropdown.
   *   In **"Repository URL"**, enter the HTTPS URL of **your forked `cicd-labs` repository** (e.g., `https://github.com/YOUR_USERNAME/cicd-labs.git`).
   *   **Branch Specifier:** Ensure it matches your default branch (e.g., `*/main` or `*/master`).
   *   **Script Path:** This is crucial. Enter the path to your `Jenkinsfile` within the repository: `Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile`
   *   Ensure there are no typos in the Script Path.
   *   Click **"Save"**.

**5. Build and Observe:**
   *   After saving, you'll be on the job's page. Click **"Build Now"**.
   *   Observe the pipeline execution in the "Stage View" on the job page. You should see your defined stages.
   *   Click on a build number in the "Build History" and then "Console Output" to see the detailed logs for each step.

---

## ✅ Validation Checklist

- [ ] The `Jenkinsfile` has been completed and pushed to your forked repository.
- [ ] A new Jenkins "Pipeline" job is created and configured to use the `Jenkinsfile` from your SCM.
- [ ] The pipeline job successfully checks out the code.
- [ ] The "Install Dependencies" stage runs and installs `pytest` (check console output).
- [ ] The "Run Python Script" stage executes `app/main.py` and its output is visible in the console.
- [ ] The "Run Tests" stage executes `pytest` and all tests pass (check console output).
- [ ] The pipeline completes successfully, and all stages are shown with a success status in the Jenkins UI (Stage View).

---

## 🧹 Cleanup

1.  In Jenkins, navigate to the `python-declarative-pipeline` job.
2.  Click **"Delete Pipeline"** from the left menu.
3.  Confirm deletion.

---

## 🧠 Key Concepts

-   **Pipeline-as-Code:** Defining your CI/CD process in a script (`Jenkinsfile`) that is version-controlled alongside your application code.
-   **Declarative Pipeline:** A structured syntax for `Jenkinsfile` (e.g., `pipeline`, `agent`, `stages`, `stage`, `steps`, `post`).
-   **`Jenkinsfile`:** The default name for the pipeline script file.
-   **`agent` directive:** Specifies where the pipeline or stage executes.
-   **`stages` & `stage` directives:** Define the logical sections of your pipeline.
-   **`steps` directive:** Contains the actual commands or actions for a stage.
-   **`sh` step:** Executes shell commands.
-   **`checkout scm` step:** Checks out source code based on the SCM configuration of the Jenkins job.
-   **`post` section:** Defines actions to run after the pipeline or stages complete (e.g., cleanup, notifications).
-   **Pipeline Script from SCM:** Jenkins job configuration option to source the `Jenkinsfile` directly from a Git repository.

---

## 🔁 What's Next?

Now that you've built your first Declarative Pipeline from a `Jenkinsfile` in SCM, you're ready to explore more advanced SCM integration features.

Proceed to **[../LAB04-SCM-Polling-Webhooks/README.md](../LAB04-SCM-Polling-Webhooks/)**.

