# Solutions for LAB01: Deploying Your First Application with Argo CD

This document provides a recap of the key steps and expected outcomes for deploying your first application using Argo CD. Since this lab primarily involves UI interactions and `kubectl` commands, there are no specific code blocks with `TODO`s to fill in.

---

## Summary of Steps and Expected Outcomes

**1. Verify Argo CD Setup:**
   - **Action:** Check `minikube status`, `kubectl cluster-info`, ensure port-forwarding for Argo CD UI is active, and log in to the Argo CD UI.
   - **Expected Outcome:** Minikube is running, `kubectl` points to Minikube, Argo CD UI is accessible and you are logged in as `admin`.

**2. Create a Namespace for the Guestbook Application:**
   - **Action:** Run `kubectl create namespace guestbook`.
   - **Expected Outcome:** The command executes successfully, and the `guestbook` namespace is created in your Kubernetes cluster. You can verify with `kubectl get ns`.

**3. Create the "guestbook" Application in Argo CD UI:**
   - **Action:** Click "+ NEW APP" in Argo CD UI and fill in the form:
      - **Application Name:** `guestbook`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual`
      - **SOURCE Repository URL:** `https://github.com/argoproj/argocd-example-apps.git`
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** `guestbook`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `guestbook`
   - **Action:** Click "CREATE".
   - **Expected Outcome:** The `guestbook` application appears on the Argo CD dashboard, initially with `Missing` and `OutOfSync` status.

**4. Observe Application Status in Argo CD:**
   - **Action:** Click on the `guestbook` application card to view details.
   - **Expected Outcome:** You can see the application's desired state (resources defined in Git) and its (currently empty) live state. Resources will be listed with `Missing` status.

**5. Manually Sync the Application:**
   - **Action:** In the application details view, click "SYNC", then "SYNCHRONIZE" in the panel.
   - **Expected Outcome:** Argo CD starts deploying the resources. The UI shows the progress, and resource statuses change from `Missing` to various states (e.g., `Progressing`) and finally to `Healthy`. The overall application status becomes `Healthy` and `Synced`.

**6. Verify Deployed Resources with `kubectl`:**
   - **Action:** Run `kubectl get all -n guestbook`.
   - **Expected Outcome:** You see Kubernetes resources like Pods, Services, and Deployments/StatefulSets for the guestbook app (e.g., `guestbook-ui`, `redis-master`, `redis-slave`). Pods should eventually reach `Running` status.

**7. Access the Deployed Guestbook Application:**
   - **Action:** Run `minikube service guestbook-ui -n guestbook`.
   - **Expected Outcome:** Your web browser opens, displaying the guestbook application. You can interact with it (e.g., post a message).

**8. (Conceptual) The GitOps Flow:**
   - **Action:** Understand the explanation provided in the lab `README.md` about how changes in a Git repository would trigger an `OutOfSync` status in Argo CD, prompting a new sync.
   - **Expected Outcome:** Conceptual understanding of the GitOps update cycle.

---

## Cleanup Steps Recap

1.  **Delete Application from Argo CD UI:**
    - Navigate to the `guestbook` application, click "DELETE", check the option to delete target resources, and confirm.
    - **Expected:** Application disappears from Argo CD UI, and associated Kubernetes resources are removed.

2.  **Verify Resource Deletion and Delete Namespace:**
    - `kubectl get all -n guestbook` (should show no resources found).
    - `kubectl delete namespace guestbook`.
    - **Expected:** Namespace `guestbook` is deleted.

3.  **Stop Minikube (Optional):**
    - `minikube stop`.
    - Stop the `kubectl port-forward` command.
    - **Expected:** Minikube VM stops, freeing resources. Port-forwarding ceases.

---

This lab provides the foundational experience of deploying an application with Argo CD. The subsequent labs will build upon these concepts. 