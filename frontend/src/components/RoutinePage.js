// src/RoutinePage.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaHome } from 'react-icons/fa';
import './RoutinePage.css';

function RoutinePage() {
  const navigate = useNavigate();

  // Function to navigate to specific exercise pages
  const goToExercisePage = (exercisePath) => {
    navigate(exercisePath);
  };

  // Function to navigate to the home page
  const goToHomePage = () => {
    navigate('/home');
  };

  return (
    <div className="routine-page">
      <button className="home-button" onClick={goToHomePage}>
        <FaHome className="home-icon" /> Home
      </button>
      <h1>Exercise Routine</h1>
      <button className="start-workout-btn" onClick={() => goToExercisePage('/WorkoutPage')}>
        Start Today's Workout
      </button>
      <ul className="exercise-list">
        <li onClick={() => goToExercisePage('/WorkoutPage')}>Squats</li>
        <li onClick={() => goToExercisePage('/curl-exercise')}>Bicep Curls</li>
        <li onClick={() => goToExercisePage('/high-knees-exercise')}>High Knees</li>
        <li onClick={() => goToExercisePage('/jumping-exercise')}>Jumping Jacks</li>
        <li onClick={() => goToExercisePage('/lunges-exercise')}>Lunges</li>
        <li onClick={() => goToExercisePage('/push-ups')}>Push-Ups</li>
        <li onClick={() => goToExercisePage('/shoulder-press')}>Shoulder Press</li>
      </ul>
    </div>
  );
}

export default RoutinePage;
