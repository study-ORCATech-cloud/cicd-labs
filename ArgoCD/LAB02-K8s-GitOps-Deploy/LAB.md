# Lab Instructions for LAB02: Deploying Your Own Application from Git with Argo CD

This document provides the detailed step-by-step instructions for deploying your own application using your personal Git repository and Argo CD.

---

## 🚀 Lab Steps

### Phase 1: Prepare Your Application and Git Repository

**1. Review the Provided Application Files:**
   a. Navigate to the `ArgoCD/LAB02-K8s-GitOps-Deploy/` directory and examine the provided files:
      - `app/main.py`: A simple Python Flask application
      - `app/Dockerfile`: Complete Dockerfile to containerize the Flask app
      - `k8s-manifests/deployment.yaml`: Complete Kubernetes Deployment manifest
      - `k8s-manifests/service.yaml`: Complete Kubernetes Service manifest

**2. Build Your Docker Image:**
   a. Open a terminal and navigate to the `ArgoCD/LAB02-K8s-GitOps-Deploy/app/` directory:
      ```bash
      cd ArgoCD/LAB02-K8s-GitOps-Deploy/app/
      ```
   b. Build the Docker image (replace `your-dockerhub-username` with your actual Docker Hub username):
      ```bash
      docker build -t your-dockerhub-username/my-flask-app:v1 .
      ```
   c. **Option 1 - Push to Docker Hub (Recommended):**
      ```bash
      docker login
      docker push your-dockerhub-username/my-flask-app:v1
      ```
   d. **Option 2 - Load into Minikube (Local testing):**
      ```bash
      minikube image load your-dockerhub-username/my-flask-app:v1
      ```

**3. Create Your Personal Git Repository:**
   a. Create a new **public** repository on GitHub (or your preferred Git hosting service)
   b. Name it `my-argocd-app` (or any name you prefer)
   c. Do NOT initialize it with README, .gitignore, or license files
   d. Note the repository URL (e.g., `https://github.com/your-username/my-argocd-app.git`)

**4. Prepare Your Local Git Repository:**
   a. Create a new directory on your local machine:
      ```bash
      mkdir my-argocd-app-local
      cd my-argocd-app-local
      ```
   b. Copy the provided files from the lab directory:
      ```bash
      # Copy the app directory
      cp -r ../path-to-cicd-labs/ArgoCD/LAB02-K8s-GitOps-Deploy/app .
      # Copy the k8s-manifests directory
      cp -r ../path-to-cicd-labs/ArgoCD/LAB02-K8s-GitOps-Deploy/k8s-manifests .
      ```
   c. Your directory structure should now look like:
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
   a. Open `k8s-manifests/deployment.yaml` in your text editor
   b. Find the line with `image: your-dockerhub-username/my-custom-app:v1`
   c. Change it to match your Docker image name: `image: your-dockerhub-username/my-flask-app:v1`
   d. Find the line with `replicas: 1` and change it to `replicas: 2`
   e. Save the file

**6. Initialize and Push to Git:**
   a. Initialize a Git repository:
      ```bash
      git init -b main
      git add .
      git commit -m "Initial commit: Flask app with Kubernetes manifests"
      ```
   b. Connect to your remote repository (replace with your actual repository URL):
      ```bash
      git remote add origin https://github.com/your-username/my-argocd-app.git
      git push -u origin main
      ```
   c. Verify your files are visible in your Git repository on the web

### Phase 2: Deploy with Argo CD

**7. Create a Kubernetes Namespace:**
   ```bash
   kubectl create namespace my-flask-app
   ```

**8. Create the Application in Argo CD:**
   a. Open the Argo CD UI in your browser
   b. Click **"+ NEW APP"** button
   c. Fill in the application details:
      - **Application Name:** `my-flask-app`
      - **Project Name:** `default`
      - **SYNC POLICY:** `Manual`
      - **SOURCE Repository URL:** Your Git repository URL (e.g., `https://github.com/your-username/my-argocd-app.git`)
      - **SOURCE Revision:** `HEAD`
      - **SOURCE Path:** `k8s-manifests`
      - **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
      - **DESTINATION Namespace:** `my-flask-app`
   d. Click **"CREATE"**

**9. Synchronize the Application:**
   a. Your new application will appear with `Missing` and `OutOfSync` status
   b. Click on the application card to open its detailed view
   c. Click the **"SYNC"** button
   d. Click **"SYNCHRONIZE"** in the confirmation dialog
   e. Watch as Argo CD deploys your application
   f. Wait for the status to change to `Healthy` and `Synced`

**10. Verify the Deployment:**
   a. Check the deployed resources:
      ```bash
      kubectl get all -n my-flask-app
      ```
   b. You should see:
      - 1 deployment named `my-custom-app-deployment`
      - 2 pods (since we set replicas to 2)
      - 1 service named `my-custom-app-service`
   c. Wait for all pods to be in `Running` status

**11. Access Your Application:**
   a. Find the NodePort assigned to your service:
      ```bash
      kubectl get svc my-custom-app-service -n my-flask-app -o jsonpath='{.spec.ports[0].nodePort}'
      ```
   b. Get your Minikube IP:
      ```bash
      minikube ip
      ```
   c. Open your browser and navigate to: `http://<MINIKUBE_IP>:<NODE_PORT>`
   d. You should see the message: "Hello, Argo CD User! Welcome to your own deployed app."

### Phase 3: Experience the GitOps Loop

**12. Make a Change via Git:**
   a. Open `k8s-manifests/deployment.yaml` in your local repository
   b. Change `replicas: 2` to `replicas: 3`
   c. Save the file and commit the change:
      ```bash
      git add k8s-manifests/deployment.yaml
      git commit -m "Scale up to 3 replicas"
      git push origin main
      ```

**13. Observe Argo CD Detecting the Change:**
   a. Go back to the Argo CD UI
   b. After a few minutes, your application should show `OutOfSync` status
   c. Click on the application to see the detected changes
   d. You'll see a diff showing the replica count change

**14. Synchronize the Changes:**
   a. Click **"SYNC"** and then **"SYNCHRONIZE"**
   b. Watch as Argo CD applies the changes
   c. Verify the change was applied:
      ```bash
      kubectl get pods -n my-flask-app
      ```
   d. You should now see 3 running pods instead of 2

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
   a. In the Argo CD UI, click on your `my-flask-app` application
   b. Click the **"DELETE"** button (usually represented by three dots menu)
   c. Check the option to **"Delete resources"** to remove Kubernetes resources
   d. Confirm the deletion

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