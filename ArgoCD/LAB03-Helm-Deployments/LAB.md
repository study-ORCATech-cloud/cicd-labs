# Lab Instructions for LAB03: Deploying Applications with Helm Charts via Argo CD

This document provides the detailed step-by-step instructions for deploying and customizing a Helm chart using Argo CD, with a focus on managing custom values via your Git repository.

We will use a public Helm chart, for example, `bitnami/nginx`.

---

## 🚀 Lab Steps

**Phase 1: Prepare Your Git Repository for Helm Values**

1.  **Choose a Public Helm Chart to Deploy:**
    For this lab, we'll use the `nginx` chart from the Bitnami Helm repository as an example.
    *   **Chart:** `nginx`
    *   **Repository URL:** `https://charts.bitnami.com/bitnami`
    You can browse available charts and their default values on [Artifact Hub](https://artifacthub.io/) or the chart provider's documentation.

2.  **Prepare Your Git Repository and Values Directory:**
    a.  Ensure you have a personal Git repository ready (e.g., the one used in LAB02, or a new one). Let's refer to this as `your-git-repo`.
    b.  In your local clone of `your-git-repo`, create a directory named `helm-values` at the root if it doesn't already exist.
        ```bash
        # In the root of your local Git repository (your-git-repo)
        mkdir -p helm-values
        cd helm-values
        ```

3.  **Copy the Provided Custom Values File:**
    The lab materials for `ArgoCD/LAB03-Helm-Deployments/` include a pre-configured values file at `helm-values/my-nginx-values.yaml`. This file is complete and contains sensible defaults.
    a.  Copy this `my-nginx-values.yaml` file from the lab materials (`ArgoCD/LAB03-Helm-Deployments/helm-values/my-nginx-values.yaml`) into the `helm-values` directory within *your own* local Git repository (`your-git-repo/helm-values/`).
    b.  After copying, your structure in `your-git-repo` should include:
        ```
        your-git-repo/
        └── helm-values/
            └── my-nginx-values.yaml
        ```
    c.  Familiarize yourself with the content of `your-git-repo/helm-values/my-nginx-values.yaml`. Notice it provides initial settings for `replicaCount`, `service.type`, `service.nodePort`, etc., and includes commented-out examples for `ingress` and `resources` for further learning.

4.  **Modify Your Custom Values (`your-git-repo/helm-values/my-nginx-values.yaml`):**
    Now, open the `my-nginx-values.yaml` file located in *your* Git repository's `helm-values` directory. You will make the following specific changes as part of this lab's tasks:
    *   **Modify `replicaCount`**:
        Locate the `replicaCount` parameter. It is initially set to `1`. Change its value to `2`.
    *   **Modify `service.nodePort`**:
        Locate the `service` section. Confirm `type` is `NodePort` (which is its initial setting).
        Find the `nodePort` parameter, which is initially set to `30080`. Change its value to `30088`.

    After your modifications, the relevant sections in your `my-nginx-values.yaml` should look like this:
    ```yaml
    # ... (other parts of the file, like image settings, remain as initially provided) ...

    replicaCount: 2

    service:
      type: NodePort
      # ... (port remains 80)
      nodePort: 30088
      # ...
    # ... (other parts of the file, like commented-out ingress/resources, remain) ...
    ```
    Save the file.

5.  **Commit and Push Your Helm Values to Git:**
    a.  Navigate to the root of your local Git repository (`your-git-repo`).
    b.  Add, commit, and push the `helm-values/my-nginx-values.yaml` file:
        ```bash
        git add helm-values/my-nginx-values.yaml
        git commit -m "Customize nginx Helm values for LAB03"
        git push origin main # Or your default branch name
        ```
    c.  Verify on your Git provider (e.g., GitHub) that the `helm-values/my-nginx-values.yaml` file reflects your changes.

**Phase 2: Deploy the Helm Chart with Argo CD using Git-managed Values**

6.  **Create a Target Namespace in Kubernetes:**
    It's good practice to deploy applications into their own namespaces.
    ```bash
    kubectl create namespace helm-nginx-app
    ```

7.  **Deploy Application using Argo CD UI:**
    a.  Go to your Argo CD UI.
    b.  Click **"+ NEW APP"**.
    c.  Fill in the details:
        *   **Application Name:** `my-helm-nginx` (or your choice)
        *   **Project Name:** `default`
        *   **SYNC POLICY:** `Manual`

        *   **SOURCE - Repository URL:** Enter the URL of *your Git repository* (`your-git-repo`, e.g., `https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git`).
        *   **SOURCE - Revision:** `HEAD` (or `main`).
        *   **SOURCE - Path:** Leave this blank or use `.`. (The path to the values file will be specified in the Helm parameters).

        *   **DESTINATION - Cluster URL:** `https://kubernetes.default.svc`
        *   **DESTINATION - Namespace:** `helm-nginx-app`

        *   **HELM Parameters:**
            *   **Source Type:** Select `Helm`.
            *   **Chart:** `nginx`
            *   **Repo URL:** `https://charts.bitnami.com/bitnami` (This is for the chart itself)
            *   **Chart Version:** You can specify a version (e.g., `15.5.1` - check Artifact Hub for current versions) or leave it blank for the latest stable. It's good practice to pin versions for consistency.
            *   **Values Files:** Click "Add" or "Specify Values File" if needed. Provide the path *from the root of your Git repository* to your values file:
                `helm-values/my-nginx-values.yaml`

    d.  Click **"CREATE"**.

8.  **Observe and Sync in Argo CD:**
    a.  Your new application `my-helm-nginx` will appear, likely `Missing` and `OutOfSync`.
    b.  Click on it. You should see Argo CD has detected the chart and intends to use your custom values from your Git repo.
    c.  Click **"SYNC"** and **"SYNCHRONIZE"**.
    d.  Watch as Argo CD deploys the Nginx application using the Helm chart and your overrides. It should become `Healthy` and `Synced`.

9.  **Verify and Access Your Nginx Application:**
    a.  Use `kubectl` to check your resources in the `helm-nginx-app` namespace:
        ```bash
        kubectl get all -n helm-nginx-app
        ```
        You should see resources created by the Helm chart (deployment, service, pods, etc.), and the deployment should have 2 replicas.
    b.  To find the NodePort, run:
        ```bash
        # The service name might vary slightly based on the Helm release name.
        # A common pattern is <RELEASE_NAME>-<CHART_NAME>, e.g., my-helm-nginx-nginx.
        # Use kubectl get svc -n helm-nginx-app to list services if unsure.
        kubectl get svc -n helm-nginx-app -l app.kubernetes.io/instance=my-helm-nginx -o jsonpath='{.items[0].spec.ports[0].nodePort}'
        ```
        This should show `30088`.
    c.  Access your application:
        First, get your Minikube IP:
        ```bash
        minikube ip 
        ```
        Then open in your browser: `http://<MINIKUBE_IP>:<NODE_PORT>` (e.g., `http://<MINIKUBE_IP>:30088`).
        Alternatively, you can try:
        ```bash
        # Replace <SERVICE_NAME> with the actual service name, e.g., my-helm-nginx-nginx
        minikube service -n helm-nginx-app <SERVICE_NAME> --url
        ```
        You should see the Nginx welcome page.

**Phase 3: The GitOps Loop - Modifying Helm Values in Git**

10. **Modify `my-nginx-values.yaml` in Your Git Repository (The GitOps Loop):**
    a.  Open `your-git-repo/helm-values/my-nginx-values.yaml` in your local editor.
    b.  Change `replicaCount` from `2` (which you set earlier) to `3`.
    c.  Commit and push this change to your Git repository:
        ```bash
        git add helm-values/my-nginx-values.yaml
        git commit -m "Update nginx replicaCount to 3 via Helm values"
        git push origin main
        ```

11. **Observe in Argo CD:**
    a.  Go back to the Argo CD UI. After a short period, your `my-helm-nginx` application should show `OutOfSync` status.
    b.  Click on the application. Argo CD will show a diff indicating the change (e.g., in the Deployment resource for replica count).
    c.  Click **"SYNC"** and **"SYNCHRONIZE"** again.
    d.  Argo CD will apply the change. Verify with `kubectl get pods -n helm-nginx-app` that the number of Nginx pods has changed to 3.

---

## ✅ Validation Checklist

- [ ] `helm-values` directory created in your personal Git repository.
- [ ] The provided `my-nginx-values.yaml` (from lab materials) copied into `your-git-repo/helm-values/`.
- [ ] `my-nginx-values.yaml` in your Git repository modified as per lab instructions (`replicaCount: 2`, `service.nodePort: 30088`).
- [ ] Changes to `my-nginx-values.yaml` committed and pushed to your Git repository.
- [ ] `helm-nginx-app` namespace created in Kubernetes.
- [ ] Argo CD application `my-helm-nginx` created:
    -   Source Repository URL points to *your* Git repo.
    -   Helm Chart Repository URL points to `https://charts.bitnami.com/bitnami`, Chart is `nginx`.
    -   Helm Values file path is `helm-values/my-nginx-values.yaml`.
- [ ] Application synced successfully in Argo CD, shows `Healthy` / `Synced`, and Nginx is running with 2 replicas.
- [ ] Able to access the running Nginx application via browser using the correct NodePort (`30088`).
- [ ] Modified `replicaCount` to `3` in `my-nginx-values.yaml` in your Git repo, and pushed the change.
- [ ] Argo CD detected the `OutOfSync` status.
- [ ] Re-synced the application in Argo CD and verified 3 Nginx replicas are running.

---

## 🧹 Cleanup

1.  **Delete the Application from Argo CD:**
    In the Argo CD UI, delete your `my-helm-nginx` application (ensure to check the option to delete resources).
2.  **Delete the Namespace:**
    ```bash
    kubectl delete namespace helm-nginx-app
    ```
3.  **Delete Helm Values from Git (Optional):**
    Remove the `helm-values` directory and its contents from your personal Git repository if you wish.
4.  **Stop Minikube (If Done):**
    ```bash
    minikube stop
    ```

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 