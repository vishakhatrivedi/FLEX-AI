import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './SuccessPage.css';

function SuccessPage() {
  const [formData, setFormData] = useState({
    height_cm: '',
    weight_kg: '',
    age: '',
    gender: '',
  });
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  // Get the username from localStorage
  const username = localStorage.getItem('username');

  // Check if the user is signed in (i.e., if the username is in localStorage)
  useEffect(() => {
    if (!username) {
      alert('User session expired. Please sign up again.');
      navigate('/signup');  // Redirect to signup page if session expired
    }
  }, [navigate, username]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   try {
  //     // Send form data to calculate BMI and body fat
  //     const response = await axios.post('http://localhost:2000/calculate', formData);
  //     const calculatedResult = response.data;
  //     setResult(calculatedResult);

  //     // Save the result to the database
  //     await axios.post('http://localhost:2000/api/saveResult', {
  //       username,  // Send the username stored in localStorage
  //       ...formData,  // Send the form data (height, weight, age, gender)
  //       body_fat: calculatedResult.body_fat,  // Send the calculated body fat
  //       bmi: calculatedResult.bmi,            // Send the calculated BMI
  //       fitness_level: calculatedResult.fitness_level  // Send the calculated fitness level
  //     });

  //     console.log('Results saved successfully!');
  //   } catch (error) {
  //     console.error('Error calculating or saving result:', error);
  //   }
  // };
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send form data to calculate BMI and body fat
      const response = await axios.post('http://localhost:2000/calculate', formData);
      const calculatedResult = response.data;
      setResult(calculatedResult);
  
      // Retrieve the JWT token from localStorage
      const token = localStorage.getItem('token');
  
      // Save the result to the database with the JWT token in the Authorization header
      await axios.post(
        'http://localhost:2000/api/saveResult',
        {
          username,  // Send the username stored in localStorage
          ...formData,  // Send the form data (height, weight, age, gender)
          body_fat: calculatedResult.body_fat,  // Send the calculated body fat
          bmi: calculatedResult.bmi,            // Send the calculated BMI
          fitness_level: calculatedResult.fitness_level  // Send the calculated fitness level
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,  // Add the JWT token here
          },
        }
      );
  
      console.log('Results saved successfully!');
    } catch (error) {
      console.error('Error calculating or saving result:', error);
    }
  };
  

  // Navigate to home page
  const goToLoginPage = () => {
    navigate('/login');
  };

  return (
    <div className="success-page">
      <h1>Congratulations on signing up!</h1>
      <h2>Fill in the details below to calculate your Body Fat Percentage, BMI, and Fitness Level</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="height_cm"
          placeholder="Height (cm)"
          value={formData.height_cm}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="weight_kg"
          placeholder="Weight (kg)"
          value={formData.weight_kg}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="age"
          placeholder="Age"
          value={formData.age}
          onChange={handleChange}
          required
        />
        <select name="gender" value={formData.gender} onChange={handleChange} required>
          <option value="">Select Gender</option>
          <option value="M">Male</option>
          <option value="F">Female</option>
        </select>
        <button type="submit">Calculate</button>
      </form>

      {/* Display results */}
      {result && (
        <div className="result">
          <h3>Your Results:</h3>
          <p>Body Fat Percentage: {result.body_fat.toFixed(2)}%</p>
          <p>BMI: {result.bmi.toFixed(2)}</p>
          <p>Fitness Level: {result.fitness_level}</p>
          <button onClick={goToLoginPage}>Login Now!</button>
        </div>
      )}
    </div>
  );
}

export default SuccessPage;
