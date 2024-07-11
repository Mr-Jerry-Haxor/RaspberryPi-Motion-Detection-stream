import cv2
import numpy as np
import socket
import asyncio
from flask import Flask, render_template, Response, request, jsonify
import mediapipe as mp
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack

app = Flask(__name__)

# Get the device IP dynamically
def get_ip_address():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))  # Doesn't even have to be reachable
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

DEVICE_IP = get_ip_address()
STREAM_URL = f'http://{DEVICE_IP}:8889/cam'

# MediaPipe Pose Solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

class PoseDetectionTrack(MediaStreamTrack):
    def __init__(self):
        super().__init__()  # initialize base class
        self.video = cv2.VideoCapture(STREAM_URL)
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.video.get(cv2.CAP_PROP_FPS))
        self.frame_rate = self.fps
        self.last_frame_time = 0

    async def recv(self):
        ret, img = self.video.read()
        if not ret:
            raise Exception("Failed to grab frame from RTSP stream.")
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        self.frame_rate = 1 / (current_time - self.last_frame_time)
        self.last_frame_time = current_time
        # Apply Pose Detection
        results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        # Draw Pose Landmarks
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                               mp_draw.DrawingSpec((255, 0, 0), 2, 2),
                               mp_draw.DrawingSpec((255, 0, 255), 2, 2))
        ret, buffer = cv2.imencode('.jpeg', img)
        frame = buffer.tobytes()
        return frame

# WebRTC Peer Connection
peer_connections = {}

@app.route('/')
def index():
    """Serve the HTML page to display the WebRTC video stream."""
    return render_template('index.html' , stream_url=STREAM_URL)

@app.route('/offer', methods=['POST'])
async def offer():
    data = await request.json
    offer_sdp = data['sdp']
    peer_connection = RTCPeerConnection()
    peer_connections[request.remote_addr] = peer_connection
    peer_connection.addTrack(PoseDetectionTrack())
    
    @peer_connection.on('track')
    def on_track(track):
        if track.kind == 'video':
            print('Track received:', track)

    @peer_connection.on('iceconnectionstatechange')
    async def on_ice_connection_state_change():
        if peer_connection.iceConnectionState == 'failed':
            await peer_connection.close()
            del peer_connections[request.remote_addr]

    offer = RTCSessionDescription(sdp=offer_sdp, type='offer')
    await peer_connection.setRemoteDescription(offer)
    answer = await peer_connection.createAnswer()
    await peer_connection.setLocalDescription(answer)

    return jsonify({'sdp': peer_connection.localDescription.sdp})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
