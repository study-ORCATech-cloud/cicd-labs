# LAB10: Log Aggregation and Management with Docker Compose

Effective log management is crucial for monitoring and debugging containerized applications, especially in a multi-service environment. Docker and Docker Compose provide mechanisms to manage and aggregate logs from your services. This lab focuses on configuring logging drivers in Docker Compose, particularly the `json-file` driver, to control log storage and rotation for local development and CI/CD simulation.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand how to configure logging drivers for services in Docker Compose.
- Implement the `json-file` logging driver with options for log rotation (`max-size`, `max-file`).
- View aggregated logs from multiple services using `docker-compose logs`.
- Understand the benefits of managing log output for containerized applications.

---

## 🧰 Prerequisites

- Docker and Docker Compose installed.
- Basic understanding of application logging concepts.
- Completion of previous Docker-CD labs, particularly those involving multiple services.

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB10-Logs-Aggregation-CD/
├── service1/                     # First microservice (Flask app)
│   ├── Dockerfile                # Dockerfile for service1 (COMPLETE)
│   ├── app.py                    # Flask app code for service1 (COMPLETE)
│   └── requirements.txt          # Python dependencies for service1 (COMPLETE)
├── service2/                     # Second microservice (Flask app)
│   ├── Dockerfile                # Dockerfile for service2 (COMPLETE)
│   ├── app.py                    # Flask app code for service2 (COMPLETE)
│   └── requirements.txt          # Python dependencies for service2 (COMPLETE)
├── docker-compose.yml              # Contains TODOs for configuring logging drivers
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed docker-compose.yml with logging setup
```

---

## 🚀 Lab Steps

**1. Review Service Code and Dockerfiles:**
   Familiarize yourself with the simple Flask applications in `service1/app.py` and `service2/app.py`. Each application logs a message to standard output when its root (`/`) or `/health` endpoint is accessed. Their `Dockerfile`s are standard Python service setups.

**2. Configure Logging in `docker-compose.yml`:**
   Open the `docker-compose.yml` file. You will find two services defined: `service1` and `service2`.
   Your task is to complete the `TODO` items for logging configuration:
   *   **`TODO_SERVICE1_LOGGING`**: 
      *   Uncomment the example `logging` section for `service1`.
      *   Ensure the `driver` is set to `"json-file"`.
      *   Set the `max-size` option to a value like `"100k"` (100 kilobytes) or `"1m"` (1 megabyte).
      *   Set the `max-file` option to a value like `"3"` or `"5"` (number of log files to keep).
   *   **`TODO_SERVICE2_LOGGING`**: 
      *   Similarly, uncomment and configure the `logging` section for `service2`.
      *   Use the `"json-file"` driver.
      *   Choose appropriate `max-size` (e.g., `"50k"`) and `max-file` (e.g., `"2"`) values. You can use different values than service1 to observe distinct behavior if you generate enough logs.

**3. Build and Run Services:**
   Once you have configured the logging in `docker-compose.yml`, build and start the services:
   ```bash
   docker-compose up --build -d
   ```
   The `-d` flag runs the services in detached mode.

**4. Generate Log Data:**
   Access the services in your web browser or using `curl` to generate some log entries:
   *   `service1`: `http://localhost:5050/` and `http://localhost:5050/health`
   *   `service2`: `http://localhost:5051/` and `http://localhost:5051/health`
   Repeat this multiple times for each service to generate enough log data to potentially trigger log rotation (depending on your `max-size` settings).

**5. View Aggregated Logs:**
   Use the `docker-compose logs` command to view the aggregated logs from both services:
   ```bash
   docker-compose logs -f
   ```
   The `-f` flag follows the log output. You should see interleaved log messages from `service1` and `service2`.
   To view logs for a specific service:
   ```bash
   docker-compose logs -f service1
   # or
   docker-compose logs -f service2
   ```
   Press `Ctrl+C` to stop following the logs.

**6. Observe Log Files (Optional - Advanced):**
   If you're curious and know where Docker stores its container logs on your system (typically under `/var/lib/docker/containers/<container_id>/`), you can inspect the JSON log files directly. You should see multiple files if rotation has occurred due_to the `max-size` and `max-file` settings.
   *This step is for deeper understanding and not strictly required for lab completion.*

---

## ✅ Validation Checklist

- [ ] `docker-compose.yml` has the `logging` section configured for both `service1` and `service2`.
- [ ] The `json-file` driver is specified for both services.
- [ ] `options` for `max-size` and `max-file` are set for both services.
- [ ] `docker-compose up --build -d` successfully starts both services.
- [ ] Accessing service endpoints (e.g., `http://localhost:5050/`) generates log messages.
- [ ] `docker-compose logs -f` shows an aggregated stream of logs from both `service1` and `service2`.
- [ ] (Conceptual) Understand that the configured options will cause log files to rotate once they reach the `max-size` limit, up to `max-file` number of files.

---

## 🧹 Cleanup

To stop and remove the containers, networks, and volumes created by Docker Compose:
```bash
docker-compose down
```
This will also remove the logs associated with the containers if they were using the default `json-file` driver and the containers are removed.
If you want to be more aggressive in cleaning up general Docker resources (use with caution):
```bash
# docker system prune -a -f
```
However, for this lab, `docker-compose down` is sufficient.

---

## 🧠 Key Concepts Review

-   **Docker Logging Drivers**: Mechanisms Docker uses to collect and handle container logs (e.g., `json-file`, `local`, `syslog`, `journald`, `fluentd`).
-   **`json-file` Driver**: The default Docker logging driver. It writes logs to JSON-formatted files on the Docker host. It supports options for log rotation (`max-size`, `max-file`).
-   **Log Aggregation with Docker Compose**: `docker-compose logs` command allows you to view a combined stream of logs from all services defined in a `docker-compose.yml` file, or logs for specific services.
-   **Log Rotation**: A process to manage log file sizes by creating new log files and potentially deleting old ones once certain size or number limits are reached. This prevents logs from consuming excessive disk space.

---

## 🎉 Docker-CD Track Complete!

Congratulations! You've successfully navigated the Docker-CD track, covering Dockerfile creation, multi-container applications with Docker Compose, CI simulations, deployment to ECS, Dockerfile linting, and now log aggregation. You've built a strong foundation in using Docker and its ecosystem for Continuous Delivery practices locally and in the cloud.

From here, you can further explore advanced CI/CD concepts with tools like ArgoCD or Jenkins, build more complex microservice applications, or dive deeper into container orchestration with Kubernetes.

Well done on completing this journey! 🐳🚀🎓

