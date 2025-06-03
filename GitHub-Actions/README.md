# GitHub Actions CI/CD Labs

This section of the **CI/CD Automation Labs** repository is dedicated to mastering **GitHub Actions** — GitHub's built-in automation and CI/CD platform.

These labs will guide you through automating builds, tests, deployments, and managing workflows across various types of projects using complete, production-ready workflow configurations.

---

## 🚀 What You'll Learn

- How to write basic and advanced GitHub Actions workflows.
- Automate CI for Python projects, Docker images, and static websites (GitHub Pages).
- Secure your workflows with encrypted secrets and manage GitHub Environments.
- Implement caching for dependencies and manage build artifacts.
- Schedule jobs using cron and understand GitHub Actions contexts.
- Design workflows for monorepos with conditional execution based on paths.
- Create and use local reusable workflows to avoid duplication.
- Implement advanced deployment strategies like Canary Releases with manual approvals.

---

## 🛠️ How to Use These Labs

To effectively work through these labs, you'll need to have your own copy of this repository where you can make changes, commit, push, and see your GitHub Actions workflows run.

1.  **Fork this Repository:**
    *   Click the "Fork" button at the top right of this repository page.
    *   This will create a copy of the entire `cicd-labs` repository under your own GitHub account.

2.  **Clone Your Fork:**
    *   Clone your forked repository to your local machine:
        ```bash
        git clone https://github.com/YOUR_USERNAME/cicd-labs.git
        cd cicd-labs/GitHub-Actions/
        ```
    *   Replace `YOUR_USERNAME` with your actual GitHub username.

3.  **Work on Labs in Your Fork:**
    *   Navigate to the specific lab directory (e.g., `LAB01-Hello-World/`).
    *   Follow the instructions in the lab's `README.md` file.
    *   You will be copying complete, working workflow files from the lab materials to your `.github/workflows/` directory.

4.  **Commit and Push Changes:**
    *   After copying the workflow files to your repository, commit and push those changes **to your forked repository**.
    *   This push will trigger the GitHub Actions workflow you've configured, and you can observe its execution in the "Actions" tab of *your forked repository*.

5.  **Repository Secrets & Environments:**
    *   Some labs require you to set up repository secrets (e.g., `DOCKER_USERNAME`, `DOCKER_PASSWORD` for Lab 03, `MY_SECRET_VALUE` for Lab 06).
    *   Lab 10 requires configuring GitHub Environments (`canary`, `production`).
    *   **Important:** You must configure these secrets and environments in the settings of **your forked repository**, not the original one.

6.  **Learn by Doing:**
    *   Each lab provides complete, working workflow configurations that demonstrate production-ready CI/CD patterns.
    *   Focus on understanding how each workflow works and the GitHub Actions features being demonstrated.

---

## 📁 Lab Structure

```bash
GitHub-Actions/
├── LAB01-Hello-World/
├── LAB02-Python-Test-Workflow/
├── LAB03-Docker-Build-And-Push/
├── LAB04-Deploy-GitHub-Pages/
├── LAB05-Scheduled-Cron-Jobs/
├── LAB06-Secrets-And-Contexts/
├── LAB07-Artifact-Caching/
├── LAB08-Monorepo-Strategy/
├── LAB09-Reusable-Workflows/
└── LAB10-Canary-Deployment/
```

Each lab directory typically contains:
- `README.md`: Detailed instructions, objectives, step-by-step procedures, and validation steps for that specific lab.
- `.github/workflows/`: Complete, working YAML workflow files ready to copy and use.
- **Copy-and-Learn Methodology**: All workflow files are production-ready and functional - students copy them and learn by following detailed instructions.
- Optional sample application code (`app/`, `services/`, etc.) relevant to the lab's scenario.

---

## 🧠 Prerequisites (General)

- A GitHub account with GitHub Actions enabled (usually enabled by default).
- Basic Git knowledge (clone, add, commit, push) and familiarity with using GitHub.
- A code editor (like VS Code) for editing YAML and other lab files locally.
- Familiarity with YAML syntax will be helpful.

---

## 💬 Contributing

While these labs are designed for individual learning, if you find errors or have suggestions for improvements to the lab instructions or configurations:
1.  Consider opening an Issue in the original repository.
2.  Alternatively, you can fork the original repository, make your suggested changes in a branch, and then open a Pull Request back to the original repository with a clear description of your proposed improvements.

---

**Automate everything with GitHub Actions and happy learning!** 🚀🐙

