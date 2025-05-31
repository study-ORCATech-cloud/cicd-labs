# Solutions for LAB01 - Hello World Workflow

This file contains the solutions for the `TODO` items in the `hello-world.yml` workflow file.

---

## `hello-world.yml` Solutions

```yaml
name: Hello World CI

on:
  push:
    branches:
      - main

jobs:
  say-hello:
    runs-on: ubuntu-latest
    steps:
      - name: Echo greeting
        run: echo "👋 Hello from GitHub Actions!"

      - name: Show date and runner OS
        run: |
          echo "📅 Date: $(date)"
          echo "🖥️ Running on: ${{ runner.os }}"
```

---

### Explanation:

1.  **Trigger Configuration (`on` block):**
    *   `on: push:`: This specifies that the workflow will trigger on `push` events.
    *   `branches: - main`: This filters the push events to only trigger the workflow when changes are pushed to the `main` branch.

2.  **Runner OS (`runs-on`):**
    *   `runs-on: ubuntu-latest`: This tells GitHub Actions to run the `say-hello` job on the latest available Ubuntu Linux virtual machine.

3.  **Echo Greeting (`run` step):**
    *   `run: echo "👋 Hello from GitHub Actions!"`: This step executes a shell command to print the greeting string to the workflow log.

4.  **Show Date and Runner OS (`run` step with multi-line script):**
    *   `run: |`: The pipe `|` allows for a multi-line script.
    *   `echo "📅 Date: $(date)"`: This command prints the current date and time. The `$(date)` part is a command substitution that executes the `date` command.
    *   `echo "🖥️ Running on: ${{ runner.os }}"`: This command prints the operating system of the runner. `${{ runner.os }}` is a GitHub Actions expression that accesses the `os` property of the `runner` context object. 