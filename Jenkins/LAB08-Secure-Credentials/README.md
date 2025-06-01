# LAB08: Securely Managing Credentials in Jenkins

This lab focuses on a critical aspect of CI/CD: managing sensitive information like API tokens, passwords, and SSH keys. Jenkins provides a robust **Credentials Plugin** (installed by default) to store such secrets securely and make them available to your pipelines without exposing them in your `Jenkinsfile` or console logs.

In this lab, you will:
1.  Learn how to add "Secret text" and "Username with password" credentials to Jenkins' global credential store.
2.  Modify a `Jenkinsfile` to securely access and use these credentials through the `credentials()` helper and the `withCredentials` step.
3.  Observe how Jenkins automatically masks secret values in the build logs.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the importance of secure credential management in Jenkins.
- Be able to add different types of credentials (Secret text, Username with password) to the Jenkins Credentials Manager.
- Use the `credentials()` helper to bind a secret to an environment variable in a `Jenkinsfile`.
- Use the `withCredentials` step to scope credential access within a pipeline stage.
- Verify that Jenkins automatically masks secrets in console output.
- Recognize best practices for handling sensitive data in pipelines.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** Jenkins must be installed and accessible. Refer to **`../../install-and-setup.md`**.
-   **Jenkins Credentials Plugin:** This plugin is typically installed and enabled by default in Jenkins.
-   **Administrator Access to Jenkins:** You'll need this to add credentials to the Jenkins system.
-   **GitHub Account and Fork:** Your forked `cicd-labs` repository. The `Jenkinsfile` for this lab is within `Jenkins/LAB08-Secure-Credentials/`.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB08-Secure-Credentials/
├── README.md       # Lab overview, objectives, setup, TODOs (this file)
├── Jenkinsfile     # Declarative Pipeline script to practice using credentials (contains TODOs)
└── solutions.md    # Contains the completed Jenkinsfile
```
The lab does not involve a separate application; the focus is entirely on the `Jenkinsfile` and Jenkins credential management.

---

## 🔐 Jenkins Credentials: Adding and Managing

Jenkins provides a central place to manage credentials. For this lab, we'll add two types: "Secret text" and "Username with password".

**Part 1: Adding a "Secret text" Credential (e.g., for an API Key)**

1.  Navigate to your Jenkins Dashboard.
2.  Go to **Manage Jenkins** (usually on the left sidebar).
3.  Click on **Credentials** (under the "Security" section or search for it).
4.  Under **Stores scoped to Jenkins**, click on **System**.
5.  Click on **Global credentials (unrestricted)**.
6.  Click **"Add Credentials"** on the left sidebar.
7.  Configure the credential as follows:
    *   **Kind:** Select `Secret text`.
    *   **Scope:** Keep it as `Global (Jenkins, nodes, items, all child items, etc)`.
    *   **Secret:** Enter a dummy secret value, for example: `my-super-secret-api-key-for-lab08`
        *   *Note: In a real scenario, this would be an actual sensitive token.*
    *   **ID:** `lab08-api-key`
        *   *This ID is crucial. Your `Jenkinsfile` will use this ID to refer to this specific credential.*
    *   **Description:** (Optional but recommended) `API Key for Lab 08 demo`
8.  Click **"Create"**.

You have now stored an API key securely in Jenkins!

**Part 2: Adding a "Username with password" Credential**

1.  Follow steps 1-5 from Part 1 to get to the **Global credentials (unrestricted)** page.
2.  Click **"Add Credentials"** on the left sidebar.
3.  Configure the credential as follows:
    *   **Kind:** Select `Username with password`.
    *   **Scope:** Keep it as `Global`.
    *   **Username:** Enter a dummy username, for example: `lab_user`
    *   **Password:** Enter a dummy password, for example: `lab_password123!`
    *   **ID:** `lab08-user-pass`
        *   *This ID will be used in the `Jenkinsfile`.*
    *   **Description:** (Optional but recommended) `Username/Password for Lab 08 demo`
4.  Click **"Create"**.

You now have a username/password credential stored securely.

---

## 🚀 Lab Steps: Using Credentials in `Jenkinsfile`

Your task is to complete the `Jenkins/LAB08-Secure-Credentials/Jenkinsfile`. This file is designed to use the credentials you just created.

**1. Locate and Open `Jenkinsfile`:**
   Open `Jenkins/LAB08-Secure-Credentials/Jenkinsfile` in your local clone of your forked repository.

**2. Complete the `TODO` items in `Jenkinsfile`:**

   *   **`TODO_ENV_CREDENTIAL` (around line 4-13):**
        *   **Goal:** Use the `credentials()` helper to bind the "Secret text" credential (`lab08-api-key`) you created to an environment variable named `MY_API_KEY`.
        *   **Action:** Inside the `environment { ... }` block, assign `credentials('lab08-api-key')` to `MY_API_KEY`.
            ```groovy
            environment {
                MY_API_KEY = credentials('lab08-api-key')
            }
            ```

   *   **`TODO_ECHO_ENV_CREDENTIAL` (around line 20-23):**
        *   **Goal:** Print the value of the `MY_API_KEY` environment variable to the console.
        *   **Action:** Use a `sh` step to echo the variable. Jenkins should automatically mask the actual secret value in the output.
            ```groovy
            sh 'echo "My API Key is: $MY_API_KEY"'
            ```

   *   **`TODO_WITH_CREDENTIALS` (around line 30-40):**
        *   **Goal:** Use the `withCredentials` step to securely access the "Username with password" credential (`lab08-user-pass`) you created. This makes the username and password available as temporary variables within a specific block of code.
        *   **Action:** Wrap the existing `script { ... }` block (or just the echo commands if you prefer) inside a `withCredentials` step.
            *   The `credentialsId` will be `'lab08-user-pass'`.
            *   Define `usernameVariable: 'USERPASS_USR'` to store the username.
            *   Define `passwordVariable: 'USERPASS_PSW'` to store the password.
            ```groovy
            withCredentials([usernamePassword(credentialsId: 'lab08-user-pass', usernameVariable: 'USERPASS_USR', passwordVariable: 'USERPASS_PSW')]) {
                // The existing script block or echo commands will go here
                script {
                    // ...
                }
            }
            ```

   *   **`TODO_ECHO_USERPASS_CREDENTIALS` (around line 43-48, now inside `withCredentials`):**
        *   **Goal:** Print the username and password obtained via `withCredentials`.
        *   **Action:** Inside the `script` block, which is now nested within `withCredentials`, use `echo` to print the values of `USERPASS_USR` and `USERPASS_PSW`. The password should be masked by Jenkins.
            ```groovy
            // Ensure this is inside the withCredentials block
            echo "Username from credential: $USERPASS_USR"
            echo "Password from credential: $USERPASS_PSW" // This will be masked
            ```

**3. Commit and Push `Jenkinsfile` Changes:**
   Save your completed `Jenkinsfile`, then commit and push it to your forked GitHub repository.

**4. Configure and Run Jenkins Pipeline Job:**
   *   In Jenkins, create a new "Pipeline" job (e.g., `lab08-secure-credentials-pipeline`).
   *   Configure it to use "Pipeline script from SCM," pointing to your forked repository and the `Jenkins/LAB08-Secure-Credentials/Jenkinsfile` script path.
   *   Ensure the branch is correct (e.g., `*/main`).
   *   Save and click **"Build Now"**.

---

## ✅ Validation Checklist

- [ ] Successfully added a "Secret text" credential with ID `lab08-api-key` in Jenkins.
- [ ] Successfully added a "Username with password" credential with ID `lab08-user-pass` in Jenkins.
- [ ] The `Jenkinsfile` correctly uses `MY_API_KEY = credentials('lab08-api-key')`.
- [ ] The pipeline job runs, and the output for `MY_API_KEY` shows it being masked (e.g., `********`).
- [ ] The `Jenkinsfile` correctly uses `withCredentials` for `lab08-user-pass`, binding to `USERPASS_USR` and `USERPASS_PSW`.
- [ ] The pipeline job runs, and the output for `USERPASS_USR` shows the username, while `USERPASS_PSW` is masked.
- [ ] The pipeline completes successfully.

---

## 🧹 Cleanup

1.  **Jenkins Job:** Delete the `lab08-secure-credentials-pipeline` job in Jenkins if no longer needed.
2.  **Jenkins Credentials:**
    *   Navigate back to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials (unrestricted)**.
    *   Locate `lab08-api-key` and `lab08-user-pass`.
    *   You can delete them by clicking on the credential and then selecting "Delete" from its left sidebar. This is good practice for temporary lab credentials.

---

## 🧠 Key Concepts

-   **Jenkins Credentials Plugin:** The core Jenkins component for managing secrets.
-   **Credential Store:** A secure location within Jenkins where secrets are stored, encrypted at rest.
-   **Credential Types:** Jenkins supports various types (Secret text, Username/Password, SSH keys, Secret files, Certificates). This lab covers the first two.
-   **Credential ID:** A unique string identifier you assign to a credential, used to reference it in pipelines.
-   **`credentials()` helper:** Used in the `environment` block of a `Jenkinsfile` to bind a credential's value to an environment variable. The secret itself is not exposed directly in the variable if it's a "secret" type; Jenkins handles its injection.
-   **`withCredentials` step:** A more fine-grained way to access credentials. It makes the credential's components available as variables only within its specific block, limiting their scope.
-   **Masking:** Jenkins automatically attempts to identify and mask secret values when they are printed to the console log, preventing accidental exposure.
-   **Security Best Practice:** Never hardcode secrets directly in your `Jenkinsfile` or source code. Always use the Jenkins Credentials Plugin.

---

## 🔁 What's Next?

With an understanding of how to handle credentials securely, you're ready to explore integrations that often require them, such as sending notifications.

Proceed to **[../LAB09-Slack-Notifications/README.md](../LAB09-Slack-Notifications/)**.

