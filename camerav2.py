import cv2
import numpy as np
from flask import Flask, render_template, Response, stream_with_context, request
import mediapipe as mp
import time
import threading

video = cv2.VideoCapture(0)
app = Flask('__name__')

# Initialize Mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Global variables for threading
frame_lock = threading.Lock()
ret = False
frame = None

def capture_frames():
    global ret, frame
    while True:
        with frame_lock:
            ret, frame = video.read()
        if not ret:
            break

# Start frame capture thread
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

def video_stream():
    global ret, frame
    prev_frame_time = time.time()
    while True:
        with frame_lock:
            if not ret or frame is None:
                continue
            img = frame.copy()

        # Perform pose detection
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Draw the detected pose on the original video/live stream
        if results.pose_landmarks:
            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                   mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                                   mp_draw.DrawingSpec((255, 0, 255), 2, 2))

        # Calculate frame rate
        new_frame_time = time.time()
        frame_rate = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time

        # Display frame rate on the frame
        cv2.putText(img, f'FPS: {frame_rate:.2f}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpeg', img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)
