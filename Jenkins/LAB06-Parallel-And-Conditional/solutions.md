# Solutions for LAB06: Parallel & Conditional Stages

This document provides the completed `Jenkinsfile` for LAB06. Students should refer to this after attempting to complete the `TODO` items in `Jenkins/LAB06-Parallel-And-Conditional/Jenkinsfile` themselves.

---

## ✅ Completed `Jenkinsfile`

Below is the complete and working `Jenkinsfile` for this lab, demonstrating parameters, parallel stages, and conditional execution.

```groovy
pipeline {
    agent any

    // Solution for TODO_PARAMETERS:
    parameters {
        booleanParam(name: 'RUN_UNIT_TESTS', defaultValue: true, description: 'Run unit tests for the Python app')
        booleanParam(name: 'RUN_LINTING', defaultValue: false, description: 'Run placeholder linting checks')
    }

    environment {
        APP_PATH = 'Jenkins/LAB06-Parallel-And-Conditional/app'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out code...'
                checkout scm
                script {
                    sh 'echo "Workspace content after checkout:" && ls -la'
                    sh 'echo "App directory content:" && ls -la ${APP_PATH}'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh "python -m pip install --upgrade pip"
                sh "pip install -r ${APP_PATH}/requirements.txt"
            }
        }
        
        stage('Run Main Python Script (Always Runs)') {
            steps {
                echo 'Running the main Python script for Lab 06...'
                sh "python ${APP_PATH}/main.py"
            }
        }

        // Solution for TODO_PARALLEL_STAGES:
        stage('Quality Checks (Parallel)') {
            parallel {
                stage('Unit Tests') {
                    // Solution for TODO_UNIT_TESTS_CONDITION:
                    when {
                        expression { params.RUN_UNIT_TESTS == true }
                    }
                    steps {
                        echo 'Running Python unit tests for Lab 06...'
                        // Solution for TODO_UNIT_TESTS_COMMAND:
                        sh "pytest ${APP_PATH}/tests/"
                    }
                }
                stage('Code Linting (Placeholder)') {
                    // Solution for TODO_LINTING_CONDITION:
                    when {
                        expression { params.RUN_LINTING == true }
                    }
                    steps {
                        echo 'Simulating code linting (e.g., with pylint, flake8)...
                        // Solution for TODO_LINTING_COMMAND (Optional):
                        sh 'echo "Linting checks would run here. No actual linter configured for this lab."'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline for Lab 06 finished.'
            cleanWs() // Cleans up the workspace
        }
    }
}
```

---

## 📝 Explanation of Solutions

1.  **`TODO_PARAMETERS`**:
    *   The `parameters` block is added at the top level of the `pipeline`.
    *   `booleanParam(name: 'RUN_UNIT_TESTS', defaultValue: true, description: '...')`: Defines a checkbox parameter for running unit tests, which will be true (checked) by default when a build is triggered manually with parameters.
    *   `booleanParam(name: 'RUN_LINTING', defaultValue: false, description: '...')`: Defines a checkbox parameter for running linting, which will be false (unchecked) by default.
    *   These parameters can be accessed within the pipeline using `params.PARAMETER_NAME` (e.g., `params.RUN_UNIT_TESTS`).

2.  **`TODO_PARALLEL_STAGES`**:
    *   A new parent stage named `Quality Checks (Parallel)` is created.
    *   Inside this stage, a `parallel { ... }` block is used.
    *   The original standalone `Unit Tests` and `Code Linting (Placeholder)` stages from the skeleton are moved *inside* this `parallel` block. This allows Jenkins to attempt to run them concurrently, potentially saving overall pipeline execution time if sufficient agent executors are available.

3.  **`TODO_UNIT_TESTS_CONDITION`** (within the 'Unit Tests' stage inside `parallel`):
    *   `when { expression { params.RUN_UNIT_TESTS == true } }`
    *   This `when` directive is added to the 'Unit Tests' stage. The stage will only execute if the `RUN_UNIT_TESTS` build parameter is true.

4.  **`TODO_UNIT_TESTS_COMMAND`** (within the 'Unit Tests' stage inside `parallel`):
    *   `sh "pytest ${APP_PATH}/tests/"`
    *   This shell command executes `pytest` against the tests located in the `app/tests/` directory (path relative to the workspace root, using the `APP_PATH` environment variable).

5.  **`TODO_LINTING_CONDITION`** (within the 'Code Linting (Placeholder)' stage inside `parallel`):
    *   `when { expression { params.RUN_LINTING == true } }`
    *   This `when` directive is added to the 'Code Linting (Placeholder)' stage. The stage will only execute if the `RUN_LINTING` build parameter is true.

6.  **`TODO_LINTING_COMMAND`** (within the 'Code Linting (Placeholder)' stage inside `parallel`):
    *   `sh 'echo "Linting checks would run here. No actual linter configured for this lab."'`
    *   For this lab, a simple `echo` suffices to simulate a linting step. In a real-world scenario, this would be a command like `pylint`, `flake8`, or another linter.

This `Jenkinsfile` structure allows students to manually trigger the pipeline and choose whether to run unit tests and/or linting via build parameters. The chosen quality checks will then attempt to run in parallel. 