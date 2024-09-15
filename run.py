from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from utils.table_extractor import extract_table
from flask_cors import CORS

# Set up the Flask app
app = Flask(__name__)
CORS(app)

# Directory for uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # Check if the file has a valid filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Process the image to extract table data
    table_data = extract_table(filepath)

    # Return JSON response with table data
    return jsonify({"table_data": table_data})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "Server is running"}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
