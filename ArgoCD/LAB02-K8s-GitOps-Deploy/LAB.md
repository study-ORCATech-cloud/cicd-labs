# Lab Instructions for LAB02: Deploying Your Own Application from Git with Argo CD

This document provides the detailed step-by-step instructions for deploying your own application using your personal Git repository and Argo CD.

---

## 🚀 Lab Steps

### Phase 1: Prepare Your Application and Git Repository

**1. Review the Provided Application Files:**
   * Navigate to the `ArgoCD/LAB02-K8s-GitOps-Deploy/` directory and examine the provided files:
      - `app/main.py`: A simple Python Flask application
      - `app/Dockerfile`: Complete Dockerfile to containerize the Flask app
      - `k8s-manifests/deployment.yaml`: Complete Kubernetes Deployment manifest
      - `k8s-manifests/service.yaml`: Complete Kubernetes Service manifest

**2. Build Your Docker Image:**
   * Open a terminal and navigate to the `ArgoCD/LAB02-K8s-GitOps-Deploy/app/` directory:
      ```bash
      cd ArgoCD/LAB02-K8s-GitOps-Deploy/app/
      ```
   * Build the Docker image (replace `your-dockerhub-username` with your actual Docker Hub username):
      ```bash
      docker build -t your-dockerhub-username/my-flask-app:v1 .
      ```
   * **Option 1 - Push to Docker Hub (Recommended):**
      ```bash
      docker login
      docker push your-dockerhub-username/my-flask-app:v1
      ```
   * **Option 2 - Load into Minikube (Local testing):**
      ```bash
      minikube image load your-dockerhub-username/my-flask-app:v1
      ```

**3. Create Your Personal Git Repository:**
   * Create a new **public** repository on GitHub (or your preferred Git hosting service)
   * Name it `my-argocd-app` (or any name you prefer)
   * Do NOT initialize it with README, .gitignore, or license files
   * Note the repository URL (e.g., `https://github.com/your-username/my-argocd-app.git`)

**4. Prepare Your Local Git Repository:**
   * Create a new directory on your local machine:
      ```bash
      mkdir my-argocd-app-local
      cd my-argocd-app-local
      ```
   * Copy the provided files from the lab directory:
      ```bash
      # Copy the app directory
      cp -r ../path-to-cicd-labs/ArgoCD/LAB02-K8s-GitOps-Deploy/app .
      # Copy the k8s-manifests directory
      cp -r ../path-to-cicd-labs/ArgoCD/LAB02-K8s-GitOps-Deploy/k8s-manifests .
      ```
   * Your directory structure should now look like:
      ```
      my-argocd-app-local/
      ├── app/
      │   ├── main.py
      │   └── Dockerfile
      └── k8s-manifests/
          ├── deployment.yaml
          └── service.yaml
      ```

**5. Modify the Kubernetes Manifest for Your Image:**
   * Open `k8s-manifests/deployment.yaml` in your text editor
   * Find the line with `image: your-dockerhub-username/my-custom-app:v1`
   * Change it to match your Docker image name: `image: your-dockerhub-username/my-flask-app:v1`
   * Find the line with `replicas: 1` and change it to `replicas: 2`
   * Save the file

**6. Initialize and Push to Git:**
   * Initialize a Git repository:
      ```bash
      git init -b main
      git add .
      git commit -m "Initial commit: Flask app with Kubernetes manifests"
      ```
   * Connect to your remote repository (replace with your actual repository URL):
      ```bash
      git remote add origin https://github.com/your-username/my-argocd-app.git
      git push -u origin main
      ```
   * Verify your files are visible in your Git repository on the web

### Phase 2: Deploy with Argo CD

**7. Create a Kubernetes Namespace:**
   ```bash
   kubectl create namespace my-flask-app
   ```

**8. Create the Application in Argo CD:**
   * Open the Argo CD UI in your browser
   * Click **"+ NEW APP"** button
   * Fill in the application details:
      - **Application Name:** `my-flask-app`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual`
      - **SOURCE Repository URL:** Your Git repository URL (e.g., `https://github.com/your-username/my-argocd-app.git`)
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** `k8s-manifests`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `my-flask-app`
   * Click **"CREATE"**

**9. Synchronize the Application:**
   * Your new application will appear with `Missing` and `OutOfSync` status
   * Click on the application card to open its detailed view
   * Click the **"SYNC"** button
   * Click **"SYNCHRONIZE"** in the confirmation dialog
   * Watch as Argo CD deploys your application
   * Wait for the status to change to `Healthy` and `Synced`

**10. Verify the Deployment:**
   * Check the deployed resources:
      ```bash
      kubectl get all -n my-flask-app
      ```
   * You should see:
      - 1 deployment named `my-custom-app-deployment`
      - 2 pods (since we set replicas to 2)
      - 1 service named `my-custom-app-service`
   * Wait for all pods to be in `Running` status

**11. Access Your Application:**
   * Find the NodePort assigned to your service:
      ```bash
      kubectl get svc my-custom-app-service -n my-flask-app -o jsonpath='{.spec.ports[0].nodePort}'
      ```
   * Get your Minikube IP:
      ```bash
      minikube ip
      ```
   * Open your browser and navigate to: `http://<MINIKUBE_IP>:<NODE_PORT>`
   * You should see the message: "Hello, Argo CD User! Welcome to your own deployed app."

### Phase 3: Experience the GitOps Loop

**12. Make a Change via Git:**
   * Open `k8s-manifests/deployment.yaml` in your local repository
   * Change `replicas: 2` to `replicas: 3`
   * Save the file and commit the change:
      ```bash
      git add k8s-manifests/deployment.yaml
      git commit -m "Scale up to 3 replicas"
      git push origin main
      ```

**13. Observe Argo CD Detecting the Change:**
   * Go back to the Argo CD UI
   * After a few minutes, your application should show `OutOfSync` status
   * Click on the application to see the detected changes
   * You'll see a diff showing the replica count change

**14. Synchronize the Changes:**
   * Click **"SYNC"** and then **"SYNCHRONIZE"**
   * Watch as Argo CD applies the changes
   * Verify the change was applied:
      ```bash
      kubectl get pods -n my-flask-app
      ```
   * You should now see 3 running pods instead of 2

---

## ✅ Validation Checklist

- [ ] Successfully built Docker image with your own tag
- [ ] Created personal Git repository and pushed application code
- [ ] Modified deployment.yaml with correct image name and replica count
- [ ] Created namespace `my-flask-app` in Kubernetes
- [ ] Created Argo CD application `my-flask-app` pointing to your Git repository
- [ ] Successfully synchronized the application in Argo CD
- [ ] Application shows `Healthy` and `Synced` status with 2 replicas initially
- [ ] Successfully accessed the Flask application in browser
- [ ] Made change to replica count in Git and pushed the change
- [ ] Argo CD detected the `OutOfSync` status automatically
- [ ] Successfully re-synchronized and verified 3 replicas are running

---

## 🧹 Cleanup

**1. Delete the Application from Argo CD:**
   * In the Argo CD UI, click on your `my-flask-app` application
   * Click the **"DELETE"** button (usually represented by three dots menu)
   * Check the option to **"Delete resources"** to remove Kubernetes resources
   * Confirm the deletion

**2. Delete the Namespace:**
   ```bash
   kubectl delete namespace my-flask-app
   ```

**3. Clean Up Docker Image (Optional):**
   ```bash
   docker rmi your-dockerhub-username/my-flask-app:v1
   ```

**4. Clean Up Git Repository (Optional):**
   - Delete the repository from your Git hosting service
   - Remove the local directory: `rm -rf my-argocd-app-local`

**5. Stop Minikube (If Done):**
   ```bash
   minikube stop
   ```

---

End of Lab Instructions. Return to the main `README.md` for Key Concepts and Next Steps. 