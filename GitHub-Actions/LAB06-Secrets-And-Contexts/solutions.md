# Solutions for LAB06 - Secrets & Contexts

This file contains the solutions for the `TODO` items in the `.github/workflows/show-secrets.yml` workflow file.

---

## `show-secrets.yml` Solutions

```yaml
name: Secrets and Contexts Demo

on:
  push:
    branches: [ main ]
  workflow_dispatch: # Allows manual triggering

jobs:
  demonstrate_secrets_and_contexts:
    runs-on: ubuntu-latest
    env:
      JOB_LEVEL_ENV_VAR: "I am a job-level variable from the job scope!"

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Display GitHub Context Information
        run: |
          echo "Workflow triggered by: ${{ github.actor }}"
          echo "Repository name: ${{ github.repository }}"
          echo "Event type: ${{ github.event_name }}"
          echo "Git Ref: ${{ github.ref }}"
          echo "Commit SHA: ${{ github.sha }}"
          echo "Workflow name: ${{ github.workflow }}"

      - name: Display Runner Context Information
        run: |
          echo "Runner OS: ${{ runner.os }}"
          echo "Runner architecture: ${{ runner.arch }}"
          echo "Runner temporary directory: ${{ runner.temp }}"
          echo "Runner workspace: ${{ runner.workspace }}"

      - name: Access Job-Level Environment Variable
        run: |
          echo "Job-level environment variable (JOB_LEVEL_ENV_VAR): $JOB_LEVEL_ENV_VAR"

      - name: Access a Secret (Securely)
        # This step assumes you have a secret named MY_SECRET_VALUE configured in your repository.
        env:
          MY_SECRET_FROM_WORKFLOW: ${{ secrets.MY_SECRET_VALUE }}
        run: |
          echo "Attempting to access MY_SECRET_VALUE via MY_SECRET_FROM_WORKFLOW..."
          if [ -n "$MY_SECRET_FROM_WORKFLOW" ]; then
            echo "MY_SECRET_VALUE is set."
            echo "Length of MY_SECRET_VALUE: ${#MY_SECRET_FROM_WORKFLOW}"
            # Example of using the secret: For demonstration, let's check if it equals a specific string.
            # NEVER echo the actual secret value in a real workflow for security reasons.
            if [ "$MY_SECRET_FROM_WORKFLOW" == "super-secret-value-for-testing" ]; then
              echo "Secret content matches the test string! (This is for demo only)"
            else
              echo "Secret content does NOT match the test string."
            fi
          else
            echo "MY_SECRET_VALUE is not set or is empty. Please ensure it is configured in repository secrets."
            echo "If you haven't set it, please go to Repository Settings > Secrets and variables > Actions and add a new repository secret named MY_SECRET_VALUE."
          fi

      - name: Access Step-Level Environment Variable
        env:
          STEP_LEVEL_ENV_VAR: "I am a step-level variable, specific to this step!"
          ANOTHER_STEP_VAR: "Hello from step env!"
        run: |
          echo "Step-level environment variable (STEP_LEVEL_ENV_VAR): $STEP_LEVEL_ENV_VAR"
          echo "Another step-level variable (ANOTHER_STEP_VAR): $ANOTHER_STEP_VAR"

```

---

### Explanation (`show-secrets.yml`):

1.  **Trigger Configuration (`on`):**
    *   `push: branches: [ main ]`: Triggers the workflow on pushes to the `main` branch.
    *   `workflow_dispatch:`: Allows manual triggering from the Actions tab.

2.  **Job: `demonstrate_secrets_and_contexts` (`jobs.demonstrate_secrets_and_contexts`):**
    *   **Runner OS (`runs-on`):** `ubuntu-latest` is used.
    *   **Job-Level Environment Variable (`env`):**
        *   `JOB_LEVEL_ENV_VAR: "..."`: Defines an environment variable available to all steps within this job.

3.  **Steps (`steps`):**
    *   **`Checkout code` (`actions/checkout@v3`):** Standard step to access repository files if needed (though not strictly used for outputs in this lab, it's good practice).
    *   **`Display GitHub Context Information`**: This step uses inline expressions like `${{ github.actor }}` to print various details from the `github` context object. This context contains information about the event, repository, actor, etc.
    *   **`Display Runner Context Information`**: Similar to the above, this step prints information from the `runner` context, like OS, architecture, and paths.
    *   **`Access Job-Level Environment Variable`**: Demonstrates accessing the `JOB_LEVEL_ENV_VAR` (defined at the job level) directly as `$JOB_LEVEL_ENV_VAR` within the script.
    *   **`Access a Secret (Securely)`**:
        *   `env: MY_SECRET_FROM_WORKFLOW: ${{ secrets.MY_SECRET_VALUE }}`: This is the crucial part for using secrets. The secret `MY_SECRET_VALUE` (which the student must create in repository settings) is mapped to an environment variable `MY_SECRET_FROM_WORKFLOW` specifically for this step.
        *   The script then checks if `MY_SECRET_FROM_WORKFLOW` is set and prints its length (`${#MY_SECRET_FROM_WORKFLOW}`). **It deliberately avoids printing the actual secret value (`$MY_SECRET_FROM_WORKFLOW`) to maintain security.**
        *   A conditional check is added as a *demonstration* of how a secret might be *used* (e.g., compared), but even this should be done carefully.
    *   **`Access Step-Level Environment Variable`**:
        *   `env: STEP_LEVEL_ENV_VAR: "..."`: Defines environment variables that are only available within this specific step.
        *   The script then accesses these as `$STEP_LEVEL_ENV_VAR` and `$ANOTHER_STEP_VAR`.

### Important Notes for Students:

*   **Create the Secret:** This lab **requires** you to create a repository secret named `MY_SECRET_VALUE`. Go to your repository's `Settings` > `Secrets and variables` > `Actions` > `New repository secret`.
*   **NEVER Print Secrets:** In a real-world scenario, **never print your actual secrets to the logs** using `echo $SECRET_NAME` or similar. The example shows printing the length or using it in a conditional check (for illustrative purposes) which are safer ways to confirm a secret is accessible. If a secret is exposed in logs, it is compromised.
*   **Context Availability:** Different contexts (`github`, `env`, `job`, `steps`, `runner`, `secrets`, `strategy`, `matrix`, `needs`) are available at different points in your workflow. Refer to the [official GitHub Actions documentation on Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts) for more details. 