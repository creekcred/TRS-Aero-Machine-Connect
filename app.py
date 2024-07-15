from flask import Flask, request, jsonify

app = Flask(__name__)

machines = [
    {"id": 1, "name": "CNC Machine 1", "status": "Active"},
    {"id": 2, "name": "CNC Machine 2", "status": "Idle"}
]

jobs = [
    {"id": 1, "machine_id": 1, "job_name": "Job 1", "status": "Running"},
    {"id": 2, "machine_id": 2, "job_name": "Job 2", "status": "Pending"}
]

@app.route('/api/machines', methods=['GET'])
def get_machines():
    return jsonify(machines)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    return jsonify(jobs)

@app.route('/api/files/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(f"/ftp_directory/{file.filename}")
    return jsonify({"message": "File uploaded successfully"})

if __name__ == '__main__':
    app.run(debug=True)
