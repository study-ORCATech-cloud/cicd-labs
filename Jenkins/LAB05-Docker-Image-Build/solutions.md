# Solutions for LAB05: Building Docker Images with Jenkins

This document provides the completed `Jenkinsfile` for LAB05. Students should refer to this after attempting to complete the `TODO` items in `Jenkins/LAB05-Docker-Image-Build/Jenkinsfile` themselves.

---

## ✅ Completed `Jenkinsfile`

Below is a complete and working `Jenkinsfile` for this lab. The specific `IMAGE_NAME` and the choice of agent setup might vary based on the student's environment and whether they intend to push to Docker Hub.

```groovy
pipeline {
    // Solution for TODO_AGENT_SETUP:
    // Using a Docker agent is a robust choice. Assumes Docker Pipeline plugin is installed
    // and Docker socket is correctly mounted and accessible.
    agent {
        docker {
            image 'docker:24.0-git' // Includes Docker CLI and Git
            args '-v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp'
            // Important: The user inside this container (often root by default in official Docker images)
            // or the Jenkins user if running with a specific user, needs permissions to access the mounted Docker socket.
            // If Jenkins is running as a 'jenkins' user on the host and that user was added to the 'docker' group on the host,
            // and Jenkins itself runs in Docker with the socket mounted, `agent any` might also work if the Jenkins
            // container itself has the `docker` CLI. The Docker agent is generally more explicit.
        }
    }

    environment {
        // Solution for TODO_IMAGE_NAME:
        // Replace 'your-dockerhub-username' with your actual Docker Hub username if pushing.
        // If not pushing, a simple name like 'lab05-flask-app' is fine.
        IMAGE_NAME = 'your-dockerhub-username/lab05-flask-app' // Or 'lab05-flask-app' for local only
        
        // Solution for TODO_IMAGE_TAG (mostly provided):
        IMAGE_TAG = "0.1.${env.BUILD_NUMBER}"
        DOCKERFILE_PATH = 'Jenkins/LAB05-Docker-Image-Build/app'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out code...'
                checkout scm
                script {
                    sh 'echo "Workspace content after checkout:" && ls -la'
                    sh 'echo "App directory content:" && ls -la ${DOCKERFILE_PATH}'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                // Solution for TODO_BUILD_IMAGE:
                script {
                    docker.build("${IMAGE_NAME}:${IMAGE_TAG}", "--pull -f ${DOCKERFILE_PATH}/Dockerfile ${DOCKERFILE_PATH}")
                }
            }
        }

        stage('Scan Docker Image (Placeholder)') {
            steps {
                echo "(Placeholder) In a real pipeline, you would scan the image for vulnerabilities here."
                echo "Tools like Trivy, Clair, or services like Docker Hub scanning could be used."
            }
        }

        stage('Test Run Docker Image (Optional)') {
            when {
                expression { env.IMAGE_NAME != '' && !env.IMAGE_NAME.startsWith('your-dockerhub-username') } // Example: Run only if not pushing to a real Docker Hub user or if it's a local name
                                                                                                            // Or simply: expression { env.IMAGE_NAME != '' }
            }
            steps {
                echo "Attempting to run the Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                // Solution for TODO_RUN_IMAGE:
                sh 'docker run -d -p 5001:5000 --name lab05app --rm ${IMAGE_NAME}:${IMAGE_TAG}'
                script {
                    try {
                        sleep 10 // Give the app time to start
                        echo "Accessing the application via curl..."
                        sh 'curl --fail http://localhost:5001'
                        echo "Application accessible. Fetching logs..."
                        sh 'docker logs lab05app'
                    } catch (Exception e) {
                        echo "Failed to run or access container: ${e.getMessage()}"
                        // Force cleanup if run failed mid-way
                        sh 'docker logs lab05app || true' 
                    } finally {
                        echo "Stopping and removing test container..."
                        sh 'docker stop lab05app || true' // --rm in docker run should handle removal, but explicit stop is good.
                    }
                }
            }
        }

        stage('Push Docker Image (Optional/Advanced)') {
            when {
                // Only push if IMAGE_NAME contains a '/', implying a Docker Hub user/repo format.
                // And if a Jenkins credential for Docker is actually specified by the student.
                expression { env.IMAGE_NAME.contains('/') && env.DOCKER_CREDENTIAL_ID != null && env.DOCKER_CREDENTIAL_ID != '' }
            }
            environment {
                // Student would need to set this Credential ID in Jenkins and then potentially define it here
                // or pass it via job parameters for a more production-like setup.
                // For this lab, we expect them to replace 'your-jenkins-docker-credential-id' if they proceed.
                DOCKER_CREDENTIAL_ID = 'your-jenkins-docker-credential-id' // Student needs to replace this or configure it
            }
            steps {
                echo "(Optional) Pushing Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                echo "Using Jenkins credential ID: ${DOCKER_CREDENTIAL_ID}"
                // Solution for TODO_PUSH_IMAGE:
                script {
                    docker.withRegistry('', DOCKER_CREDENTIAL_ID) { // Empty string for Docker Hub URL
                        docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push()
                        // Optionally push a 'latest' tag or other tags
                        // docker.image("${IMAGE_NAME}").push("latest") 
                    }
                    echo "Image ${IMAGE_NAME}:${IMAGE_TAG} pushed successfully."
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            // Solution for TODO_CLEANUP_RUNNING_CONTAINER (Optional):
            sh 'docker stop lab05app || true'
            sh 'docker rm lab05app || true'
            echo "Remember to manually prune unused Docker images on the agent if needed: docker image prune -a -f"
        }
    }
}
```

---

## 📝 Explanation of Solutions

1.  **`TODO_AGENT_SETUP`**: 
    *   The solution uses `agent { docker { ... } }` which is a clean way to ensure Docker CLI tools are available. It mounts the Docker socket (`/var/run/docker.sock`) from the host, allowing the Docker commands inside this agent container to control the host's Docker daemon. This is a common pattern.
    *   **Important Note:** The user running Jenkins or the Docker daemon process within the agent container needs appropriate permissions for `/var/run/docker.sock` on the host machine.

2.  **`TODO_IMAGE_NAME`**: 
    *   `IMAGE_NAME = 'your-dockerhub-username/lab05-flask-app'`
    *   Students should replace `your-dockerhub-username` with their actual Docker Hub ID if they intend to push. Otherwise, a local name like `lab05-flask-app` is sufficient for building and local testing.

3.  **`TODO_IMAGE_TAG`**: 
    *   `IMAGE_TAG = "0.1.${env.BUILD_NUMBER}"`
    *   This creates a unique tag for each build (e.g., `0.1.1`, `0.1.2`), which is good practice for versioning.

4.  **`TODO_BUILD_IMAGE`**: 
    *   `docker.build("${IMAGE_NAME}:${IMAGE_TAG}", "--pull -f ${DOCKERFILE_PATH}/Dockerfile ${DOCKERFILE_PATH}")`
    *   This command builds the Docker image.
        *   `"${IMAGE_NAME}:${IMAGE_TAG}"`: Specifies the full name and tag for the new image.
        *   `"--pull ..."`: These are arguments passed to the `docker build` command.
            *   `--pull`: Ensures the base image (`python:3.9-slim`) is updated before building.
            *   `-f ${DOCKERFILE_PATH}/Dockerfile`: Specifies the path to the `Dockerfile`.
            *   `${DOCKERFILE_PATH}`: Specifies the build context (the `app` directory).

5.  **`TODO_RUN_IMAGE` (Optional)**:
    *   `sh 'docker run -d -p 5001:5000 --name lab05app --rm ${IMAGE_NAME}:${IMAGE_TAG}'`
        *   Runs the container in detached mode (`-d`), maps port 5000 in the container to 5001 on the host (`-p 5001:5000`), names it `lab05app`, and ensures it's removed on stop (`--rm`).
    *   The `script` block with `sleep`, `curl`, and `docker logs/stop` provides a basic test and cleanup for the running container.

6.  **`TODO_PUSH_IMAGE` (Optional/Advanced)**:
    *   The `when` condition `expression { env.IMAGE_NAME.contains('/') && env.DOCKER_CREDENTIAL_ID != null && env.DOCKER_CREDENTIAL_ID != '' }` is a safeguard to only attempt push if the image name looks like a Docker Hub repo and a credential ID is specified.
    *   `DOCKER_CREDENTIAL_ID = 'your-jenkins-docker-credential-id'`: Students **must** replace `your-jenkins-docker-credential-id` with the ID of a credential they've configured in Jenkins for Docker Hub.
    *   `docker.withRegistry('', DOCKER_CREDENTIAL_ID) { ... }`: This block tells Jenkins to use the specified credentials when interacting with Docker Hub (the `''` indicates the default Docker Hub registry).
    *   `docker.image("${IMAGE_NAME}:${IMAGE_TAG}").push()`: Pushes the tagged image.

7.  **`TODO_CLEANUP_RUNNING_CONTAINER` (Optional)**:
    *   `sh 'docker stop lab05app || true'` and `sh 'docker rm lab05app || true'` are added in the `post` block to ensure the test container (if run) is stopped and removed, even if earlier steps failed. The `|| true` prevents the pipeline from failing if the container doesn't exist.

---

This setup provides a solid foundation for building Docker images within a Jenkins CI/CD pipeline. 