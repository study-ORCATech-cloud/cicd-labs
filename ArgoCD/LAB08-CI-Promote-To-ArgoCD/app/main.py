from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from CI/CD GitOps Demo!',
        'version': os.getenv('APP_VERSION', 'v1.0.0'),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'timestamp': datetime.datetime.now().isoformat(),
        'hostname': os.getenv('HOSTNAME', 'localhost')
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/version')
def version():
    return jsonify({
        'version': os.getenv('APP_VERSION', 'v1.0.0'),
        'build_date': os.getenv('BUILD_DATE', 'unknown'),
        'git_commit': os.getenv('GIT_COMMIT', 'unknown')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) 