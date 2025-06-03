# CI/CD Automation Labs – Roadmap

Welcome to the master roadmap for the **CI/CD Automation Labs** repository. This roadmap organizes labs by CI/CD tool to provide deep, hands-on experience in building, testing, and deploying software with real-world workflows using **copy-based learning methodology** with production-ready configurations.

---

## 🚦 GitHub Actions Labs
Automate workflows with GitHub-native CI/CD pipelines.

| Lab | Title                                | Focus                                  |
|-----|--------------------------------------|----------------------------------------|
| 01  | Hello World Workflow                 | Workflow structure, push trigger       |
| 02  | Python CI Workflow                   | `pytest`, linting, test matrix         |
| 03  | Docker Build & Push                  | DockerHub integration                  |
| 04  | Deploy to GitHub Pages               | Static site CD                         |
| 05  | Scheduled Jobs & Cron Triggers       | Automated scheduled workflows          |
| 06  | Environment Secrets & Context        | Secure workflows, env usage            |
| 07  | Workflow Artifacts & Caching         | Caching, artifact retention            |
| 08  | Monorepo Multi-Project Strategy      | Multi-workspace automation             |
| 09  | Reusable Workflow Templates          | DRY pipelines across projects          |
| 10  | Canary Deployment with GitHub Actions| Advanced deployment strategies         |

---

## 🧰 Jenkins Labs
Use Jenkins for local or enterprise-grade CI/CD pipelines.

| Lab | Title                                | Focus                                  |
|-----|--------------------------------------|----------------------------------------|
| 01  | My First Jenkins Job - Freestyle 'Hello World' | Basic UI interaction, Freestyle job, manual build, console output |
| 02  | Freestyle Job: Python Test           | Manual job execution, SCM basics       |
| 03  | Declarative Pipeline with Jenkinsfile| Groovy pipelines                       |
| 04  | SCM Polling and GitHub Webhooks      | Triggering builds from repo changes    |
| 05  | Build Docker Images in Pipeline      | Jenkins-Docker integration             |
| 06  | Parallel & Conditional Stages        | Advanced pipeline logic                |
| 07  | Use Shared Libraries in Jenkins      | Reusable pipeline code                 |
| 08  | Secure Secrets with Jenkins Credentials| Masked secrets, credentials plugin     |
| 09  | Slack Notification Integration       | Pipeline notifications                 |
| 10  | Deploy to Remote Server via SSH      | Delivery step with SSH and rsync       |

---

## 🐳 Docker-CD Labs
Use Docker and Docker Compose to manage deployments.

| Lab | Title                                | Focus                                  |
|-----|--------------------------------------|----------------------------------------|
| 01  | Dockerfile CI Build                  | Build/test Docker images               |
| 02  | Docker Compose Local CI              | Compose up/down in CI pipeline         |
| 03  | Docker Compose for Dev Environments  | Local dev automation                   |
| 04  | Multi-Stage Dockerfile Builds        | Optimized builds and image size        |
| 05  | Compose with Secrets & Volumes       | Security, persistence                  |
| 06  | Service Health Checks & Retry        | Health checks in orchestration         |
| 07  | CI Workflow for Microservices        | Test & deploy multi-service stack      |
| 08  | Push Compose Stack to AWS ECS        | Docker + ECS deployment                |
| 09  | CI Linting for Dockerfiles           | Best practices validation              |
| 10  | Compose Logs Aggregation Setup       | Centralized logging during CD         |

---

## 🌐 ArgoCD Labs (GitOps)
Learn GitOps by automating Kubernetes deployments with ArgoCD.

| Lab | Title                                | Focus                                  |
|-----|--------------------------------------|----------------------------------------|
| 01  | Deploy First Application with ArgoCD | ArgoCD UI mastery and GitOps introduction |
| 02  | Deploy K8s App via Git Repo          | GitOps fundamentals and personal repos |
| 03  | Use Helm Charts with ArgoCD          | Helm + GitOps CD flow                  |
| 04  | App Rollback with GitOps             | Revisions and rollbacks                |
| 05  | Sync Policies and Auto Deployments   | Sync policies, self-healing apps       |
| 06  | Add External Secrets to CD           | ArgoCD with Sealed Secrets/ESO         |
| 07  | Deploy to Staging + Production       | Multi-env pipelines                    |
| 08  | Promote Images from CI to ArgoCD     | CI/CD handoff                          |
| 09  | Notifications via ArgoCD Notifiers   | CD event alerting                      |
| 10  | Secure ArgoCD with RBAC & SSO        | Team-based access control              |

---

## 🧠 Suggested Learning Flow

**Teaching Methodology**: All labs use a **copy-based learning approach** — complete, production-ready configurations are provided for students to copy and deploy while following detailed step-by-step instructions. This methodology ensures immediate success and builds confidence through hands-on experience with enterprise-grade DevOps tools.

**Recommended Progression**:
- Start with **GitHub Actions** for basic CI concepts and cloud-native automation
- Advance to **Jenkins** for custom pipelines, agent control, and enterprise CI/CD
- Explore **Docker-CD** for containerized CD pipelines and microservices deployment
- Finish with **ArgoCD** to adopt a GitOps deployment model and Kubernetes-native CD

Each track builds foundational knowledge that enhances understanding of the subsequent technologies.

---

**Build pipelines. Automate delivery. Deploy with confidence.** 🚀
