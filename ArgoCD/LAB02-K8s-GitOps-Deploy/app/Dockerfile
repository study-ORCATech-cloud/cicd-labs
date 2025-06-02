# This is a complete and working Dockerfile for the Python Flask application.
# LAB02 README.md will guide you on building an image from this file.
FROM python:3.9-slim

WORKDIR /app

COPY ./ ./

RUN pip install Flask

EXPOSE 5000

CMD ["python", "./main.py"] 