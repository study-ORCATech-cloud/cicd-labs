# GitHub Actions: Environment Setup Guide

Welcome to the GitHub Actions track! This guide will help you set up your environment to effectively work through the labs. GitHub Actions is a powerful CI/CD (Continuous Integration/Continuous Delivery) platform directly integrated into GitHub, allowing you to automate your build, test, and deployment pipelines.

Unlike tools you install locally (like Docker or Jenkins), GitHub Actions runs based on configurations within your GitHub repository. Therefore, the setup primarily involves preparing your GitHub account and repository.

**Follow these instructions carefully to prepare for the GitHub Actions labs.**

---

## 🎯 What You'll Achieve

By following this guide, you will have:
- Understood the prerequisites for using GitHub Actions.
- Forked and cloned the lab repository to your local machine, ready for work.
- A basic understanding of how to interact with GitHub Actions via the GitHub website.
- (Optional) Installed the GitHub CLI for enhanced command-line interaction.

---

## 🧰 Prerequisites

Before you begin, ensure you have the following:

-   **A GitHub Account:** This is essential, as GitHub Actions is a feature of GitHub. If you don't have one, sign up at [https://github.com/join](https://github.com/join).
-   **Basic Git Knowledge:** You should be familiar with fundamental Git operations such as `clone`, `add`, `commit`, and `push`. These labs will require you to make changes and push them to GitHub to trigger workflows.
-   **Web Browser:** A modern web browser (e.g., Chrome, Firefox, Edge) to interact with GitHub.
-   **Text Editor or IDE:** A good text editor or Integrated Development Environment (IDE) for editing YAML workflow files and any application code involved in the labs. VS Code with its YAML extension is a popular choice.
-   **Internet Access:** To access GitHub and for Actions to fetch dependencies or interact with other services.

---

## ⚙️ Setting Up Your Environment for the Labs

To run GitHub Actions workflows within your own GitHub account and experiment freely, the recommended approach is to fork the main lab repository and then work with your fork.

**Step 1: Fork the Main Lab Repository (`cicd-labs`)
   *   **Why Fork?** Forking creates a personal copy of the `cicd-labs` repository under your GitHub account. This allows you to make commits, push changes, and trigger GitHub Actions workflows without affecting the original repository. The Actions will run using your account's quota and context.
   *   **How to Fork:**
        1.  Navigate to the main `cicd-labs` repository on GitHub (your instructor or the project will provide the URL, e.g., `https://github.com/your-instructor/cicd-labs`).
        2.  In the top-right corner of the repository page, click the "Fork" button.
        3.  Follow the on-screen prompts. You can usually keep the default repository name or customize it.
        4.  Once forked, you will have a copy under `https://github.com/YOUR_USERNAME/cicd-labs`.

**Step 2: Clone Your Forked Repository to Your Local Machine**
   Once you have forked the repository, clone it to your local computer to make changes.
   1.  On your forked repository's GitHub page (`https://github.com/YOUR_USERNAME/cicd-labs`), click the green "<> Code" button.
   2.  Copy the HTTPS or SSH clone URL provided.
   3.  Open your terminal or command prompt and run the `git clone` command. Replace the URL with the one you copied:
       ```bash
       git clone https://github.com/YOUR_USERNAME/cicd-labs.git
       ```
       Or, if using SSH:
       ```bash
       git clone git@github.com:YOUR_USERNAME/cicd-labs.git
       ```
   4.  This will create a `cicd-labs` directory on your local machine containing all the lab files.

**Step 3: Navigating to Lab Directories**
   Each lab is in its own subdirectory within the `GitHub-Actions` folder. Before starting a lab, navigate into its specific directory:
   ```bash
   cd cicd-labs/GitHub-Actions/LAB_NAME
   # e.g., cd cicd-labs/GitHub-Actions/LAB01-Hello-World
   ```

---

## ✨ Key Concepts for GitHub Actions (A Brief Overview)

As you work through the labs, you'll become familiar with these core components:

-   **Workflows:** Automated processes defined by YAML files stored in the `.github/workflows` directory of your repository. A repository can have multiple workflows.
-   **Events:** Specific activities that trigger a workflow run (e.g., a `push` to a branch, a `pull_request` being opened, a schedule, or manual dispatch).
-   **Jobs:** A set of steps within a workflow that execute on the same runner. Jobs can run in parallel or depend on other jobs.
-   **Steps:** Individual tasks that run in sequence within a job. A step can run shell commands or use a pre-built **action**.
-   **Actions:** Reusable units of code that perform common tasks. You can use actions created by GitHub, the community, or create your own.
-   **Runners:** Servers that execute your workflow jobs. GitHub provides and maintains runners for common operating systems (Linux, Windows, macOS), known as GitHub-hosted runners. You can also host your own self-hosted runners.
    *For these labs, we will primarily use GitHub-hosted runners.*

---

##  CLI (Optional) Installing and Using the GitHub CLI (`gh`)

The GitHub CLI (`gh`) is a command-line tool that brings GitHub to your terminal. While not strictly required for these labs (as GitHub Actions are primarily managed through Git events and the GitHub website), it can be a very convenient tool for interacting with your repositories, viewing workflow runs, managing pull requests, issues, and more, directly from the command line.

**Benefits:**
-   View repository information and status quickly.
-   Manage PRs and issues without leaving the terminal.
-   Check the status of workflow runs.
-   Authenticate with GitHub for other tools.

**Installation:**
-   Follow the official installation instructions for your operating system: [https://cli.github.com/manual/install_gh](https://cli.github.com/manual/install_gh)

**Basic Authentication (usually done once after install):**
```bash
gh auth login
```
Follow the prompts to authenticate with your GitHub account.

**Example Useful `gh` Commands (try them on your forked repository):**
-   View your current repository in the browser:
    ```bash
    gh repo view --web
    ```
-   List recent workflow runs for the current repository:
    ```bash
    gh run list
    ```
-   View details for a specific workflow run (you'll get the run ID from `gh run list`):
    ```bash
    gh run view <RUN_ID>
    ```

Using `gh` is optional for these labs but encouraged if you want to become more proficient with GitHub tooling.

---

## 🚀 Next Steps

You are now set up to begin the GitHub Actions labs! Start with **[LAB01-Hello-World/README.md](./LAB01-Hello-World/README.md)** to create and run your first basic GitHub Actions workflow.

As you complete labs, you will typically:
1.  Read the lab's `README.md`.
2.  Modify or create workflow YAML files (`.github/workflows/*.yml`).
3.  Commit your changes.
4.  Push your changes to your forked repository on GitHub.
5.  Observe the workflow run under the "Actions" tab of your repository on GitHub.

Enjoy automating with GitHub Actions! 🚀 