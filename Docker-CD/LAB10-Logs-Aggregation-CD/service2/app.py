from flask import Flask
import logging
import sys

app = Flask(__name__)

# Configure logging to stdout for Docker
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)

@app.route('/')
def home():
    app.logger.info("SERVICE 2 HIT: Request received at root.")
    return "Greetings from Service 2!"

@app.route('/health')
def health():
    app.logger.info("SERVICE 2 HIT: Health check successful.")
    return "Service 2 is up and running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 