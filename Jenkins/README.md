# Jenkins CI/CD Labs

Welcome to the **Jenkins** section of the **CI/CD Automation Labs**. These hands-on labs are designed to teach you how to configure and build powerful CI/CD pipelines using Jenkins — one of the most widely used open-source automation servers.

---

## 🛠️ Setting Up Jenkins: Before You Begin

**Crucial First Step:** Before diving into the labs below, you **must** have a working Jenkins instance. 

Please follow our detailed installation guide:
➡️ **[Jenkins Installation and Initial Setup Guide](./install-and-setup.md)**

This guide covers:
- Installing Jenkins using Docker (recommended for these labs).
- Alternative native installation.
- Initial Jenkins setup (unlocking, plugin installation, admin user creation).

Once your Jenkins server is up and running, you're ready to start with LAB01!

---

## 🚀 What You'll Learn in These Labs

- Configure various Jenkins job types, starting with Freestyle projects and progressing to powerful Pipeline jobs.
- Utilize `Jenkinsfile` (both Declarative and Scripted) to define build-as-code pipelines.
- Integrate Jenkins with Source Code Management (SCM) like Git, including webhooks and SCM polling.
- Build and manage Docker images within Jenkins pipelines.
- Implement parallel execution and conditional logic in your pipelines.
- Leverage Jenkins Shared Libraries to create reusable pipeline code.
- Securely manage credentials and secrets within Jenkins.
- Set up notifications (e.g., Slack) for build statuses.
- Automate deployments to remote servers using SSH.
- Understand core Jenkins concepts like agents, workspaces, plugins, and job configurations.

---

## 📁 Lab Structure

The labs are designed to be followed in sequence, building upon concepts from previous labs.

```bash
Jenkins/
├── install-and-setup.md            # <-- START HERE: Jenkins Setup Guide
├── LAB01-My-First-Jenkins-Job/     # Your first interactive job in Jenkins
├── LAB02-Freestyle-Python-Job/     # Running Python scripts, SCM basics
├── LAB03-Declarative-Pipeline/     # Introduction to Jenkinsfile (Declarative)
├── LAB04-SCM-Polling-Webhooks/     # Automated triggers for pipelines
├── LAB05-Docker-Image-Build/       # Building Docker images with Jenkins
├── LAB06-Parallel-And-Conditional/ # Advanced pipeline syntax
├── LAB07-Shared-Libraries/         # Reusable pipeline code
├── LAB08-Secure-Credentials/       # Managing secrets in Jenkins
├── LAB09-Slack-Notifications/      # Integrating notifications
└── LAB10-SSH-Remote-Deploy/        # Deploying applications via SSH
```

Each lab directory (`LABxx-*`) typically contains:
- `README.md`: Detailed instructions, objectives, and validation steps.
- `LAB.md`: Step-by-step procedures for hands-on Jenkins configuration and pipeline development.
- Complete, working configuration files (e.g., `Jenkinsfile`) ready to copy and use.
- **Copy-and-Learn Methodology**: All configurations are production-ready - students copy them and learn by following detailed instructions.
- Supporting files (e.g., Python scripts, `Dockerfile`) as needed for the lab.

---

## 🧠 Prerequisites for the Labs

(Assuming Jenkins is installed as per the guide above)

-   Basic understanding of Continuous Integration (CI) and Continuous Delivery (CD) concepts.
-   Familiarity with basic Git commands and using GitHub (or a similar Git platform) for SCM.
-   Basic Linux shell scripting knowledge will be helpful for many labs.
-   Docker knowledge is beneficial, especially for labs involving Docker image builds (e.g., LAB05).
-   A GitHub account for SCM integration labs.

---

## 💬 Contributing

If you find errors, have suggestions for improvements, or would like to contribute a new lab:
1.  Fork the main `cicd-labs` repository.
2.  Create a branch for your changes/additions.
3.  Follow the lab naming pattern (`LABxx-Descriptive-Name`).
4.  Ensure your lab includes a clear `README.md`, detailed `LAB.md` instructions, and complete working configurations.
5.  Open a Pull Request back to the original repository with a clear description of your contribution.

---

**Learn Jenkins. Automate everything. Deliver with confidence.** ⚙️📦🚀

