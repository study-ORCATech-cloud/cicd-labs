# LAB09 - Reusable Workflows (Local Repository)

This lab walks you through how to create and use **reusable workflows within the same repository** using the `workflow_call` trigger in GitHub Actions. This is a powerful way to DRY (Don't Repeat Yourself) your CI/CD processes by centralizing common job sequences.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Define a reusable (callable) workflow template using `on.workflow_call`.
- Define `inputs` that the callable workflow accepts (e.g., Python version, application directory).
- Define `outputs` that the callable workflow produces (e.g., test results).
- Create caller workflows that trigger on specific path changes (e.g., for different services).
- Call the reusable workflow from another workflow file using `jobs.<job_id>.uses` with a local path.
- Pass inputs to the reusable workflow using `jobs.<job_id>.with`.
- Receive and use outputs from the reusable workflow in subsequent jobs in the caller workflow.
- Understand the benefits of local reusable workflows for standardizing CI tasks for multiple components within a single repository.

---

## 🧰 Prerequisites

- A GitHub account and a repository with Actions enabled.
- Basic understanding of YAML and GitHub Actions workflow syntax (triggers, jobs, steps, `needs` context).
- Familiarity with structuring a project with multiple services/components in subdirectories.

---

## 🗂️ Folder Structure

For this lab, your directory will be structured as follows. You will be completing `TODO`s in all three workflow YAML files.

```bash
GitHub-Actions/LAB09-Reusable-Workflows/
├── .github/
│   └── workflows/
│       ├── reusable-build-test.yml  # The callable workflow with TODOs
│       ├── caller-service-alpha.yml # Caller for Service Alpha with TODOs
│       └── caller-service-beta.yml  # Caller for Service Beta with TODOs
├── services/
│   ├── service-alpha/
│   │   ├── app.py                   # Sample Python app (provided)
│   │   └── requirements.txt         # Dependencies for Alpha (provided)
│   └── service-beta/
│       ├── app.py                   # Sample Python app (provided)
│       └── requirements.txt         # Dependencies for Beta (provided)
├── README.md                        # Lab instructions (this file)
└── solutions.md                     # Solutions for all workflow files
```

---

## 🚀 Lab Steps

### 1. Create the Reusable Workflow (`.github/workflows/reusable-build-test.yml`)

This workflow will contain the common logic for building and testing a Python application.

*   **Open `.github/workflows/reusable-build-test.yml`**.
*   **`on.workflow_call`**: 
    *   TODO: Define this trigger.
    *   TODO: Specify `inputs` for `python-version` (string, required) and `app-directory` (string, required).
    *   TODO: Specify an `output` named `test-result` (string), which will take its value from `jobs.build_and_test.outputs.test_outcome`.
*   **Job: `build_and_test`**: 
    *   TODO: Define a job `output` named `test_outcome` that gets its value from `steps.run_tests.outputs.outcome`.
    *   **Step: Set up Python**: 
        *   TODO: Use `actions/setup-python@v4`. Its `python-version` should come from the `inputs.python-version` workflow input.
    *   **Step: Install dependencies**: 
        *   TODO: Write a script to install dependencies using `pip install -r ./<app-directory-input>/requirements.txt`.
    *   **Step: Run application tests (placeholder)**:
        *   This step has an `id: run_tests`.
        *   TODO: Write a script to `cd` into the `inputs.app-directory`, set an environment variable `PYTHON_VERSION_INFO` using `inputs.python-version`, and run `python app.py`.
        *   TODO: The script should then use `echo "::set-output name=outcome::Your test message"` to set the step's `outcome` output. For example, make the message indicate which service passed and on which Python version.

### 2. Create the Caller Workflow for Service Alpha (`.github/workflows/caller-service-alpha.yml`)

This workflow will call the reusable workflow specifically for `service-alpha`.

*   **Open `.github/workflows/caller-service-alpha.yml`**.
*   **Trigger**: 
    *   TODO: Configure it to trigger on pushes to `paths: ['services/service-alpha/**']`. Add `workflow_dispatch:` for manual testing.
*   **Job: `call_reusable_workflow_for_alpha`**: 
    *   TODO: Use `uses: ./.github/workflows/reusable-build-test.yml` to call the local reusable workflow.
    *   TODO: Use `with:` to pass `python-version: '3.9'` and `app-directory: 'services/service-alpha'`.
*   **Job: `report_alpha_test_result`**: 
    *   TODO: This job should `needs: call_reusable_workflow_for_alpha`.
    *   TODO: Its `run` step should echo the output from the called workflow: `echo "Test Result: ${{ needs.call_reusable_workflow_for_alpha.outputs.test-result }}"`.
    *   Consider adding `if: always()` to this reporting job so it runs even if the called workflow fails, to help see the outcome.

### 3. Create the Caller Workflow for Service Beta (`.github/workflows/caller-service-beta.yml`)

This workflow is similar to Alpha's but for `service-beta` and uses a different Python version.

*   **Open `.github/workflows/caller-service-beta.yml`**.
*   **Trigger**: 
    *   TODO: Configure it to trigger on pushes to `paths: ['services/service-beta/**']`. Add `workflow_dispatch:`.
*   **Job: `call_reusable_workflow_for_beta`**: 
    *   TODO: Call `uses: ./.github/workflows/reusable-build-test.yml`.
    *   TODO: Pass `with:` inputs: `python-version: '3.10'` and `app-directory: 'services/service-beta'`.
*   **Job: `report_beta_test_result`**: 
    *   TODO: This job `needs: call_reusable_workflow_for_beta`.
    *   TODO: Echo the output: `echo "Test Result: ${{ needs.call_reusable_workflow_for_beta.outputs.test-result }}"`.
    *   Consider `if: always()` here too.

### 4. Commit and Push Your Changes

```bash
git add .github/workflows/ services/
# (Ensure you add requirements.txt and app.py files for both services if not already done)
git commit -m "feat: Implement reusable and caller workflows for LAB09"
git push origin main
```

### 5. Verify Workflow Executions

*   **Test Service Alpha:** Make a change only to a file inside `GitHub-Actions/LAB09-Reusable-Workflows/services/service-alpha/` (e.g., add a comment to `app.py`). Push the change.
    *   *Expected:* Only the "Caller for Service Alpha" workflow should trigger. It should call the reusable workflow, and the output should indicate tests passed for Alpha on Python 3.9.
*   **Test Service Beta:** Make a change only to a file inside `GitHub-Actions/LAB09-Reusable-Workflows/services/service-beta/`. Push the change.
    *   *Expected:* Only the "Caller for Service Beta" workflow should trigger. It should call the reusable workflow, and the output should indicate tests passed for Beta on Python 3.10.
*   **Test No Trigger:** Make a change to the main `README.md` of this lab, or a file outside the `services/service-alpha/**` or `services/service-beta/**` paths. Push the change.
    *   *Expected:* Neither of the caller workflows should trigger.
*   Inspect the "Actions" tab in your GitHub repository for each push. Check the workflow runs, inputs passed, and outputs received.

---

## ✅ Validation Checklist

- [ ] `reusable-build-test.yml` is correctly defined with `on.workflow_call`, specified `inputs`, and `outputs`.
- [ ] The `build_and_test` job in `reusable-build-test.yml` correctly uses inputs and sets its `test_outcome` output via a step output.
- [ ] `caller-service-alpha.yml` triggers only for changes in `services/service-alpha/**`.
- [ ] `caller-service-alpha.yml` correctly calls `reusable-build-test.yml` using a local path and passes the correct `inputs` for Alpha.
- [ ] The `report_alpha_test_result` job correctly displays the `test-result` output from the reusable workflow for Alpha.
- [ ] `caller-service-beta.yml` triggers only for changes in `services/service-beta/**`.
- [ ] `caller-service-beta.yml` correctly calls `reusable-build-test.yml` and passes the correct `inputs` for Beta (including a different Python version).
- [ ] The `report_beta_test_result` job correctly displays the `test-result` output for Beta.
- [ ] Changes outside the specified service paths do not trigger the caller workflows.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for all three workflow YAML files with detailed explanations.

---

## 🧹 Cleanup

-   **Workflow Files:** Delete the three workflow files from `.github/workflows/`.
-   **Service Directories:** Delete the `services/` directory and its contents if created solely for this lab.
-   Commit and push any cleanup changes.

---

## 🧠 Key Concepts

-   **`on.workflow_call`**: Defines a workflow as callable by other workflows.
-   **`inputs` (in `workflow_call`):** Typed parameters that a reusable workflow can accept. Can be marked as `required`.
-   **`outputs` (in `workflow_call`):** Data that a reusable workflow can return to its caller. Values are typically mapped from job outputs.
-   **`jobs.<job_id>.uses`**: Syntax for calling a reusable workflow. For local workflows, use the path: `./.github/workflows/your-reusable-workflow.yml`.
-   **`jobs.<job_id>.with`**: Used with `uses` to provide values for the `inputs` of the reusable workflow.
-   **`jobs.<job_id>.secrets`**: Used with `uses` to pass secrets to the reusable workflow (e.g., `secrets: inherit` or individual mapping).
-   **Accessing Outputs from Called Workflow:** `needs.<calling_job_id>.outputs.<output_name>`.
-   **Accessing Result of Called Workflow Job:** `needs.<calling_job_id>.result` (e.g., `success`, `failure`).
-   **Local Reusable Workflows:** Great for reducing duplication and enforcing standards for CI/CD processes that are common across multiple services or components within the *same repository*.

---

## 🌟 Well Done!

You've successfully created and used local reusable workflows, a key skill for writing maintainable and efficient GitHub Actions pipelines!

---

## 🔁 What's Next?
Finish the GitHub Actions track with [LAB10 - Canary Deployment](../LAB10-Canary-Deployment/) to implement safer deployment strategies.

Standardize. Parameterize. Reuse. ⚙️🔄🚀