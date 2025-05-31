# LAB06 - Secrets & Contexts (GitHub Actions)

In this lab, you'll learn how to securely use **secrets** and explore various **contexts** in GitHub Actions. Secrets are essential for protecting sensitive data like API keys or passwords, while contexts provide dynamic access to runtime metadata about your workflow, runner, and events.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand how to store and use encrypted secrets in a GitHub Actions workflow.
- Securely pass secret values to specific steps without exposing them in logs.
- Access and utilize different GitHub Actions contexts, such as `github`, `runner`, and `env`.
- Define and use job-level and step-level environment variables.
- Differentiate between secrets and environment variables and their use cases.

---

## 🧰 Prerequisites

- A GitHub account and a repository with Actions enabled.
- **Crucially**: You must create a repository secret before starting this lab. Go to your repository's `Settings` > `Secrets and variables` > `Actions`. Click `New repository secret` and create a secret named `MY_SECRET_VALUE` with any value you like (e.g., `super-secret-password123`).

---

## 🗂️ Folder Structure

Your lab directory is set up with the following structure. You will be completing the `TODO`s in `show-secrets.yml`.

```bash
GitHub-Actions/LAB06-Secrets-And-Contexts/
├── .github/
│   └── workflows/
│       └── show-secrets.yml  # Your partially completed workflow file with TODOs
├── README.md               # Lab instructions (this file)
└── solutions.md            # Solutions for show-secrets.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB06-Secrets-And-Contexts/` directory.

2.  **Ensure Your Secret is Created:**
    Double-check that you have created the `MY_SECRET_VALUE` secret in your repository settings as described in the "Prerequisites" section. The lab will not work correctly without it.

3.  **Examine and Complete the Workflow File (`.github/workflows/show-secrets.yml`):**
    Open `.github/workflows/show-secrets.yml`. This file contains `TODO` comments guiding you through various tasks:
    *   **Triggers:** Configure the workflow to run on pushes to `main` and also allow manual `workflow_dispatch`.
    *   **Runner OS:** Specify `runs-on: ubuntu-latest`.
    *   **Job-Level Environment Variable:** Define `JOB_LEVEL_ENV_VAR` under the job's `env` block.
    *   **Checkout Action:** Add the `actions/checkout@v3` step.
    *   **GitHub Context:** In the "Display GitHub Context Information" step, modify the `echo` commands to print the actual values from the `github` context (e.g., `echo "Workflow triggered by: ${{ github.actor }}"`).
    *   **Runner Context:** Similarly, update the "Display Runner Context Information" step to print values from the `runner` context.
    *   **Access Job-Level Env Var:** Update the `echo` command to correctly print the `$JOB_LEVEL_ENV_VAR`.
    *   **Access Secret Securely:** In the "Access a Secret (Securely)" step:
        *   Ensure the `env` block correctly maps `MY_SECRET_VALUE` to `EXAMPLE_SECRET` (or a name of your choice) for that step: `EXAMPLE_SECRET: ${{ secrets.MY_SECRET_VALUE }}`.
        *   Complete the `run` script to print the *length* of the secret (`${#EXAMPLE_SECRET}`). The script already includes a check to see if the secret is set.
        *   **Security Reminder:** Do NOT print the secret's actual value directly.
    *   **Step-Level Environment Variable:** In the "Access Step-Level Environment Variable" step:
        *   Define `STEP_LEVEL_ENV_VAR` under that step's `env` block.
        *   Update the `echo` command to print the `$STEP_LEVEL_ENV_VAR`.
    Refer to the hints in the `TODO` comments and the `solutions.md` file if you need help.

4.  **Commit and Push Your Changes:**
    ```bash
    git add .github/workflows/show-secrets.yml
    git commit -m "feat: Implement secrets and contexts demo for LAB06"
    git push origin main
    ```

5.  **Verify Workflow Execution:**
    *   Go to your GitHub repository's "Actions" tab.
    *   You can trigger the "Secrets & Contexts Demo" workflow manually using the "Run workflow" button (due to `workflow_dispatch`).
    *   Alternatively, a push to `main` will also trigger it.
    *   Inspect the logs for the `demonstrate_secrets_and_contexts` job. Verify that:
        *   GitHub and Runner context information is printed correctly.
        *   Job-level and step-level environment variables are displayed with their defined values.
        *   The length of `MY_SECRET_VALUE` is printed, and the log indicates if the secret was found. The actual secret value should NOT be visible.

---

## ✅ Validation Checklist

- [ ] The repository secret `MY_SECRET_VALUE` is created and accessible.
- [ ] The `.github/workflows/show-secrets.yml` file is correctly completed, addressing all `TODO`s.
- [ ] The workflow triggers on push to `main` and can be run manually.
- [ ] Values from `github` and `runner` contexts are correctly printed in the logs.
- [ ] Job-level and step-level environment variables are correctly defined and accessed.
- [ ] The length of the secret `MY_SECRET_VALUE` is printed, but the secret itself is **not** exposed in the logs.
- [ ] You understand the importance of not printing secrets directly.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for `show-secrets.yml` with detailed explanations and important security notes.

---

## 🧹 Cleanup

-   **Repository Secret:** Delete the `MY_SECRET_VALUE` secret from your GitHub repository settings (`Settings` > `Secrets and variables` > `Actions`) if it's no longer needed or was created just for this lab.
-   **Workflow File:**
    ```bash
    rm .github/workflows/show-secrets.yml
    ```
    Commit and push the deletion.

---

## 🧠 Key Concepts

-   **Secrets (`secrets.*`):** Encrypted environment variables intended for sensitive information. GitHub Actions automatically redacts exact matches of secrets found in logs, but it's best practice to avoid printing them altogether.
-   **Contexts:** Objects that provide access to information about the workflow run, runner, event, etc. Common contexts include `github`, `env`, `job`, `steps`, `runner`, `secrets`.
-   **Environment Variables (`env.*` or `$VARNAME`):** A way to set variables at the workflow, job, or step level. These are not encrypted by default and are suitable for non-sensitive configuration data.
-   **`workflow_dispatch`:** Allows manual triggering of a workflow.
-   **Security Best Practices:** Always handle secrets with care. Avoid printing them, and only pass them to steps/actions that genuinely need them.

---

## 🌟 Well Done!

You've learned how to manage sensitive data with secrets and leverage contextual information in your GitHub Actions workflows. These are vital skills for building robust and secure CI/CD pipelines!

---

## 🔁 What's Next?
Continue to [LAB07 - Artifact Caching](../LAB07-Artifact-Caching/) to speed up workflows with dependency caching.

Secure it. Access it. Context matters. 🔐📦⚙️