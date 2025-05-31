# LAB01: Step-by-Step Instructions - My First Jenkins Job

This document provides the detailed steps to complete LAB01. Follow these instructions carefully in your Jenkins User Interface.

---

## 🚀 Creating Your First Freestyle Job

1.  **Navigate to the Jenkins Dashboard:**
    *   Open your browser and go to your Jenkins URL (e.g., `http://localhost:8080`).
    *   Log in with the admin user you created during setup.

2.  **Create a New Item (Job):**
    *   On the Jenkins dashboard, click on **"New Item"** in the left-hand navigation menu.
    *   **Enter an item name:** Type `hello-world-freestyle` (or a similar descriptive name).
    *   **Select project type:** Click on **"Freestyle project"** from the list of options.
    *   Click the **"OK"** button at the bottom of the page.

3.  **Configure the Job:**
    You will be redirected to the job configuration page. Let's keep it simple for this first job.
    *   **(Optional) Description:** You can add a brief description for your job, like "My first Jenkins Freestyle project to print Hello World."
    *   **Scroll down to the "Build Steps" section.** (Prior to Jenkins 2.414, this section was called "Build").
    *   Click the **"Add build step"** dropdown button.
    *   Select **"Execute shell"** from the dropdown menu. (If you are running Jenkins controller on Windows, you would select **"Execute Windows batch command"** and use a command like `echo "Hello Jenkins from my first Freestyle job!"`)

4.  **Add a Shell Command:**
    *   A text box will appear for the shell command.
    *   In the **"Command"** text area, type the following simple shell command:
        ```bash
        echo "Hello Jenkins from my first Freestyle job!"
        echo "Today is: $(date)"
        ```
        *This command will print two lines to the console output.*
        *(If using "Execute Windows batch command", use:*
        ```batch
        echo "Hello Jenkins from my first Freestyle job!"
        echo Today is: %date% %time%
        ```
        *)*

5.  **Save the Job Configuration:**
    *   Scroll to the bottom of the configuration page.
    *   Click the **"Save"** button.

6.  **Manually Trigger a Build:**
    *   After saving, you'll be taken to the job's main page for `hello-world-freestyle`.
    *   In the left-hand navigation menu for this job, click on **"Build Now"**.
    *   You will see a new build appear in the **"Build History"** section (usually at the bottom left of the job page), marked as `#1`.

7.  **Inspect the Console Output:**
    *   Wait for the build to complete (it should be very quick). A successfully completed build will typically show a blue ball icon 🔵 (or green for some themes).
    *   Click on the build number (e.g., `#1`) in the "Build History."
    *   On the build-specific page, click on **"Console Output"** in the left-hand menu.

8.  **Verify the Output:**
    *   The Console Output page will show the logs of your build. You should see something similar to (for Linux/macOS):
        ```text
        Started by user YourAdminUserName
        Running as SYSTEM
        Building in workspace /var/jenkins_home/workspace/hello-world-freestyle  (or a different path depending on your Jenkins setup)
        [hello-world-freestyle] $ /bin/sh -xe /tmp/jenkins1234567890.sh
        + echo 'Hello Jenkins from my first Freestyle job!'
        Hello Jenkins from my first Freestyle job!
        + echo 'Today is: Tue Jan 30 10:00:00 UTC 2024' (Your date will vary)
        Today is: Tue Jan 30 10:00:00 UTC 2024 (Your date will vary)
        Finished: SUCCESS
        ```
    *   Confirm that your `echo` messages are present and the build status is `Finished: SUCCESS`.

Congratulations! You've successfully created, configured, run, and inspected your first Jenkins job.

---

Refer back to the `README.md` for objectives, validation, cleanup, and key concepts related to this lab. 