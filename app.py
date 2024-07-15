from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
from ftplib import FTP

app = Flask(__name__)

# Sample data for machines and jobs
machines = [
    {"id": 1, "name": "CNC Machine 1", "status": "Active"},
    {"id": 2, "name": "CNC Machine 2", "status": "Idle"}
]

jobs = [
    {"id": 1, "machine_id": 1, "job_name": "Job 1", "status": "Running"},
    {"id": 2, "machine_id": 2, "job_name": "Job 2", "status": "Pending"}
]

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'trimas_aerospace-logo-220.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/machines', methods=['GET'])
def get_machines():
    return jsonify(machines)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify(jobs)

@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

# FTP upload function
def upload_file_to_ftp(file_path, ftp_url, username, password):
    try:
        with FTP(ftp_url) as ftp:
            ftp.login(user=username, passwd=password)
            with open(file_path, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)
        return True
    except Exception as e:
        print(f"FTP upload failed: {e}")
        return False

@app.route('/api/files/upload_ftp', methods=['POST'])
def upload_file_via_ftp():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # FTP credentials (replace with your actual credentials)
        ftp_url = 'ftp.yourserver.com'
        username = 'your_username'
        password = 'your_password'

        if upload_file_to_ftp(file_path, ftp_url, username, password):
            return jsonify({"message": "File uploaded to FTP successfully"}), 200
        else:
            return jsonify({"error": "FTP upload failed"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(debug=True)
