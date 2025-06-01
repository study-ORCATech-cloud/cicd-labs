# LAB09: Integrating Jenkins with Slack for Build Notifications

Effective communication is key in DevOps. This lab will guide you through configuring Jenkins to send automated notifications about your CI/CD pipeline statuses directly to a Slack channel. This keeps your team informed in real-time about build successes, failures, and other important events.

In this lab, you will:
1.  Install and configure the Slack Notification plugin in Jenkins.
2.  Create an Incoming Webhook in your Slack workspace.
3.  Securely store the Slack webhook URL in Jenkins using a credential.
4.  Modify a `Jenkinsfile` to send different notifications to Slack based on the pipeline's outcome (success, failure, etc.) using the `post` block and `slackSend` step.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand how to integrate Jenkins with Slack for automated notifications.
- Be able to install and configure the Jenkins Slack Notification plugin.
- Know how to create and manage Incoming Webhooks in Slack.
- Securely manage Slack webhook URLs using Jenkins credentials (building on Lab 08).
- Implement conditional notifications in a `Jenkinsfile` using the `post` block and `slackSend` function.
- Customize Slack messages with build status, job name, build number, and build URL.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Refer to **`../../install-and-setup.md`**.
-   **Administrator Access to Jenkins:** Required for installing plugins and system configuration.
-   **A Slack Workspace:** You need a Slack workspace where you have permissions to add apps and create Incoming Webhooks. If you don't have one, you can create a free Slack workspace.
-   **GitHub Account and Fork:** Your forked `cicd-labs` repository. The `Jenkinsfile` for this lab is within `Jenkins/LAB09-Slack-Notifications/`.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB09-Slack-Notifications/
├── README.md       # Lab overview, objectives, setup, TODOs (this file)
├── Jenkinsfile     # Declarative Pipeline script for sending Slack notifications (contains TODOs)
└── solutions.md    # Contains the completed Jenkinsfile and configuration recap
```
This lab does not involve a separate application; the focus is on Jenkins configuration and the `Jenkinsfile`.

---

## 🔌 Step 1: Install Slack Notification Plugin in Jenkins

1.  Go to your Jenkins Dashboard.
2.  Click **Manage Jenkins** -> **Plugins** (or **Manage Plugins**).
3.  Go to the **Available plugins** tab.
4.  In the search bar, type `Slack Notification`.
5.  Select the checkbox next to the "Slack Notification" plugin.
6.  Click **"Install without restart"** or **"Download now and install after restart"** (choose the option that suits you; installing without restart is usually fine for this plugin).
    *   If you choose to restart, Jenkins will guide you.

---

## 🔗 Step 2: Create an Incoming Webhook in Slack

Incoming Webhooks are a simple way to post messages from external sources into Slack.

1.  Open your Slack workspace in your browser or desktop app.
2.  Go to your workspace's app directory: Click on your workspace name (top left) -> **Settings & administration** -> **Manage apps**.
3.  In the App Directory, search for `Incoming WebHooks`.
4.  Click on **"Incoming WebHooks"** and then click **"Add to Slack"** or **"Add Configuration"**.
5.  **Choose a channel** where Jenkins notifications should be posted (e.g., `#ci-cd-alerts`, `#jenkins-notifications`, or create a new one). Then click **"Add Incoming WebHooks integration"**.
6.  Slack will generate a **Webhook URL**. This URL is sensitive. **Copy this URL** – you'll need it for Jenkins configuration.
    *   Example URL: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX`
7.  You can customize the name and icon for this integration if you wish (e.g., name it "Jenkins CI").
8.  Scroll down and click **"Save Settings"**.

---

## 🔐 Step 3: Configure Slack Plugin in Jenkins (and Secure Webhook)

Now, you'll configure Jenkins to use the webhook URL you just created. We'll store the webhook URL securely using Jenkins credentials, as learned in Lab 08.

**Part A: Create a Jenkins Credential for the Slack Webhook URL**

1.  In Jenkins, go to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials (unrestricted)**.
2.  Click **"Add Credentials"**.
3.  Configure as follows:
    *   **Kind:** `Secret text`.
    *   **Scope:** `Global`.
    *   **Secret:** Paste the **Webhook URL** you copied from Slack.
    *   **ID:** `slack-webhook-lab09` (You'll use this ID in Jenkins system configuration).
    *   **Description:** `Slack Webhook URL for Lab09 Notifications`.
4.  Click **"Create"**.

**Part B: Configure Slack Plugin in Jenkins System**

1.  In Jenkins, go to **Manage Jenkins** -> **Configure System**.
2.  Scroll down to the **"Slack"** section (this section appears after you've installed the Slack Notification plugin).
3.  Configure the following fields:
    *   **Workspace:** Your Slack workspace URL (e.g., `your-team.slack.com`). You can often leave this blank if using a full webhook URL in the credential, but some versions of the plugin might require it. Start by leaving it blank or using your workspace name (e.g. `myworkspace` if your slack is `myworkspace.slack.com`)
    *   **Credential:** Select the credential ID you created: `slack-webhook-lab09`.
    *   **Default channel / member ID:** Enter the name of the Slack channel you want to send messages to by default (e.g., `#jenkins-notifications` or the channel you configured for the webhook). This can be overridden in the `Jenkinsfile`.
    *   **Bot User:** (Usually unchecked unless you've configured a Slack bot user specifically).
    *   **Send As Text:** (Usually unchecked, allows richer formatting if unchecked).
4.  You can click the **"Test Connection"** button to ensure Jenkins can send a message to your Slack channel using the configured webhook and channel.
5.  Click **"Save"** at the bottom of the page.

---

## 🚀 Lab Steps: Sending Notifications from `Jenkinsfile`

Your task is to complete the `Jenkins/LAB09-Slack-Notifications/Jenkinsfile`.

**1. Locate and Open `Jenkinsfile`:**
   Open `Jenkins/LAB09-Slack-Notifications/Jenkinsfile` in your local clone of your forked repository.

**2. Complete the `TODO` items in the `post { ... }` block:**

The `post` section in a Declarative Pipeline allows you to define actions that run at the end of a pipeline run, based on its outcome.

   *   **`TODO_SLACK_NOTIFY_ALWAYS`:**
        *   **Goal:** Send a Slack message every time the pipeline finishes, regardless of status.
        *   **Action:** Inside the `always { ... }` block (you'll need to add this block if it's not there), use `slackSend`.
            ```groovy
            always {
                slackSend channel: '#your-slack-channel', \
                          color: '#439FE0', \
                          message: "Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] has completed. Status: ${currentBuild.currentResult}"
            }
            ```
            *   Replace `#your-slack-channel` with your actual channel if different from default.
            *   `currentBuild.currentResult` gives the status (SUCCESS, FAILURE, etc.).

   *   **`TODO_SLACK_NOTIFY_SUCCESS`:**
        *   **Goal:** Send a specific message only if the pipeline succeeds.
        *   **Action:** Inside a `success { ... }` block, use `slackSend`.
            ```groovy
            success {
                slackSend channel: '#your-slack-channel', \
                          color: 'good', \
                          message: "✅ SUCCESS: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] completed successfully. Details: ${env.BUILD_URL}"
            }
            ```

   *   **`TODO_SLACK_NOTIFY_FAILURE`:**
        *   **Goal:** Send a specific message only if the pipeline fails.
        *   **Action:** Inside a `failure { ... }` block, use `slackSend`.
            ```groovy
            failure {
                slackSend channel: '#your-slack-channel', \
                          color: 'danger', \
                          message: "❌ FAILURE: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] failed. Check console: ${env.BUILD_URL}"
            }
            ```

   *   **`TODO_SLACK_NOTIFY_UNSTABLE`:**
        *   **Goal:** Send a specific message if the pipeline is marked as unstable (e.g., tests passed but with some issues).
        *   **Action:** Inside an `unstable { ... }` block, use `slackSend`.
            ```groovy
            unstable {
                slackSend channel: '#your-slack-channel', \
                          color: 'warning', \
                          message: "⚠️ UNSTABLE: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] is unstable. Details: ${env.BUILD_URL}"
            }
            ```

   *   **`TODO_OPTIONAL_FAILURE` (in `stages`):**
        *   To test the `failure` notification, you can uncomment the `error 'Simulating a build failure!'` line within the 'Simulate Build' stage.

**3. Commit and Push `Jenkinsfile` Changes:**
   Save your completed `Jenkinsfile`, commit, and push to your forked GitHub repository.

**4. Configure and Run Jenkins Pipeline Job:**
   *   Create a new "Pipeline" job in Jenkins (e.g., `lab09-slack-notifications-pipeline`).
   *   Configure it to use "Pipeline script from SCM," pointing to your forked repository and the `Jenkins/LAB09-Slack-Notifications/Jenkinsfile` script path.
   *   Save and click **"Build Now"**.
   *   Run it once. Then, uncomment the `error` step in the `Jenkinsfile`, commit/push, and run it again to test failure notifications.

---

## ✅ Validation Checklist

- [ ] "Slack Notification" plugin is installed in Jenkins.
- [ ] An Incoming Webhook is created in Slack, and its URL is copied.
- [ ] The Slack Webhook URL is securely stored as a Jenkins credential (e.g., ID `slack-webhook-lab09`).
- [ ] Jenkins system configuration for Slack points to the correct credential and default channel.
- [ ] The "Test Connection" button in Jenkins Slack configuration sends a message successfully to Slack.
- [ ] The `Jenkinsfile` includes `slackSend` calls within `always`, `success`, `failure`, and `unstable` blocks in the `post` section.
- [ ] A successful pipeline run sends the appropriate "SUCCESS" and "ALWAYS" messages to Slack.
- [ ] A failed pipeline run (after uncommenting the `error` step) sends the appropriate "FAILURE" and "ALWAYS" messages to Slack.
- [ ] Slack messages include dynamic content like Job Name, Build Number, Status, and Build URL.

---

## 🧹 Cleanup

1.  **Jenkins Job:** Delete the `lab09-slack-notifications-pipeline` job.
2.  **Jenkins Slack Configuration:**
    *   Go to **Manage Jenkins** -> **Configure System** -> **Slack**.
    *   You can clear the Workspace, Credential, and Default channel fields if desired.
3.  **Jenkins Credential:** Delete the `slack-webhook-lab09` credential from **Manage Jenkins** -> **Credentials**.
4.  **Slack Incoming Webhook:**
    *   In Slack, go to **Apps** -> **Incoming WebHooks** -> **Configurations**.
    *   Find the webhook you created for this lab and click the **pencil icon** to edit.
    *   Scroll down and click **"Remove"** or **"Disable"**.

---

## 🧠 Key Concepts

-   **Slack Notification Plugin:** Enables Jenkins to communicate with Slack.
-   **Incoming Webhooks (Slack):** A simple way for external applications to send messages to Slack channels.
-   **`post` block (Jenkinsfile):** Defines actions to be executed at the end of a pipeline based on its outcome (e.g., `always`, `success`, `failure`, `unstable`, `changed`).
-   **`slackSend` function:** The Jenkins pipeline step provided by the Slack plugin to send messages. It accepts parameters like `channel`, `message`, `color`, `tokenCredentialId` (if not using global config).
-   **`env.JOB_NAME`, `env.BUILD_NUMBER`, `env.BUILD_URL`:** Built-in Jenkins environment variables that provide context about the current build.
-   **`currentBuild.currentResult`:** A Jenkins pipeline variable that holds the current status of the build (e.g., `SUCCESS`, `FAILURE`, `UNSTABLE`, `ABORTED`).
-   **Real-time Feedback:** Integrating notifications provides immediate feedback to the development team about their CI/CD processes.

---

## 🔁 What's Next?

After mastering notifications, the next step is often deploying your application to a remote server.

Proceed to **[../LAB10-SSH-Remote-Deploy/README.md](../LAB10-SSH-Remote-Deploy/)**.

Ping your team. Stay in sync. 📣💬📦

