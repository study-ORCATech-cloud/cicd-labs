# Solutions for LAB08 - Monorepo Strategy

This file contains the solutions for the `TODO` items in the `.github/workflows/monorepo-conditional.yml` workflow file.

---

## `monorepo-conditional.yml` Solutions

```yaml
name: Monorepo Conditional Builds

on:
  push:
    branches:
      - main
    paths: # Workflow triggers if changes are in these paths
      - 'service-a/**'
      - 'service-b/**'
      - 'common-lib/**'

jobs:
  filter_paths:
    runs-on: ubuntu-latest
    outputs:
      service_a_changed: ${{ steps.filter.outputs.service_a }}
      service_b_changed: ${{ steps.filter.outputs.service_b }}
      common_lib_changed: ${{ steps.filter.outputs.common_lib }}
      any_service_changed: ${{ steps.filter.outputs.any_service }}
    steps:
      - uses: actions/checkout@v3
      - name: Calculate changed paths
        uses: dorny/paths-filter@v2
        id: filter
        with:
          # For push events, the filter compares against the previous commit (HEAD^).
          # For pull_request events, it compares against the base branch.
          # list-files: shell # Can be useful for debugging to see what files the action is considering
          filters: |
            service_a: 
              - 'service-a/**'
            service_b:
              - 'service-b/**'
            common_lib:
              - 'common-lib/**'
            # 'any_service' will be true if any of the above paths have changes.
            # This is useful for a job that should run if any component is updated.
            any_service:
              - 'service-a/**'
              - 'service-b/**'
              - 'common-lib/**'

  build_service_a:
    needs: filter_paths
    if: needs.filter_paths.outputs.service_a_changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3 # Checkout again as each job runs on a fresh runner
      - name: Build Service A
        run: |
          echo "Building Service A because changes were detected in service-a/**"
          echo "Running Service A application..."
          cd service-a
          python app_a.py

  build_service_b:
    needs: filter_paths
    if: needs.filter_paths.outputs.service_b_changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Service B
        run: |
          echo "Building Service B because changes were detected in service-b/**"
          echo "Running Service B application..."
          cd service-b
          python app_b.py

  build_common_lib:
    needs: filter_paths
    if: needs.filter_paths.outputs.common_lib_changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Common Lib
        run: |
          echo "Building Common Lib because changes were detected in common-lib/**"
          echo "Running Common Lib utility..."
          cd common-lib
          python utils.py

  run_integration_tests:
    needs: filter_paths # Could also depend on specific build jobs if needed
    if: needs.filter_paths.outputs.any_service_changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Integration Tests
        run: |
          echo "Running integration tests because a relevant service or library changed..."
          echo "Service A changed: ${{ needs.filter_paths.outputs.service_a_changed }}"
          echo "Service B changed: ${{ needs.filter_paths.outputs.service_b_changed }}"
          echo "Common Lib changed: ${{ needs.filter_paths.outputs.common_lib_changed }}"
          # Add actual integration test commands here that might use outputs from other jobs
          # For example, download artifacts from build_service_a and build_service_b if they ran.
```

---

### Explanation (`monorepo-conditional.yml`):

1.  **Workflow Trigger (`on.push.paths`):**
    *   The workflow is configured to run on `push` events to the `main` branch.
    *   Crucially, the `paths` filter (`service-a/**`, `service-b/**`, `common-lib/**`) ensures that the workflow *only* starts if changes are pushed that affect files within these specified directories. If changes are made to other files outside these paths, the workflow will not run.

2.  **Job: `filter_paths`**
    *   This job is the first to run and its purpose is to determine precisely which of the monitored directories have changes.
    *   **`uses: dorny/paths-filter@v2`**: This popular third-party action is used to compare the changes in the push with the defined filters.
    *   **`id: filter`**: Gives the step an ID so its outputs can be referenced.
    *   **`with.filters`**: This is where you define your path groups.
        *   `service_a: ['service-a/**']`: Creates an output `steps.filter.outputs.service_a` which will be `'true'` if changes occurred in `service-a/` and `'false'` otherwise.
        *   Similar filters are defined for `service_b` and `common_lib`.
        *   `any_service: ['service-a/**', 'service-b/**', 'common-lib/**']`: This filter (`steps.filter.outputs.any_service`) will be `'true'` if *any* of the listed paths have changes.
    *   **`outputs`**: The job formally defines outputs (`service_a_changed`, `service_b_changed`, etc.) that map to the outputs of the `paths-filter` step. This makes them easily accessible to other jobs that `need` this one.

3.  **Conditional Build Jobs (`build_service_a`, `build_service_b`, `build_common_lib`):**
    *   **`needs: filter_paths`**: Each of these jobs depends on the `filter_paths` job to complete first.
    *   **`if: needs.filter_paths.outputs.service_a_changed == 'true'`**: This is the conditional execution. For example, `build_service_a` will only run if the `service_a_changed` output from the `filter_paths` job is true.
    *   Each job checks out the code and then runs mock build/execution commands for its respective service/library. In a real scenario, these would be actual build, test, and packaging commands.

4.  **Job: `run_integration_tests`**
    *   **`if: needs.filter_paths.outputs.any_service_changed == 'true'`**: This job runs if *any* of the monitored services or the common library has changed, as determined by the `any_service` output.
    *   This demonstrates a scenario where a broader action (like integration testing) is triggered if any relevant component is modified.

### How to Test:

To test this workflow, you can try the following scenarios by committing and pushing changes to `main`:

*   Modify only a file in `service-a/` (e.g., `service-a/app_a.py`).
    *   Expected: `filter_paths` runs. `build_service_a` runs. `run_integration_tests` runs. `build_service_b` and `build_common_lib` are skipped.
*   Modify only a file in `service-b/`.
    *   Expected: `filter_paths` runs. `build_service_b` runs. `run_integration_tests` runs. `build_service_a` and `build_common_lib` are skipped.
*   Modify only a file in `common-lib/`.
    *   Expected: `filter_paths` runs. `build_common_lib` runs. `run_integration_tests` runs. `build_service_a` and `build_service_b` are skipped.
*   Modify files in both `service-a/` and `common-lib/`.
    *   Expected: `filter_paths` runs. `build_service_a`, `build_common_lib`, and `run_integration_tests` run. `build_service_b` is skipped.
*   Modify a file *outside* these directories (e.g., the main `README.md` of the repository or a file in a new, unmonitored directory).
    *   Expected: The workflow does not trigger at all due to the `on.push.paths` filter.

### Important Notes for Students:

*   **`actions/checkout@v3` in each job:** Remember that each job runs on a fresh runner instance. If a job needs access to the repository files, it must have its own `actions/checkout` step.
*   **`dorny/paths-filter` Behavior:** This action is quite versatile. For pushes, it typically compares against `HEAD^`. For pull requests, it compares against the PR's base branch. You can customize its behavior further if needed.
*   **Alternative to Third-Party Actions:** While `dorny/paths-filter` is convenient, you could achieve similar path filtering by writing custom scripts using `git diff` and setting outputs, but it's more complex.
*   **Granularity:** This approach gives you fine-grained control over your CI/CD pipeline, saving resources by only running jobs relevant to the changes made. 