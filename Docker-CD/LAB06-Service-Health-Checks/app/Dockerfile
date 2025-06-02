# Base image: Python 3.9 slim version
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# TODO_INSTALL_CURL: Install curl for the health check.
# On Debian-based images (like python:3.9-slim), you can use apt-get.
# Remember to update package lists first and clean up apt cache afterwards to keep the image small.
# Example structure: RUN <package_manager_update_cmd> && <package_manager_install_cmd> -y curl && <package_manager_cleanup_cmd>

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to reduce image size
# Using --default-timeout to avoid issues in constrained CI environments
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application code
# For development, this will be overwritten by the volume mount in docker-compose.yml
# However, it's good practice to include it so the image can also run standalone if needed.
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
# For development, Flask's reloader is often enabled via environment variables like FLASK_DEBUG=1 or FLASK_ENV=development
# The CMD here is a sensible default. The actual command behavior might be influenced by these env vars if set.
CMD ["python", "-u", "main.py"] 