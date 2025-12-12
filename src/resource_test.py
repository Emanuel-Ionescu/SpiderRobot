import psutil
import time
import threading
import os

def test_function():
    import cv2
    import numpy as np
    import time
    import mediapipe as mp

    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    l = []
    for i in range(100):
        frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        l.append(frame)
        time.sleep(0.5)
    

def monitor_resources(pid, duration, interval=1):
    process = psutil.Process(pid)
    end_time = time.time() + duration
    
    print(f"Monitoring PID {pid} for {duration} seconds...")
    print(f"{'Time':<10} {'CPU (%)':<10} {'Memory (MB)':<10}")
    
    try:
        while time.time() < end_time:
            cpu_usage = process.cpu_percent(interval=None)
            memory_usage = process.memory_info().rss / (1024 * 1024) # Convert to MB
            
            print(f"{time.strftime('%H:%M:%S'):<10} {cpu_usage:<10.2f} {memory_usage:<10.2f}")
            time.sleep(interval)
    except psutil.NoSuchProcess:
        print("Process ended.")

if __name__ == "__main__":
    pid = os.getpid()
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_resources, args=(pid, 60))
    monitor_thread.start()
    
    # Run the function
    print("Starting test_function...")
    test_function()
    print("test_function finished.")
    
    # Wait for monitor to finish (if test_function finishes early)
    monitor_thread.join()
