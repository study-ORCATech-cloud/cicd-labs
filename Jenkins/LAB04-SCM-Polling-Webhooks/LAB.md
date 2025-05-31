# Lab Steps: Configuring SCM Polling and GitHub Webhooks

This lab will guide you through setting up two different methods to automatically trigger your Jenkins pipeline (the one created in Lab 03, e.g., `python-declarative-pipeline`) when changes are pushed to your forked GitHub repository.

**Important:** You will typically use *either* SCM Polling *or* a Webhook for a given job, not both simultaneously for the same purpose. This lab covers both so you understand each method. For actual projects, Webhooks are generally preferred if Jenkins is accessible from GitHub.

---

## Part 1: Configure SCM Polling

SCM Polling makes Jenkins check your repository for changes on a defined schedule.

**Steps:**

1.  **Navigate to Your Jenkins Pipeline Job:**
    *   Open your Jenkins dashboard.
    *   Find the pipeline job you created in Lab 03 (e.g., `python-declarative-pipeline`). Click on its name.

2.  **Open Job Configuration:**
    *   On the job's page, click on **"Configure"** in the left-hand menu.

3.  **Locate Build Triggers Section:**
    *   Scroll down the configuration page until you find the **"Build Triggers"** section.

4.  **Enable Poll SCM:**
    *   Check the box next to **"Poll SCM"**.

5.  **Define Polling Schedule:**
    *   A text box labeled **"Schedule"** will appear. This uses a cron-like syntax.
    *   The format is `MINUTE HOUR DOM MONTH DOW` (DayOfMonth, DayOfWeek).
    *   `H` can be used to mean "hash" or spread load evenly. For example, `H/2 * * * *` means "poll approximately every two minutes."
    *   **Enter the following schedule to poll every two minutes (for testing purposes):**
        ```cron
        H/2 * * * *
        ```
        *   **Explanation of `H/2 * * * *`:**
            *   `H/2`: Jenkins will pick a minute value (0-59) based on a hash of the job name and divide it by 2, effectively meaning "at some consistent minute within every 2-minute interval." This helps distribute polling load if you have many jobs.
            *   `*` (for HOUR, DOM, MONTH, DOW): Means "every" hour, "every" day of the month, "every" month, "every" day of the week.

6.  **Save Configuration:**
    *   Scroll to the bottom of the page and click **"Save"**.

7.  **Test SCM Polling:**
    *   Open your local clone of your forked `cicd-labs` repository.
    *   Make a small, noticeable change to any file within the `Jenkins/LAB03-Declarative-Pipeline/app/` directory (e.g., modify the print statement in `main.py`). You can also just add a comment.
        ```bash
        # Example: Modify Jenkins/LAB03-Declarative-Pipeline/app/main.py
        # Change:
        # print(greet("Student"))
        # To:
        # print(greet("Student via SCM Polling"))
        ```
    *   Commit and push this change to your forked repository (ensure you're on the branch your Jenkins job is monitoring, likely `main` or `master`).
        ```bash
        git add Jenkins/LAB03-Declarative-Pipeline/app/main.py
        git commit -m "Test SCM polling trigger for Lab 04"
        git push
        ```
    *   **Wait:** Go back to your Jenkins job page. Within the next couple of minutes (due to the `H/2` schedule), a new build should automatically start.
    *   **Observe:** You should see a new build appear in the "Build History." Click on it and check the "Console Output" to verify it ran your pipeline with the new change. Look for "SCM change detected" or similar in the logs.

8.  **Disable SCM Polling (Before Proceeding to Webhooks):**
    *   Once you've confirmed polling works, go back to the job's **"Configure"** page.
    *   Uncheck **"Poll SCM"** under "Build Triggers."
    *   Click **"Save"**. This is to prevent polling from interfering while you test webhooks.

---

## Part 2: Configure GitHub Webhook (Recommended Method)

Webhooks are more efficient as GitHub instantly notifies Jenkins when a push occurs.

**Prerequisite: Jenkins Accessibility**

*   For GitHub webhooks to work, your Jenkins instance must be accessible from the internet.
*   If Jenkins is running on your local machine (e.g., `http://localhost:8080`), GitHub cannot reach it directly.
*   **Solution: Use `ngrok` (or a similar tunneling service).**

**Using `ngrok` (if Jenkins is local):**

1.  **Download and Install `ngrok`:**
    *   Go to [https://ngrok.com/download](https://ngrok.com/download) and download the version for your OS.
    *   Follow their installation instructions (usually just unzipping and placing the executable in your PATH).
    *   You may need to sign up for a free `ngrok` account and authenticate your agent using `ngrok config add-authtoken YOUR_AUTH_TOKEN`.

2.  **Start `ngrok` Tunnel:**
    *   Open a new terminal or command prompt.
    *   If your Jenkins is running on `http://localhost:8080`, run the command:
        ```bash
        ngrok http 8080
        ```
    *   `ngrok` will start and display a public URL (e.g., `https://<random_string>.ngrok-free.app`). This URL now forwards to your local Jenkins.
    *   **Note down this public "Forwarding" URL (the `https://...` one). You will use it as `<your-public-jenkins-url>` below.**
    *   Keep this `ngrok` terminal window open while you are testing webhooks. Closing it will stop the tunnel.

**Steps to Configure GitHub Webhook:**

1.  **Navigate to Your Jenkins Pipeline Job Configuration:**
    *   Go to your Jenkins job (e.g., `python-declarative-pipeline`) -> **"Configure"**.

2.  **Enable GitHub Hook Trigger:**
    *   In the **"Build Triggers"** section, check the box next to **"GitHub hook trigger for GITScm polling"**.
        *   *Note: Despite the name "GITScm polling" in the option, this enables Jenkins to listen for a webhook. It doesn't actively poll when this specific option is used in conjunction with a GitHub webhook.*

3.  **Save Jenkins Configuration:**
    *   Click **"Save"**.

4.  **Go to Your GitHub Repository Settings:**
    *   Open your forked `cicd-labs` repository on GitHub.
    *   Click on the **"Settings"** tab for the repository.

5.  **Navigate to Webhooks:**
    *   In the left sidebar, click on **"Webhooks"**.

6.  **Add a New Webhook:**
    *   Click the **"Add webhook"** button. You might be asked to confirm your GitHub password.

7.  **Configure the Webhook:**
    *   **Payload URL:**
        *   This is the URL on your Jenkins instance that GitHub will send notifications to.
        *   The standard URL is `http://<your-jenkins-url>/github-webhook/`.
        *   **If using `ngrok`:** Replace `<your-jenkins-url>` with your `ngrok` public forwarding URL (e.g., `https://<random_string>.ngrok-free.app/github-webhook/`).
        *   **If Jenkins is publicly accessible:** Use your actual public Jenkins URL (e.g., `http://your-jenkins.example.com/github-webhook/`).
        *   **Important:** Ensure the URL ends with a trailing slash `/`.
    *   **Content type:**
        *   Select `application/json` from the dropdown.
    *   **Secret:**
        *   (Optional but Recommended for security) You can set a secret token here. Jenkins can be configured to verify this secret to ensure payloads are from GitHub. For this beginner lab, we'll skip setting a secret, but be aware of this for production setups.
    *   **Which events would you like to trigger this webhook?**
        *   Select **"Just the push event."** This is usually sufficient for CI.
    *   **Active:**
        *   Ensure this checkbox is checked.

8.  **Save the Webhook:**
    *   Click the **"Add webhook"** button at the bottom of the page.

9.  **Verify Webhook Delivery (Optional but Recommended):**
    *   After adding the webhook, GitHub will usually send a "ping" event to your Jenkins.
    *   In GitHub, on the Webhooks page, click on your newly created webhook (or the "Edit" button next to it).
    *   Scroll down to the **"Recent Deliveries"** section. You should see a delivery attempt.
    *   A green checkmark indicates success. A red X indicates failure.
    *   If it failed, click on the delivery attempt to see the "Request" and "Response" details, which can help troubleshoot (e.g., incorrect ngrok URL, Jenkins not running, firewall issues).

10. **Test the GitHub Webhook:**
    *   Go back to your local clone of your forked `cicd-labs` repository.
    *   Make another small, noticeable change to a file (e.g., `Jenkins/LAB03-Declarative-Pipeline/app/main.py`).
        ```bash
        # Example: Modify Jenkins/LAB03-Declarative-Pipeline/app/main.py
        # Change:
        # print(greet("Student via SCM Polling"))
        # To:
        # print(greet("Student via GitHub Webhook"))
        ```
    *   Commit and push this change to your forked repository.
        ```bash
        git add Jenkins/LAB03-Declarative-Pipeline/app/main.py
        git commit -m "Test GitHub webhook trigger for Lab 04"
        git push
        ```
    *   **Observe Jenkins:** Almost immediately after the push completes, a new build should start in your Jenkins job.
    *   Check the "Build History" and "Console Output" to verify the pipeline ran with your latest change.

---

## Troubleshooting Tips

*   **SCM Polling Not Triggering:**
    *   Double-check the cron schedule in Jenkins.
    *   Ensure the Jenkins job is configured to monitor the correct branch of your repository.
    *   Check the "Poll SCM Log" for your job in Jenkins (usually accessible from the job's main page) for any errors.
*   **Webhook Not Triggering / Red X in GitHub Deliveries:**
    *   **Jenkins URL:** Is the Payload URL correct in GitHub? If using `ngrok`, did you use the `https` forwarding URL? Does it end with `/github-webhook/`?
    *   **`ngrok` Running:** Is your `ngrok` tunnel still active in its terminal window?
    *   **Jenkins Running:** Is your Jenkins server actually running?
    *   **Firewall:** If Jenkins is on a server, could a firewall be blocking incoming requests from GitHub?
    *   **Jenkins "GitHub hook trigger" Enabled:** Did you check the "GitHub hook trigger for GITScm polling" box in the Jenkins job configuration?
    *   **GitHub Plugin:** Ensure the "GitHub Integration Plugin" (or similar, usually installed by default) is installed and enabled in Jenkins (`Manage Jenkins` -> `Plugins` -> `Installed plugins`).
*   **Builds Triggered by Both Polling and Webhook (if you forgot to disable one):**
    *   This can happen if you accidentally leave both enabled. Simply go back to the Jenkins job configuration and disable the one you are not currently testing.

---

You have now successfully configured and tested both SCM polling and GitHub webhooks for triggering your Jenkins pipeline! Remember to perform the cleanup steps mentioned in the `README.md`. 