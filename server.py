from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
pending_data = []

@app.route("/send", methods=["POST"])
def receive_data():
    global pending_data
    try:
        data = request.get_json()
        pending_data.append(data)
        return jsonify({"status": "✅ Data received and queued"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/fetch", methods=["POST"])
def send_data_to_host():
    global pending_data
    req = request.get_json()
    user_id = req.get("user_id")
    if not user_id:
        return jsonify({"error": "❌ Missing user_id"}), 400
    
    user_data = [d for d in pending_data if d.get("user_id") == user_id]
    pending_data = [d for d in pending_data if d.get("user_id") != user_id]
    return jsonify(user_data), 200

@app.route("/", methods=["GET"])
def index():
    return "🛰️ Relay Server Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
