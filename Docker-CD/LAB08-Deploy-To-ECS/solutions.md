# Solutions for LAB08: Deploying to AWS ECS with Docker Compose

This document provides an example of a completed `docker-compose.yml` for deploying the multi-service application to AWS ECS. It also recaps the conceptual AWS setup steps that students need to perform in their own accounts.

**Disclaimer:** Actual ARNs, Account IDs, and specific resource names will vary based on the student's AWS account and region.

---

## ✅ Example Completed `docker-compose.yml` for ECS

Below is an example of how the `docker-compose.yml` might look after a student has:
1.  Pushed their images to ECR and updated the `image` URIs.
2.  Configured basic CloudWatch logging.
3.  Specified CPU and Memory resources.
4.  (Optionally) Included a placeholder for ALB integration (actual ARN would be student-specific).

```yaml
version: '3.8'

# Example: Deployed to us-east-1 with AWS Account ID 123456789012
# ECR Repos: lab08/api-service, lab08/web-frontend-service

services:
  api_service:
    # Solution for TODO_API_IMAGE:
    image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/lab08/api-service:latest
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SERVICE_ID=ecs_api_instance
    # Solution for TODO_API_LOGGING:
    logging:
      driver: awslogs
      options:
        awslogs-group: /ecs/lab08-api-service # Student should ensure this log group is created or will be created
        awslogs-region: us-east-1 # Student should use their AWS region
        awslogs-stream-prefix: ecs
    # Solution for TODO_API_RESOURCES:
    x-aws-cpu: "256"    # 0.25 vCPU
    x-aws-memory: "512" # 512 MiB
    # Optional: x-aws-iam-role: arn:aws:iam::123456789012:role/ECSTaskExecutionRole # Or a custom one
    healthcheck:
        test: ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"]
        interval: 15s
        timeout: 5s
        retries: 3
        start_period: 10s

  web_frontend_service:
    # Solution for TODO_WEB_IMAGE:
    image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/lab08/web-frontend-service:latest
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - API_SERVICE_URL=http://api_service:5000
      - SERVICE_ID=ecs_web_instance
    depends_on:
      api_service:
        condition: service_healthy
    # Solution for TODO_WEB_LOGGING:
    logging:
      driver: awslogs
      options:
        awslogs-group: /ecs/lab08-web-frontend # Student should ensure this log group is created or will be created
        awslogs-region: us-east-1 # Student should use their AWS region
        awslogs-stream-prefix: ecs
    # Solution for TODO_WEB_RESOURCES:
    x-aws-cpu: "256"
    x-aws-memory: "512"
    # Solution for TODO_WEB_LOAD_BALANCER (Example, student needs their own ALB Target Group ARN):
    # x-aws-loadbalancer:
    #   target_group_arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/lab08-web-frontend-tg/xxxxxxxxxxxxxxxxx"
    healthcheck:
        test: ["CMD-SHELL", "curl -f http://localhost:5001/health || exit 1"]
        interval: 15s
        timeout: 5s
        retries: 3
        start_period: 15s

# Student would need to ensure their Docker AWS context is configured to point to a VPC
# (e.g., default VPC) with appropriate subnets and security groups that allow traffic
# on the necessary ports (e.g., 5000, 5001 internally, and ALB listener port externally if used).
```

---

## 🔑 Recap of AWS Setup Steps (Conceptual)

The student is responsible for performing these steps in their AWS account:

1.  **ECR Repositories:**
    *   Create two private ECR repositories (e.g., `lab08/api-service`, `lab08/web-frontend-service`).
    *   Note their URIs.

2.  **Build and Push Images:**
    *   Authenticate Docker to ECR.
    *   Build images for `api_service` and `web_frontend_service`.
    *   Tag images with their respective ECR repository URIs (e.g., `YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/lab08/api-service:latest`).
    *   Push the tagged images to ECR.

3.  **ECS Cluster:**
    *   Create an ECS cluster (e.g., `lab08-cluster`) using the "Networking only" (AWS Fargate) template.
    *   Select a VPC and subnets (default VPC/subnets are acceptable for this lab).

4.  **(Optional but Recommended) Application Load Balancer (ALB):**
    *   If exposing `web_frontend_service` publicly, create an Internet-facing ALB.
    *   Configure a listener (e.g., HTTP:80).
    *   Create a Target Group for the `web_frontend_service`:
        *   Protocol: HTTP, Port: 5001 (matching container port).
        *   Health Check Path: `/health`.
        *   VPC: Same as ECS Cluster.
    *   Note the Target Group ARN to use in the `x-aws-loadbalancer` section of `docker-compose.yml`.

5.  **IAM Roles:**
    *   Ensure the default ECS Task Execution Role (`ecsTaskExecutionRole`) exists and has permissions to pull images from ECR and write logs to CloudWatch. This is usually created automatically.
    *   If services require other AWS permissions, custom IAM task roles might be needed (specified via `x-aws-iam-role`).

6.  **Docker AWS Context:**
    *   Run `docker context create ecs <your-context-name>` and follow prompts.
    *   Use `docker context use <your-context-name>` before running `docker compose up`.

By completing these AWS setup steps and correctly configuring the `docker-compose.yml`, students can deploy their application to ECS using the Docker CLI.

--- 

This completes the solution guidance for LAB08. Students should now be able to deploy their application to AWS ECS. 