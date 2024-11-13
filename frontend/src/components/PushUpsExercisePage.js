import React, { useState } from 'react';
import './PushUpsPage.css';
import { useNavigate } from 'react-router-dom';

function PushUpsExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5004/pushup_feed");
  const navigate = useNavigate();

  const startPushUpsExercise = async () => {
    try {
      const token = localStorage.getItem('token'); // Retrieve the JWT token from localStorage

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
        body: JSON.stringify({ workoutName: 'Push-Ups' }) // Specify the workout name
      });

      // Start the video feed
      const response = await fetch('http://localhost:2000/api/runPushUps', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data = await response.json();

      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl("http://localhost:5004/pushup_feed");
      } else {
        console.error('Error starting push-ups exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const stopPushUpsExercise = () => {
    // Additional logic to stop the video feed can go here
  };

  return (
    <div className="pushups-workout-page">
      <div className="pushups-left-section">
        <button className="pushups-back-arrow-button" onClick={() => navigate(-1)}>←</button>
        <h2>Push-Ups Exercise</h2>
        <div className="video-container">
          <video
            src="/push.mov" // Path to your local video file in the public folder
            loop
            autoPlay
            muted
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="pushups-divider"></div>
      <div className="pushups-right-section">
        <button className="start-pushups-btn" onClick={startPushUpsExercise}>Start Push-Ups Exercise</button>
        <button className="pushups-next-arrow-button" onClick={() => { navigate('/shoulder-press'); stopPushUpsExercise(); }}>➔</button>
        <div className="pushups-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="Push-Ups Video Feed" />
          ) : (
            <p>Please click "Start Push-Ups Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default PushUpsExercisePage;
