# Solutions for LAB08: Securely Managing Credentials in Jenkins

This document provides the completed `Jenkinsfile` for LAB08. Students should refer to this after attempting the lab steps and ensure they have correctly configured the credentials in Jenkins as per the `README.md` instructions.

---

## 🔐 Jenkins Credentials Configuration Recap

Before running the solution `Jenkinsfile`, ensure you have created the following credentials in Jenkins under **Manage Jenkins → Credentials → System → Global credentials (unrestricted)**:

1.  **API Key Credential:**
    *   **Kind:** `Secret text`
    *   **ID:** `lab08-api-key`
    *   **Secret:** (Your dummy secret, e.g., `my-super-secret-api-key-for-lab08`)

2.  **Username/Password Credential:**
    *   **Kind:** `Username with password`
    *   **ID:** `lab08-user-pass`
    *   **Username:** (Your dummy username, e.g., `lab_user`)
    *   **Password:** (Your dummy password, e.g., `lab_password123!`)

---

## ✅ Completed `Jenkinsfile`

Below is the complete and working `Jenkinsfile` for this lab. It assumes the credentials `lab08-api-key` and `lab08-user-pass` have been configured in Jenkins.

```groovy
pipeline {
    agent any

    // Solution for TODO_ENV_CREDENTIAL:
    environment {
        MY_API_KEY = credentials('lab08-api-key')
    }

    stages {
        stage('Access Secret Text Credential') {
            steps {
                echo "Attempting to use the API Key from environment variable..."
                // Solution for TODO_ECHO_ENV_CREDENTIAL:
                sh 'echo "My API Key is: $MY_API_KEY"' // Jenkins will mask this
                echo "If the above line showed '********' or similar, the credential was masked!"
            }
        }

        stage('Access Username/Password Credential') {
            steps {
                // Solution for TODO_WITH_CREDENTIALS:
                withCredentials([usernamePassword(credentialsId: 'lab08-user-pass', usernameVariable: 'USERPASS_USR', passwordVariable: 'USERPASS_PSW')]) {
                    script {
                        // Solution for TODO_ECHO_USERPASS_CREDENTIALS:
                        echo "Username from credential: $USERPASS_USR"
                        echo "Password from credential: $USERPASS_PSW" // Jenkins will mask the password
                    }
                    echo "If the password above was masked, the withCredentials step is working correctly!"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline for Lab 08 (Secure Credentials) finished.'
            cleanWs()
        }
    }
}
```

---

## 📝 Explanation of Solutions

1.  **`TODO_ENV_CREDENTIAL` / `environment { MY_API_KEY = credentials('lab08-api-key') }`**
    *   This block tells Jenkins to fetch the secret associated with the ID `lab08-api-key` from its credential store.
    *   It then binds this secret to an environment variable named `MY_API_KEY`.
    *   This variable is available throughout the pipeline.

2.  **`TODO_ECHO_ENV_CREDENTIAL` / `sh 'echo "My API Key is: $MY_API_KEY"'`**
    *   This line attempts to print the value of `MY_API_KEY`.
    *   Jenkins automatically detects that this variable holds a secret fetched via the `credentials()` helper and masks its value in the console output (usually replacing it with asterisks `********`). This prevents accidental exposure of the actual secret.

3.  **`TODO_WITH_CREDENTIALS` / `withCredentials([...]) { ... }`**
    *   The `withCredentials` step is used to access credentials for a limited scope. It's generally preferred for credentials that are not needed globally as environment variables.
    *   `usernamePassword(credentialsId: 'lab08-user-pass', usernameVariable: 'USERPASS_USR', passwordVariable: 'USERPASS_PSW')` specifies:
        *   `credentialsId: 'lab08-user-pass'`: The ID of the "Username with password" credential to use.
        *   `usernameVariable: 'USERPASS_USR'`: The username from the credential will be available in a temporary variable named `USERPASS_USR` within the `withCredentials` block.
        *   `passwordVariable: 'USERPASS_PSW'`: The password from the credential will be available in a temporary variable named `USERPASS_PSW` within the `withCredentials` block.

4.  **`TODO_ECHO_USERPASS_CREDENTIALS` / `echo "Username: $USERPASS_USR"` and `echo "Password: $USERPASS_PSW"`**
    *   These lines, placed inside the `withCredentials` block, print the username and password.
    *   The username (`USERPASS_USR`) is typically not sensitive and will be printed as is.
    *   The password (`USERPASS_PSW`), however, is sensitive. Jenkins will detect this and mask its value in the console output, similar to the API key.

This lab demonstrates fundamental techniques for securely handling sensitive data in Jenkins pipelines, a crucial skill for any DevOps practitioner. 