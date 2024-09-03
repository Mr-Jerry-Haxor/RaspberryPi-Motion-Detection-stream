import cv2
import mediapipe as mp
from datetime import datetime
import socket
import json
import threading

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# RTSP stream URL (localhost)
rtsp_url = "rtsp://127.0.0.1:8554/stream"

# Initialize video capture from RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Mapping landmark indices to their corresponding names
landmark_names = mp_pose.PoseLandmark


# TCP server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)
clients = []

def broadcast_data(data):
    for client in clients:
        try:
            client.sendall(data.encode('utf-8'))
        except:
            clients.remove(client)
            
            
# Accepting clients in a separate thread
def accept_clients():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"New connection from {addr}")
        # threading.Thread(target=handle_client, args=(client_socket,)).start()

def main():
    if not cap.isOpened():
        print("Error: Unable to open video capture")
        return

    while cap.isOpened():
        # Discard frames in the buffer to ensure the latest frame is processed
        for _ in range(5):
            cap.grab()

        ret, img = cap.read()
        if not ret:
            print("Error: Unable to read frame")
            break

        # Convert the frame to RGB for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Perform pose detection
        results = pose.process(img_rgb)
        
        # Draw the detected pose on the original video stream
        if results.pose_landmarks:
            
            #drawing lines and points on image
            # mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),mp_draw.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2))
            
            # Print landmark names and their corresponding coordinates
            keypoints = {}
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                name = landmark_names(idx).name
                coordinates = (landmark.x, landmark.y, landmark.z)
                keypoints[name] = coordinates

            # Convert the keypoints dictionary to a JSON string
            keypoints_json = json.dumps(keypoints, indent=4)
            
            # print(keypoints_json)
            broadcast_data(keypoints_json)
            
            # Print current timestamp
            # print(datetime.now().strftime("%H:%M:%S.%f"))

        # Display the frame
        # cv2.imshow('Frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Start the client handling thread
    client_thread = threading.Thread(target=accept_clients)
    client_thread.start()
    main()
