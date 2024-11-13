# from flask import Flask, Response
# import cv2
# import numpy as np
# import mediapipe as mp
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)


# # Function to calculate angle between three points
# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)
#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)
#     return 360 - angle if angle > 180.0 else angle

# # MediaPipe and camera initialization
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# # Curl counter variables
# counter = 0
# stage = None
# accuracy = 0

# # Ideal angles for curl positions
# ideal_top_angle = 30
# ideal_bottom_angle = 160

# # Required landmark indices
# required_indices = [
#     mp_pose.PoseLandmark.LEFT_SHOULDER.value,
#     mp_pose.PoseLandmark.LEFT_ELBOW.value,
#     mp_pose.PoseLandmark.LEFT_WRIST.value
# ]

# def are_landmarks_visible(landmarks, indices):
#     return all(landmarks[i].visibility > 0.5 for i in indices)

# def generate_frames():
#     global counter, stage, accuracy
#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success:
#                 break

#             # Process the frame
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = pose.process(image)
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             if results.pose_landmarks:
#                 landmarks = results.pose_landmarks.landmark

#                 if are_landmarks_visible(landmarks, required_indices):
#                     shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                     elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#                     wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

#                     # Calculate the angle
#                     angle = calculate_angle(shoulder, elbow, wrist)

#                     # Calculate accuracy
#                     if angle > ideal_bottom_angle:
#                         accuracy = 100 - abs(angle - ideal_bottom_angle) / ideal_bottom_angle * 100
#                     elif angle < ideal_top_angle:
#                         accuracy = 100 - abs(angle - ideal_top_angle) / ideal_top_angle * 100
#                     else:
#                         mid_angle = (ideal_top_angle + ideal_bottom_angle) / 2
#                         accuracy = 100 - abs(angle - mid_angle) / (ideal_bottom_angle - ideal_top_angle) * 100

#                     accuracy = max(0, min(accuracy, 100))

#                     # Curl counter logic
#                     if angle > ideal_bottom_angle:
#                         stage = "down"
#                     if angle < ideal_top_angle and stage == "down":
#                         stage = "up"
#                         counter += 1

#                     # Display metrics on the frame
#                     cv2.putText(image, f'Angle: {int(angle)}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#                     cv2.putText(image, f'Accuracy: {int(accuracy)}%', (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#                     cv2.putText(image, f'REPS: {counter}', (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#                     cv2.putText(image, f'Stage: {stage}', (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#                 else:
#                     cv2.putText(image, "Adjust Position", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#             # Render pose landmarks on the image
#             mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                       mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                                       mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

#             # Convert the frame to JPEG format
#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/curl_feed')
# def curl_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)

from flask import Flask, Response, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables
jwt_token = None  # Global variable to store the token
username = None
fitness_level = 'basic'
count_goal = 8  # Default goal for 'basic' level

# Define count goals for each fitness level
fitness_level_goals = {
    "basic": 8,
    "intermediate": 12,
    "advanced": 15
}

# Endpoint to receive and store token and user information
@app.route('/store_token', methods=['POST'])
def store_token():
    global jwt_token, username, fitness_level, count_goal
    data = request.json
    token = data.get("token")
    username = data.get("username")
    fitness_level = data.get("fitness_level")  # Default to 'basic' if not provided

    # Set count goal based on fitness level from the dictionary
    count_goal = fitness_level_goals.get(fitness_level)  # Default to 8 if level not found

    if token:
        jwt_token = token
        return jsonify({"message": "Token stored successfully!", "username": username, "fitness_level": fitness_level, "count_goal": count_goal}), 200
    else:
        return jsonify({"error": "No token provided"}), 400

# Endpoint to get username
@app.route('/get_username', methods=['GET'])
def get_username():
    if username:
        return jsonify({"username": username}), 200
    else:
        return jsonify({"error": "Username not set"}), 400

# Endpoint to get fitness level and count goal
@app.route('/get_fitness_level', methods=['GET'])
def get_fitness_level():
    if fitness_level:
        return jsonify({"fitness_level": fitness_level, "count_goal": count_goal}), 200
    else:
        return jsonify({"error": "Fitness level not set"}), 400

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

# MediaPipe and camera initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Curl counter variables
counter = 0
stage = None
accuracy = 0
exercise_completed = False  # Flag to stop once the count goal is reached

# Ideal angles for curl positions
ideal_top_angle = 30
ideal_bottom_angle = 160

# Required landmark indices
required_indices = [
    mp_pose.PoseLandmark.LEFT_SHOULDER.value,
    mp_pose.PoseLandmark.LEFT_ELBOW.value,
    mp_pose.PoseLandmark.LEFT_WRIST.value
]

def are_landmarks_visible(landmarks, indices):
    return all(landmarks[i].visibility > 0.5 for i in indices)

def generate_frames():
    global counter, stage, accuracy, exercise_completed

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # If exercise is completed, display final message and stop
            if counter >= count_goal and not exercise_completed:
                exercise_completed = True
                cv2.rectangle(frame, (30, 50), (700, 130), (0, 128, 0), -1)  # Green background for completion text
                cv2.putText(frame, "Exercise Completed! Move to the Next Exercise", (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                break

            # Process the frame if exercise is not over
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                if are_landmarks_visible(landmarks, required_indices):
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate the angle
                    angle = calculate_angle(shoulder, elbow, wrist)

                    # Calculate accuracy
                    if angle > ideal_bottom_angle:
                        accuracy = 100 - abs(angle - ideal_bottom_angle) / ideal_bottom_angle * 100
                    elif angle < ideal_top_angle:
                        accuracy = 100 - abs(angle - ideal_top_angle) / ideal_top_angle * 100
                    else:
                        mid_angle = (ideal_top_angle + ideal_bottom_angle) / 2
                        accuracy = 100 - abs(angle - mid_angle) / (ideal_bottom_angle - ideal_top_angle) * 100

                    accuracy = max(0, min(accuracy, 100))

                    # Curl counter logic
                    if angle > ideal_bottom_angle:
                        stage = "down"
                    if angle < ideal_top_angle and stage == "down":
                        stage = "up"
                        counter += 1

                    # Draw background rectangles for the text
                    cv2.rectangle(image, (10, 10), (350 , 80), (255, 0, 0), -1)  # Blue box for reps
                    cv2.rectangle(image, (10, 90), (300, 150), (255, 0, 0), -1)  # Blue box for stage
                    cv2.rectangle(image, (10, 160), (300, 220), (255, 0, 0), -1)  # Blue box for angle
                    cv2.rectangle(image, (10, 230), (300, 290), (255, 0, 0), -1)  # Blue box for accuracy

                    # Display metrics on the frame
                    cv2.putText(image, f'REPS: {counter}', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                    cv2.putText(image, f'Stage: {stage}', (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(image, f'Angle: {int(angle)}', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(image, f'Accuracy: {int(accuracy)}%', (20, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    # Display a warning if the required landmarks are not visible
                    cv2.rectangle(image, (10, 160), (400, 220), (0, 0, 255), -1)  # Red box for "Adjust Position"
                    cv2.putText(image, "Adjust Position", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Render pose landmarks on the image
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/curl_feed')
def curl_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003,debug=False)
