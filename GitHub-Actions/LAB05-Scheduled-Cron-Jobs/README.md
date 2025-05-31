# LAB05 - Scheduled Jobs & Cron Triggers (GitHub Actions)

This lab demonstrates how to schedule GitHub Actions workflows to run automatically at specified time intervals using `cron` syntax. This is extremely useful for automating routine tasks such as nightly reports, weekly data backups, or periodic system health checks.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand and use the `on.schedule` event to trigger workflows based on time.
- Write and interpret `cron` expressions to define specific schedules.
- Create a workflow that executes a simple task (like printing a message and timestamp) on a recurring schedule.
- Utilize `workflow_dispatch` for manually triggering and testing scheduled workflows.
- Find and verify scheduled job executions in the GitHub Actions UI.

---

## 🧰 Prerequisites

- A GitHub account and a repository for this lab.
- Basic familiarity with YAML syntax.
- A conceptual understanding of what cron jobs are (prior detailed cron expertise is not required, as we will cover the basics).

---

## 🗂️ Folder Structure

Your lab directory is set up with the following structure. The focus is solely on the workflow file.

```bash
GitHub-Actions/LAB05-Scheduled-Cron-Jobs/
├── .github/
│   └── workflows/
│       └── scheduled-task.yml  # Your partially completed workflow file with TODOs
├── README.md                 # Lab instructions (this file)
└── solutions.md              # Solutions for scheduled-task.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB05-Scheduled-Cron-Jobs/` directory.

2.  **Understand Cron Syntax (Brief Overview):**
    A cron expression is a string of five fields (or sometimes six) that represent a time schedule. The five standard fields are:
    ```
    ┌───────────── minute (0 - 59)
    │ ┌───────────── hour (0 - 23)  -- Based on UTC time on GitHub Actions
    │ │ ┌───────────── day of the month (1 - 31)
    │ │ │ ┌───────────── month (1 - 12)
    │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday; some systems use 7 for Sunday)
    * * * * *
    ```
    *   `*` means "any value" or "every".
    *   Example: `0 * * * *` means "at minute 0 of every hour" (i.e., hourly on the hour).
    *   Example: `0 9 * * 1` means "at 09:00 AM UTC on every Monday".
    *   For help generating cron expressions, a great tool is [crontab.guru](https://crontab.guru/).

3.  **Complete the GitHub Actions Workflow (`.github/workflows/scheduled-task.yml`):**
    Open `.github/workflows/scheduled-task.yml`. This file has `TODO` comments for you to complete:
    *   **Define the Schedule:**
        *   Under `on.schedule:`, uncomment the `- cron:` line.
        *   Provide a valid cron expression inside the quotes. For testing, you might initially set it to run frequently (e.g., `*/15 * * * *` for every 15 minutes), but be mindful of GitHub Actions usage. For a less frequent schedule, try something like `0 */2 * * *` (every 2 hours on the hour) or `0 8 * * *` (at 8 AM UTC daily).
        *   **Remember:** GitHub Actions uses UTC for cron schedules.
    *   **Specify Runner OS:** Set `runs-on:` to `ubuntu-latest` (or your preferred OS).
    *   **Write the Script:** In the `run:` block for the step, write a few `echo` commands:
        *   One to print a friendly greeting.
        *   Another to print the current date and time in UTC (use `date -u`).

4.  **Commit and Push Your Changes:**
    ```bash
    git add .github/workflows/scheduled-task.yml
    git commit -m "feat: Implement scheduled greeting workflow for LAB05"
    git push origin main
    ```

5.  **Verify Workflow Execution:**
    *   **Manual Trigger (Optional but Recommended for Testing):** Go to your GitHub repository's "Actions" tab. Select the "Scheduled Greeting" workflow from the list on the left. You should see a "Run workflow" button (because we included `workflow_dispatch`). Click it to trigger the job manually and check if your script works as expected.
    *   **Scheduled Trigger:** Wait for the time defined in your cron schedule to pass. Then, check the "Actions" tab. You should see a new workflow run triggered by the schedule.
    *   Inspect the logs for the `greet` job. Verify that your echo commands ran and the timestamp is correct (and in UTC).

---

## ✅ Validation Checklist

- [ ] The `.github/workflows/scheduled-task.yml` file is correctly completed with a valid cron schedule and script.
- [ ] The workflow can be triggered manually using `workflow_dispatch` (if enabled).
- [ ] The workflow automatically triggers according to the cron schedule you defined (allow for slight delays by GitHub Actions).
- [ ] The workflow logs show the correct greeting message and the current UTC timestamp when the job ran.
- [ ] You understand how to use [crontab.guru](https://crontab.guru/) or similar tools to create cron expressions.
- [ ] You are aware that GitHub Actions schedules are in UTC.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains a sample solution for `scheduled-task.yml` with explanations.

---

## 🧹 Cleanup

-   To stop the scheduled task from running automatically, you can either:
    *   Delete the `.github/workflows/scheduled-task.yml` file from your repository.
    *   Or, comment out or remove the `schedule:` block within the workflow file.
-   Commit and push any changes made for cleanup.

---

## 🧠 Key Concepts

-   **`on.schedule`:** The GitHub Actions event trigger used for cron-based scheduling.
-   **`cron` syntax:** A standard way to define time-based job schedules.
-   **UTC (Coordinated Universal Time):** The time standard used by GitHub Actions for its schedulers. You must account for this if you need jobs to run at specific local times.
-   **`workflow_dispatch`:** An event trigger that allows a workflow to be run manually from the GitHub UI, useful for testing.
-   **Idempotency:** While not strictly enforced in this simple lab, when designing real-world scheduled tasks, consider making them idempotent (i.e., running them multiple times should not have unintended side effects).

---

## 🌟 Well Done!

You've learned how to harness the power of time by scheduling your GitHub Actions workflows! This is a key automation technique for many operational tasks.

---

## 🔁 What's Next?
Move on to [LAB06 - Secrets and Contexts](../LAB06-Secrets-And-Contexts/) to secure workflows and access runtime variables.

Automate on time — every time. 🕒📈🔁

