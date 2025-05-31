# LAB04: SCM Polling & Webhooks for Automated Jenkins Builds

In this lab, you will learn how to automate the triggering of your Jenkins pipeline jobs based on changes in your GitHub repository. You'll explore two common methods: **SCM Polling** and **GitHub Webhooks**. This builds upon the Declarative Pipeline job you configured in Lab 03.

Automating build triggers is a fundamental concept in CI/CD, ensuring that your pipeline runs automatically whenever new code is pushed, providing rapid feedback to developers.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand the difference between SCM polling and webhooks for triggering Jenkins jobs.
- Configure a Jenkins pipeline job to periodically poll a GitHub repository for changes.
- Configure a GitHub webhook to instantly notify Jenkins upon code pushes.
- Test both triggering mechanisms by making changes to your forked repository.
- Understand the prerequisites and implications of using webhooks (e.g., Jenkins accessibility).

---

## 🧰 Prerequisites

- **Jenkins Installed and Running:** Jenkins must be installed and accessible. Refer to **`../../install-and-setup.md`**.
- **Lab 03 Completed:** You should have a working "Pipeline" job configured in Jenkins that uses the `Jenkinsfile` from your forked `cicd-labs` repository, as set up in `../LAB03-Declarative-Pipeline/README.md`. This job (`python-declarative-pipeline` or similar) will be the one you configure for polling and webhooks.
- **GitHub Account and Fork:**
    *   Your forked `cicd-labs` repository (`https://github.com/YOUR_USERNAME/cicd-labs.git`) containing the `Jenkinsfile` at `Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile`.
    *   You will need to be able to make changes to this forked repository and push them.
- **`ngrok` (Optional, for Webhooks):** If your Jenkins instance is running locally and is not publicly accessible via the internet, you will need `ngrok` or a similar tunneling service to expose your Jenkins URL to GitHub for webhooks to function. Instructions for `ngrok` are included in the `LAB.md` file.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB04-SCM-Polling-Webhooks/
├── README.md     # Lab overview, objectives, prerequisites (this file)
└── LAB.md        # Detailed step-by-step instructions for configuring polling and webhooks
```

---

## 🤔 Lab Scenario: Why Automate Triggers?

In Lab 03, you manually triggered your pipeline by clicking "Build Now" in Jenkins. While this is useful for initial setup and testing, real-world CI/CD practices demand automation. You want your pipeline to run automatically whenever a developer pushes new code to the repository. This ensures:
- **Rapid Feedback:** Developers quickly learn if their changes introduced issues.
- **Consistent Builds:** Every relevant change is built and tested.
- **Reduced Manual Effort:** No need to remember to click "Build Now."

SCM Polling and Webhooks are two ways to achieve this automation.

---

## 🚀 Lab Steps

Detailed, step-by-step instructions for configuring SCM Polling and GitHub Webhooks are provided in the **`LAB.md`** file in this directory.

Please proceed to **[./LAB.md](./LAB.md)** to begin the hands-on portion of this lab.

---

## ✅ Validation Checklist

After completing the steps in `LAB.md`:
- [ ] For SCM Polling:
    - [ ] The Jenkins job is configured with a polling schedule.
    - [ ] Pushing a commit to your forked repository (the branch monitored by the pipeline) triggers a new Jenkins build automatically after the polling interval.
- [ ] For GitHub Webhooks:
    - [ ] A webhook is configured in your GitHub repository settings, pointing to your Jenkins URL.
    - [ ] Pushing a commit to your forked repository triggers a new Jenkins build almost instantly.
- [ ] The console output of the automatically triggered Jenkins builds shows that the pipeline ran successfully using the latest committed code.

---

## 🧹 Cleanup

1.  **In Jenkins:**
    *   Open the configuration of your pipeline job (`python-declarative-pipeline` or similar).
    *   Under "Build Triggers," uncheck "Poll SCM" if you enabled it.
    *   Uncheck "GitHub hook trigger for GITScm polling" if you enabled it.
    *   Save the job configuration.
2.  **In GitHub:**
    *   Navigate to your forked `cicd-labs` repository.
    *   Go to `Settings` -> `Webhooks`.
    *   Delete the webhook you configured for Jenkins.
3.  **`ngrok` (if used):**
    *   Stop the `ngrok` tunnel if it's still running in your terminal (usually `Ctrl+C`).

---

## 🧠 Key Concepts

-   **SCM Polling:** Jenkins periodically checks the Source Code Management (SCM) system (e.g., Git) at a defined schedule (e.g., every 5 minutes) for new changes.
    *   **Pros:** Simple to set up, doesn't require Jenkins to be publicly accessible.
    *   **Cons:** Can be resource-intensive on Jenkins and the SCM server, introduces a delay between commit and build (up to the polling interval).
-   **Webhooks:** The SCM system (e.g., GitHub) sends a notification (an HTTP POST request) to a specific URL on Jenkins whenever a certain event occurs (e.g., a code push).
    *   **Pros:** Near real-time build triggers, more efficient as Jenkins only acts when notified.
    *   **Cons:** Requires Jenkins to be accessible from the SCM server (e.g., via a public IP address or a tunnel like `ngrok`). The endpoint on Jenkins (`/github-webhook/`) must be reachable.
-   **`ngrok`:** A tool that creates secure tunnels from a public endpoint (URL) to a locally running web service, useful for exposing a local Jenkins instance to the internet for webhooks.
-   **Build Triggers:** The section in Jenkins job configuration where you define how a job should be started automatically.

---

## 🔁 What’s Next?

After understanding how to automate your builds, you'll learn how to build and manage Docker images within your Jenkins pipeline.

Proceed to **[../LAB05-Docker-Image-Build/README.md](../LAB05-Docker-Image-Build/)**.

