# Docker and Container-Based Continuous Delivery (CD) Labs

Welcome to the **Docker-CD** section of the **CI/CD Automation Labs collection**! This track is designed to introduce you to the world of containerization with Docker and how it revolutionizes Continuous Integration and Continuous Delivery (CI/CD) pipelines.

Docker allows you to package your applications and their dependencies into standardized, portable units called containers. These containers can run consistently across different environments, from a developer's laptop to staging and production servers. This consistency is a cornerstone of modern DevOps practices.

In these labs, you'll progress from building your first `Dockerfile` to orchestrating multi-container applications with Docker Compose, integrating Docker builds into CI pipelines, and eventually deploying containerized applications to cloud services.

---

## 🚀 What You'll Learn

Throughout this Docker-CD track, you will explore:

-   **`Dockerfile` Fundamentals:** Writing `Dockerfile`s to define your application images.
-   **Image Building & Management:** Building, tagging, and managing Docker images locally.
-   **Container Orchestration with Docker Compose:** Defining and running multi-container applications for local development and testing.
-   **CI/CD Integration:** Building Docker images within automated CI pipelines (e.g., using GitHub Actions).
-   **Best Practices:** Optimizing `Dockerfile`s for build speed and image size, managing secrets and configurations, and implementing health checks.
-   **Deployment Strategies:** Deploying containerized applications, including to cloud platforms like AWS ECS (Elastic Container Service).
-   **Advanced Topics:** Multi-stage builds, Dockerfile linting, and log aggregation for containerized services.

---

## 📁 Lab Structure

The labs are designed to be followed sequentially, as concepts build upon each other:

```bash
Docker-CD/
├── README.md                          # Overview of the Docker-CD track (this file)
├── LAB01-Dockerfile-Build/            # Learn to write your first Dockerfile for a Python app
├── LAB02-Compose-CI-Integration/      # Integrate Docker Compose with CI for multi-container apps
├── LAB03-Compose-Dev-Environments/    # Use Docker Compose to create consistent development environments
├── LAB04-Multi-Stage-Dockerfile-Builds/ # Master multi-stage Docker builds for optimized images
├── LAB05-Secrets-And-Volumes/         # Manage sensitive data and persistent storage with Docker
├── LAB06-Service-Health-Checks/       # Implement health checks in Docker services
├── LAB07-Microservices-CI-Pipeline/   # Build a CI pipeline for a multi-service (microservices) application
├── LAB08-Deploy-To-ECS/               # Deploy Docker containers to Amazon Elastic Container Service
├── LAB09-Dockerfile-Linting/          # Improve Dockerfile quality with linting tools
└── LAB10-Logs-Aggregation-CD/         # Aggregate logs from multiple Docker containers
```

Each individual lab directory (e.g., `LAB01-Dockerfile-Build/`) contains:
-   A `README.md` file with detailed objectives, prerequisites, step-by-step instructions for that lab, validation checklists, cleanup steps, and key concepts.
-   Any necessary sample application code (usually in an `app/` subdirectory).
-   Complete, working `Dockerfile` configurations ready to copy and use.
-   `docker-compose.yml` files where applicable, fully functional out of the box.
-   Workflow files (e.g., for GitHub Actions) when the lab involves CI/CD automation.
-   **Copy-and-Learn Methodology**: All files are complete and functional - students copy configurations and learn by following detailed step-by-step instructions.

---

## 🧰 Prerequisites for This Track

To successfully complete the labs in this Docker-CD track, you should have the following:

1.  **Docker Installed and Running:**
    *   **Windows/macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
    *   **Linux:** Install Docker Engine and Docker Compose. Follow the official Docker documentation for your distribution.
    *   Ensure the Docker daemon/service is running. You can verify your installation by opening a terminal and running `docker --version` and `docker ps` (which should execute without errors).
2.  **Basic Command Line / Terminal Familiarity:** You should be comfortable navigating directories and running commands in a terminal (e.g., Command Prompt or PowerShell on Windows, Terminal on macOS/Linux).
3.  **Text Editor or IDE:** A good text editor or Integrated Development Environment (IDE) for editing `Dockerfile`s, Python code, YAML files, etc. (e.g., VS Code, Sublime Text, Atom, IntelliJ IDEA).
4.  **Git and GitHub Account:**
    *   Basic understanding of Git version control (cloning, committing, pushing).
    *   A [GitHub](https://github.com/) account to fork the main `cicd-labs` repository, as you'll be pushing changes to your fork.
5.  **Internet Access:** Required for pulling base Docker images and installing software packages.
6.  **(Optional, for later labs) AWS Account:** For labs involving deployment to AWS services like ECS (e.g., LAB08), an AWS account with appropriate permissions will be needed. A free tier account is usually sufficient for lab purposes.

---

## 📖 How to Use These Labs

1.  **Fork the Repository:** Start by forking the main `ORCATech-study/cicd-labs` repository to your own GitHub account.
2.  **Clone Your Fork:** Clone your forked repository to your local machine.
3.  **Navigate to the Lab:** Change into the specific lab directory you are working on (e.g., `cd Docker-CD/LAB01-Dockerfile-Build`).
4.  **Read the Lab `README.md`:** Each lab has its own `README.md` with detailed instructions. Read it carefully!
5.  **Copy the Provided Files:** All Docker configurations, compose files, and application code are complete and ready to use. Simply copy them to your working directory as instructed.
6.  **Follow Instructions:** Execute the commands as described in the lab's `README.md` to build, run, and test the containerized applications.
7.  **Validate:** Use the validation checklist in each lab's `README.md` to ensure you've achieved the objectives.
8.  **Learn by Doing:** Focus on understanding how each configuration works rather than solving puzzles - all files are production-ready examples.
9.  **Clean Up:** Follow the cleanup steps to remove any created Docker images, containers, or other resources.

---

## 💬 Contributing

We welcome contributions! If you have ideas for new Docker-CD labs, improvements to existing ones, or find any issues:
-   Fork this repository.
-   Create a new branch for your changes.
-   Follow the existing lab format (e.g., `LABxx-Descriptive-Name`).
-   Ensure your lab is well-documented with a clear `README.md` and complete working configurations.
-   Submit a Pull Request to the main repository.

---

**Containerize. Orchestrate. Deploy with Docker.** 🐳🚀🛠️

Let's begin your journey into Docker and containerized CI/CD!

