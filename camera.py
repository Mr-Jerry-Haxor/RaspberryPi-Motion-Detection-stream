import cv2
import numpy as np
from flask import Flask, render_template, Response, stream_with_context, request
import mediapipe as mp
import time

video = cv2.VideoCapture(0)
app = Flask('__name__')

# initialize mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def video_stream():
    prev_frame_time = 0
    while True:
        ret, img = video.read()
        if not ret:
            break
        else:
            # do Pose detection
            results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # draw the detected pose on original video/ live stream
            mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                   mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                                   mp_draw.DrawingSpec((255, 0, 255), 2, 2)
                                   )
            # Calculate frame rate
            new_frame_time = time.time()
            frame_rate = 1 / (new_frame_time - prev_frame_time)
            prev_frame_time = new_frame_time
            # Display frame rate on the frame
            cv2.putText(img, f'FPS: {frame_rate}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            ret, buffer = cv2.imencode('.jpeg', img)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/pose_detection_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port='5000', debug=False)