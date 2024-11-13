// src/HomePage.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const navigate = useNavigate();

  // Function to handle clicking the Workout button
  const goToRoutinePage = () => {
    navigate('/routine');  // Navigate to the Routine page
  };

  return (
    <div className="home-page">
      <div className="navbar">
        <img src={require('./assets/logo.png')} alt="Flex-AI Logo" className="logo" />
        <div className="nav-links">
          <Link to="/program">PROGRAM</Link>
          <Link to="/profile">MY PROFILE</Link>
        </div>
      </div>
      <div className="content">
        <h1>BUILD <span className="highlight">YOUR</span> BODY STRONG</h1>
        <button className="workout-btn" onClick={goToRoutinePage}>WORKOUT</button>
      </div>
    </div>
  );
}

export default HomePage;
