# LAB04 - Deploy to GitHub Pages (Static Site CD)

In this lab, you'll set up a GitHub Actions workflow to **build and deploy a simple static HTML website** to **GitHub Pages**. This is a common way to host personal portfolios, project documentation, or any static content directly from your GitHub repository.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Configure a GitHub Actions workflow to automatically deploy a static site to GitHub Pages on every push to the `main` branch.
- Understand and set the necessary `permissions` for the `GITHUB_TOKEN` to allow deployment to GitHub Pages.
- Use the standard GitHub Actions for deploying to Pages: `actions/checkout`, `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`.
- Configure your GitHub repository settings to enable GitHub Pages and use GitHub Actions as the deployment source.
- Verify the deployment and access your live static site.

---

## 🧰 Prerequisites

- A GitHub account.
- A GitHub repository (can be new or existing, public or private) where you will perform this lab.
- **Crucially**: You must have owner or admin privileges for the repository to change GitHub Pages settings.

---

## 🗂️ Folder Structure

Your lab directory is already set up with the following structure. You will be working primarily with the `deploy-pages.yml` file.

```bash
GitHub-Actions/LAB04-Deploy-GitHub-Pages/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml  # Your partially completed workflow file with TODOs
├── site/
│   └── index.html          # A simple HTML site (provided)
├── README.md               # Lab instructions (this file)
└── solutions.md            # Solutions for deploy-pages.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB04-Deploy-GitHub-Pages/` directory.

2.  **Examine the Static Site (`site/index.html`):**
    Open `site/index.html`. This is a simple, styled HTML page that will be deployed. You don't need to modify it for this lab, but feel free to personalize it later!

3.  **Configure GitHub Pages Settings in Your Repository (CRITICAL STEP):**
    Before the workflow can deploy, you **must** enable GitHub Pages and set it to use GitHub Actions:
    *   Go to your GitHub repository on the web.
    *   Click on the `Settings` tab.
    *   In the left sidebar, navigate to `Pages` (under the "Code and automation" section).
    *   Under "Build and deployment", for the **Source**, select **`GitHub Actions`** from the dropdown.
    *   If you see options for a branch, ensure "GitHub Actions" is selected instead.

4.  **Complete the GitHub Actions Workflow (`.github/workflows/deploy-pages.yml`):**
    Open `.github/workflows/deploy-pages.yml`. This file contains a partially completed workflow with `TODO` comments. Your task is to complete these `TODO`s:
    *   **Trigger:** Configure the `on` section to trigger the workflow on pushes to the `main` branch.
    *   **Permissions:** Set the `permissions` block correctly. You'll need `contents: read`, `pages: write`, and `id-token: write`.
    *   **Job Runner:** Specify `runs-on: ubuntu-latest` for the `deploy` job.
    *   **Checkout Code:** Use `actions/checkout@v3`.
    *   **Setup Pages:** Use `actions/configure-pages@v3`.
    *   **Upload Artifact:** Use `actions/upload-pages-artifact@v2`. For the `with.path` argument, provide the path to the directory containing your static site, which is `./site` for this lab.
    *   **Deploy to GitHub Pages:** Use `actions/deploy-pages@v2`. Note the `id: deployment` is already there to help access the deployed page URL.
    Refer to the hints in the `TODO` comments and the `solutions.md` if needed.

5.  **Commit and Push Your Changes:**
    Once you have completed all the `TODO`s in `.github/workflows/deploy-pages.yml`:
    ```bash
    git add .github/workflows/deploy-pages.yml
    git commit -m "feat: Implement GitHub Pages deployment workflow for LAB04"
    git push origin main
    ```

6.  **Verify Workflow Execution and Site Deployment:**
    *   Go to your GitHub repository and open the "Actions" tab. You should see your "Deploy Static Site to GitHub Pages" workflow running or completed.
    *   Inspect the logs for the `deploy` job. Verify that all steps completed successfully.
    *   After a successful run, go back to your repository `Settings` > `Pages`. The URL of your deployed site should be displayed at the top (e.g., `https://your-username.github.io/your-repository-name/`).
    *   Click the URL to visit your live static site! It might take a minute or two after the workflow completes for the site to become available.

---

## ✅ Validation Checklist

- [ ] GitHub Pages is enabled in repository settings, with **Source** set to **`GitHub Actions`**.
- [ ] The `.github/workflows/deploy-pages.yml` file is correctly completed with all `TODO`s addressed.
- [ ] Pushing changes to the `main` branch automatically triggers the "Deploy Static Site to GitHub Pages" workflow.
- [ ] The workflow run completes successfully in the GitHub Actions tab.
- [ ] All steps in the `deploy` job succeed, including artifact upload and deployment.
- [ ] Your static site (the content of `site/index.html`) is publicly accessible at the GitHub Pages URL provided in your repository settings.
- [ ] You understand where to find the `solutions.md` file for this lab.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for `deploy-pages.yml` with detailed explanations.

---

## 🧹 Cleanup

-   **Disable GitHub Pages:** In your repository `Settings` > `Pages`, you can change the source back to "None" or manage the site deletion if it was a temporary deployment.
-   **Remove Workflow File:**
    ```bash
    rm .github/workflows/deploy-pages.yml
    ```
    Commit and push the deletion.
-   The `site/index.html` file can be kept or removed as per your preference.

---

## 🧠 Key Concepts

-   **GitHub Pages:** A static site hosting service that takes HTML, CSS, and JavaScript files straight from a repository on GitHub, optionally runs them through a build process, and publishes a website.
-   **`actions/configure-pages`:** Prepares the environment for a GitHub Pages deployment.
-   **`actions/upload-pages-artifact`:** Packages specified files as a GitHub Pages artifact, ready for deployment.
-   **`actions/deploy-pages`:** Deploys a previously uploaded GitHub Pages artifact to the Pages service.
-   **Workflow Permissions (`permissions` block):** Essential for granting the `GITHUB_TOKEN` the necessary scopes to interact with GitHub Pages and other services.
-   **Deployment Environments:** GitHub Actions can define environments (like `github-pages`) which can have their own protection rules and secrets, and display the deployment URL.

---

## 🌟 Well Done!

You've successfully automated the deployment of a static website to GitHub Pages! This is a fantastic way to quickly publish and share your web projects.

---

## 🔁 What's Next?
Continue to [LAB05 - Scheduled Jobs & Cron Triggers](../LAB05-Scheduled-Cron-Jobs/) to automate jobs that run on a schedule.

Serve your site with a single push. 🌐🚀📄