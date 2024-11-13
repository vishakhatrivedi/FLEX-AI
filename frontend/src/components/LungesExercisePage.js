import React, { useState } from 'react';
import './LungesPage.css';
import { useNavigate } from 'react-router-dom';

function LungesExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5006/lunge_feed");
  const navigate = useNavigate();

  const startLungesExercise = async () => {
    try {
      const token = localStorage.getItem('token'); // Retrieve the JWT token from localStorage

      if (!token) {
        console.error("No token found. Redirecting to login.");
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:2000/api/runLunges', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data = await response.json();

      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl("http://localhost:5006/lunge_feed");
      } else {
        console.error('Error starting lunges exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const stopLungesExercise = () => {
    // Additional logic to stop the video feed can go here
  };

  return (
    <div className="lunges-workout-page">
      <div className="lunges-left-section">
        <h2>Lunges Exercise</h2>
        <div className="video-container">
          {/* Autoplaying, looping local video */}
          <video
            src="/lunges.mov" // Path to your local video file in the public folder
            loop
            autoPlay
            muted
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="lunges-divider"></div>
      <div className="lunges-right-section">
        <button className="start-lunges-btn" onClick={startLungesExercise}>Start Lunges Exercise</button>
        <button className="lunges-next-arrow-button" onClick={() => { navigate('/push-ups'); stopLungesExercise(); }}>➔</button>
        <div className="lunges-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="Lunges Video Feed" />
          ) : (
            <p>Please click "Start Lunges Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default LungesExercisePage;
