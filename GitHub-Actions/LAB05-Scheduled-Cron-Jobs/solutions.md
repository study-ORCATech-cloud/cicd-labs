# Solutions for LAB05 - Scheduled Jobs & Cron Triggers

This file contains the solutions for the `TODO` items in the `.github/workflows/scheduled-task.yml` workflow file.

---

## `scheduled-task.yml` Solutions

```yaml
name: Scheduled Greeting

on:
  schedule:
    # Example: Runs at 02:00 AM UTC every day
    - cron: '0 2 * * *'

  # Optional: Allow manual triggering for easier testing
  workflow_dispatch:

jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
      - name: Print a greeting and the current time
        run: |
          echo "👋 Hello! This is a scheduled greeting from your GitHub Actions workflow."
          echo "🌍 The current Coordinated Universal Time (UTC) is: $(date -u)"
          echo "💡 This job was triggered by the cron schedule or a manual dispatch."
```

---

### Explanation (`scheduled-task.yml`):

1.  **Trigger Configuration (`on`):**
    *   **`schedule:`**: This keyword is used to define scheduled triggers.
        *   **`- cron: '0 2 * * *'`**: This is a cron expression.
            *   The expression `'0 2 * * *'` means the workflow will run at 2:00 AM UTC every day.
            *   **Cron Syntax Breakdown:**
                *   `0`: Minute (0-59)
                *   `2`: Hour (0-23, in UTC)
                *   `*`: Day of the month (1-31)
                *   `*`: Month (1-12)
                *   `*`: Day of the week (0-7, where both 0 and 7 represent Sunday)
            *   An asterisk (`*`) means "any value".
    *   **`workflow_dispatch:`**: This allows the workflow to be manually triggered from the GitHub Actions UI (under the "Actions" tab, select the workflow, and click "Run workflow"). This is very useful for testing scheduled workflows without waiting for the actual schedule.

2.  **Job: `greet` (`jobs.greet`):**
    *   **Runner OS (`runs-on`):**
        *   `runs-on: ubuntu-latest`: The job runs on the latest Ubuntu runner.
    *   **Steps (`steps`):**
        1.  **`Print a greeting and the current time`**: This step executes a multi-line shell script.
            *   `echo "👋 Hello! ..."`: Prints a friendly greeting message.
            *   `echo "🌍 The current Coordinated Universal Time (UTC) is: $(date -u)"`: Prints the current date and time in UTC. The `date -u` command is used to get the UTC time.
            *   `echo "💡 This job was triggered ..."`: Provides context on how the job might have started.

### Important Notes for Students:

*   **Cron Syntax:** Cron syntax can be tricky. Use a tool like [crontab.guru](https://crontab.guru/) to help build and verify your cron expressions.
*   **UTC Time:** GitHub Actions schedules run based on Coordinated Universal Time (UTC). Make sure to adjust your cron expression for your local timezone if you need it to run at a specific local time.
*   **Minimum Schedule Frequency:** GitHub Actions workflows scheduled with `cron` are not guaranteed to run at the exact scheduled time. They may be delayed depending on GitHub's load. The shortest interval you can reliably schedule is typically every 5 minutes (`*/5 * * * *`). However, for learning purposes, it's better to use less frequent schedules (e.g., hourly or daily) to avoid excessive runs.
*   **Testing:** Use the `workflow_dispatch` trigger extensively during development and testing to avoid waiting for the cron schedule. 