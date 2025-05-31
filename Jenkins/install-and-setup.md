# Jenkins Installation and Initial Setup Guide

This guide walks you through installing Jenkins on your local machine and performing the initial configuration. We'll primarily use Docker for a quick and isolated setup (recommended for these labs), but we'll also cover native installation.

**Follow these instructions carefully to set up Jenkins before starting any of the Jenkins labs in this repository.**

---

## 🎯 What You'll Achieve

By following this guide, you will have:
- A running Jenkins server.
- Access to the Jenkins user interface (UI).
- Jenkins unlocked with the initial administrator password.
- A basic set of useful plugins installed.
- Your first Jenkins admin user account created.
- A brief understanding of the Jenkins dashboard.

---

## 🧰 Prerequisites

Before you begin, ensure you have the following:

-   **Method 1: Docker (Recommended for Labs)**
    *   **Docker Desktop (Windows/macOS) or Docker Engine (Linux):** Installed and actively running. Docker simplifies the setup by bundling Jenkins and its Java dependency.
        *   Download: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
        *   Verify Docker is running by opening Docker Desktop or typing `docker version` in your terminal.
-   **Method 2: Native Installation (Alternative)**
    *   **Java Development Kit (JDK):** Version 11 or 17. Jenkins requires a specific Java version. If you choose native install, ensure you have a compatible JDK installed and configured in your system's PATH. Check the official Jenkins documentation for the most up-to-date Java compatibility.
-   **General:**
    *   A modern web browser (e.g., Chrome, Firefox, Edge).
    *   Basic command-line/terminal proficiency.
    *   Internet access (for downloading Jenkins and plugins).

---

## 🐳 Method 1: Running Jenkins with Docker (Recommended)

Using Docker is the quickest and most common way to run Jenkins locally for learning and development.

1.  **Ensure Docker is Running:**
    Confirm that Docker Desktop is running or that the Docker daemon/service is active on your system.

2.  **Create a Docker Volume for Jenkins Data (Persistence):**
    This crucial step ensures that your Jenkins configuration, jobs, plugins, and other data persist even if you stop and remove the Jenkins container. Without this, you'd lose your work each time the container is removed.
    ```bash
    docker volume create jenkins-data
    ```
    *Purpose: Provides a dedicated, named volume managed by Docker to store Jenkins home directory contents.*

3.  **Run the Jenkins LTS (Long-Term Support) Docker Container:**
    This command downloads the `jenkins/jenkins:lts-jdk17` image (Long-Term Support version with JDK 17, a good modern choice) if you don't have it locally, and then starts a container from it.
    ```bash
    docker run -d \
      --name jenkins-server \
      -p 8080:8080 \
      -p 50000:50000 \
      -v jenkins-data:/var/jenkins_home \
      jenkins/jenkins:lts-jdk17
    ```
    *Key command parameters explained:*
    *   `-d`: Runs the container in "detached" mode (in the background).
    *   `--name jenkins-server`: Assigns a convenient name (`jenkins-server`) to your container. This makes it easier to manage (e.g., `docker stop jenkins-server`).
    *   `-p 8080:8080`: Maps port 8080 on your host machine to port 8080 inside the container. Jenkins web UI listens on port 8080 by default.
    *   `-p 50000:50000`: Maps port 50000 on your host to port 50000 in the container. This port is used for communication between the Jenkins controller (master) and Jenkins agents (we'll explore agents in later labs).
    *   `-v jenkins-data:/var/jenkins_home`: Mounts the `jenkins-data` Docker volume (created in the previous step) to the `/var/jenkins_home` directory inside the container. This is where Jenkins stores all its data.
    *   `jenkins/jenkins:lts-jdk17`: Specifies the Docker image to use.

    *After running this command, wait a minute or two for Jenkins to initialize inside the container.* You can check the container's status using `docker ps`. You should see `jenkins-server` listed.

4.  **Access Jenkins UI:**
    Once Jenkins has started, open your web browser and navigate to:
    [http://localhost:8080](http://localhost:8080)
    You should be greeted with the "Unlock Jenkins" page.

5.  **Retrieve and Enter Initial Admin Password:**
    For security, Jenkins locks the initial setup with an auto-generated password. You need to retrieve this password to proceed.

    *   **Option A: Using `docker logs` (Recommended first try)**
        Open your terminal and run:
        ```bash
        docker logs jenkins-server
        ```
        Look through the log output. Jenkins prints the initial admin password to the console, usually enclosed in a block of asterisks. It might take a few moments for this to appear if Jenkins is still starting up.
        Example of what to look for (your password will be different):
        ```
        *************************************************************
        *************************************************************
        *************************************************************

        Jenkins initial setup is required. An admin user has been created and a password generated.
        Please use the following password to proceed to installation:

        THIS_WILL_BE_YOUR_LONG_ALPHANUMERIC_PASSWORD

        This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

        *************************************************************
        *************************************************************
        *************************************************************
        ```
    *   **Option B: Using `docker exec` (If password not found in logs or scrolled past)**
        If you can't find the password in the logs, you can directly read it from the file inside the container:
        ```bash
        docker exec jenkins-server cat /var/jenkins_home/secrets/initialAdminPassword
        ```
        This command executes `cat /var/jenkins_home/secrets/initialAdminPassword` inside the running `jenkins-server` container and prints the password to your terminal.

    Copy the retrieved password, paste it into the "Administrator password" field on the Jenkins UI page ("Unlock Jenkins"), and click "Continue."

6.  **Customize Jenkins - Install Plugins:**
    *   After successfully entering the password, you'll land on the "Customize Jenkins" page. Jenkins will offer to install plugins.
    *   **Click the "Install suggested plugins" option.** This installs a curated set of plugins that are generally useful for most Jenkins setups, including essentials like Pipeline (for `Jenkinsfile` based pipelines), Git integration, and more.
    *   Wait patiently as Jenkins downloads and installs the plugins. This process can take several minutes depending on your internet connection. You'll see progress indicators for each plugin.

7.  **Create First Admin User:**
    *   Once plugin installation is complete, Jenkins will prompt you to "Create First Admin User."
    *   Fill in the form with your desired credentials:
        *   **Username:** (e.g., `admin`, or your preferred username)
        *   **Password:** (choose a strong, memorable password)
        *   **Confirm password:** (re-enter your chosen password)
        *   **Full name:** (your name)
        *   **E-mail address:** (your email address)
    *   Click "Save and Continue."

8.  **Instance Configuration - Jenkins URL:**
    *   The "Instance Configuration" page will appear next. It usually correctly auto-detects your Jenkins URL (e.g., `http://localhost:8080/`).
    *   Verify the URL is correct and click "Save and Finish."

9.  **Jenkins is Ready!**
    *   You should now see a "Jenkins is ready!" page.
    *   Click "Start using Jenkins."
    *   This will take you to the main Jenkins dashboard, logged in as the admin user you just created.

---

## 🏙️ Method 2: Native Installation (Alternative, Not Recommended for These Labs)

If you prefer not to use Docker, or cannot, you can install Jenkins directly on your system. This method requires you to manage the Java dependency yourself. **For consistency in these labs, the Docker method is strongly recommended.**

1.  **Download Jenkins:**
    *   Go to the official Jenkins download page: [https://www.jenkins.io/download/](https://www.jenkins.io/download/)
    *   Download the "Generic Java package (.war)" for the LTS (Long-Term Support) release.

2.  **Run Jenkins from the Command Line:**
    *   Open your terminal or command prompt.
    *   Navigate to the directory where you downloaded the `jenkins.war` file.
    *   Execute the following command (ensure your compatible JDK's `java` executable is in your system's PATH):
        ```bash
        java -jar jenkins.war --httpPort=8080
        ```
        (Using `--httpPort=8080` explicitly sets the port, though it's often the default. Jenkins will create a `.jenkins` home directory in your user's home folder by default to store its data.)

3.  **Follow On-Screen Instructions & UI Setup:**
    *   When Jenkins starts, it will print the location of the initial admin password to the console.
        *   Typical locations:
            *   Linux/macOS: `~/.jenkins/secrets/initialAdminPassword`
            *   Windows: `C:\Users\YourUserName\.jenkins\secrets\initialAdminPassword` (or wherever your user profile is)
    *   Open your web browser and navigate to [http://localhost:8080](http://localhost:8080).
    *   You will see the "Unlock Jenkins" page. Retrieve the password from the file path indicated in your console.
    *   Proceed with the UI setup steps 5 through 9 as described in the Docker installation method (Unlock Jenkins, Install Suggested Plugins, Create First Admin User, Instance Configuration).

---

## ✨ A Quick Tour of the Jenkins Dashboard

Once you've successfully logged into Jenkins, you'll be on the main dashboard. Here are a few key areas to familiarize yourself with:

-   **Left Sidebar (Navigation Menu):** This is your primary navigation hub.
    *   `New Item`: This is where you'll go to create new Jenkins jobs (e.g., Freestyle projects, Pipelines).
    *   `People`: Manage Jenkins users and their permissions.
    *   `Build History`: A chronological view of all builds that have run on your Jenkins instance.
    *   `Manage Jenkins`: The central administration page. From here, you can configure system settings, manage plugins (install, update, remove), manage nodes (agents), configure security, view system information, and much more.
    *   `My Views`: Customize how you see jobs on the dashboard.
-   **Main Content Panel:**
    *   Initially, this area might show a welcome message or a list of your Jenkins jobs (which will be empty after a fresh install). As you create jobs, they'll be listed here.
-   **Build Queue (Bottom Left):** Shows any builds that are currently waiting to be executed.
-   **Build Executor Status (Bottom Left):** Shows the Jenkins controller's built-in executors and their status (e.g., idle, or busy running a build).

Take a few moments to click around, especially "Manage Jenkins," to get a feel for the layout and the options available. **Avoid changing any settings randomly at this stage.**

---

## 🧹 Cleanup

When you're finished with your Jenkins session or want to reset your environment:

**If you used Docker (Method 1):**

1.  **Stop the Jenkins container:**
    ```bash
    docker stop jenkins-server
    ```
2.  **Remove the Jenkins container:**
    (Stopping it first is good practice before removing)
    ```bash
    docker rm jenkins-server
    ```
3.  **(Optional) Remove the Docker volume to delete all Jenkins data:**
    If you want to completely reset Jenkins and remove all configurations, jobs, plugins, and build history that were stored in the persistent volume, you can delete the volume.
    ```bash
    docker volume rm jenkins-data
    ```
    **⚠️ Caution:** This command permanently deletes the `jenkins-data` volume and all its contents. Only do this if you want a completely fresh start or are done with the labs and want to free up disk space.

**If you used Native Installation (Method 2):**

1.  **Stop the Jenkins process:**
    *   If you ran `java -jar jenkins.war` in a terminal, you can usually stop it by pressing `Ctrl+C` in that terminal window.
    *   If you installed Jenkins as a service, use your operating system's service management tools to stop the Jenkins service.
2.  **(Optional) Delete the Jenkins home directory:**
    To completely remove all Jenkins data for a native installation, you would delete the Jenkins home directory.
    *   Default locations:
        *   Linux/macOS: `~/.jenkins/`
        *   Windows: `C:\Users\YourUserName\.jenkins\` (or the `.jenkins` folder within your user profile directory)
    **⚠️ Caution:** Deleting this directory removes all your Jenkins configurations, jobs, and history. Only do this if you intend a full reset.

---

You have now successfully installed and configured Jenkins! You are ready to proceed with the labs. Remember to refer back to this guide if you need to set up Jenkins again or clarify any installation steps. 