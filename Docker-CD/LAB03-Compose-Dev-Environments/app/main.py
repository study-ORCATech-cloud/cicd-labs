from flask import Flask
import redis
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get Redis host from environment variable or use a default
# This allows flexibility for local Docker Compose and other environments.
redis_host = os.environ.get('REDIS_HOST', 'redis') # Default to 'redis' which is the service name in docker-compose
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Initialize Redis connection
try:
    r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=5, health_check_interval=30)
    r.ping() # Check connection
    app.logger.info(f"Successfully connected to Redis at {redis_host}:{redis_port}")
except redis.exceptions.ConnectionError as e:
    app.logger.error(f"Could not connect to Redis at {redis_host}:{redis_port}: {e}")
    r = None # Set r to None if connection fails

@app.route('/')
def hello_world():
    if r:
        try:
            hits = r.incr('hits')
            return f'Hello from the Web App! This page has been visited {hits} times. (Dev Mode)\n'
        except redis.exceptions.ConnectionError as e:
            app.logger.error(f"Redis connection error during request: {e}")
            return "Hello from the Web App! Could not connect to Redis to update counter. (Dev Mode)\n", 500
        except Exception as e:
            app.logger.error(f"An unexpected error occurred with Redis: {e}")
            return "Hello from the Web App! An error occurred with the counter. (Dev Mode)\n", 500
    else:
        return "Hello from the Web App! Redis is not connected. (Dev Mode)\n", 500

@app.route('/health')
def health_check():
    if r:
        try:
            r.ping()
            return "Web app is healthy and connected to Redis (Dev Mode)", 200
        except redis.exceptions.ConnectionError:
            return "Web app is running, but Redis connection failed (Dev Mode)", 503
    return "Web app is running, but Redis is not configured/connected (Dev Mode)", 503

if __name__ == '__main__':
    # Port 5000 is exposed by the Dockerfile for the web service
    # DEBUG mode is typically enabled via FLASK_DEBUG=1 or FLASK_ENV=development environment variable
    # which Flask's app.run() picks up.
    app.run(host='0.0.0.0', port=5000) # debug=True is often set by FLASK_DEBUG or FLASK_ENV 