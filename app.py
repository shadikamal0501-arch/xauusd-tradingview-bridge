from flask import Flask, request, jsonify
import time

app = Flask(__name__)
latest_signal = {
    "action": "",
    "id": "",
    "sl": 0,
    "tp": 0
}

signal_time = 0


@app.route("/signal", methods=["POST"])
def receive_signal():
    global latest_signal, signal_time

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"ok": False, "error": "Invalid JSON"}), 400

    latest_signal = data
    signal_time = time.time()

    print("SIGNAL RECEIVED:", data)

    return jsonify({"ok": True})


@app.route("/signal", methods=["GET"])
def send_signal():
    # Signal expires after 15 seconds
    if time.time() - signal_time > 15:
        return jsonify({
            "action": "",
            "id": ""
        })

    return jsonify(latest_signal)


@app.route("/", methods=["GET"])
def home():
    return "XAUUSD TradingView Bridge is running."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
