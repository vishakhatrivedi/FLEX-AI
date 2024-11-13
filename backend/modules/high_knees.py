# 

from flask import Flask, Response, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
import requests
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Backend API endpoint
BACKEND_URL = 'http://localhost:2000'
jwt_token = None  # Global variable to store the token
username = None  # Global variable for username
fitness_level = None  # Global variable for fitness level

# Fitness level count goals
fitness_levels = {
    "Beginner": 10,
    "Intermediate": 20,
    "Advanced": 30
}

# Endpoint to receive the token and username from the frontend and store it in global variables
@app.route('/store_token', methods=['POST'])
def store_token():
    global jwt_token, username, fitness_level
    data = request.json
    jwt_token = data.get("token")
    username = data.get("username")
    fitness_level = data.get("fitness_level")
    
    if jwt_token and username and fitness_level:
        return jsonify({"message": "Token and user info stored successfully!"}), 200
    else:
        return jsonify({"error": "Incomplete user info provided"}), 400

# Function to calculate vertical distance between knee and hip
def calculate_distance(knee, hip):
    return knee[1] - hip[1]  # Only the Y-coordinate (vertical distance)

# Function to get the count goal based on fitness level
def get_count_goal():
    global fitness_level
    return fitness_levels.get(fitness_level, 10)  # Default to beginner level goal if not found

# MediaPipe and camera initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# High knee counter variables
counter = 0
left_stage = None
right_stage = None
knee_threshold = 0.1  # Adjust based on desired knee lift height

# Function to check if required landmarks are visible
def are_landmarks_visible(landmarks, indices):
    return all(landmarks[i].visibility > 0.5 for i in indices)

# High knees exercise tracking and frame generation
def generate_high_knees_frames():
    global counter, left_stage, right_stage
    exercise_completed = False  # Flag to check if the exercise is completed
    count_goal = get_count_goal()  # Retrieve goal count based on fitness level

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # If exercise is completed, display final message with background and stop
            if counter >= count_goal and not exercise_completed:
                exercise_completed = True  # Set the flag to stop further processing
                cv2.rectangle(frame, (30, 50), (700, 130), (0, 128, 0), -1)  # Green background for completion text
                cv2.putText(frame, "Exercise Completed! Move to the Next Exercise", (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                break  # Exit the loop to stop sending frames

            # Process the frame if exercise is not over
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Check if necessary landmarks are visible
                required_landmarks = [
                    mp_pose.PoseLandmark.LEFT_HIP.value,
                    mp_pose.PoseLandmark.LEFT_KNEE.value,
                    mp_pose.PoseLandmark.RIGHT_HIP.value,
                    mp_pose.PoseLandmark.RIGHT_KNEE.value
                ]
                
                if are_landmarks_visible(landmarks, required_landmarks):
                    # Get coordinates for knees and hips
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    
                    # Calculate vertical distances for both knees
                    left_knee_distance = calculate_distance(left_knee, left_hip)
                    right_knee_distance = calculate_distance(right_knee, right_hip)

                    # High knee counter logic for left knee
                    if left_knee_distance < -knee_threshold:  # Knee raised
                        left_stage = "up"
                    if left_knee_distance > -knee_threshold and left_stage == 'up':  # Knee back to neutral
                        left_stage = "down"
                        counter += 1

                    # High knee counter logic for right knee
                    if right_knee_distance < -knee_threshold:  # Knee raised
                        right_stage = "up"
                    if right_knee_distance > -knee_threshold and right_stage == 'up':  # Knee back to neutral
                        right_stage = "down"
                        counter += 1
            
            # Render high knee counter and status box with a larger font and square boxes
            cv2.rectangle(image, (10, 20), (500, 250), (255, 0, 0), -1)  # Background for username and counter
            cv2.putText(image, f'High Knees: {counter}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            cv2.putText(image, f'Left knee: {left_stage}', (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(image, f'Right knee: {right_stage}', (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Draw landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            # Convert the frame to JPEG format for video feed
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/high_knee_feed')
def video_feed():
    return Response(generate_high_knees_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
