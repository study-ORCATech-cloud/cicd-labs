# Solutions for LAB04 - Deploy to GitHub Pages

This file contains the solutions for the `TODO` items in the `.github/workflows/deploy-pages.yml` workflow file.

---

## `deploy-pages.yml` Solutions

```yaml
name: Deploy Static Site to GitHub Pages

on:
  push:
    branches: [main]

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Pages
        uses: actions/configure-pages@v3

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          # Upload entire repository
          path: './site'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
```

---

### Explanation (`deploy-pages.yml`):

1.  **Trigger Configuration (`on`):**
    *   `on: push: branches: [main]`: The workflow triggers on push events to the `main` branch.

2.  **Permissions (`permissions`):**
    *   `contents: read`: Allows the workflow to read the repository content (checkout code).
    *   `pages: write`: Allows the workflow to write to GitHub Pages (create/update the deployment).
    *   `id-token: write`: Allows the workflow to request an OpenID Connect (OIDC) token, which is used by the `deploy-pages` action for authentication.

3.  **Job: `deploy` (`jobs.deploy`):**
    *   **Environment (`environment`):**
        *   `name: github-pages`: Specifies the deployment environment. This is conventional for GitHub Pages deployments.
        *   `url: ${{ steps.deployment.outputs.page_url }}`: Sets the environment URL to the output of the deployment step. This URL will be displayed on the workflow run summary page after successful deployment.
    *   **Runner OS (`runs-on`):**
        *   `runs-on: ubuntu-latest`: The job runs on the latest Ubuntu runner.
    *   **Steps (`steps`):**
        1.  **`Checkout repository` (`actions/checkout@v3`):** Checks out the repository code so the workflow can access the `site/` directory.
        2.  **`Setup Pages` (`actions/configure-pages@v3`):** Configures the GitHub Pages environment. This action prepares for the deployment, often by setting up necessary environment variables or build configurations if a static site generator were used (though not strictly necessary for plain HTML in this lab, it's good practice).
        3.  **`Upload artifact` (`actions/upload-pages-artifact@v2`):**
            *   This action packages the specified directory as a GitHub Pages artifact.
            *   `with: path: './site'`: Specifies that the contents of the `./site` directory should be uploaded.
        4.  **`Deploy to GitHub Pages` (`actions/deploy-pages@v2`):**
            *   `id: deployment`: Assigns an ID to this step so its outputs (like `page_url`) can be referenced.
            *   This action takes the artifact uploaded by `upload-pages-artifact` and deploys it to GitHub Pages.

### Important Notes for Students:

*   **Enable GitHub Pages:** Before this workflow can deploy your site, you **must** enable GitHub Pages in your repository settings:
    1.  Go to your GitHub repository.
    2.  Click on `Settings` (usually on the top bar or right sidebar).
    3.  In the left sidebar, navigate to `Pages` (under "Code and automation").
    4.  Under "Build and deployment", for the **Source**, select **`GitHub Actions`**.
*   **No `gh-pages` branch needed:** When deploying with `actions/deploy-pages`, you typically don't need to manage a separate `gh-pages` branch yourself. The action handles the deployment process directly.
*   **Site URL:** After a successful deployment, the URL to your GitHub Pages site will be available in the workflow run's summary page (in the `deploy` job, under the `github-pages` environment section). 