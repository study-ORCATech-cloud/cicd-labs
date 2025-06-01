# LAB10: Deploying to a Remote Server via SSH with Jenkins

This final lab in the Jenkins series demonstrates a common deployment pattern: transferring files and executing commands on a remote server using SSH (Secure Shell). This is often used for deploying applications to virtual machines, on-premise servers, or any environment accessible via SSH.

In this lab, you will:
1.  Understand the prerequisites for SSH-based deployment (SSH key pairs, server accessibility).
2.  Install and use the "SSH Agent" plugin in Jenkins.
3.  Securely store an SSH private key as a Jenkins credential.
4.  Modify a `Jenkinsfile` to use the `sshagent` wrapper to:
    *   Create a deployment directory on a remote server.
    *   Copy a sample artifact to the remote server using `scp`.
    *   Execute commands on the remote server using `ssh` to verify the deployment.
    *   (Optional) Clean up the remote deployment directory.

---

## 🎯 Objectives

By the end of this lab, you will:
- Be able to configure Jenkins for SSH-based deployments.
- Know how to generate and use SSH key pairs for server authentication.
- Securely manage SSH private keys using Jenkins credentials (Kind: "SSH Username with private key").
- Use the `sshagent` pipeline step to make SSH credentials available to shell commands.
- Execute remote commands (`mkdir`, `ls`, `cat`) via `ssh` from a Jenkins pipeline.
- Transfer files to a remote server using `scp` from a Jenkins pipeline.
- Understand how to structure a Jenkinsfile for simple remote deployments.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** With administrator access. Refer to **`../../install-and-setup.md`**.
-   **A Remote Linux Server:** This server will be your deployment target. Examples:
    *   An AWS EC2 instance (a `t2.micro` or `t3.micro` on the free tier is sufficient).
    *   A virtual machine (VM) on your local machine (e.g., using VirtualBox, VMware) running Linux.
    *   Any other Linux server you have SSH access to.
    *   Ensure your Jenkins controller/agent can reach this server over the network on the SSH port (usually 22).
-   **SSH Key Pair (Public/Private):**
    *   You need an SSH key pair. If you don't have one, you can generate it using `ssh-keygen -t rsa -b 4096` on a Linux/macOS machine or using PuTTYgen on Windows.
    *   The **public key** (`.pub` file, e.g., `~/.ssh/id_rsa.pub`) must be added to the `~/.ssh/authorized_keys` file on your **remote Linux server** for the user Jenkins will connect as (e.g., `ec2-user`, `ubuntu`).
    *   The **private key** (e.g., `~/.ssh/id_rsa`) will be stored securely in Jenkins.
-   **GitHub Account and Fork:** Your forked `cicd-labs` repository. The `Jenkinsfile` and sample artifact for this lab are within `Jenkins/LAB10-SSH-Remote-Deploy/`.

---

## 📂 Folder Structure for This Lab

```bash
Jenkins/LAB10-SSH-Remote-Deploy/
├── README.md       # Lab overview, objectives, setup, TODOs (this file)
├── Jenkinsfile     # Declarative Pipeline script for SSH deployment (contains TODOs)
├── solutions.md    # Contains the completed Jenkinsfile and configuration recap
└── app/
    └── artifact.txt # A simple text file to be "deployed"
```

---

## 🔌 Step 1: Install "SSH Agent" Plugin in Jenkins

This plugin allows your pipeline to use SSH credentials (like private keys) securely.

1.  Go to your Jenkins Dashboard.
2.  Click **Manage Jenkins** -> **Plugins** (or **Manage Plugins**).
3.  Go to the **Available plugins** tab.
4.  In the search bar, type `SSH Agent`.
5.  Select the checkbox next to the "SSH Agent" plugin.
6.  Click **"Install without restart"** or **"Download now and install after restart"**.

---

## 🔐 Step 2: Add SSH Credential to Jenkins

You'll store the private key part of your SSH key pair in Jenkins.

1.  In Jenkins, go to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials (unrestricted)**.
2.  Click **"Add Credentials"** on the left sidebar.
3.  Configure the credential as follows:
    *   **Kind:** Select `SSH Username with private key`.
    *   **Scope:** Keep it as `Global`.
    *   **ID:** `lab10-remote-ssh-key` (This ID will be used in your `Jenkinsfile`).
    *   **Description:** (Optional but recommended) `SSH key for Lab 10 remote deployment server`.
    *   **Username:** Enter the username you will use to connect to your remote server (e.g., `ec2-user`, `ubuntu`, the user whose `authorized_keys` file has your public key).
    *   **Private Key:**
        *   Select **"Enter directly"**.
        *   In the **Key** text box, paste the entire content of your **SSH private key file** (e.g., the content of `~/.ssh/id_rsa`). This includes the `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----` lines.
    *   **Passphrase:** If your private key is encrypted with a passphrase, enter it here. If not, leave it blank.
4.  Click **"Create"**.

---

## 🚀 Lab Steps: Configuring the `Jenkinsfile` for SSH Deployment

Your task is to complete the `Jenkins/LAB10-SSH-Remote-Deploy/Jenkinsfile`.

**1. Locate and Open `Jenkinsfile`:**
   Open `Jenkins/LAB10-SSH-Remote-Deploy/Jenkinsfile` in your local clone of your forked repository.

**2. Complete the `TODO` items in `Jenkinsfile`:**

   *   **`TODO_ENV_VARS` (Environment Block):**
        *   **Goal:** Define essential variables for your remote server connection.
        *   **Action:** Update the placeholder values for `REMOTE_USER`, `REMOTE_HOST`, and `REMOTE_BASE_PATH` with your actual remote server's username, IP address (or hostname), and a base path where you want to deploy files (e.g., `/tmp/jenkins-deployments`).
            ```groovy
            environment {
                REMOTE_USER = 'your-actual-remote-user'
                REMOTE_HOST = 'your-actual-remote-ip-or-hostname'
                REMOTE_BASE_PATH = '/tmp/my-app-deployments' // Or any path you have write access to
                ARTIFACT_PATH = 'Jenkins/LAB10-SSH-Remote-Deploy/app/artifact.txt'
            }
            ```

   *   **Stage: 'Prepare Deployment Directory on Remote'**
        *   **`TODO_SSH_AGENT_WRAPPER_PREPARE`:**
            *   **Goal:** Wrap the shell command with `sshagent` to make your SSH credential (`lab10-remote-ssh-key`) available.
            *   **Action:** Enclose the `sh` command within an `sshagent(['lab10-remote-ssh-key']) { ... }` block.
        *   **`TODO_MKDIR_COMMAND`:**
            *   **Goal:** Create a unique deployment directory on the remote server for the current build.
            *   **Action:** Write an `sh` command that uses `ssh` to execute `mkdir -p` on the remote server. The directory path should be `${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}`.
                ```groovy
                sshagent(['lab10-remote-ssh-key']) {
                    sh "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'mkdir -p ${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}'"
                }
                ```
                *   *Note: `-o StrictHostKeyChecking=no` is used here for lab simplicity to avoid host key verification prompts. In production, manage known hosts properly.* 

   *   **Stage: 'Deploy Artifact via SCP'**
        *   **`TODO_SSH_AGENT_WRAPPER_DEPLOY`:**
            *   **Goal:** Wrap the `scp` command with `sshagent`.
            *   **Action:** Similar to the prepare stage, use `sshagent(['lab10-remote-ssh-key']) { ... }`.
        *   **`TODO_SCP_COMMAND`:**
            *   **Goal:** Copy `artifact.txt` from the Jenkins workspace to the newly created remote directory.
            *   **Action:** Write an `sh` command that uses `scp` to transfer the file specified by `ARTIFACT_PATH` to `${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}/artifact.txt`.
                ```groovy
                sshagent(['lab10-remote-ssh-key']) {
                    sh "scp -o StrictHostKeyChecking=no ${ARTIFACT_PATH} ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}/artifact.txt"
                }
                ```

   *   **Stage: 'Verify Deployment on Remote'**
        *   **`TODO_SSH_AGENT_WRAPPER_VERIFY`:** Wrap with `sshagent`.
        *   **`TODO_LS_COMMAND`:**
            *   **Goal:** List files in the remote deployment directory to confirm `artifact.txt` is present.
            *   **Action:** `sh "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'ls -la ${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}'"`
        *   **`TODO_CAT_COMMAND` (Optional):**
            *   **Goal:** Display the content of the deployed `artifact.txt` from the remote server.
            *   **Action:** `sh "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'cat ${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}/artifact.txt'"`

   *   **`post { always { ... } }` block:**
        *   **`TODO_CLEANUP_REMOTE` (Optional):**
            *   **Goal:** Remove the deployment directory from the remote server after the build.
            *   **Action:** (Use with caution!) Inside an `sshagent` block, use `sh "ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_HOST} 'rm -rf ${REMOTE_BASE_PATH}/${env.JOB_NAME}/${env.BUILD_NUMBER}'"`.

**3. Commit and Push `Jenkinsfile` Changes:**
   Save your completed `Jenkinsfile`, then commit and push it to your forked GitHub repository.

**4. Configure and Run Jenkins Pipeline Job:**
   *   Create a new "Pipeline" job in Jenkins (e.g., `lab10-ssh-deploy-pipeline`).
   *   Configure it for "Pipeline script from SCM," pointing to your forked repository and `Jenkins/LAB10-SSH-Remote-Deploy/Jenkinsfile`.
   *   Save and click **"Build Now"**.

---

## ✅ Validation Checklist

- [ ] "SSH Agent" plugin is installed in Jenkins.
- [ ] An SSH credential (e.g., ID `lab10-remote-ssh-key`) with your remote server username and private key is correctly configured in Jenkins.
- [ ] Your remote server is accessible from Jenkins, and your public key is in the correct user's `~/.ssh/authorized_keys` file on the server.
- [ ] The `Jenkinsfile` environment variables (`REMOTE_USER`, `REMOTE_HOST`, `REMOTE_BASE_PATH`) are correctly set for your server.
- [ ] The pipeline job completes successfully.
- [ ] The console output shows successful execution of `mkdir` on the remote server.
- [ ] The console output shows successful execution of `scp`, transferring `artifact.txt`.
- [ ] The console output for the `ls` command shows `artifact.txt` in the remote deployment directory.
- [ ] (If `cat` command added) The console output shows the content of `artifact.txt` from the remote server.
- [ ] (If cleanup added) The remote deployment directory is removed after the pipeline finishes.

---

## 🧹 Cleanup

1.  **Jenkins Job:** Delete the `lab10-ssh-deploy-pipeline` job.
2.  **Jenkins Credential:** Delete the `lab10-remote-ssh-key` credential.
3.  **Remote Server:**
    *   Manually delete any deployment directories created under `REMOTE_BASE_PATH` if the pipeline cleanup didn't run or wasn't configured.
    *   Remove the public key from `~/.ssh/authorized_keys` on the remote server if it was only for this lab.
4.  **SSH Agent Plugin:** Can be left installed, it's generally useful.

---

## 🧠 Key Concepts

-   **SSH (Secure Shell):** A protocol for secure remote login and other secure network services over an insecure network.
-   **SSH Key Pair Authentication:** A more secure method than password authentication, using a private key (kept secret) and a public key (shared with servers).
-   **`ssh-keygen`:** A tool to create SSH key pairs.
-   **`authorized_keys`:** A file on an SSH server (`~/.ssh/authorized_keys`) that lists the public keys permitted to log in to a user account.
-   **SSH Agent Plugin (Jenkins):** Provides the `sshagent` wrapper, which allows pipelines to authenticate with SSH servers using credentials stored in Jenkins.
-   **`sshagent(['credential-id']) { ... }`:** A pipeline step that makes the specified SSH credential available for SSH-based commands executed within its block.
-   **`scp` (Secure Copy):** A command-line utility that allows you to securely copy files and directories between two locations, typically using SSH.
-   **`-o StrictHostKeyChecking=no`:** An SSH client option to disable strict host key checking. **Warning:** This bypasses a security feature that protects against man-in-the-middle attacks. It's used in labs for convenience but should be handled properly in production (e.g., by pre-populating `known_hosts` or using other verification methods).

---

## 🎉 Congratulations on Completing the Jenkins Track!

You've journeyed through building, testing, containerizing (with Docker), and deploying applications and artifacts using Jenkins, incorporating various modern CI/CD practices. You've covered freestyle jobs, declarative pipelines, shared libraries, credential management, notifications, and now remote deployments via SSH.

From here, you can explore other CI/CD tools and concepts. Consider diving into:
-   **The Docker-CD Track:** For deeper dives into containerization and Docker-centric CI/CD pipelines.
-   **The ArgoCD Track:** To learn about GitOps principles and continuous delivery to Kubernetes using ArgoCD.

Keep building, keep automating, and keep learning!

