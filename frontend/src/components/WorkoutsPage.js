import React, { useState, useEffect } from 'react';
import './WorkoutsPage.css';
import { useNavigate } from 'react-router-dom';

function WorkoutsPage() {
  const [firstName, setFirstName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Retrieve user's data from local storage
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const parsedUser = JSON.parse(userData); // Parse the JSON string
        setFirstName(parsedUser.firstName);
      } catch (error) {
        console.error("Error parsing user data from local storage:", error);
      }
    } else {
      console.log("No user data found in local storage");
    }
  }, []);

  return (
    <div className="workouts-page">
      <button className="go-back-button" onClick={() => navigate('/home')}>Go Back to Home</button>
      <h1>Hey {firstName || 'there'}, congratulations on completing the workout!</h1>
    </div>
  );
}

export default WorkoutsPage;
