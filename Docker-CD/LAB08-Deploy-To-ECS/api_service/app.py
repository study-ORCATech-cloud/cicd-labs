from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the API Service!", service_id=os.environ.get("SERVICE_ID", "api_service_01"))

@app.route('/data')
def get_data():
    return jsonify(data=[
        {"id": 1, "name": "Item 1", "value": 100},
        {"id": 2, "name": "Item 2", "value": 200}
    ], source="API Service")

@app.route('/health')
def health_check():
    return jsonify(status="healthy", service="API Service"), 200

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 5000))
    app.run(host='0.0.0.0', port=port) 