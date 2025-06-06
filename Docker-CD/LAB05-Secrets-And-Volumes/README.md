# LAB05: Managing Secrets and Persistent Data with Docker Compose

In real-world applications, you need to handle sensitive information like API keys or database credentials securely. You also need to ensure that important data, such as database files or user uploads, persists even if containers are stopped or recreated. This lab explores how Docker Compose helps manage both **secrets** and **persistent data volumes**.

We will focus on:
1.  **Docker Compose Secrets:** A mechanism to securely pass sensitive data to services as files, rather than environment variables (which can sometimes be exposed more easily).
2.  **Docker Named Volumes:** The preferred way to persist data generated by and used by Docker services, ensuring data durability.

---

## 🎯 Objectives

By the end of this lab, you will:
- Understand the difference between environment variables and Docker Compose secrets for managing sensitive data.
- Define and use Docker Compose secrets from an external file.
- Modify an application to read a secret from its file mount path (typically `/run/secrets/<secret_name>`).
- Understand the importance of named volumes for data persistence.
- Configure named volumes for services like Redis to persist their data.
- Configure a named volume for application-specific data.
- Verify that secrets are being used and data persists across container restarts.

---

## 🧰 Prerequisites

- Completion of Docker-CD Labs 01-04 (understanding of `Dockerfile`, `docker-compose.yml`).
- Docker and Docker Compose installed.
- Basic terminal/command-line knowledge.
- A text editor/IDE.

---

## 📂 Folder Structure for This Lab

```bash
Docker-CD/LAB05-Secrets-And-Volumes/
├── app/                            # Python Flask application (modified for secrets & file counter)
│   ├── Dockerfile                  # Standard/Development Dockerfile (COMPLETE)
│   ├── main.py                     # Flask app logic (COMPLETE, reads secret, uses file counter)
│   ├── requirements.txt            # Python dependencies (COMPLETE)
│   └── tests/
│       └── test_main.py            # Basic unit tests (COMPLETE, mocks secret/data paths)
├── docker-compose.yml              # Contains TODOs for secrets and volumes
├── api_key.txt                     # Student will create this file to store the secret API key
├── README.md                       # Lab instructions (this file)
└── solutions.md                    # Completed docker-compose.yml and example api_key.txt content
```

---

## 🐍 The Sample Application (`app/`)

The `app/main.py` has been modified:
- It now attempts to read an API key from a file path (defaulting to `/run/secrets/api_key_secret`). This path is where Docker Compose will mount the secret you define.
- It also implements a simple file-based counter, reading from and writing to `/data/app_counter.txt`. This will be used to demonstrate data persistence using a named volume for the web app itself.
- The Redis hit counter functionality remains.

--- 

## ✨ Part 1: Understanding and Using Docker Compose Secrets

While environment variables are easy to use, they might not always be the most secure way to handle sensitive data, as they can sometimes be inadvertently logged or inspected. Docker Compose offers a `secrets` feature that allows you to make sensitive data available to services as files inside the container (typically mounted read-only in `/run/secrets/`).

**1. Create the Secret File:**

   In the `Docker-CD/LAB05-Secrets-And-Volumes/` directory, create a new file named `api_key.txt`.
   Put a simple string in this file that will act as your secret API key. For example:
   ```
   mySuperSecretApiKey12345
   ```
   **Important:** In a real project, such files containing actual secrets should be listed in your `.gitignore` file to prevent them from being committed to version control.

**2. Define the Secret in `docker-compose.yml`:**

   Open `docker-compose.yml`. You will find `TODO` items to guide you:
   *   **`TODO_SECRETS_GLOBAL`**: At the top level of the `docker-compose.yml` file, you need to define a `secrets` block. This declares the secret named `api_key_secret` and tells Docker Compose to source its content from the `./api_key.txt` file you just created.
   *   **`TODO_WEB_SECRETS`**: Within the `web` service definition, you need to assign the globally defined `api_key_secret` to this service. This makes the secret available to the `web` container.
        By default, the content of `api_key.txt` will be mounted as a file at `/run/secrets/api_key_secret` inside the `web` container. The `app/main.py` is already coded to look for the key at this location.

--- 

## 💾 Part 2: Ensuring Data Persistence with Named Volumes

Containers are ephemeral by default. If a container stops or is removed, any data written inside its filesystem (that isn't part of the image) is lost. For stateful services like databases (Redis in our case) or for application data that needs to survive container lifecycles, you must use **volumes**.

**Named volumes** are managed by Docker and are the recommended way to persist data.

**1. Configure Volumes in `docker-compose.yml`:**

   Continue editing `docker-compose.yml`:
   *   **`TODO_REDIS_VOLUME`**: In the `redis` service definition, you need to configure a volume mount. You'll map a named volume (e.g., `redis_data`) to Redis's internal data directory, which is `/data`. This will ensure that all data Redis writes (like our hit counter) is stored in the `redis_data` volume on the host machine.
   *   **`TODO_WEB_VOLUMES`**: In the `web` service definition, configure another volume mount. You'll map a named volume (e.g., `app_data`) to the `/data` directory inside the `web` container. The `app/main.py` is now writing its own counter to `/data/app_counter.txt`, and this will ensure that counter also persists.
   *   **`TODO_VOLUMES_GLOBAL`**: At the top level of `docker-compose.yml`, you need to define a `volumes` block. This is where you declare the named volumes `redis_data` and `app_data` that your services will use.

--- 

## 🚀 Part 3: Building, Running, and Validating

**1. Build and Run the Services:**

   Once you have completed all the `TODO`s in `docker-compose.yml` and created `api_key.txt`:
   In your terminal, from the `Docker-CD/LAB05-Secrets-And-Volumes/` directory:
   ```bash
   # Build images (if changed) and start services in detached mode
   docker-compose up --build -d
   ```

**2. Test the Application:**

   *   Access the web application in your browser: `http://localhost:5006` (or the host port you configured for the `web` service).
   *   **Verify Secret:** You should see the API key from your `api_key.txt` file displayed on the page.
   *   **Verify App Counter:** Note the value of "This app endpoint has been visited X times". Refresh the page a few times; this counter should increment.
   *   **Verify Redis Counter:** Note the value of the "Redis counter". Refresh the page; this counter should also increment.

**3. Test Persistence:**

   *   Stop and remove the containers:
     ```bash
     docker-compose down
     ```
     **Important:** Do NOT use the `-v` flag with `docker-compose down` at this stage if you want to test data persistence. The `-v` flag would also remove the named volumes.
   *   Restart the services:
     ```bash
     docker-compose up -d
     ```
   *   Access `http://localhost:5006` again.
        *   **App Counter Persistence:** The "app endpoint" counter should have retained its value from before you stopped the containers and should continue incrementing from there.
        *   **Redis Persistence:** The "Redis counter" should also have retained its value and continue incrementing.

**4. Inspect Volumes (Optional):**

   You can list Docker volumes to see the named volumes you created:
   ```bash
   docker volume ls
   ```
   You should see `lab05-secrets-and-volumes_redis_data` and `lab05-secrets-and-volumes_app_data` (or similar, prefixed with your project directory name).

**5. Check Secret Mount Path (Optional, for deeper understanding):**

   You can exec into the running `web` container to see how the secret is mounted:
   ```bash
   # Find your web container ID or name
   docker ps 

   # Exec into the web container (replace <container_id_or_name>)
   docker exec -it <container_id_or_name> sh 

   # Inside the container, check for the secret file:
   ls -l /run/secrets/
   cat /run/secrets/api_key_secret 
   exit
   ```

--- 

## ✅ Validation Checklist

- [ ] `api_key.txt` file created in the lab directory with a secret string.
- [ ] `docker-compose.yml` has a top-level `secrets` block defining `api_key_secret` sourced from `api_key.txt`.
- [ ] The `web` service in `docker-compose.yml` is configured to use `api_key_secret`.
- [ ] `docker-compose.yml` has a top-level `volumes` block defining `redis_data` and `app_data` named volumes.
- [ ] The `redis` service in `docker-compose.yml` mounts `redis_data` to `/data`.
- [ ] The `web` service in `docker-compose.yml` mounts `app_data` to `/data`.
- [ ] `docker-compose up --build -d` starts all services successfully.
- [ ] The web application at `http://localhost:5006` displays the API key from `api_key.txt`.
- [ ] The web application's file-based counter (`/data/app_counter.txt`) increments on refresh and persists after `docker-compose down` and `docker-compose up -d`.
- [ ] The Redis hit counter increments on refresh and persists after `docker-compose down` and `docker-compose up -d`.

---

## 🧹 Cleanup

To stop and remove containers, networks, AND the named volumes created by this lab:
```bash
docker-compose down -v
```
If you want to keep the volumes, omit the `-v` flag:
```bash
docker-compose down
```
Consider removing the `api_key.txt` file if it contained a real sensitive value and you are done with the lab.

--- 

## 🧠 Key Concepts Review

-   **Docker Compose Secrets**: Provides a secure way to deliver sensitive data to services as files mounted in `/run/secrets/`. Defined globally and then assigned to services.
-   **Named Volumes**: Docker-managed persistent storage. They exist independently of container lifecycles. Essential for stateful applications.
-   **Data Persistence**: Ensuring that data survives container restarts, stops, or removals.
-   **Configuration vs. Runtime Data**: Secrets and configurations are often image-agnostic and injected at runtime. Application data (databases, logs, uploads) is runtime data that needs persistence.

--- 

## 🔁 What's Next?

Having mastered secrets and volumes, you are now better equipped to manage production-like containerized applications.

Next, consider exploring **[../LAB06-Service-Health-Checks/README.md](../LAB06-Service-Health-Checks/)**, which focuses on defining and using health checks in Docker Compose to ensure your services are running correctly. 

