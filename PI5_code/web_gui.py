"""
Spider Robot Web GUI - Flask Backend
Serves the dashboard, video stream, and system metrics.
"""

from flask import Flask, Response, jsonify, render_template
import time
import multiprocessing as mp
import subprocess
import platform
import json
import psutil
import cv2
import numpy as np
from utils import SerialClient, DummySerialClient
import json

app = Flask(__name__)
frame_queue = mp.Queue()
command_queue = mp.Queue()
FAST_MODE = False

# getting sequences from json file
with open("sequences.json", "r") as f:
    sequences_json = json.load(f)

# setting up serial connection
serial_connection = None
for device in ["ttyACM0", "ttyACM1"]:
    try:
        serial_connection = SerialClient(f"/dev/{device}")
        print("PICO found!")
        print(f"Pico on port: /dev/{device}")
        break
    except Exception as e:
        pass    

if serial_connection is None:
    print("No PICO found!")
    print("Using dummy serial connection")
    serial_connection = DummySerialClient()

# ---------------------------------------------------------------------------
# System metrics helpers
# ---------------------------------------------------------------------------

def _get_cpu_percent() -> float:
    return psutil.cpu_percent(interval=None)

# ---------------------------------------------------------------------------
# PMIC helpers — cache the subprocess output for 1 s to avoid spawning a
# new process on every metric poll.
# ---------------------------------------------------------------------------
_pmic_cache: dict = {"ts": 0.0, "data": {}}

def _read_pmic() -> dict[str, float]:
    """Run vcgencmd pmic_read_adc and return a name→value dict (cached 1 s)."""
    now = time.time()
    if now - _pmic_cache["ts"] < 1.0:
        return _pmic_cache["data"]

    try:
        raw = subprocess.check_output(
            ["vcgencmd", "pmic_read_adc"],
            timeout=2, text=True, stderr=subprocess.DEVNULL
        )
        # Each line looks like:  "  EXT5V_V volt(24)=4.95130000V"
        # or                     "  VDD_CORE_A current(7)=0.43757000A"
        data: dict[str, float] = {}
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            # name is the first token, value is after '='
            parts = line.split()
            if len(parts) >= 2 and "=" in parts[-1]:
                name = parts[0]
                val_str = parts[-1].split("=")[-1]  # e.g. "4.95130000V"
                val_str = val_str.rstrip("VAvc")     # strip unit suffix
                try:
                    data[name] = float(val_str)
                except ValueError:
                    pass
        _pmic_cache["data"] = data
    except Exception:
        pass  # keep stale cache on error

    _pmic_cache["ts"] = now
    return _pmic_cache["data"]

def _get_vdd_voltage() -> float:
    try:
        return _read_pmic().get("EXT5V_V", 0.0)
    except Exception:
        return 0.0

def _get_current() -> float:
    try:
        return _read_pmic().get("VDD_CORE_A", 0.0)
    except Exception:
        return 0.0

def _get_cpu_temp() -> float:
    try:
        raw = subprocess.check_output(
            ["vcgencmd", "measure_temp"],
            timeout=2, text=True, stderr=subprocess.DEVNULL
        )
        return float(raw.split("=")[1][:-3])
    except Exception:
        return 0.0  

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    """MJPEG stream endpoint."""

    def stream():
        while True:
            if frame_queue.empty():
                time.sleep(0.02)
                continue
            print("Sending frame to frontend")
            frame = frame_queue.get()
            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + buf.tobytes() + b"\r\n"
            )

    return Response(
        stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/metrics")
def metrics():
    """JSON endpoint polled by the frontend every second."""
    data = {
        "cpu": round(_get_cpu_percent(), 1),
        "vdd": round(_get_vdd_voltage(), 1),
        "current": round(_get_current(), 1),
        "temp": round(_get_cpu_temp(), 1),
        "timestamp": time.time(),
    }
    return jsonify(data)


@app.route("/command/<cmd>", methods=["POST"])
def command(cmd: str):
    """Receives robot commands from the frontend."""
    valid = {
        "pause", "sit_down", "stand_up",
        "walk_forward", "walk_backward",
        "turn_left", "turn_right",
    }
    if cmd not in valid:
        return jsonify({"status": "error", "message": "unknown command"}), 400
    print(f"[CMD] Received: {cmd}")
    if FAST_MODE and cmd in ["walk_forward", "turn_left", "turn_right"]:
        cmd = "fast_" + cmd
    command_queue.put(cmd)
    return jsonify({"status": "ok", "command": cmd})


@app.route("/set_fast_mode", methods=["POST"])
def set_fast_mode():
    global FAST_MODE
    from flask import request
    data = request.get_json()
    if data and "fast_mode" in data:
        FAST_MODE = bool(data["fast_mode"])
        print(f"[CMD] Fast mode set to: {'ON' if FAST_MODE else 'OFF'}")
        return jsonify({"status": "ok", "fast_mode": FAST_MODE})
    return jsonify({"status": "error"}), 400


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_sequence_loop(command_queue : mp.Queue):
    seq_name = None
    iterator = 0

    while True:
        if command_queue.empty() and seq_name is None:
            time.sleep(0.02)
            continue

        if not command_queue.empty():
            seq_name = command_queue.get()
            if seq_name == "pause":
                seq_name = None
                iterator = 0

        if seq_name is not None:
            print("Running:", seq_name)
            if iterator < len(sequences_json[seq_name]["commands"]):
                print("PI5 ==> PICO:", sequences_json[seq_name]["commands"][iterator])
                response = serial_connection(sequences_json[seq_name]["commands"][iterator])
                time.sleep(sequences_json[seq_name]["delay"])
                print("PI5 <== PICO:", response)
                iterator += 1
            else:
                seq_name = None
                iterator = 0
    

if __name__ == "__main__":
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    seq_loop_proc = mp.Process(
        target=run_sequence_loop,
        args=(command_queue,)
    )
    seq_loop_proc.start()

    psutil.cpu_percent(interval=None)
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
