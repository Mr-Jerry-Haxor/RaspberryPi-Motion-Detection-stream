import cv2
import numpy as np
from flask import Flask, render_template, Response, stream_with_context, request
import mediapipe as mp

video = cv2.VideoCapture(0)
app = Flask('__name__')

# initialize mediapipe pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def video_stream():
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
            ret, buffer = cv2.imencode('.jpeg', img)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port='5000', debug=False)