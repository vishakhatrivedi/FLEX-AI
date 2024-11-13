import React, { useState } from 'react';
import axios from 'axios';
import './SignUpForm.css';
import { useNavigate } from 'react-router-dom';

function SignUpForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    password: ''
  });
  const [error, setError] = useState('');  // Added error state

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:2000/api/register', formData);

      if (response.status === 201) {
        // Store the username in localStorage to be used in SuccessPage
        localStorage.setItem('username', formData.username);
        // Redirect to the success page
        navigate('/success');
      } else {
        setError('Registration failed, please try again.');
      }
    } catch (error) {
      console.error('Error registering user:', error);
      setError('Error registering user. Please try again.');
    }
  };

  return (
    <div className="signup-form">
      <h1>FLEX-AI</h1>
      <h3>Sign Up!</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="firstName"
          placeholder="First Name"
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="lastName"
          placeholder="Last Name"
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="username"
          placeholder="Username"
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
        />
        <button type="submit">Submit</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
}

export default SignUpForm;
