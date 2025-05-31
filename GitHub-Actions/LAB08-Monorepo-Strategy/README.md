# LAB08 - Monorepo Strategy with Conditional Workflows (GitHub Actions)

This lab teaches you how to create **conditional workflows** in GitHub Actions that run specific jobs based on which folder (or service/library) in a monorepo was modified. This is crucial for optimizing CI/CD pipelines in large repositories by only building and testing what has changed.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Configure a workflow to trigger only when changes occur in specified paths using `on.push.paths`.
- Use a dedicated job with an action like `dorny/paths-filter@v2` to determine which specific sub-directories (services/libraries) have changes.
- Define job outputs from the path-filtering job.
- Implement conditional execution of subsequent jobs using `if` conditions that consume these outputs (e.g., `if: needs.filter_job.outputs.service_a_changed == 'true'`).
- Understand how to structure a workflow for a monorepo to build/test services independently or run broader tasks based on detected changes.

---

## 🧰 Prerequisites

- A GitHub account and a repository with Actions enabled.
- Basic understanding of monorepo structures (multiple services/libraries in one repository).
- Familiarity with basic YAML and GitHub Actions workflow syntax, including job dependencies (`needs`) and `if` conditions.

---

## 🗂️ Folder Structure

Your lab directory should be set up with a structure similar to this, with the `TODO`s in `monorepo-conditional.yml`:

```bash
GitHub-Actions/LAB08-Monorepo-Strategy/
├── .github/
│   └── workflows/
│       └── monorepo-conditional.yml  # Your partially completed workflow file with TODOs
├── service-a/
│   └── app_a.py                     # Sample Python app for Service A (provided)
├── service-b/
│   └── app_b.py                     # Sample Python app for Service B (provided)
├── common-lib/
│   └── utils.py                     # Sample Python utility for Common Lib (provided)
├── README.md                        # Lab instructions (this file)
└── solutions.md                     # Solutions for monorepo-conditional.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB08-Monorepo-Strategy/` directory.

2.  **Examine the Service and Library Files:**
    Briefly look at `service-a/app_a.py`, `service-b/app_b.py`, and `common-lib/utils.py`. These are simple placeholder files representing different components in your monorepo.

3.  **Complete the GitHub Actions Workflow (`.github/workflows/monorepo-conditional.yml`):**
    Open `.github/workflows/monorepo-conditional.yml`. This file contains `TODO` comments to guide you:

    *   **Workflow Trigger (`on.push.paths`):**
        *   TODO: Configure the `on.push.paths` section to ensure the workflow *only* triggers if changes are detected within `service-a/**`, `service-b/**`, or `common-lib/**`.

    *   **Job: `filter_paths`**
        *   This job uses `dorny/paths-filter@v2` to check for changes in specific directories.
        *   TODO: Complete the `uses:` line to specify `dorny/paths-filter@v2`.
        *   TODO: In the `with.filters` section, define filters for `service_a`, `service_b`, `common_lib`, and `any_service` by uncommenting and completing the provided path patterns (e.g., `service_a: ['service-a/**']`).
        *   The job is already configured to output boolean flags like `service_a_changed`, `service_b_changed`, etc.

    *   **Job: `build_service_a`**
        *   This job should only run if Service A's files changed.
        *   TODO: Complete the `if:` condition to use the `service_a_changed` output from the `filter_paths` job (e.g., `if: needs.filter_paths.outputs.service_a_changed == 'true'`).
        *   The `run` step has placeholder commands. In a real scenario, you'd build/test Service A here.

    *   **Job: `build_service_b`**
        *   Similar to `build_service_a`, but for Service B.
        *   TODO: Complete the `if:` condition using `needs.filter_paths.outputs.service_b_changed == 'true'`.

    *   **Job: `build_common_lib`**
        *   Similar, but for the `common-lib`.
        *   TODO: Complete the `if:` condition using `needs.filter_paths.outputs.common_lib_changed == 'true'`.

    *   **Job: `run_integration_tests`**
        *   This job should run if *any* of the monitored services or the library changed.
        *   TODO: Complete the `if:` condition using `needs.filter_paths.outputs.any_service_changed == 'true'`.

4.  **Commit and Push Your Changes:**
    ```bash
    git add .github/workflows/monorepo-conditional.yml
    git commit -m "feat: Implement monorepo conditional workflow for LAB08"
    git push origin main
    ```

5.  **Verify Workflow Execution (Test Different Scenarios):**
    This is the most important part. You need to test by making changes in different directories and observing which jobs run:
    *   **Scenario 1:** Modify only a file in `service-a/` (e.g., add a comment to `app_a.py`). Commit and push.
        *   *Expected:* The workflow triggers. `filter_paths` runs. `build_service_a` runs. `run_integration_tests` runs. `build_service_b` and `build_common_lib` are skipped.
    *   **Scenario 2:** Modify only a file in `service-b/`. Commit and push.
        *   *Expected:* `build_service_b` and `run_integration_tests` run. Others are skipped (after `filter_paths`).
    *   **Scenario 3:** Modify only a file in `common-lib/`. Commit and push.
        *   *Expected:* `build_common_lib` and `run_integration_tests` run. Others are skipped.
    *   **Scenario 4:** Modify a file in `service-a/` AND a file in `common-lib/` in the same commit. Push.
        *   *Expected:* `build_service_a`, `build_common_lib`, and `run_integration_tests` run. `build_service_b` is skipped.
    *   **Scenario 5:** Modify only the main `README.md` for this lab (or create a new file at the root of `LAB08-Monorepo-Strategy/`). Commit and push.
        *   *Expected:* The "Monorepo Conditional Builds" workflow should **not** trigger at all, because the change is outside the paths defined in `on.push.paths`.
    *   Check the "Actions" tab in your GitHub repository for each push. Inspect the visual workflow graph and the logs for each job to confirm the correct behavior and see the `echo` messages.

---

## ✅ Validation Checklist

- [ ] The `.github/workflows/monorepo-conditional.yml` file is correctly completed, addressing all `TODO`s.
- [ ] The workflow correctly uses `on.push.paths` to only trigger on relevant directory changes.
- [ ] The `filter_paths` job correctly uses `dorny/paths-filter@v2` and sets its outputs.
- [ ] The `build_service_a`, `build_service_b`, and `build_common_lib` jobs run *only* when changes are detected in their respective directories.
- [ ] The `run_integration_tests` job runs if changes are detected in *any* of the `service-a`, `service-b`, or `common-lib` directories.
- [ ] Pushing changes *outside* the specified paths (e.g., to the root `README.md` of this lab) does **not** trigger the workflow.
- [ ] You understand how job outputs and `if` conditions enable this conditional logic.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for `monorepo-conditional.yml` with detailed explanations.

---

## 🧹 Cleanup

-   **Workflow File:** Delete `.github/workflows/monorepo-conditional.yml`.
-   **Service/Lib files:** You can delete `service-a/`, `service-b/`, and `common-lib/` directories if created solely for this lab.
-   Commit and push any cleanup changes.

---

## 🧠 Key Concepts

-   **`on.push.paths` / `on.pull_request.paths`:** Workflow-level filters that determine if a workflow should run at all based on changed file paths.
-   **Path Filtering Actions (e.g., `dorny/paths-filter@v2`):** Actions that inspect the changeset within a triggered workflow to determine which specific configured paths were affected. They typically provide outputs (booleans) for each path filter.
-   **Job Outputs (`jobs.<job_id>.outputs`):** Allows a job to expose data (like the boolean flags from path filtering) to other jobs that depend on it.
-   **`needs` context:** Used to access outputs from jobs that current job depends on (e.g., `needs.filter_job.outputs.some_output`).
-   **`if` conditionals on jobs:** Controls whether a job runs based on an expression. Essential for implementing the conditional logic based on filtered paths.
-   **Monorepo CI Optimization:** These techniques are vital for monorepos to avoid running lengthy CI processes for all services when only one has changed, saving time and computational resources.

---

## 🌟 Well Done!

You've now learned a robust strategy for managing CI/CD in a monorepo environment, ensuring that your workflows run efficiently and intelligently!

---

## 🔁 What's Next?
Continue to [LAB09 - Reusable Workflows](../LAB09-Reusable-Workflows/) to create shareable and callable pipeline templates.

One repo. Many paths. Smart builds. 🗺️✨