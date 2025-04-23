from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variable to store network data
network_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global network_data
    if request.method == 'GET':
        return jsonify({"networks": network_data}), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data or "networks" not in data:
            return jsonify({"error": "No valid JSON data received"}), 400

        network_data = data["networks"]  # Store received data
        print("Received data:", network_data)
        return jsonify({"message": "Data received successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
