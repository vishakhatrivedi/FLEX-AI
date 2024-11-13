// import React, { useState } from 'react';
// import './SquatExercisePage.css';
// import { useNavigate } from 'react-router-dom';

// function SquatExercisePage() {
//   const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5001/video_feed");
//   const navigate = useNavigate();

//   const startSquatExercise = async () => {
//     try {
//       const token = localStorage.getItem('token');
  
//       const response = await fetch('http://localhost:2000/api/runSquatExercise', {
//         method: 'POST',
//         headers: {
//           'Authorization': `Bearer ${token}`
//         },
//       });
//       const data = await response.json();
  
//       if (response.ok && data.videoFeedPort) {
//         setVideoFeedUrl(`http://localhost:5001/video_feed`);
//       } else {
//         console.error('Error starting squat exercise:', data.error);
//       }
//     } catch (error) {
//       console.error('Error connecting to backend:', error);
//     }
//   };

//   const stopSquatExercise = () => {
//     // Additional logic to stop the video feed can go here
//   };

//   return (
//     <div className="squat-workout-page">
//       <div className="squat-left-section">
//         <h2>Squat Exercise</h2>
//         <div className="video-container">
//           {/* Autoplaying, looping local video */}
//           <video
//             src="/squat.mov" // Updated path to public folder
//             loop
//             autoPlay
//             muted
//             className="exercise-video"
//           ></video>
//         </div>
//       </div>
//       <div className="squat-divider"></div>
//       <div className="squat-right-section">
//         <button className="start-squat-btn" onClick={startSquatExercise}>Start Squat Exercise</button>
//         <button className="squat-next-arrow-button" onClick={() => { navigate('/curl-exercise'); stopSquatExercise(); }}>➔</button>
//         <div className="squat-video-container">
//           {videoFeedUrl ? (
//             <img src={videoFeedUrl} alt="Squat Video Feed" />
//           ) : (
//             <p>Please click "Start Squat Exercise" to begin the video feed.</p>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

// export default SquatExercisePage;


import React, { useState } from 'react';
import './SquatExercisePage.css';
import { useNavigate } from 'react-router-dom';

function SquatExercisePage() {
  const [videoFeedUrl, setVideoFeedUrl] = useState("http://localhost:5001/video_feed");
  const navigate = useNavigate();

  const startSquatExercise = async () => {
    try {
      const token = localStorage.getItem('token');

      // Save workout to MongoDB
      await fetch('http://localhost:2000/saveworkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ workoutName: 'Squat' }) // Specify the workout name
      });

      // Start video feed
      const response = await fetch('http://localhost:2000/api/runSquatExercise', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data = await response.json();
  
      if (response.ok && data.videoFeedPort) {
        setVideoFeedUrl(`http://localhost:5001/video_feed`);
      } else {
        console.error('Error starting squat exercise:', data.error);
      }
    } catch (error) {
      console.error('Error connecting to backend:', error);
    }
  };

  const stopSquatExercise = () => {
    // Additional logic to stop the video feed can go here
  };

  return (
    <div className="squat-workout-page">
      <div className="squat-left-section">
        <h2>Squat Exercise</h2>
        <div className="video-container">
          <video
            src="/squat.mov"
            loop
            autoPlay
            muted
            className="exercise-video"
          ></video>
        </div>
      </div>
      <div className="squat-divider"></div>
      <div className="squat-right-section">
        <button className="start-squat-btn" onClick={startSquatExercise}>Start Squat Exercise</button>
        <button className="squat-next-arrow-button" onClick={() => { navigate('/curl-exercise'); stopSquatExercise(); }}>➔</button>
        <div className="squat-video-container">
          {videoFeedUrl ? (
            <img src={videoFeedUrl} alt="Squat Video Feed" />
          ) : (
            <p>Please click "Start Squat Exercise" to begin the video feed.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default SquatExercisePage;
