import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ProfilePage.css';

function ProfilePage({ setUser }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Remove JWT token and user data from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('username');

    // Clear user state in the app
    setUser(null);

    // Navigate to the landing page
    navigate('/');
  };

  return (
    <div className="profile-page">
      <h2>Welcome to Your Profile</h2>
      <button onClick={handleLogout} className="logout-btn">Logout</button>
    </div>
  );
}

export default ProfilePage;
