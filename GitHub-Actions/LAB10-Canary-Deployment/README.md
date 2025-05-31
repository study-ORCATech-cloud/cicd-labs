# LAB10 - Canary Deployment with GitHub Environments

In this advanced GitHub Actions lab, you'll implement a **canary deployment strategy** using GitHub Environments. The new version will first be deployed to a `canary` environment. After verification (simulated), it can be promoted to a `production` environment, ideally guarded by a manual approval step configured in GitHub.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the concept of canary deployments for phased rollouts.
- Configure and use GitHub Environments (`canary` and `production`).
- Implement a manual approval gate for production deployments using Environment protection rules.
- Create a workflow triggered by `workflow_dispatch` with inputs to specify version and target environment.
- Conditionally execute jobs based on input parameters (`if: github.event.inputs.deploy_target == 'canary'`).
- Simulate deployment steps to different environments.

---

## 🧰 Prerequisites

- A GitHub account and a repository with Actions enabled.
- **Crucial:** Ability to configure **GitHub Environments** in your repository settings (`Settings` > `Environments`). You will need to create two environments: `canary` and `production`.
    - For the `production` environment, you should add a **Protection Rule** for **Required reviewers** (you can assign yourself as the reviewer for this lab).
- Basic understanding of YAML and GitHub Actions workflow syntax.

---

## 🗂️ Folder Structure

Your lab directory will be structured as follows. The main work will be in `canary-production-deploy.yml`.

```bash
GitHub-Actions/LAB10-Canary-Deployment/
├── .github/
│   └── workflows/
│       └── canary-production-deploy.yml  # Your partially completed workflow with TODOs
├── app/
│   └── version.txt                     # Simple file to simulate version update (provided)
├── README.md                           # Lab instructions (this file)
└── solutions.md                        # Solution for the workflow
```

---

## 🚀 Lab Steps

### 1. Configure GitHub Environments (Critical Prerequisite)

Before starting the workflow file, you **must** set up environments in your GitHub repository:

1.  Go to your repository on GitHub.
2.  Click on `Settings` (usually a tab at the top).
3.  In the left sidebar, scroll down to `Environments` (under the "Code and automation" section).
4.  Click `New environment`.
    *   Name it `canary`. Click `Configure environment`. (No protection rules needed for canary in this lab, but you could add some like deployment branches if desired).
5.  Click `New environment` again.
    *   Name it `production`. Click `Configure environment`.
    *   Under **Protection rules**, check `Required reviewers`.
    *   Search for and select your own GitHub username to be the reviewer. You can set the number of reviewers to 1.
    *   Click `Save protection rules`.

### 2. Examine `app/version.txt`

This lab includes a simple `app/version.txt` file. Our workflow will simulate updating this file to reflect the version being "deployed".

### 3. Complete the GitHub Actions Workflow (`.github/workflows/canary-production-deploy.yml`)

Open `.github/workflows/canary-production-deploy.yml`. This file has `TODO` comments to guide you:

*   **`on.workflow_dispatch.inputs`**:
    *   TODO: Define this manual trigger.
    *   TODO: Add a `version` input (string, required, e.g., description: 'The application version to deploy (v1.0.1)').
    *   TODO: Add a `deploy_target` input (choice, required, options: `canary`, `production`).
*   **Job: `deploy_canary`**:
    *   TODO: Add an `if` condition: `github.event.inputs.deploy_target == 'canary'`.
    *   TODO: Assign this job to the `canary` environment using `environment: name: canary`. You can optionally add a `url` like `https://my-app-canary.example.com`.
    *   **Step: Update version file for Canary**:
        *   TODO: Write a script to `echo "${{ github.event.inputs.version }}" > app/version.txt` and then `cat app/version.txt` to verify.
    *   **Step: Simulate Canary Deployment**:
        *   TODO: Add an `echo` command to simulate deploying the `inputs.version` to the `CANARY` environment. Include the environment URL: `Deployment URL: ${{ job.environment.url }}`.
*   **Job: `deploy_production`**:
    *   TODO: Add an `if` condition: `github.event.inputs.deploy_target == 'production'`.
    *   TODO: Assign this job to the `production` environment (`environment: name: production`). Add an optional `url`.
    *   **Step: Update version file for Production**:
        *   TODO: Similar to canary, update `app/version.txt` with `inputs.version`.
    *   **Step: Simulate Production Deployment**:
        *   TODO: Add an `echo` command to simulate deploying `inputs.version` to the `PRODUCTION` environment. Include the environment URL.

### 4. Commit and Push Your Changes

```bash
git add .github/workflows/canary-production-deploy.yml app/version.txt
git commit -m "feat: Implement canary and production deployment workflow for LAB10"
git push origin main
```

### 5. Verify Workflow Execution & Manual Approval

*   **Test Canary Deployment:**
    1.  Go to your repository's "Actions" tab.
    2.  Select the "Canary and Production Deployment" workflow in the left sidebar.
    3.  Click the "Run workflow" dropdown on the right.
    4.  Enter a version (e.g., `v1.0.1-canary`).
    5.  For `deploy_target`, choose `canary`.
    6.  Click "Run workflow".
    7.  Observe the `deploy_canary` job running and completing. The `deploy_production` job should be skipped.
*   **Test Production Deployment (with Manual Approval):**
    1.  Again, click "Run workflow" for the "Canary and Production Deployment" workflow.
    2.  Enter a new version (e.g., `v1.0.1-final` or just `v1.0.1`).
    3.  For `deploy_target`, choose `production`.
    4.  Click "Run workflow".
    5.  The `deploy_canary` job should be skipped.
    6.  The `deploy_production` job should start but then **pause**, showing a status like "Waiting". You (or the designated reviewer) should receive a notification from GitHub to review the deployment.
    7.  Go to the workflow run in the Actions tab. You should see a prompt to "Review deployments". Click it.
    8.  Select the `production` environment, optionally add a comment, and click "Approve and deploy".
    9.  Observe the `deploy_production` job resuming and completing.

---

## ✅ Validation Checklist

- [ ] GitHub Environments `canary` and `production` are created in repository settings.
- [ ] The `production` environment has a "Required reviewers" protection rule configured.
- [ ] The `.github/workflows/canary-production-deploy.yml` workflow is correctly completed.
- [ ] Manually triggering the workflow with `deploy_target: canary` runs only the `deploy_canary` job.
- [ ] The `deploy_canary` job simulates updating `app/version.txt` and deploying to the canary environment.
- [ ] Manually triggering with `deploy_target: production` causes the `deploy_production` job to pause for manual approval.
- [ ] After approval, the `deploy_production` job runs and simulates deploying to the production environment.
- [ ] The correct version (from input) is reflected in the simulated deployment messages and `app/version.txt` update.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code with explanations.

---

## 🧹 Cleanup

-   **Workflow File:** Delete `.github/workflows/canary-production-deploy.yml`.
-   **GitHub Environments:** You can delete the `canary` and `production` environments from your repository settings if they are no longer needed.
-   Commit and push any cleanup changes.

---

## 🧠 Key Concepts

-   **Canary Deployment:** A strategy to release a new software version to a small subset of users/servers (the canary) before rolling it out to the entire user base or production environment. This minimizes risk.
-   **GitHub Environments:** Used to define deployment targets (e.g., `development`, `staging`, `production`). They can have protection rules (like manual approvals, wait timers, specific branch deployments) and environment-specific secrets.
-   **`workflow_dispatch` with `inputs`:** Allows manual triggering of workflows with user-provided parameters, making workflows flexible for tasks like deployments.
-   **Environment Protection Rules:** Enforce checks or manual gates before a job using that environment can proceed. "Required reviewers" is a common rule for production.
-   **Conditional Job Execution (`if` condition):** Controls whether a job runs based on expressions, often involving `github.event.inputs` for `workflow_dispatch`.

---

## 🎉 GitHub Actions Track Complete! 🎉

Congratulations! You've completed all 10 hands-on labs in the GitHub Actions track, covering a wide range of CI/CD concepts from basic workflows to advanced deployment strategies like canary releases with environment protections.

You should now have a solid foundation to build, test, and deploy your applications using GitHub Actions.

### Next Steps:

-   Explore other CI/CD tools and platforms in this series, such as **Jenkins**, **Docker-CD**, or **ArgoCD**, to broaden your DevOps expertise.
-   Apply these concepts to your own projects.
-   Dive deeper into specific GitHub Actions features like matrix builds, advanced artifact handling, or creating custom actions.

Deploy smart. Ship safe. Scale confidently. 🐥🚀📈