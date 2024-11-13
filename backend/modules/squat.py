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

# Global variables for exercise tracking
username = None
fitness_level = None
counter = 0
stage = None
accuracy = 0
exercise_completed = False

# Hardcoded count goals based on fitness level
fitness_levels = {
   "Beginner": 8,
   "Intermediate": 12,
   "Advanced": 15
}

# Endpoint to receive the token from the frontend and store it in a global variable
@app.route('/store_token', methods=['POST'])
def store_token():
   global jwt_token
   data = request.json
   token = data.get("token")
   if token:
       jwt_token = token  # Store the token in a global variable
       return jsonify({"message": "Token stored successfully!"}), 200
   else:
       return jsonify({"error": "No token provided"}), 400

# Function to get the username from the backend using the stored JWT token
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

# Function to get fitness level from backend using username
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

# MediaPipe and camera initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Required landmark indices for squat exercise
required_indices = [
   mp_pose.PoseLandmark.LEFT_HIP.value,
   mp_pose.PoseLandmark.LEFT_KNEE.value,
   mp_pose.PoseLandmark.LEFT_ANKLE.value
]

# Ideal angles for squat positions
ideal_top_angle = 160
ideal_bottom_angle = 90

# Define font scale and thickness
font_scale = 1.2
font_thickness = 2

def are_landmarks_visible(landmarks, indices):
   return all(landmarks[i].visibility > 0.5 for i in indices)

# Real-time reps tracking and frame generation
def generate_frames():
   global counter, stage, accuracy, exercise_completed

   # Fetch username and fitness level to set the count goal
   username = get_username()
   if username:
       fitness_level = get_fitness_level(username)
       count_goal = fitness_levels.get(fitness_level, 8)  # Default to 8 if fitness level is not recognized
   else:
       print("Could not retrieve username. Using default count goal.")
       count_goal = 8  # Default count goal for unrecognized level

   with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
       while cap.isOpened():
           success, frame = cap.read()
           if not success:
               break

           # If exercise is completed, display final message and stop
           if counter >= count_goal and not exercise_completed:
               exercise_completed = True
               cv2.rectangle(frame, (30, 50), (600, 130), (0, 128, 0), -1)
               cv2.putText(frame, "Exercise Completed! Move to the Next Exercise", (40, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
               ret, buffer = cv2.imencode('.jpg', frame)
               frame = buffer.tobytes()
               yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
               break

           # Process the frame if exercise is not over
           image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           results = pose.process(image)
           image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

           if results.pose_landmarks:
               landmarks = results.pose_landmarks.landmark

               if are_landmarks_visible(landmarks, required_indices):
                   # Get coordinates for hip, knee, and ankle
                   hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                   knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                   ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                   
                   # Calculate angle
                   angle = calculate_angle(hip, knee, ankle)

                   # Calculate accuracy based on the squat angle
                   if angle > ideal_top_angle:
                       accuracy = max(0, 100 - abs(angle - ideal_top_angle) / ideal_top_angle * 100)
                   elif angle < ideal_bottom_angle:
                       accuracy = max(0, 100 - abs(angle - ideal_bottom_angle) / ideal_bottom_angle * 100)
                   else:
                       mid_angle = (ideal_top_angle + ideal_bottom_angle) / 2
                       accuracy = max(0, 100 - abs(angle - mid_angle) / (ideal_top_angle - ideal_bottom_angle) * 100)

                   # Update counter and stage based on the angle
                   if angle > ideal_top_angle and stage == "down":
                       stage = "up"
                       counter += 1
                   elif angle < ideal_bottom_angle:
                       stage = "down"
                   
                   # Draw background rectangles for the text with appropriate spacing
                   cv2.rectangle(image, (10, 20), (250, 80), (255, 0, 0), -1)  # Blue box for reps
                   cv2.rectangle(image, (10, 90), (250, 150), (255, 0, 0), -1)  # Blue box for stage
                   cv2.rectangle(image, (10, 160), (300, 220), (255, 0, 0), -1)  # Blue box for angle
                   cv2.rectangle(image, (10, 230), (300, 290), (255, 0, 0), -1)  # Blue box for accuracy

                   # Display the angle, reps, stage, and accuracy on the frame

                   cv2.putText(image, f'REPS: {counter}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), font_thickness)
                   cv2.putText(image, f'Stage: {stage}', (20, 130), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
                   cv2.putText(image, f'Angle: {int(angle)}', (20, 200), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
                   cv2.putText(image, f'Accuracy: {int(accuracy)}%', (20, 270), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
               else:
                   # Display a warning if the required landmarks are not visible
                   cv2.rectangle(image, (10, 160), (400, 220), (0, 0, 255), -1)  # Red box for "Adjust Position"
                   cv2.putText(image, "Adjust Position", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)
           mp_drawing.draw_landmarks(
               image, 
               results.pose_landmarks, 
               mp_pose.POSE_CONNECTIONS,
               mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
               mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
           )

           # Convert the frame to JPEG format for video feed
           ret, buffer = cv2.imencode('.jpg', image)
           frame = buffer.tobytes()
           yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
   return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5001, debug=True) 