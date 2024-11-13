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
   if angle > 180.0:
    angle = 360 - angle
   return angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
counter = 0
stage = None  # Initialize the stage variable
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# Check if landmarks are visible
def are_landmarks_visible(landmarks, indices):
   return all(landmarks[i].visibility > 0.5 for i in indices)


def generate_frames():
   global counter, stage, accuracy, username, fitness_level

   # Fetch username and fitness level to set the count goal
   username = get_username()
   if username:
       fitness_level = get_fitness_level(username)
       count_goal = fitness_levels.get(fitness_level, 8)  # Default to 8 if fitness level is not recognized
   else:
       print("Could not retrieve username or fitness level. Using default count goal.")
       count_goal = 8  # Default count goal for unrecognized level

   with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
       while cap.isOpened():
           success, frame = cap.read()
           if not success:
               continue

           # Process frame
           image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           image.flags.writeable = False
           results = pose.process(image)
           image.flags.writeable = True
           image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
           angle=0
           accuracy=0
           
           if results.pose_landmarks:
               landmarks = results.pose_landmarks.landmark
               required_landmarks = [mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE]
               if all(landmarks[lm.value].visibility > 0.5 for lm in required_landmarks):
                   hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x *  frame.shape[1], landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]
                   knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * frame.shape[1], landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * frame.shape[0]]
                   ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * frame.shape[1], landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * frame.shape[0]]
                   angle = calculate_angle(hip, knee, ankle)

                # Calculate accuracy
                   if angle > 160:
                       accuracy = 100 - abs(angle - 160) / 160 * 100
                   elif angle < 90:
                       accuracy = 100 - abs(angle - 90) / 90 * 100
                   else:
                       mid_angle = (160 + 90) / 2
                       accuracy = 100 - abs(angle - mid_angle) / mid_angle * 100
                   accuracy = max(0, min(accuracy, 100))

                # Update stage and counter
                   if angle > 160 and stage == 'down':
                       stage = 'up'
                       counter += 1
                   elif angle < 120:
                       stage = 'down'

           else:
               print("No landmarks detected.")
                   
                   # Render lunge counter and status box
           cv2.rectangle(image, (0, 0), (300, 300), (245, 117, 16), -1)
           cv2.putText(image, f'Angle: {int(angle)}', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
           cv2.putText(image, f'Accuracy: {int(accuracy)}%', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
           cv2.putText(image, 'REPS', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
           cv2.putText(image, str(counter), (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 3)
           cv2.putText(image, 'LUNGES', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
           cv2.putText(image, stage if stage else '', (50, 260), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 3)
               
           # Draw landmarks
           mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        #    cv2.imshow('Mediapipe Feed', image)

           ret, buffer = cv2.imencode('.jpg', image)
           frame = buffer.tobytes()
           yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/lunge_feed')
def lunge_feed():
   return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5006, debug=True)
