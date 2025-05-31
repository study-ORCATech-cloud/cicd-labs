# Dockerfile

# Base Image: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
# Source (./app/) to Destination (in container /app/)
COPY ./app/ /app/

# Command to run the application
CMD ["python", "main.py"] 