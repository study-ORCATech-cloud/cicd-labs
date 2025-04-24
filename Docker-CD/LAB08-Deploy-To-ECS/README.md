# LAB08 - Deploy to AWS ECS (Docker-CD)

In this lab, you'll take your Docker container and deploy it to **Amazon ECS (Elastic Container Service)** using the **AWS CLI** and a simple ECS Fargate setup.

---

## 🎯 Objectives

By the end of this lab, you will:
- Push a Docker image to Amazon ECR
- Create an ECS cluster and task definition
- Run your container using ECS Fargate

---

## 🧰 Prerequisites

- AWS CLI configured with IAM access
- Docker installed
- An AWS account with permission to use ECS, ECR, and IAM

---

## 🗂️ Folder Structure

```bash
Docker-CD/LAB08-Deploy-To-ECS/
├── app/
│   └── main.py
├── Dockerfile
├── ecs-deploy.sh
└── README.md
```

---

## 🚀 Getting Started

### 1. Tag and push your Docker image to ECR:
```bash
aws ecr create-repository --repository-name ecs-lab
aws ecr get-login-password | docker login --username AWS --password-stdin <your-ecr-url>
docker build -t ecs-lab .
docker tag ecs-lab <your-ecr-url>/ecs-lab
docker push <your-ecr-url>/ecs-lab
```

### 2. Deploy using ECS CLI or script (ecs-deploy.sh):
```bash
#!/bin/bash
# Example ECS Fargate task deployment using AWS CLI

CLUSTER_NAME="ecs-lab-cluster"
SERVICE_NAME="ecs-lab-service"
TASK_DEF_NAME="ecs-lab-task"
REGION="us-east-1"

# Create cluster
echo "Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME

# Register task definition (manual or JSON)
# Create ECS service (manual via console or CLI)
```

For a full deployment, use AWS Console or tools like ECS Copilot.

---

## ✅ Validation Checklist

- [ ] Docker image pushed to ECR
- [ ] Task definition registered
- [ ] Service created and container running on ECS

---

## 🧹 Cleanup
- Delete ECS service, task definition, and cluster from AWS Console or CLI

---

## 🧠 Key Concepts

- ECR stores container images
- ECS runs containers on AWS infrastructure (Fargate or EC2)
- Use `aws ecs` CLI or ECS Copilot for full pipeline automation

---

## 🔁 What's Next?
Continue to [LAB09 - Dockerfile Linting](../LAB09-Dockerfile-Linting/) to validate Dockerfile quality and best practices.

From local to cloud — you're officially deploying! 🚢☁️🐳

