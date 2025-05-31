from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # A simple greeting message for our web app
    return "Hello from your Flask app running in a Docker container! Lab 05 is a success!"

if __name__ == '__main__':
    # Run the app on port 5000, accessible from other containers or host
    app.run(host='0.0.0.0', port=5000, debug=True) 