import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css'; // Styling for the landing page
import logo from './assets/logo.png';  // Adjust based on where 'LandingPage.js' is located

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <div className="content">
        <img src={logo} alt="Flex AI Logo" className="logo" /> {/* Imported logo displayed here */}
        <h1>Welcome to <span className="highlight">FLEX-AI</span></h1>
        <p>Your journey to a stronger body starts here</p>
        <div className="buttons">
          <button onClick={() => navigate('/login')} className="btn-login">Login</button>
          <button onClick={() => navigate('/signup')} className="btn-signup">Sign Up</button>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
