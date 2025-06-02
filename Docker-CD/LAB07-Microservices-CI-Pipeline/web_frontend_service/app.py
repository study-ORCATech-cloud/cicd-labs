from flask import Flask, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

API_SERVICE_URL = os.environ.get("API_SERVICE_URL", "http://api_service:5000")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Web Frontend</title>
</head>
<body>
    <h1>Welcome to the Web Frontend Service!</h1>
    <p>Service ID: {{ service_id }}</p>
    <h2>Data from API Service ({{ api_url }}):</h2>
    <pre>{{ api_data | tojson(indent=2) }}</pre>
    <p><i>API Call Status: {{ api_call_status }}</i></p>
    <hr>
    <p><a href="/health">Health Check</a></p>
</body>
</html>
'''

@app.route('/')
def home():
    service_id = os.environ.get("SERVICE_ID", "web_frontend_01")
    api_data = None
    api_call_status = "Not called yet"
    try:
        response = requests.get(f"{API_SERVICE_URL}/data", timeout=5)
        if response.status_code == 200:
            api_data = response.json()
            api_call_status = f"Successfully fetched data (HTTP {response.status_code})"
        else:
            api_call_status = f"Error fetching data. API returned HTTP {response.status_code}: {response.text}"
            api_data = {"error": response.text, "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        api_call_status = f"Error connecting to API service: {e}"
        api_data = {"error": str(e)}
        
    return render_template_string(HTML_TEMPLATE, 
                                service_id=service_id, 
                                api_data=api_data, 
                                api_url=API_SERVICE_URL,
                                api_call_status=api_call_status)

@app.route('/health')
def health_check():
    # Basic health check for the frontend itself
    frontend_status = {"status": "healthy", "service": "Web Frontend"}
    
    # Check connectivity to the API service as part of its health
    try:
        api_response = requests.get(f"{API_SERVICE_URL}/health", timeout=2)
        if api_response.status_code == 200:
            frontend_status["dependencies"] = {"api_service": "healthy"}
        else:
            frontend_status["dependencies"] = {"api_service": f"unhealthy (HTTP {api_response.status_code})"}
    except requests.exceptions.RequestException:
        frontend_status["dependencies"] = {"api_service": "unreachable"}
        
    return jsonify(frontend_status), 200

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_RUN_PORT", 5001))
    app.run(host='0.0.0.0', port=port) 