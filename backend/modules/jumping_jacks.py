# from flask import Flask, Response
# import cv2
# import numpy as np
# import mediapipe as mp
# from flask_cors import CORS


# app = Flask(__name__)
# CORS(app)

# # Initialize MediaPipe and webcam
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# cap = cv2.VideoCapture(0)
# frame_width = 1280
# frame_height = 720
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# # Jumping jacks counter variables
# counter = 0
# arm_stage = None
# leg_stage = None
# arm_accuracy = 0
# leg_accuracy = 0

# # Ideal arm angle and leg distance for correct jumping jack position
# ideal_arm_angle = 180  # Arms straight up
# ideal_leg_distance = 0.15 * frame_width  # Normalized distance scaled by frame width for legs spread

# def generate_frames():
#     global counter, arm_stage, leg_stage, arm_accuracy, leg_accuracy

#     with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             success, frame = cap.read()
#             if not success:
#                 break

#             # Recolor image to RGB
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = pose.process(image)
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             if results.pose_landmarks:
#                 landmarks = results.pose_landmarks.landmark

#                 # Calculate distances and angles
#                 shoulder_left, elbow_left, wrist_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
#                 shoulder_right, elbow_right, wrist_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
#                 ankle_left, ankle_right = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value], landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

#                 # Leg distance and leg accuracy
#                 leg_distance = abs((ankle_left.x - ankle_right.x) * frame_width)
#                 leg_accuracy = 100 - min(abs(leg_distance - ideal_leg_distance) / ideal_leg_distance * 100, 100)

#                 # Calculate arm angles and accuracy
#                 arm_angle_left = np.degrees(np.arctan2(wrist_left.y - elbow_left.y, wrist_left.x - elbow_left.x) - np.arctan2(shoulder_left.y - elbow_left.y, shoulder_left.x - elbow_left.x))
#                 arm_angle_right = np.degrees(np.arctan2(wrist_right.y - elbow_right.y, wrist_right.x - elbow_right.x) - np.arctan2(shoulder_right.y - elbow_right.y, shoulder_right.x - elbow_right.x))
#                 arm_angle_left = 360 + arm_angle_left if arm_angle_left < 0 else arm_angle_left
#                 arm_angle_right = 360 + arm_angle_right if arm_angle_right < 0 else arm_angle_right

#                 arm_accuracy = (100 - abs((arm_angle_left - ideal_arm_angle) / ideal_arm_angle * 100) + 100 - abs((arm_angle_right - ideal_arm_angle) / ideal_arm_angle * 100)) / 2

#                 # Update stages and count
#                 if leg_distance > ideal_leg_distance * 0.8:
#                     if arm_stage != "up":
#                         arm_stage = "up"
#                     if leg_stage != "up" and arm_stage == "up":
#                         leg_stage = "up"
#                 if leg_distance < ideal_leg_distance * 0.2:
#                     if arm_stage == "up" and leg_stage == "up":
#                         arm_stage = "down"
#                         leg_stage = "down"
#                         counter += 1

#                 # Display data
#                 cv2.putText(image, f'REPS: {counter}', (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#                 cv2.putText(image, f'Arm Accuracy: {int(arm_accuracy)}%', (15, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#                 cv2.putText(image, f'Leg Accuracy: {int(leg_accuracy)}%', (15, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#             else:
#                 cv2.putText(image, "No detection", (15, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#             # Draw landmarks and bounding box
#             mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                       mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
#                                       mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/jumping_jacks_feed')
# def jumping_jacks_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5009)

from flask import Flask, Response, request, jsonify
import cv2
import numpy as np
import mediapipe as mp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables for token, username, and fitness level
jwt_token = None
username = None
fitness_level = None

# Fitness level count goals
fitness_levels = {
    "Beginner": 10,
    "Intermediate": 20,
    "Advanced": 30
}

# Initialize MediaPipe and webcam
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
frame_width = 1280
frame_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

# Jumping jacks counter variables
counter = 0
arm_stage = None
leg_stage = None
arm_accuracy = 0
leg_accuracy = 0
exercise_completed = False

# Ideal arm angle and leg distance for correct jumping jack position
ideal_arm_angle = 180  # Arms straight up
ideal_leg_distance = 0.15 * frame_width  # Normalized distance scaled by frame width for legs spread

# Endpoint to receive the token, username, and fitness level from the frontend
@app.route('/store_token', methods=['POST'])
def store_token():
    global jwt_token, username, fitness_level
    data = request.json
    jwt_token = data.get("token")
    username = data.get("username")
    fitness_level = data.get("fitness_level")  # Retrieve fitness level
    
    if jwt_token and username and fitness_level:
        return jsonify({"message": "Token and user info stored successfully!"}), 200
    else:
        return jsonify({"error": "Incomplete user info provided"}), 400

# Function to determine the count goal based on fitness level
def get_count_goal():
    global fitness_level
    return fitness_levels.get(fitness_level, 10)  # Default to beginner level goal if not found

# Function to calculate angles and distances for arms and legs
def calculate_arm_leg_metrics(landmarks):
    global arm_accuracy, leg_accuracy
    # Extract key landmarks for arms and legs
    shoulder_left, elbow_left, wrist_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value], landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    shoulder_right, elbow_right, wrist_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value], landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    ankle_left, ankle_right = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value], landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate leg distance and leg accuracy
    leg_distance = abs((ankle_left.x - ankle_right.x) * frame_width)
    leg_accuracy = 100 - min(abs(leg_distance - ideal_leg_distance) / ideal_leg_distance * 100, 100)

    # Calculate arm angles and accuracy for left and right arms
    arm_angle_left = np.degrees(np.arctan2(wrist_left.y - elbow_left.y, wrist_left.x - elbow_left.x) - np.arctan2(shoulder_left.y - elbow_left.y, shoulder_left.x - elbow_left.x))
    arm_angle_right = np.degrees(np.arctan2(wrist_right.y - elbow_right.y, wrist_right.x - elbow_right.x) - np.arctan2(shoulder_right.y - elbow_right.y, shoulder_right.x - elbow_right.x))
    arm_angle_left = 360 + arm_angle_left if arm_angle_left < 0 else arm_angle_left
    arm_angle_right = 360 + arm_angle_right if arm_angle_right < 0 else arm_angle_right

    # Average accuracy for both arms
    arm_accuracy = (100 - abs((arm_angle_left - ideal_arm_angle) / ideal_arm_angle * 100) + 100 - abs((arm_angle_right - ideal_arm_angle) / ideal_arm_angle * 100)) / 2

    return leg_distance

# Jumping jacks exercise tracking and frame generation
def generate_jumping_jacks_frames():
    global counter, arm_stage, leg_stage, exercise_completed
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
                break

            # Process the frame if exercise is not over
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                leg_distance = calculate_arm_leg_metrics(landmarks)

                # Update stages and count based on arm and leg positions
                if leg_distance > ideal_leg_distance * 0.8:
                    if arm_stage != "up":
                        arm_stage = "up"
                    if leg_stage != "up" and arm_stage == "up":
                        leg_stage = "up"
                if leg_distance < ideal_leg_distance * 0.2:
                    if arm_stage == "up" and leg_stage == "up":
                        arm_stage = "down"
                        leg_stage = "down"
                        counter += 1

                # Display text with square boxes for counter and accuracy
                cv2.rectangle(image, (10, 20), (400, 200), (255, 0, 0), -1)  # Background for reps

                cv2.putText(image, f'REPS: {counter}', (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 2)
                cv2.putText(image, f'Arm Accuracy: {int(arm_accuracy)}%', (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
                cv2.putText(image, f'Leg Accuracy: {int(leg_accuracy)}%', (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
            else:
                cv2.putText(image, "No detection", (15, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Draw landmarks and bounding box
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/jumping_jacks_feed')
def jumping_jacks_feed():
    return Response(generate_jumping_jacks_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5009)
