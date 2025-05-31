# LAB07 - Dependency Caching & Build Artifacts (GitHub Actions)

In this lab, you'll learn how to use **GitHub Actions caching** to speed up CI workflows by reusing downloaded dependencies, and how to use **build artifacts** to persist and share files generated during a workflow across different jobs.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Implement dependency caching for a Python project (using `pip` and `requirements.txt`) with `actions/cache@v3`.
- Understand and define effective cache keys and restore strategies.
- Verify cache hits and misses by inspecting workflow logs.
- Create (upload) build artifacts using `actions/upload-artifact@v3`.
- Download and use these artifacts in a subsequent job using `actions/download-artifact@v3`.
- Differentiate between the purposes of caching and artifacts.

---

## 🧰 Prerequisites

- A GitHub account and a repository with Actions enabled.
- Basic understanding of Python projects and `requirements.txt`.
- Familiarity with basic YAML and GitHub Actions workflow syntax.

---

## 🗂️ Folder Structure

Your lab directory is set up with the following structure. You will be completing the `TODO`s in `cache-and-artifacts.yml`.

```bash
GitHub-Actions/LAB07-Artifact-Caching/
├── .github/
│   └── workflows/
│       └── cache-and-artifacts.yml  # Your partially completed workflow file with TODOs
├── requirements.txt               # Sample Python dependencies (provided)
├── README.md                      # Lab instructions (this file)
└── solutions.md                   # Solutions for cache-and-artifacts.yml
```

---

## 🚀 Lab Steps

1.  **Navigate to the Lab Directory:**
    Open your terminal and change to the `GitHub-Actions/LAB07-Artifact-Caching/` directory.

2.  **Examine `requirements.txt`:**
    This file lists a few Python packages that will be cached and installed.

3.  **Complete the GitHub Actions Workflow (`.github/workflows/cache-and-artifacts.yml`):**
    Open `.github/workflows/cache-and-artifacts.yml`. This file has `TODO` comments for you to complete across two jobs:

    **Job 1: `build_and_test_with_cache`**
    *   **Triggers:** Configure `on` for pushes to `main` and `workflow_dispatch`.
    *   **Runner OS:** Specify `runs-on` (e.g., `ubuntu-latest`).
    *   **Checkout Code:** Use `actions/checkout@v3`.
    *   **Set up Python:** Use `actions/setup-python@v4` and specify a Python version (e.g., `'3.9'`).
    *   **Cache Pip Dependencies:** This is a key step. Use `actions/cache@v3`.
        *   `path`: Set to `~/.cache/pip` (standard pip cache location).
        *   `key`: Define a dynamic key. A good practice is `${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}`. This means the cache is specific to the OS and will change if `requirements.txt` changes.
        *   `restore-keys` (optional but recommended): Add a more general fallback key like `${{ runner.os }}-pip-`.
    *   **Install Dependencies:** Write a script to upgrade `pip` and install packages from `requirements.txt`. Observe how this step is faster on subsequent runs if a cache hit occurs.
    *   **Create Artifact:** In the "Create a simple build artifact" step (provided), a directory `outputs` with a `build-info.txt` file is created. Examine this step.
    *   **Upload Artifact:** Use `actions/upload-artifact@v3`. Give your artifact a `name` (e.g., `my-build-outputs`) and specify the `path` to the `outputs/` directory.

    **Job 2: `deploy_or_inspect_artifact` (Initially Commented Out)**
    *   Uncomment this job definition.
    *   **`needs`:** Ensure this job `needs: build_and_test_with_cache` to run after the first job.
    *   **Runner OS:** Specify `runs-on` (e.g., `ubuntu-latest`).
    *   **Download Artifact:** Use `actions/download-artifact@v3`. Use the same `name` you gave during upload and specify a `path` for downloading (e.g., `./downloaded-data`).
    *   **Inspect Artifact:** Write a script to `ls` the contents of the download path and `cat` the `build-info.txt` file to verify.

4.  **Commit and Push Your Changes:**
    ```bash
    git add .github/workflows/cache-and-artifacts.yml requirements.txt
    git commit -m "feat: Implement dependency caching and artifacts for LAB07"
    git push origin main
    ```

5.  **Verify Workflow Execution:**
    *   **First Run:** Trigger the workflow (manually via `workflow_dispatch` or by pushing). Observe the "Install dependencies" step; it will likely be a cache miss, and dependencies will be downloaded fresh. The artifact will be created and uploaded.
    *   **Second Run:** Re-run the workflow without changing `requirements.txt`. 
        *   In the "Cache pip dependencies" step logs, you should see a "Cache hit" message.
        *   The "Install dependencies" step should complete much faster.
        *   The second job should download the artifact from the first job and display its contents.
    *   Inspect the logs of both jobs to confirm all steps behave as expected.

---

## ✅ Validation Checklist

- [ ] The `.github/workflows/cache-and-artifacts.yml` file is correctly completed.
- [ ] **Caching:**
    - [ ] On the first workflow run, dependencies are installed, and the cache is saved.
    - [ ] On subsequent runs (without changes to `requirements.txt`), the pip cache is restored (cache hit), and the dependency installation step is noticeably faster.
    - [ ] Changing `requirements.txt` results in a cache miss and a new cache being saved.
- [ ] **Artifacts:**
    - [ ] The `build_and_test_with_cache` job successfully creates and uploads an artifact named `my-build-outputs` (or your chosen name).
    - [ ] The `deploy_or_inspect_artifact` job successfully downloads this artifact.
    - [ ] The contents of the downloaded `build-info.txt` are correctly displayed in the logs of the second job.
- [ ] You understand the difference between caching for performance and artifacts for data persistence/sharing.

---

## 💡 Solutions

If you get stuck or want to verify your work, refer to the `solutions.md` file provided in this lab directory. It contains the complete working code for `cache-and-artifacts.yml` with explanations.

---

## 🧹 Cleanup

-   **Workflow File:** Delete `.github/workflows/cache-and-artifacts.yml`.
-   **Cache:** GitHub automatically evicts caches that haven't been accessed in over 7 days or when total cache size exceeds limits. You can also manually manage caches:
    *   Go to your repository's "Actions" tab.
    *   In the left sidebar, click on "Caches".
    *   You can view and delete cache entries here.
-   Commit and push any cleanup changes.

---

## 🧠 Key Concepts

-   **`actions/cache@v3`:** The primary action for caching dependencies and other files.
    *   **`path`**: The directory to cache and restore.
    *   **`key`**: The primary identifier for the cache. A cache hit occurs if this key matches an existing cache.
    *   **`restore-keys`**: Optional fallback keys used if the primary `key` doesn't find a match.
-   **`hashFiles()` function:** Often used in cache keys to generate a hash from one or more files (like `requirements.txt` or `package-lock.json`). If the file(s) change, the hash changes, thus changing the cache key.
-   **`actions/upload-artifact@v3`:** Uploads files as a build artifact, making them available for download and use in other jobs or for archival.
-   **`actions/download-artifact@v3`:** Downloads a previously uploaded build artifact.
-   **`jobs.<job_id>.needs`:** Specifies that a job must wait for other jobs to complete successfully before it starts.
-   **Cache vs. Artifacts:** Caches are for performance (reusing unchanged dependencies). Artifacts are for persisting and sharing files produced by your build (reports, binaries, etc.).

---

## 🌟 Well Done!

You've mastered two powerful techniques for optimizing your GitHub Actions workflows: dependency caching and build artifacts. These will make your CI/CD pipelines faster and more versatile!

---

## 🔁 What's Next?
Continue to [LAB08 - Monorepo Strategy](../LAB08-Monorepo-Strategy/) to manage large projects in a single repository.

Cache smart. Build fast. 🚀📦