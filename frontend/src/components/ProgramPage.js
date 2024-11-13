import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FaHome } from 'react-icons/fa'; // Import home icon
import './ProgramPage.css';

function ProgramPage() {
  const [fitnessLevel, setFitnessLevel] = useState('');
  const [error, setError] = useState('');
  const [name, setName] = useState('');
  const navigate = useNavigate();

  const programs = {
    Beginner: {
      frequency: '3 days a week',
      focus: 'Build foundational strength and endurance',
      exercises: [
        { name: 'Lunges', details: '8 per leg' },
        { name: 'Squats', details: '8' },
        { name: 'Shoulder Press', details: '8' },
        { name: 'High Knees', details: '30 seconds' },
        { name: 'Jumping Jacks', details: '30 seconds' },
        { name: 'Curls (Bicep)', details: '8' },
        { name: 'Push-Ups', details: '8' },
      ],
    },
    Intermediate: {
      frequency: '4 days a week with varying intensity',
      focus: 'Increase exercise volume and introduce dynamic movements',
      exercises: [
        { name: 'Lunges', details: '12 per leg' },
        { name: 'Squats', details: '12' },
        { name: 'Shoulder Press', details: '12' },
        { name: 'High Knees', details: '45 seconds' },
        { name: 'Jumping Jacks', details: '45 seconds' },
        { name: 'Curls (Bicep)', details: '12' },
        { name: 'Push-Ups', details: '12' },
      ],
    },
    Advanced: {
      frequency: '5 days a week with high intensity',
      focus: 'Maximize intensity and incorporate variations for enhanced strength and agility',
      exercises: [
        { name: 'Lunges', details: '15 per leg' },
        { name: 'Squats', details: '15' },
        { name: 'Shoulder Press', details: '15' },
        { name: 'High Knees', details: '1 minute' },
        { name: 'Jumping Jacks', details: '1 minute' },
        { name: 'Curls (Bicep)', details: '15' },
        { name: 'Push-Ups', details: '15' },
      ],
    },
  };

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('User not authenticated');
          return;
        }

        const response = await axios.post(
          'http://localhost:2000/api/getUserData',
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.data) {
          setFitnessLevel(response.data.fitness_level);
          setName(response.data.first_name);
        } else {
          setError('No fitness level found for the current user.');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
        setError('Error fetching user data.');
      }
    };

    fetchUserData();
  }, []);

  const selectedProgram = programs[fitnessLevel];

  // Function to navigate to the home page
  const goToHomePage = () => {
    navigate('/home');
  };

  return (
    <div className="program-page">
      
      <h1>Your Program</h1>
      {error ? (
        <p>{error}</p>
      ) : (
        <div>
          <h2>Welcome, {name}!</h2>
          <h2>Your Fitness Level: {fitnessLevel}</h2>

          {selectedProgram ? (
            <div>
              <h3>{fitnessLevel} Program</h3>
              <p><strong>Focus:</strong> {selectedProgram.focus}</p>
              <p><strong>Frequency:</strong> {selectedProgram.frequency}</p>
              <h4>Exercises:</h4>
              <ul>
                {selectedProgram.exercises.map((exercise, index) => (
                  <li key={index}>
                    <strong>{exercise.name}:</strong> {exercise.details}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p>No program available for your fitness level.</p>
          )}
        </div>
      )}
      {/* Home Button with Icon */}
      <button onClick={goToHomePage} className="home-button">
        <FaHome className="home-icon" /> Return to Home
      </button>
    </div>
  );
}

export default ProgramPage;
