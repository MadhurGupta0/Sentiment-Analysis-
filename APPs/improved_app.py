from flask import Flask, render_template, jsonify,flash
import subprocess
import sys

app = Flask(__name__)

# Start the backend server as a subprocess
def start_backend_server():
    # Start the backend server in a new subprocess

    backend_process = subprocess.Popen([sys.executable, '../APIs/improved_api.py'])
    return backend_process


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-backend', methods=['POST'])
def start_backend():

    try:
        process = start_backend_server()
        flash("Backend server started.", "success")
        print("server started")
        return jsonify({"message": "Backend server started."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
