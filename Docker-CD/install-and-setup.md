# Docker and Docker Compose: Installation and Setup Guide

Welcome to the Docker-CD track! This guide will walk you through installing Docker and Docker Compose on your local machine. These tools are essential for completing all the labs in this section, allowing you to build, run, manage, and deploy containerized applications.

**Follow these instructions carefully to set up your Docker environment before starting any of the Docker-CD labs.**

---

## 🎯 What You'll Achieve

By following this guide, you will have:
- A working Docker Engine on your system.
- Docker CLI (Command Line Interface) to interact with Docker.
- Docker Compose (specifically the `docker compose` CLI plugin) to manage multi-container applications.
- Verified that your installation is successful and ready for the labs.

---

## 🧰 Prerequisites

Before you begin, ensure your system meets the general requirements for Docker:

-   **Operating System:**
    *   **Windows:** Windows 10/11 (64-bit Pro, Enterprise, or Education editions are typically required for Docker Desktop with Hyper-V; Home editions may use WSL 2 backend).
    *   **macOS:** A recent version of macOS (refer to Docker documentation for specific version compatibility).
    *   **Linux:** Various distributions are supported (e.g., Ubuntu, Debian, Fedora, CentOS). Ensure your kernel version is compatible.
-   **Hardware:** Sufficient RAM (at least 4GB recommended), CPU with virtualization support (often needs to be enabled in BIOS/UEFI), and disk space.
-   **General:**
    *   A modern web browser (for accessing documentation and potential web UIs from labs).
    *   Basic command-line/terminal proficiency.
    *   Internet access (for downloading Docker and container images).
    *   Administrator/sudo privileges on your machine for installation.

--- 

## ⚙️ Installation Methods

Choose the installation method appropriate for your operating system.

### Method 1: Docker Desktop (Recommended for Windows and macOS)

Docker Desktop is an easy-to-install application for your Mac or Windows environment that enables you to build and share containerized applications and microservices. It includes Docker Engine, Docker CLI client, Docker Compose, Kubernetes, and more.

1.  **Download Docker Desktop:**
    *   Go to the official Docker Desktop download page: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
    *   Download the installer appropriate for your operating system (Windows or macOS).

2.  **Install Docker Desktop:**
    *   Run the downloaded installer and follow the on-screen instructions.
    *   **Windows:** The installer might prompt you to enable Hyper-V or WSL 2 features if not already enabled. A system restart may be required.
    *   **macOS:** Typically involves dragging the Docker.app to your Applications folder.

3.  **Start Docker Desktop:**
    *   Once installed, launch Docker Desktop.
    *   Look for the Docker icon in your system tray (Windows) or menu bar (macOS). It will indicate Docker Desktop's status (e.g., starting, running).
    *   Wait for Docker Desktop to show that it is running.

Docker Desktop includes `docker compose` (as a CLI plugin), so no separate Docker Compose installation is usually needed.

### Method 2: Docker Engine and Docker Compose CLI Plugin (Linux)

For Linux, you typically install Docker Engine and then ensure the Docker Compose CLI plugin is available (it's often included with recent Docker Engine installations or can be installed separately).

1.  **Follow Official Docker Documentation for Your Linux Distribution:**
    Docker provides detailed, distribution-specific instructions for installing Docker Engine. It is crucial to follow these official guides as package names and commands can vary.
    *   **Go to the Docker Engine installation overview:** [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
    *   Select your Linux distribution (e.g., Ubuntu, Debian, CentOS, Fedora) from the list and follow the step-by-step instructions.
    *   These instructions typically involve setting up Docker's repository, then installing the Docker packages (`docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`, `docker-compose-plugin`).

2.  **Post-installation Steps for Linux (Important):**
    *   **Manage Docker as a non-root user (Highly Recommended):** By default, the `docker` command requires root privileges (sudo). To run `docker` commands without `sudo`, you need to add your user to the `docker` group.
        ```bash
        sudo groupadd docker  # May already exist
        sudo usermod -aG docker $USER
        ```
        After running these commands, you will need to **log out and log back in** (or reboot) for the group membership changes to take effect. Verify by running `docker run hello-world` without `sudo`.
    *   **Configure Docker to start on boot (Optional but Recommended for Servers):**
        ```bash
        sudo systemctl enable docker.service
        sudo systemctl enable containerd.service
        ```

3.  **Verify Docker Compose Plugin:**
    The `docker compose` command is now the standard. If you installed a recent version of Docker Engine for Linux as per the official docs, the `docker-compose-plugin` package should provide this.
    If, for some reason, you need the older standalone `docker-compose` (legacy), you would follow separate installation instructions from Docker, but try to use the plugin version (`docker compose`).

---

## ✅ Verification

Once Docker (and Docker Desktop or the necessary Linux packages) is installed and running, verify the installation by opening your terminal or command prompt and running the following commands:

1.  **Check Docker Version:**
    ```bash
    docker --version
    ```
    This should display the installed Docker version (e.g., `Docker version 20.10.17, build ...`).

2.  **Check Docker Compose Version:**
    Use the `compose` subcommand (this is the current standard):
    ```bash
    docker compose version
    ```
    This should display the Docker Compose version (e.g., `Docker Compose version v2.10.2`).
    *(If you have an older, standalone Docker Compose installation, you might use `docker-compose --version` which would output something like `docker-compose version 1.29.2, build ...`. The labs will generally assume the `docker compose` syntax.)*

3.  **Run the `hello-world` Image (Optional but Recommended):**
    This command downloads a test image and runs it in a container. It's a good way to confirm that your Docker installation is working correctly from pulling images to running containers.
    ```bash
    docker run hello-world
    ```
    You should see a message starting with "Hello from Docker!" followed by an explanation of what just happened.

If these commands run successfully, your Docker environment is ready!

---

## 🐳 A Quick Tour of Key Docker Concepts

As you go through the labs, you'll work extensively with these concepts:

-   **Images:** Read-only templates used to create containers. Images contain the application code, libraries, dependencies, and runtime. Think of them as blueprints or snapshots.
-   **Containers:** Runnable instances of images. You can create, start, stop, move, and delete containers. They are isolated environments for your applications.
-   **Dockerfile:** A text file that contains instructions for building a Docker image. You define the base image, commands to install software, copy files, set environment variables, and more.
-   **Docker Hub / Registries:** A cloud-based or on-premises repository where Docker images are stored and shared (Docker Hub is the default public registry).
-   **Volumes:** Used to persist data generated by and used by Docker containers, or to share data between the host and containers or between containers.
-   **Docker Compose:** A tool for defining and running multi-container Docker applications. You use a YAML file (`docker-compose.yml`) to configure your application's services, networks, and volumes. This is central to many labs in this track.

Don't worry if these aren't all clear yet; each lab will provide hands-on experience!

---

## 🚀 Next Steps

You are now ready to begin the Docker-CD labs! Start with **[LAB01-Dockerfile-Build/README.md](./LAB01-Dockerfile-Build/README.md)** to build your first Docker image.

---

## 🧹 General Cleanup and Uninstall (For Reference)

-   **Stopping Lab Containers:** Most labs will use Docker Compose. You can stop and remove containers, networks, and volumes defined in a `docker-compose.yml` file by navigating to the lab's directory and running:
    ```bash
    docker-compose down
    # or if using the compose plugin
    docker compose down
    ```
-   **Removing Specific Docker Resources:** You can also remove individual containers (`docker rm <container_id_or_name>`), images (`docker rmi <image_id_or_name>`), and volumes (`docker volume rm <volume_name>`) using Docker CLI commands.
-   **Uninstalling Docker:** If you need to uninstall Docker Desktop or Docker Engine, please refer to the official Docker documentation for the uninstallation procedure specific to your operating system.

Enjoy the labs, and happy containerizing! 🐳 