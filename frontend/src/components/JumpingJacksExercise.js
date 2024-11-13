import React, { useState, useEffect } from 'react';
import './JumpingJacksPage.css';
import { useNavigate } from 'react-router-dom';

function JumpingJacksExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5009/jumping_jacks_feed");
  const navigate = useNavigate();

  const startJumpingJacksExercise = async () => {
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
        body: JSON.stringify({ workoutName: 'Jumping Jacks' }) // Specify the workout name
      });

      // Start the video feed
      const response = await fetch('http://localhost:2000/api/runJumpingJacks', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data = await response.json();

      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl("http://localhost:5009/jumping_jacks_feed");
      } else {
        console.error('Error starting Jumping Jacks exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const stopJumpingJacksExercise = () => {
    // Additional logic to stop the video feed can go here
  };

  return (
    <div className="jumping-jacks-workout-page">
      <div className="jumping-jacks-left-section">
        <h2>Jumping Jacks Exercise</h2>
        <div className="video-container">
          {/* Autoplaying, looping local video */}
          <video
            src="/jumping.mov" // Path to your local video file
            loop
            autoPlay
            muted
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="jumping-jacks-divider"></div>
      <div className="jumping-jacks-right-section">
        <button className="start-jumping-jacks-btn" onClick={startJumpingJacksExercise}>Start Jumping Jacks Exercise</button>
        <button className="jumping-jacks-next-arrow-button" onClick={() => { navigate('/lunges-exercise'); stopJumpingJacksExercise(); }}>➔</button>
        <div className="jumping-jacks-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="Jumping Jacks Video Feed" />
          ) : (
            <p>Please click "Start Jumping Jacks Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default JumpingJacksExercisePage;
