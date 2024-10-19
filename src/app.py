from flask import Flask, render_template, request, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Add your processing logic here
    return jsonify({"message": "Data processed successfully"})

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "health-ai-app"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))