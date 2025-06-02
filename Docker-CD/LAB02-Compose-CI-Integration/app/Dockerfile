# Base image: Python 3.9 slim version
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to reduce image size
# Using --default-timeout to avoid issues in constrained CI environments
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
# Gunicorn is a common choice for production, but Flask dev server is fine for this lab.
# Using `python -u main.py` for unbuffered output, which is good for logging.
CMD ["python", "-u", "main.py"] 