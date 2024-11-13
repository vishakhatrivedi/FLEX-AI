import React, { useState, useEffect } from 'react';
import './HighKneesPage.css';
import { useNavigate } from 'react-router-dom';

function HighKneesExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5005/high_knee_feed");
  const [player, setPlayer] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error("Token not found, redirecting to login.");
      navigate('/login'); // Redirect if token is not found
    }
  }, [navigate]);

  useEffect(() => {
    // Load the video in the player when component mounts
    const tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    window.onYouTubeIframeAPIReady = () => {
      const newPlayer = new window.YT.Player('high-knees-video-player', {
        videoId: 'oDdkytliOqE',
        events: {
          onReady: (event) => setPlayer(event.target),
          onStateChange: (event) => {
            if (event.data === window.YT.PlayerState.ENDED) {
              event.target.playVideo(); // Loop video
            }
          },
        },
      });
    };
  }, []);

  const startHighKneesExercise = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Save workout to MongoDB
      await fetch('http://localhost:2000/saveworkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ workoutName: 'High Knees' }) // Specify the workout name
      });

      // Start the video feed
      const response = await fetch('http://localhost:2000/api/runHighKnees', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data = await response.json();

      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl("http://localhost:5005/high_knee_feed");
        if (player) player.playVideo(); // Start the video feed on button click
      } else {
        console.error('Error starting High Knees exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const stopHighKneesExercise = () => {
    if (player) player.stopVideo(); // Stop video feed when button clicked
  };

  return (
    <div className="high-knees-workout-page">
      <div className="high-knees-left-section">
        <h2>High Knees Exercise</h2>
        <div className="video-container">
          <video
            src="/high_knees.mov"
            loop
            autoPlay
            muted
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="high-knees-divider"></div>
      <div className="high-knees-right-section">
        <button className="start-high-knees-btn" onClick={startHighKneesExercise}>Start High Knees Exercise</button>
        <button className="high-knees-next-arrow-button" onClick={() => { navigate('/jumping-exercise'); stopHighKneesExercise(); }}>➔</button>
        <div className="high-knees-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="High Knees Video Feed" />
          ) : (
            <p>Please click "Start High Knees Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default HighKneesExercisePage;
