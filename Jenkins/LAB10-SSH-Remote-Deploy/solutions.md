# Solutions for LAB10: Deploying to a Remote Server via SSH with Jenkins

This document provides the completed `Jenkinsfile` for LAB10 and a recap of the necessary Jenkins and server configurations. Students should refer to this after attempting the lab steps.

---

## ⚙️ Configuration Recap

**1. Remote Server SSH Setup:**
   - Ensure your remote Linux server is running and accessible via SSH from the Jenkins environment.
   - Your **public SSH key** must be added to the `~/.ssh/authorized_keys` file for the user you intend to connect as (e.g., `ec2-user`, `ubuntu`) on the remote server.

**2. Jenkins "SSH Agent" Plugin:**
   - Verify the "SSH Agent" plugin is installed in **Manage Jenkins -> Plugins**.

**3. Jenkins SSH Credential:**
   - An "SSH Username with private key" credential should be created in Jenkins (**Manage Jenkins -> Credentials -> System -> Global credentials**) with:
     - **Kind:** `SSH Username with private key`.
     - **ID:** `lab10-remote-ssh-key` (or your chosen ID that matches the `Jenkinsfile`).
     - **Username:** The username for your remote server (e.g., `ec2-user`).
     - **Private Key:** Your SSH private key (entered directly).
     - **Passphrase:** (If your key has one).

---

## ✅ Completed `Jenkinsfile`

Below is the complete and working `Jenkinsfile` for this lab. It assumes the Jenkins SSH credential `lab10-remote-ssh-key` is configured and that the environment variables are correctly set for your target server.

```groovy
pipeline {
    agent any

    environment {
        // Ensure these are updated with your actual server details by the student
        REMOTE_USER = 'your-remote-ssh-user' // e.g., ec2-user, ubuntu
        REMOTE_HOST = 'your-remote-server-ip-or-hostname' // e.g., 192.168.1.100
        REMOTE_BASE_PATH = '/tmp/jenkins-deployments'
        ARTIFACT_PATH = 'Jenkins/LAB10-SSH-Remote-Deploy/app/artifact.txt'
        DEPLOYMENT_DIR = "${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}"
    }

    stages {
        stage('Prepare Deployment Directory on Remote') {
            steps {
                // Solution for TODO_SSH_AGENT_WRAPPER_PREPARE & TODO_MKDIR_COMMAND:
                sshagent(['lab10-remote-ssh-key']) {
                    echo "Creating remote directory: ${DEPLOYMENT_DIR}"
                    sh "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${REMOTE_USER}@${REMOTE_HOST} 'mkdir -p ${DEPLOYMENT_DIR}'"
                }
            }
        }

        stage('Deploy Artifact via SCP') {
            steps {
                // Solution for TODO_SSH_AGENT_WRAPPER_DEPLOY & TODO_SCP_COMMAND:
                sshagent(['lab10-remote-ssh-key']) {
                    echo "Copying ${ARTIFACT_PATH} to ${REMOTE_USER}@${REMOTE_HOST}:${DEPLOYMENT_DIR}/artifact.txt"
                    sh "scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${ARTIFACT_PATH} ${REMOTE_USER}@${REMOTE_HOST}:${DEPLOYMENT_DIR}/artifact.txt"
                }
            }
        }

        stage('Verify Deployment on Remote') {
            steps {
                // Solution for TODO_SSH_AGENT_WRAPPER_VERIFY, TODO_LS_COMMAND, & TODO_CAT_COMMAND:
                sshagent(['lab10-remote-ssh-key']) {
                    echo "Verifying deployment by listing remote directory:"
                    sh "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${REMOTE_USER}@${REMOTE_HOST} 'ls -la ${DEPLOYMENT_DIR}'"
                    echo "Displaying content of deployed artifact:"
                    sh "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${REMOTE_USER}@${REMOTE_HOST} 'cat ${DEPLOYMENT_DIR}/artifact.txt'"
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline for Lab 10 (SSH Remote Deploy) finished."
            // Solution for TODO_CLEANUP_REMOTE (Optional):
            sshagent(['lab10-remote-ssh-key']) {
                echo "Cleaning up remote directory: ${DEPLOYMENT_DIR}"
                sh "ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ${REMOTE_USER}@${REMOTE_HOST} 'rm -rf ${DEPLOYMENT_DIR}'"
            }
            cleanWs() // Cleans the Jenkins workspace
        }
    }
}
```

**Important Notes on SSH Options:**
-   `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null`: These options are used in the `ssh` and `scp` commands to bypass SSH host key checking. This simplifies the lab setup by avoiding the need to manually accept host keys or manage a `known_hosts` file within Jenkins. **In a production environment, you should handle host key verification properly for security.** This might involve pre-populating the `known_hosts` file on the Jenkins agent or using other mechanisms to verify server identity.

---

## 📝 Explanation of Solutions

1.  **`environment { ... }` Block:**
    *   `REMOTE_USER`, `REMOTE_HOST`, `REMOTE_BASE_PATH`: These variables must be configured by the student to match their specific remote server setup.
    *   `ARTIFACT_PATH`: Points to the sample file to be deployed from the Jenkins workspace.
    *   `DEPLOYMENT_DIR`: A constructed variable for the unique deployment path on the remote server, making it easier to reference and clean up.

2.  **`sshagent(['lab10-remote-ssh-key']) { ... }` Wrapper:**
    *   This step, provided by the SSH Agent plugin, makes the private key from the specified Jenkins credential (`lab10-remote-ssh-key`) available to any SSH-based commands run within its block. Jenkins handles the secure injection of the key.

3.  **`stage('Prepare Deployment Directory on Remote')`:**
    *   `sh "ssh ... 'mkdir -p ${DEPLOYMENT_DIR}'"`: This command connects to the remote server and creates the target deployment directory. `mkdir -p` ensures that parent directories are also created if they don't exist, and it doesn't error if the directory already exists.

4.  **`stage('Deploy Artifact via SCP')`:**
    *   `sh "scp ... ${ARTIFACT_PATH} ${REMOTE_USER}@${REMOTE_HOST}:${DEPLOYMENT_DIR}/artifact.txt"`: This command uses `scp` (secure copy) to transfer the `artifact.txt` file from the Jenkins agent's workspace to the specified `DEPLOYMENT_DIR` on the remote server.

5.  **`stage('Verify Deployment on Remote')`:**
    *   `sh "ssh ... 'ls -la ${DEPLOYMENT_DIR}'"`: Lists the contents of the remote deployment directory to visually confirm the file was copied.
    *   `sh "ssh ... 'cat ${DEPLOYMENT_DIR}/artifact.txt'"`: Displays the content of the copied file from the remote server, confirming its integrity.

6.  **`post { always { ... } }` Block (Cleanup):**
    *   The `ssh` command `rm -rf ${DEPLOYMENT_DIR}` is used to remove the deployment-specific directory from the remote server. This is good practice for labs to keep the server clean. **Students should be reminded of the danger of `rm -rf` and ensure the path is correct.**

This lab provides a foundational understanding of how to automate deployments to remote servers using Jenkins, SSH, and SCP, which is a common requirement in many CI/CD workflows. 