# Base image: Python 3.9 slim version
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install curl for health checks (if needed, or for consistency)
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (set by FLASK_RUN_PORT, defaults to 5001)
EXPOSE 5001

# Command to run the application
# Can be overridden in docker-compose for running tests
CMD ["python", "-u", "app.py"] 