from flask import Flask
import logging
import sys

app = Flask(__name__)

# Configure logging to stdout for Docker
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

@app.route('/')
def home():
    app.logger.info("Service 1 received a request at the root endpoint.")
    return "Hello from Service 1!"

@app.route('/health')
def health():
    app.logger.info("Service 1 health check accessed.")
    return "Service 1 is healthy!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 