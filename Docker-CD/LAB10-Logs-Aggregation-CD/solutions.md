# Solutions for LAB10: Log Aggregation and Management with Docker Compose

This document provides the completed `docker-compose.yml` for LAB10, demonstrating how to configure the `json-file` logging driver with rotation options for multiple services.

---

## ✅ Completed `docker-compose.yml` with Logging Configuration

Here is the `docker-compose.yml` with the `logging` sections completed for `service1` and `service2`, using the `json-file` driver and options for log rotation.

```yaml
version: '3.8'

services:
  service1:
    build: ./service1
    ports:
      - "5050:5000" # Host:Container port mapping for service1
    # Solution for TODO_SERVICE1_LOGGING:
    logging:
      driver: "json-file"
      options:
        max-size: "100k"  # Max size of 100 kilobytes per log file
        max-file: "3"     # Keep up to 3 log files (1 active, 2 archived)

  service2:
    build: ./service2
    ports:
      - "5051:5001" # Host:Container port mapping for service2
    # Solution for TODO_SERVICE2_LOGGING:
    logging:
      driver: "json-file"
      options:
        max-size: "50k"   # Max size of 50 kilobytes per log file for this service
        max-file: "2"     # Keep up to 2 log files for this service

# After configuring logging, you can view aggregated logs using:
#   docker-compose logs -f
# Or follow logs for a specific service:
#   docker-compose logs -f service1
```

---

## 📄 Explanation of Logging Configuration

In the solution above:

-   **`driver: "json-file"`**: 
    This explicitly sets the logging driver to `json-file` for both services. While `json-file` is often the default Docker logging driver, explicitly defining it ensures this behavior and allows for specifying its options.
    The `json-file` driver writes container logs to files in JSON format on the Docker host. These are typically stored in `/var/lib/docker/containers/[container-id]/[container-id]-json.log` (path may vary by OS and Docker setup).

-   **`options`**: This block allows you to pass driver-specific settings.
    -   **`max-size: "<size>"`**: This option controls the maximum size a log file can reach before it is rotated. When a log file reaches this size, it is closed, renamed (archived), and a new log file is started. 
        *   For `service1`, we set `"100k"` (100 kilobytes).
        *   For `service2`, we set `"50k"` (50 kilobytes).
    -   **`max-file: "<number>"`**: This option controls the maximum number of log files that will be kept for a container. This includes the active log file and any rotated (archived) log files.
        *   For `service1`, `"3"` means Docker will keep the current log file and the two most recent rotated log files.
        *   For `service2`, `"2"` means Docker will keep the current log file and one rotated log file.

**Benefits of this Configuration:**

1.  **Prevents Disk Space Exhaustion**: By setting `max-size` and `max-file`, you prevent container logs from endlessly growing and consuming all available disk space, which is a common issue in long-running applications.
2.  **Automatic Log Management**: Docker handles the rotation automatically based on these parameters.
3.  **Access to Recent Logs**: You still have access to a configurable amount of recent log history for debugging.
4.  **View with `docker-compose logs`**: Despite logs being rotated into multiple files on the host, the `docker-compose logs` command (and `docker logs`) can still read across these rotated files to give you a continuous view of the log history (up to the amount retained).

This setup is excellent for local development and CI environments where you need manageable, aggregated logs without setting up a complex external logging infrastructure.

--- 

This completes the solution for LAB10. Students can now use these configurations to manage log outputs effectively for their multi-service Docker Compose applications. 