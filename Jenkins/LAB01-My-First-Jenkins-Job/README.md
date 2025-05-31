# LAB01: My First Jenkins Job - Freestyle 'Hello World'

Welcome to your first truly interactive Jenkins lab! Now that you have a Jenkins instance up and running (as per the `Jenkins/install-and-setup.md` guide), it's time to create and run your very first Jenkins job. We'll start with a simple "Freestyle project" that executes a basic shell command.

This lab will familiarize you with the fundamental process of job creation, configuration, execution, and output inspection in Jenkins.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Navigate the Jenkins UI to create a new "Freestyle project."
- Configure a simple build step, specifically an "Execute shell" command.
- Manually trigger a build for your new job.
- Locate and understand the console output of a completed build.
- Understand the concept of a Jenkins job and its basic lifecycle.

---

## 🧰 Prerequisites

-   **Jenkins Installed and Running:** You must have a working Jenkins instance accessible via your browser. If you haven't set this up yet, please follow the **`../../install-and-setup.md`** guide in the `Jenkins` parent directory.
-   Access to Jenkins as an admin user (created during the initial setup).

---

## 🗂️ Folder Structure

This lab primarily involves interaction with the Jenkins User Interface. The files in this directory are for your reference and guidance:

```bash
Jenkins/LAB01-My-First-Jenkins-Job/
├── README.md     # Overview, objectives, prerequisites, validation, etc. (this file)
└── LAB.md        # Detailed step-by-step instructions to perform the lab
```

All actions for this lab are performed directly in the Jenkins UI. Please refer to **`LAB.md`** for the detailed instructions.

---

## 🚀 Lab Steps

Please refer to the **`LAB.md`** file in this directory for detailed step-by-step instructions on how to complete this lab.

---

## ✅ Validation Checklist

- [ ] You were able to create a new Freestyle project named `hello-world-freestyle` (as per `LAB.md`).
- [ ] You successfully added an "Execute shell" (or "Execute Windows batch command") build step with the specified `echo` commands (as per `LAB.md`).
- [ ] The job was saved without errors.
- [ ] You triggered the job manually using "Build Now."
- [ ] The build completed successfully (e.g., blue or green status icon).
- [ ] You found and opened the "Console Output" for the build.
- [ ] The console output shows your custom `echo` messages and a "Finished: SUCCESS" status.

---

## 🧹 Cleanup

To keep your Jenkins instance tidy, you can delete the job you created (instructions in `LAB.md` or follow these):

1.  Navigate to the dashboard of your Jenkins instance.
2.  Click on the job name (`hello-world-freestyle`).
3.  In the left-hand menu of the job page, click on **"Delete Project"**.
4.  Confirm by clicking **"Yes"**.

---

## 🧠 Key Concepts

-   **Freestyle Project:** A versatile type of Jenkins job that allows you to configure build steps for various tasks. It's a good starting point for simple automations.
-   **Build Step:** An individual action performed during a build (e.g., executing a shell script, running a Maven command, etc.).
-   **Execute Shell / Execute Windows Batch Command:** Common build steps for running command-line instructions.
-   **Build Trigger:** The event or condition that starts a build (in this lab, it was a manual trigger: "Build Now").
-   **Console Output:** A detailed log of everything that happens during a build, including commands executed, their output, and status messages. Essential for troubleshooting.
-   **Build History:** A record of all the times a job has been run.
-   **Workspace:** A directory on the Jenkins controller (or agent) where a job checks out source code and performs its build operations.

---

## 🔁 What's Next?

Now that you've mastered creating a basic Freestyle job, you're ready for more complex tasks.

Proceed to **[../LAB02-Freestyle-Python-Job/README.md](../LAB02-Freestyle-Python-Job/)** to learn how to configure a Jenkins job to run a Python script and manage source code. 