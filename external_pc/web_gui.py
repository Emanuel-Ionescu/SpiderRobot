"""
Spider Robot Web GUI - Flask Backend
Serves the dashboard, video stream, and system metrics.
"""

from flask import Flask, Response, jsonify, render_template
import time
import multiprocessing as mp
import platform
import json
import cv2
import numpy as np
from sequences import SequenceManager

app = Flask(__name__)
frame_queue = mp.Queue()
command_queue = mp.Queue()
FAST_MODE = False

print("Initializing Sequence Manager...")
sequence_manager = SequenceManager()

# precomputing the sequences
start = time.time()
print("Computing sequences...")
sequence_manager.generate()
end = time.time()
print(f"Sequences computed in {end - start} seconds")

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

def run_sequence_loop(command_queue : mp.Queue, frame_queue : mp.Queue):
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
            if iterator < len(sequence_manager[seq_name]["commands"]):
                time.sleep(0.25)
                frame_queue.put(sequence_manager[seq_name]["frames"][iterator])
                time.sleep(sequence_manager[seq_name]["delay"])
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
        args=(command_queue, frame_queue)
    )
    seq_loop_proc.start()

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
