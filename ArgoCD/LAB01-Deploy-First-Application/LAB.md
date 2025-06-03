# Lab Instructions for LAB01: Deploying Your First Application with Argo CD

This document provides the detailed step-by-step instructions for completing Lab 01.

---

## 🚀 Lab Steps

**1. Verify Argo CD Setup:**
   a. Ensure your Minikube cluster is running: `minikube status`
   b. Ensure `kubectl` is configured for Minikube: `kubectl cluster-info`
   c. Ensure the Argo CD UI port-forward is active (from the setup guide, typically `kubectl port-forward svc/argocd-server -n argocd 8080:443`).
   d. Open the Argo CD UI in your browser (e.g., [https://localhost:8080/](https://localhost:8080/)) and log in with the `admin` user and the password you set during setup.

**2. Create a Namespace for the Guestbook Application:**
   Argo CD will deploy the guestbook application into a specific namespace. Let's create it first.
   Open your terminal and run:
   ```bash
   kubectl create namespace guestbook
   ```

**3. Create the "guestbook" Application in Argo CD UI:**
   a. In the Argo CD UI, click the **"+ NEW APP"** button (usually found in the top left).
   b. You will be presented with the "Create Application" form. Fill it in as follows:

      *   **Application Name:** `guestbook`
      *   **Project Name:** Select `default` from the dropdown (this is the built-in project).
      *   **SYNC POLICY:** Select `Manual`.
          *   *(This means Argo CD will detect changes but won't automatically apply them until you click "Sync").*

      *   **SOURCE Repository URL:** 
          ```
          https://github.com/argoproj/argocd-example-apps.git
          ```
      *   **SOURCE Revision:** `HEAD`
      *   **SOURCE Path:** `guestbook`

      *   **DESTINATION Cluster URL:** Select `https://kubernetes.default.svc` (this represents the same cluster where Argo CD is running).
      *   **DESTINATION Namespace:** `guestbook`

   c. After filling in these details, click the **"CREATE"** button at the top of the form.

**4. Observe Application Status in Argo CD:**
   a. You should now see a new card for the `guestbook` application on the Argo CD dashboard.
   b. Initially, its status will likely show as `Missing` and `OutOfSync` (represented by icons and text). This is because Argo CD knows about the application definition, but the resources don't exist in the cluster yet, and their state in Git doesn't match the live state (which is nothing).
   c. Click on the `guestbook` application card to go to its detailed view.
   d. Explore this view. You'll see:
      *   A tree-like structure of the Kubernetes resources defined in the Git repository (Deployments, Services, etc.).
      *   Their current health and sync status.
      *   Information about the source Git repository and destination cluster.

**5. Manually Sync the Application:**
   Now, let's tell Argo CD to deploy the application resources to your Minikube cluster.
   a. In the `guestbook` application's detailed view, click the **"SYNC"** button (usually near the top).
   b. A "Synchronize application" panel will appear. You can review the parameters.
   c. Click the **"SYNCHRONIZE"** button at the bottom of the panel.
   d. Argo CD will now apply the manifests from the Git repository to your cluster. You can observe the progress in the UI as resources are created and their status updates.
   e. Wait for the overall application status to change to `Healthy` and `Synced` (green checkmarks).

**6. Verify Deployed Resources with `kubectl`:**
   Switch to your terminal and verify that the guestbook application's resources have been created in the `guestbook` namespace:
   ```bash
   kubectl get all -n guestbook
   ```
   You should see Pods, Services, and Deployments (or StatefulSets depending on the exact example version) related to the guestbook application (e.g., `guestbook-ui`, `redis-master`, `redis-slave`). Wait for the Pods to be in the `Running` state.

**7. Access the Deployed Guestbook Application:**
   The guestbook application has a frontend service (`guestbook-ui`) that needs to be accessed.
   a. Use Minikube to easily open this service in your browser:
      ```bash
      minikube service guestbook-ui -n guestbook
      ```
      *(Note: If the service name in the example app differs slightly, adjust the command. You can find the service name from `kubectl get svc -n guestbook`.)*
   b. This command should open your default web browser to the guestbook application's URL. You should be able to interact with it (e.g., submit messages).

**8. (Conceptual) The GitOps Flow:**
   At this point, you've deployed an application declaratively from Git. If this were your own application hosted in your own Git repository:
   *   Any changes you make to the Kubernetes manifests in that Git repository (e.g., updating an image version, changing replicas) and commit/push would be detected by Argo CD.
   *   The application in Argo CD would show an `OutOfSync` status.
   *   You (or an automated process, if auto-sync were enabled) would then sync the application to apply those changes to your cluster.
   This is the essence of the GitOps workflow, which you will explore further in subsequent labs.

---

## ✅ Validation Checklist

- [ ] Created the `guestbook` namespace using `kubectl`.
- [ ] Successfully created the `guestbook` application in the Argo CD UI, pointing to the public example repository.
- [ ] Observed the initial `Missing` / `OutOfSync` status of the application.
- [ ] Manually synced the application using the Argo CD UI.
- [ ] Observed the application status change to `Healthy` and `Synced`.
- [ ] Verified the creation of Kubernetes resources (Pods, Services, etc.) in the `guestbook` namespace using `kubectl get all -n guestbook`.
- [ ] Accessed the running guestbook application in your browser using `minikube service`.

---

## 🧹 Cleanup

It's important to clean up resources to keep your Minikube environment tidy.

1.  **Delete the Application from Argo CD:**
    a. In the Argo CD UI, navigate to the `guestbook` application.
    b. Click the "DELETE" button (often represented by three dots or a trash icon, then select Delete).
    c. In the confirmation dialog, you can usually check an option like "Delete target resources" or similar to ensure the Kubernetes resources deployed by this application are also removed from the cluster. Confirm the deletion.
    d. Wait for Argo CD to delete the application and its resources. The application card should disappear from the dashboard.

2.  **Verify Resource Deletion and Delete Namespace:**
    Check if the resources in the `guestbook` namespace are gone:
    ```bash
    kubectl get all -n guestbook
    ```
    You should see "No resources found." or very few remaining (sometimes finalizers take a moment).
    Now, delete the namespace:
    ```bash
    kubectl delete namespace guestbook
    ```

3.  **Stop Minikube (If Done with Kubernetes for Now):**
    If you are finished with Kubernetes tasks for the session, you can stop your Minikube cluster to save system resources:
    ```bash
    minikube stop
    ```
    Remember to also stop the `kubectl port-forward` command for the Argo CD UI if it's still running in another terminal.

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 