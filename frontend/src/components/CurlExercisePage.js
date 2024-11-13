import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CurlExercisePage.css';

function CurlExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5003/curl_feed");
  const navigate = useNavigate();

  const startCurlExercise = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error("No token found. Please log in.");
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
        body: JSON.stringify({ workoutName: 'Curl' }) // Specify the workout name
      });

      // Start the video feed
      const response = await fetch('http://localhost:2000/api/runCurlExercise', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data = await response.json();

      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl(`http://localhost:5003/curl_feed`);
      } else {
        console.error('Error starting curl exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const stopCurlExercise = () => {
    // Additional logic to stop the video feed can go here if necessary
  };

  return (
    <div className="curl-workout-page">
      <div className="curl-left-section">
        <h2>Curl Exercise</h2>
        <div className="video-container">
          {/* Autoplaying, looping local video */}
          <video
            src="/curl.mov" // Updated path to use the local curl.mov video
            loop
            autoPlay
            muted
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="curl-divider"></div>
      <div className="curl-right-section">
        <button className="start-curl-btn" onClick={startCurlExercise}>Start Curl Exercise</button>
        <button className="curl-next-arrow-button" onClick={() => { navigate('/high-knees-exercise'); stopCurlExercise(); }}>➔</button>
        <div className="curl-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="Curl Video Feed" />
          ) : (
            <p>Please click "Start Curl Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default CurlExercisePage;
