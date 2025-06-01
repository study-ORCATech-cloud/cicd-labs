# Solutions for LAB07: Using Jenkins Shared Libraries

This document provides the completed `Jenkinsfile` for LAB07 and a recap of the necessary Jenkins Global Pipeline Library configuration. Students should refer to this after attempting the lab steps.

---

## ⚙️ Jenkins Configuration Recap: Global Pipeline Library

To use the shared library in this lab, you must configure it in Jenkins under **Manage Jenkins → Configure System → Global Pipeline Libraries**.

Key configuration details:

-   **Name:** `cicd-lab-library` (or your chosen name)
-   **Default version:** `main` (or your primary branch name)
-   **Retrieval method:** Modern SCM
-   **Source Code Management:** Git
-   **Project Repository:** URL of YOUR FORKED `cicd-labs` repository (e.g., `https://github.com/YOUR_USERNAME/cicd-labs.git`)
-   **Library Path:** `Jenkins/LAB07-Shared-Libraries/example-shared-library`

Ensure this is saved in Jenkins for the `@Library` directive in the `Jenkinsfile` to work.

---

## ✅ Completed `Jenkinsfile`

Below is the complete and working `Jenkinsfile` for this lab. It assumes the Global Pipeline Library named `cicd-lab-library` has been configured as described above.

```groovy
// Solution for TODO_LOAD_LIBRARY:
@Library('cicd-lab-library@main') _ // Assumes 'main' is the default branch

pipeline {
    agent any

    environment {
        APP_PATH = 'Jenkins/LAB07-Shared-Libraries/app'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out code...'
                checkout scm
                script {
                    // Verify that the example-shared-library directory is checked out along with the Jenkinsfile
                    echo "Listing contents of Jenkins/LAB07-Shared-Libraries/ to show example-shared-library:"
                    sh "ls -la Jenkins/LAB07-Shared-Libraries/"
                }
            }
        }

        stage('Setup & Test with Shared Library') {
            steps {
                // Solution for TODO_CALL_PRINT_MESSAGE:
                script {
                    customSteps.printMessage("Starting Lab 07 build process using functions from cicd-lab-library!")
                }

                // Solution for TODO_CALL_INSTALL_DEPS:
                script {
                    customSteps.installPythonDependencies(appPath: env.APP_PATH)
                }
                
                // Solution for TODO_CALL_RUN_PY_TESTS:
                script {
                    customSteps.runPyTests(appPath: env.APP_PATH)
                }

                echo "Shared library functions execution finished."
            }
        }

        stage('Run Main Python Script (Directly)') {
            steps {
                echo 'Running the main Python script directly from Jenkinsfile...'
                sh "python ${APP_PATH}/main.py"
            }
        }
    }

    post {
        always {
            echo 'Pipeline for Lab 07 (Shared Libraries) finished.'
            cleanWs()
        }
    }
}
```

---

## 📝 Explanation of Solutions

1.  **`TODO_LOAD_LIBRARY`**: `@Library('cicd-lab-library@main') _`
    *   This line at the top of the `Jenkinsfile` tells Jenkins to load the shared library named `cicd-lab-library` (which you configured in Jenkins system settings).
    *   `@main` specifies that the version of the library from the `main` branch of your repository should be used.
    *   The trailing `_` is mandatory Groovy syntax for this annotation when used this way.

2.  **`TODO_CALL_PRINT_MESSAGE`**: `customSteps.printMessage("Starting Lab 07 build process using functions from cicd-lab-library!")`
    *   The shared library script `example-shared-library/vars/customSteps.groovy` defines functions.
    *   Because the script is named `customSteps.groovy` and is in the `vars/` directory, Jenkins makes its functions available through a global variable named `customSteps`.
    *   We then call the `printMessage` function defined in that script.

3.  **`TODO_CALL_INSTALL_DEPS`**: `customSteps.installPythonDependencies(appPath: env.APP_PATH)`
    *   This calls the `installPythonDependencies` function from the `customSteps` shared library script.
    *   The function is designed to accept a map of arguments. We pass the `appPath` key with the value of `env.APP_PATH` (defined in the `environment` block of the `Jenkinsfile`) to tell the function where the Python application (and its `requirements.txt`) is located.

4.  **`TODO_CALL_RUN_PY_TESTS`**: `customSteps.runPyTests(appPath: env.APP_PATH)`
    *   Similarly, this calls the `runPyTests` function from the `customSteps` shared library script.
    *   It also passes the `appPath` so the function knows where to find the Python tests.

By using the shared library, the main `Jenkinsfile` becomes much cleaner and focuses on the pipeline flow, while the detailed logic for common tasks like installing dependencies or running tests is encapsulated in the shared library, making it reusable across other pipelines. 