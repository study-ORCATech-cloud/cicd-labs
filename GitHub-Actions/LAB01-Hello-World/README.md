# LAB01 - Hello World Workflow (GitHub Actions)

In this first GitHub Actions lab, you'll create a simple workflow that runs on every code push. You'll learn how workflows are triggered, how jobs and steps are structured, and how to view logs from the Actions UI.

This foundational lab sets the stage for more complex CI/CD tasks.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the basic structure of a GitHub Actions workflow file.
- Create a workflow that triggers on a push to the `main` branch.
- Define a job with multiple steps.
- Use `echo` commands to output information in workflow logs.
- Access GitHub Actions context variables like `runner.os`.
- Locate and inspect workflow runs in the GitHub Actions UI.

---

## 🧰 Prerequisites

- A GitHub account
- A Git repository with write access (new or existing)

---

## 🗂️ Folder Structure

Ensure your lab directory looks like this after setup:

```bash
GitHub-Actions/LAB01-Hello-World/
├── .github/
│   └── workflows/
│       └── hello-world.yml  # Your workflow file with TODOs
├── README.md              # Lab instructions (this file)
└── solutions.md           # Step-by-step solutions for the TODOs
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB01-Hello-World/` directory.

2.  **Examine the Workflow File (`hello-world.yml`):**
    Open the `hello-world.yml` file located in the `.github/workflows/` directory.
    You will see a basic structure with several `TODO` comments. These are the tasks you need to complete.

    The goal is to create a workflow that:
    *   Is named "Hello World CI".
    *   Triggers on every push to the `main` branch.
    *   Has one job named `say-hello` that runs on the latest Ubuntu runner.
    *   The `say-hello` job has two steps:
        1.  `Echo greeting`: Prints a greeting message.
        2.  `Show date and runner OS`: Prints the current date and the OS of the runner.

3.  **Complete the `TODO`s:**
    Edit the `hello-world.yml` file and fill in the sections marked with `TODO`. 
    *   Configure the `on` trigger.
    *   Specify the `runs-on` environment for the job.
    *   Write the `run` commands for each step.
    *   Refer to the hints in the `TODO` comments if you get stuck.

4.  **Commit and Push Your Changes:**
    Once you have completed the `TODO`s in `hello-world.yml`:
    ```bash
    git add .github/workflows/hello-world.yml
    git commit -m "feat: Complete Hello World GitHub Actions workflow for LAB01"
    git push origin main
    ```

5.  **Verify Workflow Execution:**
    *   Go to your GitHub repository in your web browser.
    *   Click on the "Actions" tab.
    *   You should see your "Hello World CI" workflow listed. Click on it.
    *   Inspect the logs for the `say-hello` job. Verify that both steps executed successfully and printed the expected information (greeting, date, and runner OS).

---

## ✅ Validation Checklist

Make sure you can check off the following items:

- [ ] The `.github/workflows/hello-world.yml` file exists and is correctly populated.
- [ ] Pushing a commit to the `main` branch automatically triggers the "Hello World CI" workflow.
- [ ] The workflow run completes successfully in the GitHub Actions tab.
- [ ] The logs for the `say-hello` job show the greeting message you defined.
- [ ] The logs also display the current date and the correct runner OS (e.g., "ubuntu-latest" or similar).
- [ ] You understand where to find the `solutions.md` file if you need help.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working `hello-world.yml` code with explanations.

---

## 🧹 Cleanup
To remove this workflow:
```bash
rm -rf .github/
```
Commit and push the deletion.

---

## 🧠 Key Concepts

-   **Workflow (`.yml` file):** An automated process defined in a YAML file, typically located in `.github/workflows/`. It consists of one or more jobs.
-   **Event (`on`):** A specific activity that triggers a workflow (e.g., `push`, `pull_request`, `schedule`).
-   **Job (`jobs.<job_id>`):** A set of steps that execute on the same runner. Jobs run in parallel by default.
-   **Runner (`runs-on`):** A server that runs your workflow jobs. GitHub hosts Linux, Windows, and macOS runners.
-   **Step (`jobs.<job_id>.steps`):** An individual task that can run commands (actions or shell commands) in a job.
-   **Action (`uses` or `run`):** Reusable units of code. `uses` specifies pre-built actions (e.g., `actions/checkout@v3`), while `run` executes command-line programs.
-   **Contexts (`${{ <context> }}`):** Sets of variables that provide information about the workflow run, runner, secrets, etc. Example: `${{ github.event_name }}`, `${{ runner.os }}`.

---

## 🌟 Well Done!

You've successfully created and run your first GitHub Actions workflow! This is the fundamental building block for all CI/CD automation on GitHub.

---

## 🔁 What's Next?
Move on to [LAB02 - Python Test Workflow](../LAB02-Python-Test-Workflow/) to build a CI pipeline for testing Python code.

Hello world today, CI master tomorrow! 🌍🚀