# Lab Instructions for LAB03: Deploying Applications with Helm Charts via Argo CD

This document provides the detailed step-by-step instructions for deploying and customizing a Helm chart using Argo CD, with a focus on managing custom values via your Git repository.

We will use the `bitnami/nginx` public Helm chart as our example.

---

## 🚀 Lab Steps

### Phase 1: Prepare Your Git Repository for Helm Values

**1. Choose a Public Helm Chart to Deploy:**
   For this lab, we'll use the `nginx` chart from the Bitnami Helm repository.
   - **Chart:** `nginx`
   - **Repository URL:** `https://charts.bitnami.com/bitnami`
   - You can browse available charts and their documentation on [Artifact Hub](https://artifacthub.io/)

**2. Prepare Your Git Repository:**
   a. Use your existing Git repository from LAB02, or create a new public repository named `my-helm-app`
   b. In your local clone of the repository, create a `helm-values` directory:
      ```bash
      mkdir helm-values
      cd helm-values
      ```

**3. Copy the Provided Helm Values File:**
   a. Copy the provided `my-nginx-values.yaml` file from the lab materials:
      ```bash
      # Copy from the lab materials directory
      cp ../path-to-cicd-labs/ArgoCD/LAB03-Helm-Deployments/helm-values/my-nginx-values.yaml .
      ```
   b. Your directory structure should now look like:
      ```
      your-git-repo/
      └── helm-values/
          └── my-nginx-values.yaml
      ```
   c. Review the file content - it contains configuration for replica count, service type, node port, and other nginx settings

**4. Modify Your Custom Values:**
   a. Open `helm-values/my-nginx-values.yaml` in your text editor
   b. **Change the replica count:**
      - Find the line `replicaCount: 1`
      - Change it to `replicaCount: 2`
   c. **Change the NodePort:**
      - Find the line `nodePort: 30080`
      - Change it to `nodePort: 30088`
   d. Save the file

**5. Commit and Push Your Helm Values:**
   a. Navigate to the root of your Git repository
   b. Add, commit, and push the Helm values file:
      ```bash
      git add helm-values/my-nginx-values.yaml
      git commit -m "Add custom nginx Helm values for LAB03"
      git push origin main
      ```
   c. Verify the file is visible in your Git repository online

### Phase 2: Deploy the Helm Chart with Argo CD

**6. Create a Kubernetes Namespace:**
   ```bash
   kubectl create namespace nginx-helm-app
   ```

**7. Create the Helm Application in Argo CD:**
   a. Open the Argo CD UI in your browser
   b. Click **"+ NEW APP"**
   c. Fill in the application details:
      - **Application Name:** `nginx-helm-app`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual`
      - **SOURCE Repository URL:** Your Git repository URL (e.g., `https://github.com/your-username/my-helm-app.git`)
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** Leave blank or use `.`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `nginx-helm-app`
   d. Configure Helm parameters:
      - **Source Type:** Select `Helm`
      - **Chart:** `nginx`
      - **Repo URL:** `https://charts.bitnami.com/bitnami`
      - **Chart Version:** Leave blank for latest, or specify a version like `15.5.1`
      - **Values Files:** `helm-values/my-nginx-values.yaml`
   e. Click **"CREATE"**

**8. Synchronize the Application:**
   a. Your new application will appear with `Missing` and `OutOfSync` status
   b. Click on the application card to open the detailed view
   c. Click **"SYNC"** and then **"SYNCHRONIZE"**
   d. Watch as Argo CD deploys the Nginx application using your custom Helm values
   e. Wait for the status to become `Healthy` and `Synced`

**9. Verify the Deployment:**
   a. Check the deployed resources:
      ```bash
      kubectl get all -n nginx-helm-app
      ```
   b. You should see 2 nginx pods (as per your replica count setting)
   c. Find the service and its NodePort:
      ```bash
      kubectl get svc -n nginx-helm-app
      ```
   d. The service should be using NodePort 30088

**10. Access Your Nginx Application:**
   a. Get your Minikube IP:
      ```bash
      minikube ip
      ```
   b. Open your browser and navigate to: `http://<MINIKUBE_IP>:30088`
   c. You should see the Nginx welcome page

### Phase 3: Experience the GitOps Loop with Helm

**11. Make a Change via Git:**
   a. Open `helm-values/my-nginx-values.yaml` in your local repository
   b. Change `replicaCount: 2` to `replicaCount: 3`
   c. Save and commit the change:
      ```bash
      git add helm-values/my-nginx-values.yaml
      git commit -m "Scale nginx to 3 replicas"
      git push origin main
      ```

**12. Observe Argo CD Detecting the Change:**
   a. Go back to the Argo CD UI
   b. After a few minutes, your application should show `OutOfSync` status
   c. Click on the application to see the detected changes
   d. You'll see a diff showing the replica count change

**13. Synchronize the Changes:**
   a. Click **"SYNC"** and then **"SYNCHRONIZE"**
   b. Watch as Argo CD applies the changes
   c. Verify the change was applied:
      ```bash
      kubectl get pods -n nginx-helm-app
      ```
   d. You should now see 3 nginx pods running

---

## ✅ Validation Checklist

- [ ] Created `helm-values` directory in your Git repository
- [ ] Copied and modified `my-nginx-values.yaml` with correct replica count and NodePort
- [ ] Committed and pushed Helm values to your Git repository
- [ ] Created namespace `nginx-helm-app` in Kubernetes
- [ ] Created Argo CD application `nginx-helm-app` pointing to Helm chart and your values file
- [ ] Successfully synchronized the application in Argo CD
- [ ] Application shows `Healthy` and `Synced` status with 2 nginx replicas initially
- [ ] Successfully accessed nginx application via browser on port 30088
- [ ] Made change to replica count in Git and pushed the change
- [ ] Argo CD detected the `OutOfSync` status automatically
- [ ] Successfully re-synchronized and verified 3 nginx replicas are running

---

## 🧹 Cleanup

**1. Delete the Application from Argo CD:**
   a. In the Argo CD UI, click on your `nginx-helm-app` application
   b. Click the **"DELETE"** button
   c. Check the option to **"Delete resources"** to remove Kubernetes resources
   d. Confirm the deletion

**2. Delete the Namespace:**
   ```bash
   kubectl delete namespace nginx-helm-app
   ```

**3. Clean Up Git Repository (Optional):**
   - Remove the `helm-values` directory from your Git repository if desired
   - Or keep it for future Helm experiments

**4. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 