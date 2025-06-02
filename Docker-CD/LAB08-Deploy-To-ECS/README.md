# LAB08: Deploying a Multi-Service Application to AWS ECS with Docker Compose

This lab transitions from local Docker Compose usage to deploying a real multi-service application to the cloud using AWS Elastic Container Service (ECS). You will leverage the Docker CLI's integration with AWS to deploy the two-service application (api_service and web_frontend_service from Lab 07) to ECS, specifically using AWS Fargate for serverless container execution.

**Important Note:** This lab requires you to have an active AWS account and perform actions within it that may incur costs. You will be responsible for managing your AWS resources and ensuring they are cleaned up afterwards to avoid unexpected charges.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the workflow for deploying a Docker Compose application to AWS ECS.
- Create and configure Amazon ECR (Elastic Container Registry) repositories for your service images.
- Build Docker images for your microservices and push them to ECR.
- Adapt a `docker-compose.yml` file for ECS deployment, including ECR image URIs and ECS-specific configurations (e.g., logging, resources, load balancing via `x-aws-*` extensions).
- Set up a basic AWS ECS Cluster (using Fargate) to host your application.
- (Conceptually) Understand how to set up an Application Load Balancer (ALB) for your web-facing service.
- Create and use a Docker context for AWS to interact with your ECS cluster.
- Deploy your multi-service application to ECS using `docker compose up`.
- Verify the deployment and access your application running on ECS.
- Tear down your application stack from ECS using `docker compose down`.

---

## 🧰 Prerequisites

-   **An active AWS Account:** You will need full or sufficient permissions to create and manage ECR, ECS (Clusters, Task Definitions, Services, Fargate tasks), IAM Roles (for ECS tasks), VPC resources (Subnets, Security Groups), and Application Load Balancers.
-   **AWS CLI Installed and Configured:** Ensure your AWS CLI is installed and configured with credentials that have the necessary permissions. Test with `aws sts get-caller-identity`.
-   **Docker Desktop (latest version recommended):** Docker Desktop provides built-in integration for deploying to AWS ECS. Alternatively, ensure your Docker CLI can work with AWS contexts.
-   **Completion of Docker-CD Lab 07:** This lab uses the multi-service application (`api_service` and `web_frontend_service`) built in Lab 07.
-   **Familiarity with Docker and Docker Compose.**
-   **AWS Default Region:** This lab will assume you are working in a default AWS region (e.g., `eu-west-1` or `us-east-1`). Ensure your AWS CLI and console are set to your desired region.

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB08-Deploy-To-ECS/
├── api_service/                    # (Copied from Lab07) API microservice
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── tests/test_app.py
├── web_frontend_service/           # (Copied from Lab07) Web Frontend microservice
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── tests/test_app.py
├── docker-compose.yml              # Contains TODOs for ECR URIs and ECS configurations
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Example docker-compose.yml for ECS and conceptual AWS steps
```

---

## 🚀 Part 1: Preparing Your Application and AWS Environment

**1. (Local) Verify Application from Lab 07:**
   Ensure the `api_service` and `web_frontend_service` (copied into this lab's directory) build and run correctly locally using a standard Docker Compose setup (you can refer to Lab 07's `docker-compose.yml` for local running, but Lab 08's `docker-compose.yml` will be modified for ECS).

**2. (AWS) Create ECR Repositories:**
   For each service (`api_service` and `web_frontend_service`), you need an ECR repository to store its Docker image.
   *   Navigate to the Amazon ECR console in your AWS account.
   *   Create two **private** repositories. Suggested names:
        *   `lab08/api-service`
        *   `lab08/web-frontend-service`
   *   Note down the URI for each repository. It will look like: `YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/lab08/api-service`.

**3. (Local) Build, Tag, and Push Images to ECR:**
   *   **Authenticate Docker to your ECR registry:**
     ```bash
     aws ecr get-login-password --region YOUR_AWS_REGION | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com
     ```
     Replace `YOUR_AWS_REGION` and `YOUR_AWS_ACCOUNT_ID`.
   *   **For `api_service`:**
     Navigate to `Docker-CD/LAB08-Deploy-To-ECS/api_service/` directory (or use `docker build -f ...`):
     ```bash
     docker build -t YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/lab08/api-service:latest .
     docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/lab08/api-service:latest
     ```
   *   **For `web_frontend_service`:**
     Navigate to `Docker-CD/LAB08-Deploy-To-ECS/web_frontend_service/` directory:
     ```bash
     docker build -t YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/lab08/web-frontend-service:latest .
     docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_AWS_REGION.amazonaws.com/lab08/web-frontend-service:latest
     ```

**4. (Local) Configure `docker-compose.yml` for ECS:**
   *   Open `Docker-CD/LAB08-Deploy-To-ECS/docker-compose.yml`.
   *   **`TODO_API_IMAGE` and `TODO_WEB_IMAGE`**: Replace the placeholder `image` URIs with your actual ECR image URIs that you just pushed (including the `:latest` tag or a specific version).
   *   **Review other `TODO`s**: The file contains `TODO`s for ECS-specific configurations like logging (`TODO_API_LOGGING`, `TODO_WEB_LOGGING`), CPU/memory resources (`TODO_API_RESOURCES`, `TODO_WEB_RESOURCES`), and potentially load balancer integration for the web service (`TODO_WEB_LOAD_BALANCER`). For a basic deployment, you might only need image and logging. Resource allocation is highly recommended.

**5. (AWS) Set Up an ECS Cluster:**
   *   Navigate to the Amazon ECS console.
   *   Create a new cluster. Choose the **"Networking only"** template (for AWS Fargate).
   *   Configure your cluster: give it a name (e.g., `lab08-cluster`), select a VPC and subnets. Using default VPC and subnets is fine for this lab if you're unsure.
   *   Enable CloudWatch Container Insights (optional but useful).

**6. (AWS) (Conceptual) Application Load Balancer (ALB) for `web_frontend_service`:**
   For a web-facing service like `web_frontend_service` to be accessible via a stable DNS name and distribute traffic, an ALB is recommended.
   *   **Student Task:** Manually create an Internet-facing Application Load Balancer in the AWS EC2 console (under Load Balancing). 
        *   Configure listeners (e.g., HTTP on port 80).
        *   Configure a Target Group. The `docker compose up` command (with `x-aws-loadbalancer` in your compose file) can create and register targets to this group if you provide its ARN. The Target Group protocol should be HTTP, and the port should match the `web_frontend_service` container port (5001). Health check path for the target group should be `/health`.
   *   The `docker-compose.yml` has a `TODO_WEB_LOAD_BALANCER` section with an `x-aws-loadbalancer` key. If you create an ALB and Target Group, you would uncomment this and provide your Target Group ARN.
   *   For a simpler first deployment, you can skip the ALB and rely on Fargate's public IP (if enabled for the service and task, though less ideal for production).

---

## 🐳 Part 2: Deploying to ECS with Docker Compose

**1. (Local) Create a Docker AWS Context:**
   This tells Docker CLI how to interact with your AWS account for ECS deployments.
   ```bash
   # Ensure you are logged into AWS CLI with appropriate permissions
   docker context create ecs lab08-ecs-context
   # Follow the prompts. It will typically use your default AWS CLI profile and region.
   # You can also specify profile and region: 
   # docker context create ecs lab08-ecs-context --profile your-aws-profile --region your-aws-region
   ```
   Verify the context: `docker context ls`

**2. (Local) Switch to Your AWS Context:**
   ```bash
   docker context use lab08-ecs-context
   ```
   Your Docker commands will now target AWS ECS by default.

**3. (Local) Deploy the Application to ECS:**
   Navigate to the `Docker-CD/LAB08-Deploy-To-ECS/` directory where your `docker-compose.yml` is.
   ```bash
   docker compose up
   ```
   This command will:
   *   Translate your `docker-compose.yml` into an AWS CloudFormation template.
   *   Provision the necessary ECS resources (Task Definitions, Services).
   *   Start your containers (tasks) on ECS Fargate using the images from ECR.
   *   If `x-aws-loadbalancer` is configured, it will attempt to set up the ALB integration.
   Monitor the output. It may take several minutes.

**4. (AWS/Local) Verify Deployment:**
   *   **ECS Console:** Check your ECS cluster. You should see your services (`api_service`, `web_frontend_service`) running, with tasks launched.
   *   **CloudWatch Logs:** If you configured logging in `docker-compose.yml`, check the CloudWatch Log Groups (e.g., `/ecs/lab08-api-service`) for container logs.
   *   **Accessing the Application:** 
        *   If you configured an ALB, find its DNS name in the EC2 Load Balancers console and access it in your browser.
        *   If not using an ALB, you might need to find the public IP of the Fargate task for `web_frontend_service` (go to ECS -> Cluster -> Service -> Tasks -> click task -> look for Public IP in Network section). This is less reliable as IPs can change.
        *   The `web_frontend_service` should display data fetched from `api_service`.

**5. (Local) View Deployed Stack (Optional):**
   ```bash
   docker compose ps # Should show services running on ECS
   docker compose logs # To view aggregated logs from ECS
   ```

--- 

## 🧹 Part 3: Cleaning Up AWS Resources

**It is crucial to clean up resources to avoid ongoing AWS charges.**

**1. (Local) Tear Down the ECS Stack:**
   Ensure you are still in the `lab08-ecs-context` and in the `Docker-CD/LAB08-Deploy-To-ECS/` directory.
   ```bash
   docker compose down
   ```
   This command will instruct AWS CloudFormation to delete the resources created by `docker compose up` (ECS services, task definitions, etc.).

**2. (Local) Switch Back to Default Docker Context:**
   ```bash
   docker context use default
   docker context rm lab08-ecs-context # Optional: remove the context if done
   ```

**3. (AWS) Verify Deletion and Manual Cleanup:**
   *   **ECS Console:** Verify that your services and tasks are deleted from the cluster. Eventually, the CloudFormation stack should also be deleted.
   *   **ECS Cluster:** Delete the `lab08-cluster` itself if you no longer need it.
   *   **ECR Repositories:** Delete the `lab08/api-service` and `lab08/web-frontend-service` ECR repositories (you might need to delete images within them first).
   *   **CloudWatch Log Groups:** Delete the log groups (e.g., `/ecs/lab08-api-service`).
   *   **ALB:** If you created an Application Load Balancer and its Target Groups, delete them from the EC2 console.
   *   **IAM Roles:** If any specific IAM roles were created beyond the defaults, review and delete if necessary.

--- 

## 🧠 Key Concepts Review

-   **AWS ECS (Elastic Container Service):** A fully managed container orchestration service.
-   **AWS Fargate:** A serverless compute engine for containers with ECS (and EKS).
-   **Amazon ECR (Elastic Container Registry):** A managed Docker container registry service.
-   **Docker CLI ECS Integration:** Using `docker context` and `docker compose up/down` to deploy and manage applications on ECS.
-   **`x-aws-*` Compose Extensions:** Docker Compose extensions for defining AWS-specific resource configurations (logging, CPU/memory, load balancers, IAM roles).
-   **CloudFormation:** Docker's ECS integration uses CloudFormation under the hood to provision AWS resources.

--- 

## 🔁 What's Next?

Congratulations! You've deployed a multi-service Dockerized application to AWS ECS. This is a significant step in understanding cloud-native deployments.

Next, consider **[../LAB09-Dockerfile-Linting/README.md](../LAB09-Dockerfile-Linting/)** to focus on improving the quality and security of your Dockerfiles. 

