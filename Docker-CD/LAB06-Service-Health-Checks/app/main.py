import os
from flask import Flask
import redis
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Path for the API key secret
# Docker secrets are typically mounted in /run/secrets/
API_KEY_FILE_PATH = os.environ.get('API_KEY_FILE', '/run/secrets/api_key_secret')

# Path for a simple data file to demonstrate volume persistence
DATA_FILE_PATH = os.environ.get('DATA_FILE', '/data/app_counter.txt')

redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

# Initialize Redis connection
try:
    r = redis.Redis(host=redis_host, port=redis_port, socket_connect_timeout=5, health_check_interval=30)
    r.ping()
    app.logger.info(f"Successfully connected to Redis at {redis_host}:{redis_port}")
except redis.exceptions.ConnectionError as e:
    app.logger.error(f"Could not connect to Redis at {redis_host}:{redis_port}: {e}")
    r = None

def read_api_key():
    try:
        with open(API_KEY_FILE_PATH, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        app.logger.warning(f"API key file not found at {API_KEY_FILE_PATH}. Using default key.")
        return "default_api_key_not_set"
    except Exception as e:
        app.logger.error(f"Error reading API key from {API_KEY_FILE_PATH}: {e}")
        return "error_reading_api_key"

def get_app_counter():
    try:
        if not os.path.exists(os.path.dirname(DATA_FILE_PATH)):
            os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        with open(DATA_FILE_PATH, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    except (ValueError, Exception) as e:
        app.logger.error(f"Error reading or initializing app counter from {DATA_FILE_PATH}: {e}")
        return 0 # Default to 0 if file is corrupted or unreadable

def increment_app_counter():
    count = get_app_counter() + 1
    try:
        if not os.path.exists(os.path.dirname(DATA_FILE_PATH)):
            os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        with open(DATA_FILE_PATH, 'w') as f:
            f.write(str(count))
        return count
    except Exception as e:
        app.logger.error(f"Error writing app counter to {DATA_FILE_PATH}: {e}")
        return count -1 # Return previous count on failure


@app.route('/')
def hello_world():
    api_key = read_api_key()
    app_counter_val = increment_app_counter()
    
    response_text = f'Hello from the Web App! API Key: "{api_key}".<br/>'
    response_text += f'This app endpoint has been visited {app_counter_val} times (value from {DATA_FILE_PATH}).<br/>'

    if r:
        try:
            redis_hits = r.incr('redis_hits')
            response_text += f'Redis counter (at {redis_host}) has been incremented to: {redis_hits}.'
        except redis.exceptions.ConnectionError as e:
            app.logger.error(f"Redis connection error during request: {e}")
            response_text += "Could not connect to Redis to update its counter."
        except Exception as e:
            app.logger.error(f"An unexpected error occurred with Redis: {e}")
            response_text += "An error occurred with the Redis counter."
    else:
        response_text += "Redis is not connected."
    
    return response_text + "\\n"

@app.route('/health')
def health_check():
    # Check API key file presence as part of health, though app will use default if not found
    api_key_found = os.path.exists(API_KEY_FILE_PATH)
    api_key_status = "API key file found." if api_key_found else "API key file NOT found (using default)."

    redis_status = "Not Connected"
    if r:
        try:
            r.ping()
            redis_status = "Healthy and Connected"
        except redis.exceptions.ConnectionError:
            redis_status = "Connection Failed"
    
    return f"Web app is running.<br/>API Key Status: {api_key_status}<br/>Redis Status: {redis_status}\\n", 200

if __name__ == '__main__':
    # For production, debug mode should be off. 
    # Flask's default is debug=False unless FLASK_DEBUG=1 or FLASK_ENV=development is set.
    app.run(host='0.0.0.0', port=5000) 