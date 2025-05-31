# Solutions for LAB10 - Canary Deployment

This file contains the solution for the `TODO` items in the `.github/workflows/canary-production-deploy.yml` workflow file.

**Important Prerequisite:** Before this workflow can be fully tested, the student **must** configure two GitHub Environments in their repository settings: `canary` and `production`. For the `production` environment, it's highly recommended to add a "Required reviewers" protection rule to simulate a manual approval gate.

---

## `canary-production-deploy.yml` Solution

```yaml
name: Canary and Production Deployment

on:
  workflow_dispatch:
    inputs:
      version:
        description: 'The application version to deploy (e.g., v1.0.1)'
        required: true
        type: string
      deploy_target:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - canary
          - production

jobs:
  deploy_canary:
    if: github.event.inputs.deploy_target == 'canary'
    environment:
      name: canary
      url: https://my-app-canary.example.com # Example URL
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Update version file for Canary
        run: |
          echo "Updating app/version.txt to ${{ github.event.inputs.version }} for Canary deployment"
          echo "${{ github.event.inputs.version }}" > app/version.txt
          echo "Current version in app/version.txt:"
          cat app/version.txt

      - name: Simulate Canary Deployment
        run: |
          echo "🚀 Deploying version ${{ github.event.inputs.version }} to CANARY environment (URL: ${{ job.environment.url }})..."
          # Imagine actual deployment commands here, e.g., to a canary slot or specific servers
          sleep 10 # Simulate deployment time
          echo "✅ Version ${{ github.event.inputs.version }} notionally live on Canary!"

      - name: Placeholder for Canary Tests/Monitoring
        run: |
          echo "🔍 Running automated tests/monitoring on Canary for version ${{ github.event.inputs.version }}..."
          # Imagine test commands here. If they fail, the workflow might stop or roll back.
          sleep 5 # Simulate test time
          echo "👍 Canary tests passed! Ready for potential promotion."

  deploy_production:
    if: github.event.inputs.deploy_target == 'production'
    # For a strict canary flow, you might add: needs: deploy_canary
    # However, for this lab, allowing direct selection of 'production' via input demonstrates
    # environment protection rules (like manual approval) more directly.
    environment:
      name: production
      url: https://my-app-production.example.com # Example URL
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        # In a real scenario with a build step, you would download a build artifact here
        # instead of just checking out and modifying a source file directly in the deployment job.

      - name: Update version file for Production
        run: |
          echo "Updating app/version.txt to ${{ github.event.inputs.version }} for Production deployment"
          echo "${{ github.event.inputs.version }}" > app/version.txt
          echo "Current version in app/version.txt:"
          cat app/version.txt

      - name: Simulate Production Deployment
        run: |
          echo "🚀 Deploying version ${{ github.event.inputs.version }} to PRODUCTION environment (URL: ${{ job.environment.url }})..."
          # Imagine actual deployment commands here to primary production servers/services
          sleep 10 # Simulate deployment time
          echo "✅ Version ${{ github.event.inputs.version }} notionally live on Production!"
```

---

### Explanation (`canary-production-deploy.yml`):

1.  **`on.workflow_dispatch.inputs`**: 
    *   The workflow is manually triggered.
    *   `version`: A string input for the version tag/number (e.g., `v1.2.3`).
    *   `deploy_target`: A choice input, allowing the user to select either `canary` or `production` when running the workflow.

2.  **Job: `deploy_canary`**
    *   **`if: github.event.inputs.deploy_target == 'canary'`**: This condition ensures the job only runs if "canary" was selected as the deployment target.
    *   **`environment.name: canary`**: Assigns this job to the `canary` GitHub Environment. Students must create this environment in their repository settings (`Settings` > `Environments` > `New environment`).
    *   **`environment.url`**: An optional URL that can be set for the environment, often pointing to where the deployment can be viewed. It's accessible via `job.environment.url` or `steps.<step_id>.outputs.environment_url` if the environment step has an ID.
    *   **`Update version file for Canary`**: This step simulates preparing the new version by updating `app/version.txt`. In a real application, this would involve checking out the correct commit/tag or using a built artifact.
    *   **`Simulate Canary Deployment`**: Echoes messages to simulate deploying to a canary environment. It also shows how to access the environment URL (`${{ job.environment.url }}`).
    *   **`Placeholder for Canary Tests/Monitoring`**: A conceptual step. In a real canary deployment, after deploying to canary, automated tests and monitoring would run to validate the new version before wider rollout.

3.  **Job: `deploy_production`**
    *   **`if: github.event.inputs.deploy_target == 'production'`**: Ensures this job only runs if "production" was selected.
    *   **`environment.name: production`**: Assigns this job to the `production` GitHub Environment. 
        *   **Crucial for Students:** They should configure this environment in repository settings and add a **Protection Rule**, such as "Required reviewers," to enforce a manual approval step before this job can run. This is a key part of a safe production deployment.
    *   **`Update version file for Production`**: Similar to the canary job, updates the version file.
    *   **`Simulate Production Deployment`**: Echoes messages simulating the production deployment.

### How GitHub Environments Enhance This Flow:

*   **Protection Rules**: For the `production` environment, students can set up rules like:
    *   **Required reviewers**: Specific users or teams must approve the deployment before the job runs.
    *   **Wait timer**: A delay before the job starts.
    *   **Deployment branches**: Only allow deployments from specific branches (though less relevant here since we use `workflow_dispatch` and target specific versions/commits conceptually).
*   **Environment Secrets**: Environments can have their own secrets, separate from repository or organization secrets. This is useful for environment-specific credentials (e.g., different database passwords or API keys for canary vs. production).
*   **Deployment History**: The "Environments" tab in the repository shows a history of deployments to each environment.

### Testing the Workflow:

1.  **Create Environments**: Go to Repository `Settings` > `Environments`. Create `canary` and `production`. For `production`, add a "Required reviewers" rule (you can assign yourself as the reviewer for testing).
2.  **Run for Canary**: 
    *   Go to the "Actions" tab, select "Canary and Production Deployment", and click "Run workflow".
    *   Enter a version (e.g., `v1.0.0-canary`).
    *   Select `canary` as the `deploy_target`.
    *   Run. Observe the `deploy_canary` job executing.
3.  **Run for Production (and experience approval)**:
    *   Trigger the workflow again.
    *   Enter a version (e.g., `v1.0.0`).
    *   Select `production` as the `deploy_target`.
    *   Run. The workflow will start, but the `deploy_production` job will pause and show a "Waiting for approval" status. You (or the designated reviewer) will see a notification or can go to the workflow run to approve it.
    *   Once approved, the `deploy_production` job will proceed. 