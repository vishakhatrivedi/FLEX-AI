# FlexAI: AI Fitness Trainer
# Real-Time Fitness Pose Estimation

This project leverages Google's MediaPipe framework to develop a real-time fitness application that uses pose estimation to help users improve their exercise form and efficiency. Our application specifically focuses on calculating angles between body joints to provide instant feedback during workouts, ensuring exercises such as squats, push ups, shoulder presses and lunges are performed correctly.

## Features

- **Real-Time Pose Estimation**: Utilizes MediaPipe's BlazePose for detecting 33 body landmarks with high precision.
- **Angle Calculation**: Employs trigonometric methods to calculate the angles between joints like hips, knees, and ankles.
- **Dynamic Feedback System**: Provides users with real-time feedback on their exercise form to minimize the risk of injury and maximize the effectiveness of their workout.
![Screenshot 2024-10-29 191822](https://github.com/user-attachments/assets/4b0e2e8a-2321-4ca8-86fa-e99bae141312)
![image](https://github.com/user-attachments/assets/66a7e010-3f0c-4323-98e6-68e75ac52e5e)
![image](https://github.com/user-attachments/assets/59dc6e81-6883-4e50-96fb-6c9429d75982)


### Prerequisites

What you need to install the software:

- Python 3.8+
- MediaPipe
- OpenCV
- NumPy
- JavaScript
- MongoDB Atlas

## Installation


1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/FLEX-AI.git
   cd FLEX-AI
   ```
2. **Install Git LFS (if required for large files)**
   - **macOS:**
     ```bash
     brew install git-lfs
     git lfs install
     ```
   - **Windows:**
     ```plaintext
     Download and install Git LFS from https://git-lfs.github.com/.
     After installation, initialize Git LFS:
     git lfs install
     ```
3. **Install Backend Dependencies**
   ```bash
   cd backend
   npm install
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Install Frontend Dependencies**
   ```bash
   cd ../frontend
   npm install
   ```
5. **Environment Variables**
   - Create a `.env` file in both the frontend and backend folders.
   - **Backend `.env` (backend/.env)**
     ```plaintext
     DATABASE_URL=your_database_url
     JWT_SECRET=your_jwt_secret
     ```
   - **Frontend `.env` (frontend/.env)**
     ```plaintext
     REACT_APP_API_URL=http://localhost:5000
     ```
6. **Run the Backend Server**
   ```bash
   npm start
   # For Python-based backend, you may need to run:
   flask run
   # or
   python app.py
   ```
7. **Run the Frontend Server**
   ```bash
   npm start
   # This will start the frontend development server, usually accessible at http://localhost:3000.
   ```
8. **Additional Tools (if applicable)**
   - Make sure MongoDB is installed and running if required for the backend.
   - Ensure Node.js and npm are installed.

### Additional Notes
- Replace `yourusername` in the git clone URL with your GitHub username.
- Customize paths and variables according to your project requirements.
- Mention any other required installations or configurations specific to your project.


## Usage

Once the application is running:
- Position yourself so that your full body is visible in the webcam feed.
- Perform exercises as instructed by the application.
- Follow the real-time feedback provided on the screen to adjust your posture and movements.
- Ensure your webcam is enabled, as the application requires real-time video input.

## Built With

- MediaPipe - Framework for building multimodal applied machine learning pipelines
- OpenCV - Open Source Computer Vision Library
- NumPy - The fundamental package for scientific computing with Python
- React - A JavaScript library for building user interfaces
- MongoDB - Document-based database
- Express - Web application framework for Node.js
- Node.js - JavaScript runtime built on Chrome's V8 JavaScript engine

## Authors

- **Vishakha Trivedi**
- **Saumya Pandey** 
- **Dev Mahey** 


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE License - see the LICENSE file for details
