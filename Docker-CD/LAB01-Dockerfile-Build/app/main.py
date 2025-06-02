from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker World! This is Lab 01.'

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to be accessible outside the container
    # And on port 5000, which we will expose in the Dockerfile
    app.run(host='0.0.0.0', port=5000, debug=True) 