from flask import Flask, render_template, Response, request, jsonify
from multiprocessing import Queue
import threading
import time
import cv2

app = Flask(__name__)

# Global queue for frames - will be set from external process
frame_queue = None
command_queue = None

def set_frame_queue(queue):
    """Set the frame queue from external process"""
    global frame_queue
    frame_queue = queue
    print("WEB=> Frame queue connected!")

def set_command_queue(queue):
    """Set the command queue from external process"""
    global command_queue
    command_queue = queue
    print("WEB=> Command queue connected!")

def gen_frames():
    """Generator function to yield frames from the queue"""
    global frame_queue
    
    if frame_queue is None:
        print("WEB=> Warning: Frame queue not initialized")
        return
    
    while True:
        try:
            if not frame_queue.empty():
                frame = frame_queue.get(timeout=1)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                time.sleep(0.01)  # Small delay to prevent busy waiting
        except Exception as e:
            print(f"WEB=> Error in gen_frames: {e}")
            time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/button/<int:button_id>', methods=['POST'])
def button_press(button_id):
    print(f"WEB=> Button {button_id} pressed!")
    
    # Add your custom logic here based on button_id
    messages = {
        1: "Stand Up",
        2: "Sit Down", 
        3: "Walk",
        4: "Pause"
    }

    commands = {
        1: "stand_up",
        2: "sit_down", 
        3: "walk",
        4: "pause"
    }
    
    message = messages.get(button_id, f"Button {button_id} pressed")
    print(f"WEB=> {message}")

    if command_queue is not None:
        command_queue.put(commands[button_id])
    
    return jsonify({"status": "success", "message": message})

def run_server(frame_queue, command_queue, host='0.0.0.0', port=5000):
    """Run the Flask server with the provided queue"""
    set_frame_queue(frame_queue)
    set_command_queue(command_queue)
    print(f"WEB=> Starting server on http://{host}:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)

if __name__ == '__main__':
    # For testing without queue
    print("WEB=> Running in standalone mode - no frame queue")
    print("WEB=> Server starting on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
