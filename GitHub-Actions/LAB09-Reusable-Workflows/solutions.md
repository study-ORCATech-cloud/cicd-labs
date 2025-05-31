# Solutions for LAB09 - Reusable Workflows (Local)

This file contains the solutions for the `TODO` items in the reusable workflow (`.github/workflows/reusable-build-test.yml`) and the caller workflows (`.github/workflows/caller-service-alpha.yml` and `.github/workflows/caller-service-beta.yml`).

---

## 1. Reusable Workflow: `reusable-build-test.yml`

This workflow is designed to be called by other workflows within the same repository. It handles the common tasks of setting up Python, installing dependencies, and running a placeholder test for a given application directory.

```yaml
name: Reusable Build and Test

on:
  workflow_call:
    inputs:
      python-version:
        description: 'Python version to use'
        required: true
        type: string
      app-directory:
        description: 'Directory of the application to build and test'
        required: true
        type: string
    outputs:
      test-result:
        description: 'The result of the test execution'
        value: ${{ jobs.build_and_test.outputs.test_outcome }}

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    outputs:
      test_outcome: ${{ steps.run_tests.outputs.outcome }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ inputs.python-version }}

      - name: Install dependencies
        run: |
          echo "Installing dependencies from ${{ inputs.app-directory }}/requirements.txt"
          python -m pip install --upgrade pip
          pip install -r ./${{ inputs.app-directory }}/requirements.txt

      - name: Run application tests (placeholder)
        id: run_tests # Give an ID to this step to access its output
        run: |
          echo "Running tests for application in ${{ inputs.app-directory }}..."
          cd ./${{ inputs.app-directory }}
          export PYTHON_VERSION_INFO="${{ inputs.python-version }}" # Pass python version to app
          python app.py
          # Simulate test outcome based on app-directory for demonstration
          if [[ "${{ inputs.app-directory }}" == *"alpha"* ]]; then
            echo "::set-output name=outcome::Alpha tests passed successfully on Python ${{ inputs.python-version }}!"
          elif [[ "${{ inputs.app-directory }}" == *"beta"* ]]; then
            echo "::set-output name=outcome::Beta tests passed successfully on Python ${{ inputs.python-version }}!"
          else
            echo "::set-output name=outcome::Tests passed (unknown service) on Python ${{ inputs.python-version }}!"
          fi

      - name: Print test outcome from step output (for logs)
        run: |
          echo "Test outcome from step output: ${{ steps.run_tests.outputs.outcome }}"
```

### Explanation (`reusable-build-test.yml`):

1.  **`on: workflow_call:`**: This is the key trigger that makes this workflow reusable. It cannot be triggered by other events directly (like `push` or `schedule`).
2.  **`inputs:`**: Defines the parameters that calling workflows must (or can) provide.
    *   `python-version`: A required string for specifying the Python version.
    *   `app-directory`: A required string for the path to the application's code and `requirements.txt`.
3.  **`outputs:`**: Defines the data that this reusable workflow will make available to the calling workflow.
    *   `test-result`: Will carry the outcome of the tests. Its `value` is mapped from a job's output: `value: ${{ jobs.build_and_test.outputs.test_outcome }}`.
4.  **`jobs.build_and_test.outputs.test_outcome`**: The job `build_and_test` defines an output `test_outcome`. This output gets its value from a step's output: `test_outcome: ${{ steps.run_tests.outputs.outcome }}`.
5.  **Using Inputs**:
    *   `python-version: ${{ inputs.python-version }}`: The `setup-python` action uses the `python-version` input.
    *   The `Install dependencies` and `Run application tests` steps use `inputs.app-directory` to navigate to the correct directory and find files (e.g., `pip install -r ./${{ inputs.app-directory }}/requirements.txt`).
6.  **Step Output (`steps.run_tests.outputs.outcome`):**
    *   The `Run application tests` step has an `id: run_tests`.
    *   It uses `echo "::set-output name=outcome::Some value"` to create a step-level output named `outcome`. This is a way to communicate results from shell scripts within a step to the broader workflow.
    *   The final `echo` in this step demonstrates how this value can be accessed within the same job for logging.

---

## 2. Caller Workflow: `caller-service-alpha.yml`

This workflow triggers on changes to `service-alpha` and calls the `reusable-build-test.yml` workflow.

```yaml
name: Caller for Service Alpha

on:
  push:
    paths:
      - 'services/service-alpha/**'
  workflow_dispatch: # Allow manual run for easy testing

jobs:
  call_reusable_workflow_for_alpha:
    uses: ./.github/workflows/reusable-build-test.yml
    with:
      python-version: '3.9'
      app-directory: 'services/service-alpha'
    # secrets: inherit # Example if you needed to pass secrets

  report_alpha_test_result:
    runs-on: ubuntu-latest
    needs: call_reusable_workflow_for_alpha
    if: always() # Ensure this job runs even if the called workflow fails, to see the result/failure
    steps:
      - name: Display test result from reusable workflow
        run: |
          echo "Service Alpha - Called Workflow Result: ${{ needs.call_reusable_workflow_for_alpha.result }}"
          echo "Service Alpha - Test Output from Reusable Workflow: ${{ needs.call_reusable_workflow_for_alpha.outputs.test-result }}"
```

### Explanation (`caller-service-alpha.yml`):

1.  **`on.push.paths`**: Triggers the workflow only when files under `services/service-alpha/**` are pushed. `workflow_dispatch` is added for manual testing.
2.  **`jobs.call_reusable_workflow_for_alpha.uses`**: This is how a reusable workflow is called.
    *   `./.github/workflows/reusable-build-test.yml`: Specifies the path to the reusable workflow *within the same repository*. For workflows in other repositories, it would be `owner/repo/.github/workflows/filename.yml@ref`.
3.  **`jobs.call_reusable_workflow_for_alpha.with`**: This section provides the `inputs` defined by the `reusable-build-test.yml` workflow.
    *   `python-version: '3.9'`
    *   `app-directory: 'services/service-alpha'`
4.  **`secrets: inherit` (Commented Out)**: If the reusable workflow needed secrets, `secrets: inherit` would pass all the calling workflow's secrets that are permitted for the reusable workflow to access. You can also pass them individually.
5.  **`jobs.report_alpha_test_result.needs`**: The `report_alpha_test_result` job depends on `call_reusable_workflow_for_alpha` finishing.
6.  **Accessing Outputs**:
    *   `needs.call_reusable_workflow_for_alpha.outputs.test-result`: This is how the `report_alpha_test_result` job accesses the `test-result` output from the `call_reusable_workflow_for_alpha` job (which, in turn, got it from the reusable workflow).
    *   `needs.call_reusable_workflow_for_alpha.result`: This accesses the overall result (`success`, `failure`, `cancelled`, or `skipped`) of the job that called the reusable workflow. It's useful for seeing if the call itself succeeded. The `if: always()` ensures this reporting job runs to show the outcome.

---

## 3. Caller Workflow: `caller-service-beta.yml`

This workflow is very similar to Alpha's caller but targets `service-beta` and uses a different Python version for demonstration.

```yaml
name: Caller for Service Beta

on:
  push:
    paths:
      - 'services/service-beta/**'
  workflow_dispatch:

jobs:
  call_reusable_workflow_for_beta:
    uses: ./.github/workflows/reusable-build-test.yml
    with:
      python-version: '3.10' # Different Python version for Beta
      app-directory: 'services/service-beta'

  report_beta_test_result:
    runs-on: ubuntu-latest
    needs: call_reusable_workflow_for_beta
    if: always()
    steps:
      - name: Display test result from reusable workflow
        run: |
          echo "Service Beta - Called Workflow Result: ${{ needs.call_reusable_workflow_for_beta.result }}"
          echo "Service Beta - Test Output from Reusable Workflow: ${{ needs.call_reusable_workflow_for_beta.outputs.test-result }}"
```

### Explanation (`caller-service-beta.yml`):

*   The structure and logic are identical to `caller-service-alpha.yml`, with the key differences being:
    *   The `on.push.paths` trigger is for `services/service-beta/**`.
    *   The `with` block in the `call_reusable_workflow_for_beta` job passes `python-version: '3.10'` and `app-directory: 'services/service-beta'`.
*   This demonstrates how the same reusable workflow can be parameterized for different services or configurations.

---

This setup allows you to maintain the core build and test logic in one place (`reusable-build-test.yml`) and reuse it across multiple services, each with its own specific trigger paths and input parameters. 