
// export default LoginPage;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginPage.css';  // Optional: Create this file for styling the login page
import logo from './assets/logo.png';  // Adjust the path to your logo file

function LoginPage({ setUser }) {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Handle input field changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle form submission for login
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send login request to backend (Node.js server)
      const response = await axios.post('http://localhost:2000/api/login', formData);
      
      if (response.status === 200) {
        const { token, user } = response.data;  // Destructure to get token and user information

        // Store the JWT token in localStorage
        localStorage.setItem('token', token);

        // Store user details in localStorage if needed
        localStorage.setItem('user', JSON.stringify(user));

        // Set the user in the app state
        setUser(user);

        // Send the token to the Flask server
        await fetch('http://localhost:5001/store_token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ token })  // Send the token in the request body as JSON
        })
        .then(response => response.json())
        .then(data => {
          console.log(data.message); // Should log "Token stored successfully"
        })
        .catch(error => {
          console.error('Error storing token:', error);
        });

        // Navigate to the home page after login
        navigate('/home');
      } else {
        setError('Invalid login credentials'); // Set error if credentials are wrong
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Invalid login credentials or server error'); // Handle server error or invalid credentials
    }
  };

  return (
    <div className="login-page">
      {/* Logo Section */}
      <img src={logo} alt="Logo" className="login-logo" />  {/* Logo Image */}
      
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <p className="error">{error}</p>} {/* Display error if login fails */}
    </div>
  );
}

export default LoginPage;

