# LAB06: Parallel Execution and Conditional Logic in Jenkins Pipelines

This lab focuses on creating more sophisticated Jenkins pipelines by introducing **parallel execution** of stages and **conditional logic** using `when` directives. These features allow you to build faster and smarter CI/CD jobs by running independent tasks concurrently and controlling stage execution based on defined criteria, such as build parameters.

You will work with a simple Python application (similar to Lab 03) and modify a `Jenkinsfile` to implement these advanced pipeline syntaxes.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Define and use build parameters in a Jenkins pipeline (e.g., `booleanParam`).
- Structure a `Jenkinsfile` to execute multiple stages in parallel.
- Apply conditional logic using the `when` directive to control whether a stage runs based on build parameters.
- Understand how to move and refactor existing stages into a parallel block.
- Observe the behavior of parallel and conditional stages in the Jenkins UI.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Refer to **`../../install-and-setup.md`**.
-   **Lab 03 Familiarity:** While not a strict dependency, understanding the basic Declarative Pipeline structure from Lab 03 will be helpful as this lab builds upon similar concepts.
-   **GitHub Account and Fork:** Your forked `cicd-labs` repository. You will be working with the files in `Jenkins/LAB06-Parallel-And-Conditional/`.
-   **Basic Jenkins UI Navigation:** Ability to create and configure a Pipeline job, and trigger builds with parameters.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB06-Parallel-And-Conditional/
├── README.md         # Lab overview, objectives, TODO explanations (this file)
├── Jenkinsfile       # Declarative Pipeline script with TODOs for parallel/conditional logic
├── solutions.md      # Contains the completed Jenkinsfile and explanations
└── app/
    ├── main.py           # Simple Python application (from Lab 03, slightly modified for Lab 06)
    ├── requirements.txt  # Python dependencies (pytest)
    └── tests/
        └── test_main.py  # Pytest tests for main.py (modified for Lab 06)
```

---

## 🐍 Understanding the Sample Application

The `app/` directory contains a Python application nearly identical to the one used in Lab 03:
-   `main.py`: A simple script that prints a greeting. The greeting message is updated to mention Lab 06.
-   `requirements.txt`: Contains `pytest` for running tests.
-   `tests/test_main.py`: Contains basic unit tests for `main.py`, with assertions updated for Lab 06.

Your primary focus will be on the `Jenkinsfile`, not these application files.

---

## 🚀 Lab Steps: Enhancing Your `Jenkinsfile`

Your main task is to complete the `Jenkins/LAB06-Parallel-And-Conditional/Jenkinsfile`. This file has `TODO:` markers indicating where you need to add or modify Jenkins pipeline code.

**1. Locate and Open `Jenkinsfile`:**
   Open `Jenkins/LAB06-Parallel-And-Conditional/Jenkinsfile` in your local clone of your forked repository.

**2. Complete the `TODO` items in `Jenkinsfile`:**

   *   **`TODO_PARAMETERS` (Lines 4-8):**
        *   **Goal:** Define two boolean parameters that will allow users to choose whether to run unit tests and linting when they manually trigger the pipeline.
        *   **Action:** Inside the `parameters { ... }` block, add two `booleanParam` directives:
            1.  `RUN_UNIT_TESTS`: Default to `true`, with a description like 'Run unit tests for the Python app'.
            2.  `RUN_LINTING`: Default to `false`, with a description like 'Run placeholder linting checks'.
        *   These parameters will be accessible in your pipeline via `params.RUN_UNIT_TESTS` and `params.RUN_LINTING`.

   *   **`TODO_PARALLEL_STAGES` (Lines 34-45):**
        *   **Goal:** Create a parent stage that will execute unit testing and linting in parallel.
        *   **Action:**
            1.  Rename the placeholder stage `PARENT_STAGE_FOR_PARALLEL_BLOCK` to something descriptive, like `Quality Checks (Parallel)`.
            2.  Remove the placeholder `steps { echo '...' }` block within this renamed stage.
            3.  Inside the `Quality Checks (Parallel)` stage, introduce a `parallel { ... }` block.
            4.  **Move** the existing `stage('Unit Tests') { ... }` block (currently lines 50-58) and the `stage('Code Linting (Placeholder)') { ... }` block (currently lines 61-69) *entirely inside* this `parallel { ... }` block. Each of these moved stages will become a branch of the parallel execution.

   *   **`TODO_UNIT_TESTS_CONDITION` (within the 'Unit Tests' stage, now inside `parallel`):
        *   **Goal:** Make the 'Unit Tests' stage run only if the `RUN_UNIT_TESTS` parameter is true.
        *   **Action:** Add a `when { expression { params.RUN_UNIT_TESTS == true } }` directive to the 'Unit Tests' stage.

   *   **`TODO_UNIT_TESTS_COMMAND` (within the 'Unit Tests' stage, now inside `parallel`):
        *   **Goal:** Add the shell command to execute the Python unit tests.
        *   **Action:** Replace the `sh ''` placeholder with the command to run `pytest`. This will be similar to Lab 03: `sh "pytest ${APP_PATH}/tests/"` (ensure `APP_PATH` is correctly defined in your `environment` block, which it is in the skeleton).

   *   **`TODO_LINTING_CONDITION` (within the 'Code Linting (Placeholder)' stage, now inside `parallel`):
        *   **Goal:** Make the 'Code Linting (Placeholder)' stage run only if the `RUN_LINTING` parameter is true.
        *   **Action:** Add a `when { expression { params.RUN_LINTING == true } }` directive to the 'Code Linting (Placeholder)' stage.

   *   **`TODO_LINTING_COMMAND` (Optional) (within the 'Code Linting (Placeholder)' stage, now inside `parallel`):
        *   **Goal:** (Optional) This stage is a placeholder for actual linting.
        *   **Action:** The existing `sh 'echo "Linting checks would run here..."'` is sufficient for this lab. No change is strictly needed here unless you want to experiment with actual linting commands (not required).

**3. Commit and Push `Jenkinsfile` Changes:**
   Save your completed `Jenkinsfile`, then commit and push it to your forked GitHub repository.

**4. Configure and Run Jenkins Pipeline Job:**
   *   In Jenkins, create a new "Pipeline" job (e.g., `lab06-parallel-conditional-pipeline`).
   *   Configure it to use "Pipeline script from SCM," pointing to your forked repository and the `Jenkins/LAB06-Parallel-And-Conditional/Jenkinsfile` script path.
   *   Save the configuration. The first time you build, or if you select "Build with Parameters," you should see your defined boolean parameters.
   *   Trigger a build. Experiment by checking/unchecking the parameters to observe the conditional execution and parallel stages in the Jenkins Blue Ocean view or a classic Stage View.

---

## ✅ Validation Checklist

- [ ] The `Jenkinsfile` has been completed with parameters, a parallel block, and `when` conditions as described.
- [ ] When triggering the Jenkins job "Build with Parameters," the `RUN_UNIT_TESTS` and `RUN_LINTING` options appear.
- [ ] If `RUN_UNIT_TESTS` is checked and `RUN_LINTING` is unchecked:
    - [ ] The 'Unit Tests' stage runs (and passes).
    - [ ] The 'Code Linting (Placeholder)' stage is skipped.
- [ ] If `RUN_LINTING` is checked and `RUN_UNIT_TESTS` is unchecked:
    - [ ] The 'Code Linting (Placeholder)' stage runs.
    - [ ] The 'Unit Tests' stage is skipped (and doesn't fail the build if tests would have failed).
- [ ] If both are checked, both stages run, and the Jenkins UI should indicate they ran in parallel within the 'Quality Checks (Parallel)' parent stage.
- [ ] If both are unchecked, both stages are skipped.
- [ ] The pipeline completes successfully based on the conditions met.

---

## 🧹 Cleanup

1.  **Jenkins Job:** Delete the `lab06-parallel-conditional-pipeline` job in Jenkins if no longer needed.
2.  **Workspace:** The `cleanWs()` step in the `post` block should handle workspace cleanup on the agent.

---

## 🧠 Key Concepts

-   **`parameters` block:** Defines parameters that users can input when triggering a build (e.g., `booleanParam`, `stringParam`). Values are accessible via `params.YOUR_PARAM_NAME`.
-   **`parallel` block:** Allows you to define multiple stages that Jenkins will attempt to execute concurrently. This can significantly speed up pipelines where independent tasks can run simultaneously.
    ```groovy
    stage('Run in Parallel') {
        parallel {
            stage('Branch A') { /* ... */ }
            stage('Branch B') { /* ... */ }
        }
    }
    ```
-   **`when` directive:** Controls the execution of a stage based on a condition. It has several built-in conditions (e.g., `branch`, `environment`) and allows for `expression` for more complex Groovy-based logic.
    ```groovy
    stage('Conditional Stage') {
        when {
            expression { params.MY_CONDITION == true }
            // or branch 'main'
            // or environment name: 'CI_SERVER', value: 'true'
        }
        steps { /* ... */ }
    }
    ```
-   **Pipeline Speedup:** Parallel execution is a key technique for optimizing pipeline duration.
-   **Dynamic Pipelines:** Conditional execution allows for more flexible and intelligent pipelines that adapt to different scenarios (e.g., running different tests for different branches, skipping deployment stages for pull requests).

---

## 🔁 What's Next?

After mastering parallel and conditional execution, you'll learn about Jenkins Shared Libraries to create reusable and maintainable pipeline code across multiple projects.

Proceed to **[../LAB07-Shared-Libraries/README.md](../LAB07-Shared-Libraries/)**.

Smarter, faster pipelines — done right. 🧠⚙️🧪

