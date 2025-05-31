# Solutions for LAB03: Declarative Pipeline with Jenkinsfile

This document provides the completed `Jenkinsfile` for LAB03, with explanations for each `TODO` item that was in the skeleton file.

---

## ✅ Completed `Jenkinsfile`

Below is the complete and working `Jenkinsfile` for this lab. This should be placed at `Jenkins/LAB03-Declarative-Pipeline/Jenkinsfile` in your forked repository.

```groovy
pipeline {
    // TODO_AGENT: Specify the agent for this pipeline. 
    // Solution: Using 'agent any' as it's suitable for this lab.
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                // TODO_CHECKOUT: If your SCM needs specific checkout parameters, add them here.
                // Solution: `checkout scm` is used. This command tells Jenkins to use the SCM
                // configuration defined in the Jenkins Pipeline job's UI settings.
                // For this lab, the UI configuration should point to the student's fork
                // of the cicd-labs repository and the correct branch.
                checkout scm
                script {
                    sh 'echo "Workspace content after checkout:" && ls -la'
                    sh 'echo "Listing app directory:" && ls -la Jenkins/LAB03-Declarative-Pipeline/app'
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                // TODO_INSTALL_DEPS: Write the shell command to install dependencies using pip and requirements.txt.
                // Solution: The commands first upgrade pip, then install packages from the specified requirements.txt file.
                // The path is relative to the workspace root where the repository is checked out.
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r Jenkins/LAB03-Declarative-Pipeline/app/requirements.txt'
            }
        }
        stage('Run Python Script') {
            steps {
                echo 'Running the main Python script...'
                // TODO_RUN_SCRIPT: Write the shell command to execute the app/main.py script.
                // Solution: Executes the main.py script using python.
                // The path is relative to the workspace root.
                sh 'python Jenkins/LAB03-Declarative-Pipeline/app/main.py'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running Python tests with pytest...'
                // TODO_RUN_TESTS: Write the shell command to run pytest against the tests in app/tests/.
                // Solution: Executes pytest, targeting the specified tests directory.
                // The path is relative to the workspace root.
                sh 'pytest Jenkins/LAB03-Declarative-Pipeline/app/tests/'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // TODO_CLEANUP_WORKSPACE (Optional): Add a step to clean up the workspace if desired.
            // Solution (Optional): cleanWs() can be added here to wipe the workspace after the build.
            // For this lab, it's commented out to allow students to inspect the workspace if they wish.
            // cleanWs()
        }
    }
}
```

---

## 📝 Explanation of Solutions

1.  **`TODO_AGENT`**: `agent any`
    *   This directive tells Jenkins to execute this pipeline on any available agent (node). For a default Jenkins setup, this often means it runs on the Jenkins controller itself. It's simple and sufficient for this lab.

2.  **`TODO_CHECKOUT`**: `checkout scm`
    *   This step instructs Jenkins to perform a checkout using the SCM (Source Code Management - e.g., Git) settings defined in the Pipeline job's configuration page in the Jenkins UI. When you create the "Pipeline" job and configure it to use "Pipeline script from SCM," you specify the repository URL and branch there. `checkout scm` then uses those details.
    *   The `script { sh 'ls -la' }` block was added to help visualize the checked-out files in the console output for verification.

3.  **`TODO_INSTALL_DEPS`**: `sh 'python -m pip install --upgrade pip'` and `sh 'pip install -r Jenkins/LAB03-Declarative-Pipeline/app/requirements.txt'`
    *   The first command ensures `pip` (Python's package installer) is up-to-date.
    *   The second command reads the `Jenkins/LAB03-Declarative-Pipeline/app/requirements.txt` file (which contains `pytest`) and installs the listed dependencies.
The path is relative to the root of the Jenkins workspace where the repository was checked out.

4.  **`TODO_RUN_SCRIPT`**: `sh 'python Jenkins/LAB03-Declarative-Pipeline/app/main.py'`
    *   This command executes the Python script `main.py` located at `Jenkins/LAB03-Declarative-Pipeline/app/main.py` within the checked-out workspace.

5.  **`TODO_RUN_TESTS`**: `sh 'pytest Jenkins/LAB03-Declarative-Pipeline/app/tests/'`
    *   This command runs `pytest`. `pytest` will automatically discover and run the tests in the `Jenkins/LAB03-Declarative-Pipeline/app/tests/` directory.

6.  **`TODO_CLEANUP_WORKSPACE` (Optional)**: `// cleanWs()`
    *   The `cleanWs()` step, if uncommented, would instruct Jenkins to delete all files from the workspace after the pipeline completes. This is useful for saving disk space and ensuring a clean environment for the next build. It's commented out in the solution to allow students to manually inspect the workspace contents via the Jenkins UI if they need to troubleshoot.

---

By completing these `TODO` items, you create a functional Declarative Pipeline that automates the basic CI steps for the provided Python application. 