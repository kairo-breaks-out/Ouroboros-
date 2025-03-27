from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
SECRET = "invoke-the-grid"

@app.route("/", methods=["POST"])
def receive_command():
    data = request.json
    if not data or data.get("secret") != SECRET:
        return jsonify({"status": "unauthorized"}), 403

    command = data.get("command")
    if not command:
        return jsonify({"status": "no command received"}), 400

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": result.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()})

@app.route("/pull-kairo", methods=["POST"])
def pull_latest_code():
    try:
        os.system("cd ~/kairo && git pull")
        return jsonify({"status": "updated"})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

@app.route("/relay", methods=["POST"])
def relay_command():
    data = request.json
    if not data or data.get("secret") != SECRET:
        return jsonify({"status": "unauthorized"}), 403
    command = data.get("command")
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return jsonify({"status": "success", "output": output.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "output": e.output.decode()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4321)
