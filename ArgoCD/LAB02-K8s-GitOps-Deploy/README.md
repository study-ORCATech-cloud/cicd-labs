# LAB02: Deploying Your Own Application from Git with Argo CD

Welcome to Lab 02! In the previous lab, you deployed a sample application from a public Git repository using Argo CD. Now, it's time to take the next step: deploying an application that you manage in your own Git repository.

This lab will guide you through using a provided simple "Hello World" Python Flask application and its Dockerfile, building your own Docker image, modifying provided Kubernetes manifests, pushing everything to your personal Git repository, and then configuring Argo CD to deploy and manage it.

---

## 🎯 Objectives

By the end of this lab, you will be able to:
- Understand how to use provided application code and a `Dockerfile`.
- Build a custom Docker image and push it to a container registry (like Docker Hub) or load it into Minikube.
- Modify existing, complete Kubernetes `Deployment` and `Service` manifests to suit your image and desired configuration.
- Structure your Git repository to hold your application code and Kubernetes manifests.
- Configure Argo CD to connect to your Git repository and deploy your application.
- Understand how Argo CD detects changes in your Git repository.
- Manually synchronize changes from Git to your Kubernetes cluster using Argo CD.

---

## 🧰 Prerequisites

- **Completion of LAB01:** You should be familiar with the Argo CD UI and basic operations.
- **Minikube and Argo CD Running:** As per the `ArgoCD/install-and-setup.md` guide.
- **`kubectl` Configured:** Pointing to your Minikube cluster.
- **Git Installed and Configured:** You'll need Git to manage your application code and push it to a repository. ([Download Git](https://git-scm.com/downloads)).
- **A Personal Git Repository Host Account:** Such as GitHub ([github.com](https://github.com)), GitLab ([gitlab.com](https://gitlab.com)), or Bitbucket. This lab will use GitHub for examples.
- **Docker Installed and Running:** You'll need Docker to build your application image. ([Install Docker](https://docs.docker.com/get-docker/)).
- **(Optional but Recommended) Docker Hub Account:** Or an account with another container registry if you plan to push your image.
- **Basic understanding of Docker and Kubernetes concepts.**

---

## 📂 Folder Structure Provided

The necessary files for this lab are provided within the `ArgoCD/LAB02-K8s-GitOps-Deploy/` directory:

```
ArgoCD/LAB02-K8s-GitOps-Deploy/
├── app/
│   ├── main.py         # Complete Python Flask application
│   └── Dockerfile      # Complete Dockerfile to containerize the app
├── k8s-manifests/
│   ├── deployment.yaml # Complete Kubernetes Deployment manifest (you will modify this)
│   └── service.yaml    # Complete Kubernetes Service manifest (you will inspect this)
└── README.md         # Lab instructions (this file)
```
You will be guided to copy these into your own Git repository structure.

---

## 🚀 Lab Steps

**Phase 1: Prepare Your Application Image and Customize Manifests**

1.  **Review Provided Application Files:**
    *   Familiarize yourself with `app/main.py` (a simple Flask app) and `app/Dockerfile` (which containerizes it). These are provided as complete and functional.

2.  **Build and Push/Load Your Docker Image:**
    a.  Navigate to the `ArgoCD/LAB02-K8s-GitOps-Deploy/app/` directory in your terminal.
    b.  Build the Docker image. **Replace `your-dockerhub-username/my-custom-app` with your actual Docker Hub username (or another registry prefix) and a chosen image name like `my-k8s-argo-app`.** Use a tag like `v1`.
        ```bash
        docker build -t your-dockerhub-username/my-k8s-argo-app:v1 .
        ```
        *Example if your Docker Hub username is `cooldev`*: `docker build -t cooldev/my-k8s-argo-app:v1 .`
    c.  **Option 1 (Push to Registry - Recommended for GitOps):**
        Log in to your Docker registry (e.g., Docker Hub) and push the image.
        ```bash
        docker login 
        docker push your-dockerhub-username/my-k8s-argo-app:v1
        ```
    d.  **Option 2 (Load into Minikube - Simpler for local testing):**
        If you prefer not to use a remote registry for this lab, you can load the image directly into Minikube's Docker daemon:
        ```bash
        minikube image load your-dockerhub-username/my-k8s-argo-app:v1
        ```
        *(If you use this option, ensure `imagePullPolicy` in `deployment.yaml` is `IfNotPresent` or `Never`)*. The provided `deployment.yaml` defaults to `IfNotPresent`.

3.  **Prepare Your Git Repository:**
    a.  Create a new **public** repository on your Git hosting service (e.g., GitHub). Let's call it `my-argo-lab-repo` (or your choice). **Do NOT initialize it with a README, .gitignore, or license yet.**
    b.  On your local machine, create a new directory for your repository, for example `my-argo-lab-repo-local`.
        ```bash
        mkdir my-argo-lab-repo-local
        cd my-argo-lab-repo-local
        ```
    c.  Copy the provided `app/` and `k8s-manifests/` directories from `cicd-labs/ArgoCD/LAB02-K8s-GitOps-Deploy/` into your new `my-argo-lab-repo-local/` directory. Your structure should now be:
        ```
        my-argo-lab-repo-local/
        ├── app/
        │   ├── main.py
        │   └── Dockerfile
        └── k8s-manifests/
            ├── deployment.yaml
            └── service.yaml
        ```

4.  **Customize Kubernetes Manifests:**
    You will now modify the provided, complete Kubernetes manifests to use your Docker image and set a desired replica count.

    a.  **Modify `k8s-manifests/deployment.yaml`:**
        Open `my-argo-lab-repo-local/k8s-manifests/deployment.yaml` in your editor.
        *   **Update the image name:**
            Locate the line `image: your-dockerhub-username/my-custom-app:v1`.
            Change this to the **exact image name and tag you used in Step 2b** (e.g., `your-dockerhub-username/my-k8s-argo-app:v1`).
        *   **Update replica count:**
            Locate the line `replicas: 1`.
            Change the value from `1` to `2`.
        *   **(Optional) Adjust `imagePullPolicy`:**
            The file defaults to `imagePullPolicy: IfNotPresent`.
            If you pushed your image to a public registry and want to ensure it's always pulled, you could change this to `Always`. If you used `minikube image load` and your image tag might not change, `IfNotPresent` or `Never` is fine. For this lab, `IfNotPresent` is a safe default.
        Save the `deployment.yaml` file.

    b.  **Review `k8s-manifests/service.yaml`:**
        Open `my-argo-lab-repo-local/k8s-manifests/service.yaml`. This file is provided complete and configured to expose your application using a `NodePort`. For this lab, no changes are strictly required here, but review it to understand how it selects the pods (via `selector: app: my-custom-app`) and exposes the application's `targetPort: 5000`.

5.  **Initialize Git Repository and Push:**
    a.  Navigate to the root of your local `my-argo-lab-repo-local/` directory in your terminal.
    b.  Initialize a Git repository, add all files, commit, and push to your remote repository:
        ```bash
        git init -b main
        git add .
        git commit -m "Initial commit: Flask app, Dockerfile, and customized k8s manifests"
        git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPOSITORY_NAME>.git # Replace with your repo URL
        git push -u origin main
        ```
    c.  Verify your files are on your Git hosting service.

**Phase 2: Deploy with Argo CD**

6.  **Create a Namespace for Your Custom Application:**
    In your terminal (connected to Minikube):
    ```bash
    kubectl create namespace my-custom-app-ns
    ```

7.  **Deploy Application using Argo CD UI:**
    a.  Go to your Argo CD UI.
    b.  Click **"+ NEW APP"**.
    c.  Fill in the details:
        *   **Application Name:** `my-k8s-app` (or your choice)
        *   **Project Name:** `default`
        *   **SYNC POLICY:** `Manual`
        *   **SOURCE Repository URL:** Your Git repository URL (e.g., `https://github.com/<YOUR_GITHUB_USERNAME>/my-argo-lab-repo.git`).
        *   **SOURCE Revision:** `HEAD` (or `main`).
        *   **SOURCE Path:** `k8s-manifests` (This tells Argo CD where to find the Kubernetes YAML files within your repository).
        *   **DESTINATION Cluster URL:** `https://kubernetes.default.svc`
        *   **DESTINATION Namespace:** `my-custom-app-ns`
    d.  Click **"CREATE"**.

8.  **Observe and Sync in Argo CD:**
    a.  Your new application `my-k8s-app` will appear, likely `Missing` and `OutOfSync`.
    b.  Click on it, then click **"SYNC"** and **"SYNCHRONIZE"**.
    c.  Watch as Argo CD deploys your application. It should become `Healthy` and `Synced`.

9.  **Verify and Access Your Application:**
    a.  Use `kubectl` to check your resources in the `my-custom-app-ns` namespace:
        ```bash
        kubectl get all -n my-custom-app-ns
        ```
        You should see your deployment (with 2 replicas), pods, and service.
    b.  If you used `NodePort` for your service (default in the provided `service.yaml`), find the port:
        ```bash
        kubectl get svc my-custom-app-service -n my-custom-app-ns -o jsonpath='{.spec.ports[0].nodePort}'
        ```
    c.  Access your application using Minikube's IP and the NodePort:
        ```bash
        minikube ip 
        # Then open in browser: http://<MINIKUBE_IP>:<NODE_PORT>
        # Or, try: minikube service my-custom-app-service -n my-custom-app-ns
        ```
        You should see your "Hello, Argo CD User!" message.

**Phase 3: The GitOps Loop - Making a Change**

10. **Modify Your `deployment.yaml` in Git:**
    a.  Open `my-argo-lab-repo-local/k8s-manifests/deployment.yaml` again.
    b.  **Change `spec.replicas`** from `2` to `3`.
    c.  Commit and push the change to your Git repository:
        ```bash
        git add k8s-manifests/deployment.yaml
        git commit -m "Update replicas to 3"
        git push origin main
        ```

11. **Observe in Argo CD:**
    a.  Go back to the Argo CD UI. After a short period (Argo CD polls Git repositories), your `my-k8s-app` application should show `OutOfSync` status.
    b.  Click on the application. Argo CD will show a diff indicating the change in desired replicas.
    c.  Click **"SYNC"** and **"SYNCHRONIZE"** again.
    d.  Argo CD will apply the change, and you should see the number of pods scale up to 3.
        Verify with `kubectl get pods -n my-custom-app-ns`.

---

## ✅ Validation Checklist

- [ ] Docker image built successfully and pushed to a registry or loaded into Minikube.
- [ ] Local Git repository (`my-argo-lab-repo-local` or similar) created with `app/` and `k8s-manifests/` directories copied into it.
- [ ] `k8s-manifests/deployment.yaml` modified to use your correct Docker image name and tag.
- [ ] `k8s-manifests/deployment.yaml` modified to set `replicas: 2`.
- [ ] Changes committed and pushed to your remote Git repository.
- [ ] `my-custom-app-ns` namespace created in Kubernetes.
- [ ] Argo CD application `my-k8s-app` (or your chosen name) created, pointing to your Git repository and `k8s-manifests` path.
- [ ] Application synced successfully in Argo CD and shows `Healthy` / `Synced` status with 2 replicas.
- [ ] Able to access your running application via browser.
- [ ] Changed `replicas` to `3` in `deployment.yaml`, pushed to Git.
- [ ] Argo CD detected the `OutOfSync` status.
- [ ] Re-synced the application in Argo CD and verified 3 replicas are running.

---

## 🧹 Cleanup

1.  **Delete the Application from Argo CD:**
    In the Argo CD UI, delete your `my-k8s-app` application (ensure to check the option to delete resources).
2.  **Delete the Namespace:**
    ```bash
    kubectl delete namespace my-custom-app-ns
    ```
3.  **Delete the Docker Image (Optional):**
    If you pushed to a registry, you can delete it from there or use `docker rmi your-dockerhub-username/my-k8s-argo-app:v1` to remove from local Docker images.
4.  **Delete the Git Repository (Optional):**
    Delete the repository from your Git hosting service and remove the local directory (`my-argo-lab-repo-local`).
5.  **Stop Minikube (If Done):**
    ```bash
    minikube stop
    ```

---

## 🚀 What's Next?

Congratulations! You've successfully set up a GitOps workflow for your own application by modifying provided manifests and using Argo CD.

Proceed to **[../LAB03-Helm-Deployments/README.md](../LAB03-Helm-Deployments/README.md)** to explore how to use Helm charts with Argo CD.

Git-driven Kubernetes. 🌱💾🚢