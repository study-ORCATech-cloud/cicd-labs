# Solutions for LAB09: Integrating Jenkins with Slack for Build Notifications

This document provides the completed `Jenkinsfile` for LAB09 and a recap of the necessary Jenkins and Slack configurations. Students should refer to this after attempting the lab steps.

---

## ⚙️ Configuration Recap

**1. Slack Incoming Webhook:**
   - Ensure you have created an Incoming Webhook in your Slack workspace for a specific channel.
   - You should have the **Webhook URL** (e.g., `https://hooks.slack.com/services/T000.../B000.../XXXX...`).

**2. Jenkins Slack Notification Plugin:**
   - Verify the "Slack Notification" plugin is installed in **Manage Jenkins -> Plugins**.

**3. Jenkins Credential for Webhook:**
   - A "Secret text" credential should be created in Jenkins (**Manage Jenkins -> Credentials -> System -> Global credentials**) with:
     - **ID:** `slack-webhook-lab09` (or your chosen ID)
     - **Secret:** Your Slack Webhook URL.

**4. Jenkins System Configuration for Slack:**
   - In **Manage Jenkins -> Configure System -> Slack**:
     - **Workspace:** Your Slack workspace name/URL (e.g., `your-team` or `your-team.slack.com`). Can sometimes be left blank if the full webhook URL is in the credential.
     - **Credential:** `slack-webhook-lab09` (or your chosen credential ID).
     - **Default channel / member ID:** Your target Slack channel (e.g., `#jenkins-notifications`).
     - Test the connection using the "Test Connection" button.

---

## ✅ Completed `Jenkinsfile`

Below is the complete and working `Jenkinsfile` for this lab. It assumes the Jenkins system configuration for Slack has been done correctly and points to the credential holding the webhook URL.

```groovy
pipeline {
    agent any

    stages {
        stage('Simulate Build') {
            steps {
                echo 'Simulating a build step...'
                // For testing failure notifications, you can uncomment the line below:
                // error 'Simulating a build failure for Slack notification test!'
                echo 'Build simulation completed.'
            }
        }
    }

    post {
        always {
            // Solution for TODO_SLACK_NOTIFY_ALWAYS:
            script {
                // It's good practice to check if currentBuild has a result yet, especially in 'always'
                def jobName = env.JOB_NAME
                def buildNumber = env.BUILD_NUMBER
                def buildStatus = currentBuild.currentResult ?: 'IN PROGRESS' // Default if result isn't set yet
                def buildUrl = env.BUILD_URL
                def alwaysMessage = "Pipeline '${jobName}' [Build #${buildNumber}] has completed. Status: ${buildStatus}. Details: ${buildUrl}"
                def alwaysColor = '#439FE0' // Neutral blue

                if (buildStatus == 'SUCCESS') {
                    alwaysColor = 'good'
                } else if (buildStatus == 'FAILURE') {
                    alwaysColor = 'danger'
                } else if (buildStatus == 'UNSTABLE') {
                    alwaysColor = 'warning'
                }
                slackSend channel: '#your-slack-channel', \
                          color: alwaysColor, \
                          message: alwaysMessage
            }
        }

        success {
            // Solution for TODO_SLACK_NOTIFY_SUCCESS:
            slackSend channel: '#your-slack-channel', \
                      color: 'good', \
                      message: "✅ SUCCESS: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] completed successfully. Yay! ${env.BUILD_URL}"
        }

        failure {
            // Solution for TODO_SLACK_NOTIFY_FAILURE:
            slackSend channel: '#your-slack-channel', \
                      color: 'danger', \
                      message: "❌ FAILURE: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] failed. Check console: ${env.BUILD_URL}"
        }

        unstable {
            // Solution for TODO_SLACK_NOTIFY_UNSTABLE:
            slackSend channel: '#your-slack-channel', \
                      color: 'warning', \
                      message: "⚠️ UNSTABLE: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] is unstable. Please review: ${env.BUILD_URL}"
        }
        
        // Example of other conditions you could use:
        // aborted {
        //     slackSend channel: '#your-slack-channel', color: '#808080', message: "ABORTED: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] was aborted. ${env.BUILD_URL}"
        // }
        // fixed {
        //     slackSend channel: '#your-slack-channel', color: 'good', message: "FIXED: Pipeline '${env.JOB_NAME}' [Build #${env.BUILD_NUMBER}] is now stable after a previous failure. ${env.BUILD_URL}"
        // }
    }
}
```

**Note on `#your-slack-channel`**: Remember to replace `#your-slack-channel` in the `slackSend` steps with the actual Slack channel you configured (e.g., `#jenkins-notifications`), or rely on the default channel set in Jenkins system configuration if you prefer.

---

## 📝 Explanation of Solutions

1.  **`post { ... }` block:** This block in a Declarative Pipeline is executed after all stages in the pipeline have completed (or one has failed).

2.  **Conditions (`always`, `success`, `failure`, `unstable`):**
    *   `always`: Steps in this block execute regardless of the pipeline's final status.
    *   `success`: Steps execute only if the pipeline completes successfully.
    *   `failure`: Steps execute only if the pipeline fails.
    *   `unstable`: Steps execute if the pipeline is marked as unstable (often due to test failures that don't halt the entire build).

3.  **`slackSend` step:**
    *   This is the core command from the Slack Notification plugin.
    *   `channel`: Specifies the Slack channel to send the message to. If omitted, the default channel from Jenkins system configuration is used.
    *   `color`: Sets the color of the message attachment bar in Slack (e.g., `good` for green, `warning` for yellow, `danger` for red, or a hex color code like `#439FE0`).
    *   `message`: The text of the notification. You can use Jenkins environment variables (`env.JOB_NAME`, `env.BUILD_NUMBER`, `env.BUILD_URL`) and `currentBuild.currentResult` to create dynamic and informative messages.

4.  **Dynamic `always` message color:**
    *   In the `always` block solution, a small `script` block is used to dynamically set the `alwaysColor` based on `currentBuild.currentResult`. This allows the "always" message to also reflect the build status visually.

By using these configurations and `Jenkinsfile` constructs, you can set up a comprehensive notification system that keeps your team updated on the status of your CI/CD pipelines directly within Slack. 