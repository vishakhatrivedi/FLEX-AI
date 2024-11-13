import React, { useState } from 'react';
import './ShoulderPressPage.css';
import { useNavigate } from 'react-router-dom';

function ShoulderPressExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5008/shoulder_press_feed");
  const navigate = useNavigate();

  const startShoulderPressExercise = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error("No token found. Redirecting to login.");
        navigate('/login');
        return;
      }

      // Save workout to MongoDB
      await fetch('http://localhost:2000/saveworkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ workoutName: 'Shoulder Press' }) // Specify the workout name
      });

      // Start the video feed
      const response = await fetch('http://localhost:2000/api/runShoulderPress', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();

      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl("http://localhost:5008/shoulder_press_feed");
      } else {
        console.error('Error starting shoulder press exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const completeWorkout = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error("No token found. Redirecting to login.");
        navigate('/login');
        return;
      }
  
      // Stop the current exercise on the server
      const response = await fetch('http://localhost:2000/api/stopExercise', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
  
      if (!response.ok) {
        throw new Error('Failed to stop the exercise.');
      }
  
      navigate('/workout-complete'); // Redirect to workout complete page
    } catch (error) {
      console.error('Error stopping workout:', error);
    }
  };
  
  // Define goBack to navigate to the previous page
  const goBack = () => {
    navigate(-1); // Navigate back to the previous page
  };

  return (
    <div className="shoulder-press-workout-page">
      <div className="shoulder-press-left-section">
        <button className="back-arrow-button" onClick={goBack}>
          &#8592;
        </button>
        <h2>Shoulder Press Exercise</h2>
        <div className="video-container">
          <video
            src="/shoulder.mov"
            loop
            autoPlay
            muted
            controls
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="shoulder-press-divider"></div>
      <div className="shoulder-press-right-section">
        <button className="start-shoulder-press-btn" onClick={startShoulderPressExercise}>
          Start Shoulder Press Exercise
        </button>
        <button className="shoulder-press-complete-button" onClick={completeWorkout}>
          Complete Workout
        </button>
        <div className="shoulder-press-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="Shoulder Press Video Feed" />
          ) : (
            <p>Please click "Start Shoulder Press Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ShoulderPressExercisePage;
