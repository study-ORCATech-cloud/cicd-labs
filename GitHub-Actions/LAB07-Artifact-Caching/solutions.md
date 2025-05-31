# Solutions for LAB07 - Artifact Caching & Dependencies

This file contains the solutions for the `TODO` items in the `.github/workflows/cache-and-artifacts.yml` workflow file.

---

## `cache-and-artifacts.yml` Solutions

```yaml
name: Cache Dependencies and Manage Artifacts

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build_and_test_with_cache:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Cache pip dependencies
        uses: actions/cache@v3
        id: cache-pip # Give an id to the cache step to check its output
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          echo "Installing dependencies..."
          pip install -r requirements.txt
          if ${{ steps.cache-pip.outputs.cache-hit == 'true' }};
          then
            echo "Pip cache hit! Dependencies installed from cache."
          else
            echo "Pip cache miss or new dependencies. Installed fresh."
          fi

      - name: List installed packages (for verification)
        run: pip list

      - name: Create a simple build artifact
        run: |
          mkdir -p outputs
          echo "Build completed on $(date)" > outputs/build-info.txt
          echo "Python version used: $(python --version)" >> outputs/build-info.txt
          echo "Triggered by: ${{ github.actor }} for event: ${{ github.event_name }}" >> outputs/build-info.txt

      - name: Upload build artifact
        uses: actions/upload-artifact@v3
        with:
          name: my-build-outputs
          path: outputs/

  deploy_or_inspect_artifact:
    needs: build_and_test_with_cache
    runs-on: ubuntu-latest
    steps:
      - name: Download build artifact
        uses: actions/download-artifact@v3
        with:
          name: my-build-outputs
          path: ./downloaded-artifact

      - name: Inspect downloaded artifact
        run: |
          echo "Listing contents of downloaded artifact directory:"
          ls -R ./downloaded-artifact
          echo ""
          echo "Contents of build-info.txt:"
          cat ./downloaded-artifact/build-info.txt
```

---

### Explanation (`cache-and-artifacts.yml`):

1.  **Triggers (`on`):**
    *   `push: branches: [ main ]`: Runs on pushes to the main branch.
    *   `workflow_dispatch:`: Allows manual triggering.

2.  **Job 1: `build_and_test_with_cache`**
    *   **`Set up Python` (`actions/setup-python@v4`):** Configures Python 3.9.
    *   **`Cache pip dependencies` (`actions/cache@v3`):**
        *   `id: cache-pip`: Assigns an ID to this step so we can check its `outputs.cache-hit` later.
        *   `path: ~/.cache/pip`: Specifies the directory to cache (pip's default cache location).
        *   `key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}`: This is the primary cache key. It includes the runner's OS, "pip", and a hash of the `requirements.txt` file. If `requirements.txt` changes, the hash changes, invalidating the cache and forcing a fresh install + new cache save.
        *   `restore-keys: | ${{ runner.os }}-pip-`: Fallback keys. If the exact key isn't found, GitHub Actions will look for caches starting with this prefix (e.g., from a previous run with different dependencies).
    *   **`Install dependencies`**: Installs packages using `pip`. The script also checks `steps.cache-pip.outputs.cache-hit` to print whether the cache was used. This is useful for verifying caching is working.
    *   **`List installed packages`**: Runs `pip list` for manual verification in logs.
    *   **`Create a simple build artifact`**: Creates a directory `outputs/` and a file `build-info.txt` within it containing some build information.
    *   **`Upload build artifact` (`actions/upload-artifact@v3`):**
        *   `name: my-build-outputs`: The name under which the artifact will be stored.
        *   `path: outputs/`: Specifies the directory to upload.

3.  **Job 2: `deploy_or_inspect_artifact`**
    *   **`needs: build_and_test_with_cache`**: Ensures this job only runs after `build_and_test_with_cache` completes successfully.
    *   **`Download build artifact` (`actions/download-artifact@v3`):**
        *   `name: my-build-outputs`: Specifies which artifact to download.
        *   `path: ./downloaded-artifact`: The directory where the artifact content will be placed.
    *   **`Inspect downloaded artifact`**: Lists the contents of the downloaded directory and prints the content of `build-info.txt` to verify the artifact was correctly passed between jobs.

### Important Notes for Students:

*   **Cache Scope:** The cache is specific to the branch (unless `restore-keys` find a broader match) and key. Changes to the `requirements.txt` will generate a new key and a new cache entry.
*   **Cache `path`:** For `pip`, `~/.cache/pip` is a common path. If using virtual environments, you might cache the virtual environment directory itself, but be cautious about absolute paths if runners change.
*   **Artifacts vs. Cache:**
    *   **Cache:** Used for speeding up builds by reusing dependencies or other files that don't change often between runs (e.g., `node_modules`, `pip` cache). Cache is for performance.
    *   **Artifacts:** Used to persist files generated by a job (e.g., build outputs, test reports, binaries) and share them with other jobs in the same workflow, or to download them after the workflow run. Artifacts are for data persistence and sharing.
*   **Cache Hits:** Check the workflow logs for messages like "Cache hit for key..." or the output of the custom echo command in the "Install dependencies" step to confirm if the cache is being used.
*   **Artifact Retention:** Artifacts are stored for a period defined by GitHub (default is 90 days, but can vary for public/private repos or enterprise settings). 