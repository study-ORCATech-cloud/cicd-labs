# Argo CD: Local Setup Guide with Minikube

Welcome to the Argo CD GitOps track! This guide will walk you through setting up a local Kubernetes environment using Minikube and installing Argo CD into it. This setup will allow you to complete all the labs in this section, giving you hands-on experience with GitOps principles and Argo CD.

**Follow these instructions carefully to prepare your local Argo CD environment before starting any of the Argo CD labs.**

---

## 🎯 What You'll Achieve

By following this guide, you will have:
- Installed `kubectl`, the Kubernetes command-line tool.
- Installed Minikube for running a local single-node Kubernetes cluster.
- A running Minikube Kubernetes cluster.
- Argo CD installed within your Minikube cluster.
- Accessed the Argo CD web UI and logged in.
- (Optional) Installed the Argo CD CLI.

---

## 🧰 Prerequisites

Before you begin, ensure your system meets the following requirements:

-   **Hardware Virtualization:** This **must be enabled** in your system's BIOS/UEFI settings. Minikube relies on virtualization to run the Kubernetes node as a virtual machine or container.
-   **Sufficient System Resources:** 
    *   At least 2 CPUs (4 recommended for better performance during labs).
    *   At least 4GB of free RAM (8GB recommended).
    *   At least 20GB of free disk space.
-   **Compatible Operating System:** Windows 10/11, macOS, or Linux.
-   **Hypervisor (or Container Runtime for Docker driver):**
    *   **Windows:** Hyper-V (often available in Pro/Enterprise/Education editions), VirtualBox, or Docker Desktop (Minikube can use the Docker driver).
    *   **macOS:** HyperKit (comes with Docker Desktop), VirtualBox, or VMware Fusion.
    *   **Linux:** KVM, VirtualBox, or Docker (Minikube can use the Docker driver).
-   **Internet Access:** To download Minikube, `kubectl`, Kubernetes container images, and Argo CD manifests.
-   **Web Browser:** A modern web browser (e.g., Chrome, Firefox, Edge).
-   **Basic Command-Line/Terminal Proficiency.**
-   **Administrator/sudo Privileges:** May be required for installing some tools or drivers.

---

## ⚙️ Installation and Setup Steps

Follow these steps sequentially to set up your environment.

### Step 1: Install `kubectl` (Kubernetes Command-Line Tool)

`kubectl` allows you to run commands against Kubernetes clusters.

-   **Instructions:** Follow the official Kubernetes documentation to install `kubectl` for your specific operating system:
    *   [Install kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
    *   [Install kubectl on macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
    *   [Install kubectl on Windows](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
-   **Verification:** After installation, open a new terminal and run:
    ```bash
    kubectl version --client
    ```
    You should see the client version of `kubectl` printed.

### Step 2: Install Minikube

Minikube is a tool that lets you run a single-node Kubernetes cluster locally on your personal computer.

-   **Instructions:** Follow the official Minikube installation guide:
    *   [Minikube Start Guide](https://minikube.sigs.k8s.io/docs/start/)
    This guide covers installation for Windows, macOS, and Linux, and discusses choosing a hypervisor/driver (e.g., Docker, VirtualBox, Hyper-V, KVM).
    *   **Driver Choice:** If you have Docker Desktop installed, using the `docker` driver is often the simplest: `minikube start --driver=docker`.
-   **Verification:** After installation, open a new terminal and run:
    ```bash
    minikube version
    ```

### Step 3: Start Your Minikube Kubernetes Cluster

Now, start Minikube. This will download necessary images and set up your local Kubernetes cluster.

-   **Command:**
    ```bash
    # Recommended: Allocate sufficient resources. Adjust based on your system.
    minikube start --cpus=4 --memory=4096m 
    # If you want to specify a driver (e.g., docker, hyperv, kvm2, virtualbox):
    # minikube start --cpus=4 --memory=4096m --driver=<your_chosen_driver>
    ```
    This process might take several minutes the first time.
-   **Verification:**
    *   Check Minikube status:
        ```bash
        minikube status
        ```
        You should see `host`, `kubelet`, `apiserver`, and `kubeconfig` statuses, typically as `Running` or `Configured`.
    *   Check cluster information with `kubectl` (Minikube automatically configures `kubectl` to point to the new cluster):
        ```bash
        kubectl cluster-info
        ```
    *   (Optional) Access the Kubernetes Dashboard provided by Minikube:
        ```bash
        minikube dashboard
        ```
        This will open the dashboard in your web browser. Close the terminal running the dashboard or press `Ctrl+C` to stop it when done.

### Step 4: Install Argo CD into Minikube

With your Kubernetes cluster running, you can now install Argo CD.

1.  **Create a Namespace for Argo CD:**
    ```bash
    kubectl create namespace argocd
    ```
2.  **Apply the Argo CD Installation Manifest:**
    This command deploys Argo CD components using the latest stable manifest.
    ```bash
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```
3.  **Verify Argo CD Pods:**
    Wait for all Argo CD pods to be up and running. This might take a few minutes.
    ```bash
    kubectl get pods -n argocd -w
    ```
    Look for pods like `argocd-server-*`, `argocd-repo-server-*`, `argocd-application-controller-*`, etc., to reach `Running` status. Press `Ctrl+C` to stop watching once they are ready.

### Step 5: Access the Argo CD Web UI

Argo CD's UI is not exposed externally by default. Use `kubectl port-forward` to access it.

1.  **Port-Forward the Argo CD Server Service:**
    Open a **new terminal window** (as this command will run continuously) and execute:
    ```bash
    kubectl port-forward svc/argocd-server -n argocd 8080:443
    ```
    This command forwards requests from your local machine's port `8080` to the `argocd-server` service's port `443` (HTTPS) inside the cluster.
    *Keep this terminal window open while you are using the Argo CD UI.*

2.  **Open Argo CD UI in Browser:**
    Navigate to the following URL in your web browser:
    [https://localhost:8080/](https://localhost:8080/)
    *   **Note:** You will likely see a browser warning about an insecure connection or an invalid certificate ("Your connection is not private"). This is because Argo CD uses a self-signed certificate by default. It is safe to proceed for local lab purposes (usually by clicking "Advanced" and then "Proceed to localhost (unsafe)" or similar wording depending on your browser).

### Step 6: Log In to Argo CD

1.  **Retrieve the Initial Admin Password:**
    The initial password for the `admin` user is auto-generated and stored in a Kubernetes secret. Run this command in your terminal:
    ```bash
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
    ```
    This will print the password to your console.

2.  **Log In:**
    *   **Username:** `admin`
    *   **Password:** Use the password you retrieved from the previous step.
    Click "SIGN IN" on the Argo CD UI.

3.  **(Highly Recommended) Change the Admin Password:**
    Once logged in, it's crucial to change the default admin password.
    *   In the Argo CD UI, navigate to `User Info` (usually an icon/avatar in the bottom left or top right) -> `Update password`.
    *   Enter the current (initial) password and your new desired password.

### Step 7: (Optional) Install Argo CD CLI

The Argo CD CLI (`argocd`) can be very useful for managing Argo CD from the command line.

-   **Instructions:** Follow the official Argo CD CLI installation documentation:
    *   [Argo CD CLI Installation](https://argo-cd.readthedocs.io/en/stable/cli_installation/)
-   **Log In with CLI (after changing password via UI or if you want to change it via CLI):**
    Once the CLI is installed and you've port-forwarded the server (Step 5.1), you can log in:
    ```bash
    # Replace <NEW_PASSWORD_YOU_SET> with the password you set in the UI.
    argocd login localhost:8080 --username admin --password <NEW_PASSWORD_YOU_SET> --insecure
    ```
    *   The `--insecure` flag is needed because of the self-signed certificate used with local port-forwarding.
    *   You can also use the CLI to change the password: `argocd account update-password` (after logging in with the initial password).

---

## ✨ Key Concepts (A Brief Overview)

-   **Kubernetes (`k8s`):** An open-source system for automating deployment, scaling, and management of containerized applications.
-   **Minikube:** A tool to run a single-node Kubernetes cluster locally for development and testing.
-   **`kubectl`:** The command-line interface for interacting with a Kubernetes cluster.
-   **GitOps:** A way of implementing Continuous Delivery for cloud-native applications. It uses Git as a single source of truth for declarative infrastructure and applications.
-   **Argo CD:** A declarative, GitOps continuous delivery tool for Kubernetes. It monitors Git repositories and automatically deploys and synchronizes application changes to your Kubernetes cluster.
    *   **Application:** The core Argo CD resource representing a set of Kubernetes manifests to be deployed.
    *   **Sync:** The process of reconciling the live state in the cluster with the desired state in Git.
    *   **Health Status:** Argo CD assesses the health of your deployed applications based on Kubernetes resource status.

---

## 🧹 Cleanup

When you're finished with an Argo CD lab session or want to free up resources:

1.  **Stop Port-Forwarding:** Go to the terminal window running `kubectl port-forward ...` and press `Ctrl+C`.
2.  **(Optional) Delete Argo CD from Cluster:** If you want to remove Argo CD components but keep Minikube running for other K8s work:
    ```bash
    # Ensure you use the same manifest version you installed with, or simply delete the namespace
    # kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    # A more thorough way to remove everything Argo CD related in its namespace:
    kubectl delete namespace argocd
    ```
3.  **Stop the Minikube Cluster:** This stops the Kubernetes VM/container but preserves its state.
    ```bash
    minikube stop
    ```
4.  **(Optional) Delete the Minikube Cluster:** This completely removes the cluster and all its data. You'll have to run `minikube start` again to recreate it.
    ```bash
    minikube delete
    ```

---

## 🚀 Next Steps

You have now successfully set up Minikube and installed Argo CD! You are ready to proceed with the labs.

Start with **[LAB01-Deploy-First-Application/README.md](./LAB01-Deploy-First-Application/README.md)**. This lab will guide you through deploying your first application using Argo CD and experiencing the core GitOps workflow.

Enjoy your GitOps journey with Argo CD! 🚢🔄⚙️ 