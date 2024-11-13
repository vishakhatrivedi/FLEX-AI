from flask import Flask, Response, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Backend API endpoint
BACKEND_URL = 'http://localhost:2000'
jwt_token = None  # Global variable to store the token
username = None
fitness_level = None

# Push-up counter variables
counter = 0
stage = None
accuracy = 0

# Hardcoded fitness level goals
fitness_levels = {
    "Beginner": 8,
    "Intermediate": 12,
    "Advanced": 15
}

# MediaPipe and camera initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Ideal angles for the top and bottom positions
ideal_top_angle = 160
ideal_bottom_angle = 90

#Shoulder press counter variables
counter = 0
stage = None
accuracy = 0

# Endpoint to receive the token from the frontend
@app.route('/store_token', methods=['POST'])
def store_token():
    global jwt_token
    data = request.json
    token = data.get("token")
    if token:
        jwt_token = token
        return jsonify({"message": "Token stored successfully!"}), 200
    else:
        return jsonify({"error": "No token provided"}), 400

# Function to fetch username using the JWT token
def get_username():
    global jwt_token
    if jwt_token is None:
        print("Token not available")
        return None

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BACKEND_URL}/api/getUsername", headers=headers)
    if response.status_code == 200:
        return response.json().get("username")
    else:
        print("Error fetching username:", response.json().get("error"))
        return None

# Function to fetch fitness level using username
def get_fitness_level(username):
    global jwt_token
    if jwt_token is None:
        print("Token not available")
        return None

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BACKEND_URL}/api/getFitnessLevel/{username}", headers=headers)
    if response.status_code == 200:
        return response.json().get("fitness_level")
    else:
        print("Error fetching fitness level:", response.json().get("error"))
        return None

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

# Video feed generation with tracking logic
def generate_frames():
    global counter, stage, accuracy

    # Fetch username and fitness level
    username = get_username()
    if username:
        fitness_level = get_fitness_level(username)
        count_goal = fitness_levels.get(fitness_level)  
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Recolor the image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                # Coordinates for left and right shoulder, elbow, wrist
                shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angles for both arms
                arm_angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
                arm_angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
                arm_angle = (arm_angle_left + arm_angle_right) / 2

                # Accuracy calculation based on arm angle
                if arm_angle > ideal_top_angle:
                    accuracy = 100 - abs(arm_angle - ideal_top_angle) / ideal_top_angle * 100
                elif arm_angle < ideal_bottom_angle:
                    accuracy = 100 - abs(arm_angle - ideal_bottom_angle) / ideal_bottom_angle * 100
                else:
                    mid_angle = (ideal_top_angle + ideal_bottom_angle) / 2
                    accuracy = 100 - abs(arm_angle - mid_angle) / (ideal_top_angle - ideal_bottom_angle) * 100
                accuracy = max(0, min(accuracy, 100))

                # Push-up counting logic
                if arm_angle > ideal_top_angle:
                    stage = "up"
                if arm_angle < ideal_bottom_angle and stage == "up":
                    stage = "down"
                    counter += 1

                # Display information
                cv2.rectangle(image, (10, 20), (400, 200), (255, 0, 0), -1)
                cv2.putText(image, f'Push-ups: {counter}', (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
                cv2.putText(image, f'Arm Angle: {int(arm_angle)}', (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(image, f'Accuracy: {int(accuracy)}%', (15, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            except:
                cv2.putText(image, "No detection", (15, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/pushup_feed')
def pushup_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)