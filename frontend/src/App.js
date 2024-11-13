

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import WorkoutPage from './components/SquatExercisePage';
import LandingPage from './components/LandingPage';
import SignUpForm from './components/SignUpForm';
import LoginPage from './components/LoginPage';
import SuccessPage from './components/SuccessPage';
import HomePage from './components/HomePage';
import ProfilePage from './components/ProfilePage';
import ProgramPage from './components/ProgramPage';
import RoutinePage from './components/RoutinePage';
import CurlExercisePage from './components/CurlExercisePage';
import HighKneesPage from './components/HighKneesPage';
import JumpingJacksPage from './components/JumpingJacksExercise';
import PushUpsExercisePage from './components/PushUpsExercisePage';
import LungesExercisePage from './components/LungesExercisePage';
import ShoulderPressExercisePage from './components/ShoulderPressExercisePage';
import WorkoutsPage from './components/WorkoutsPage';


function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Safely retrieve and parse user data from localStorage
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        console.error("Error parsing stored user data:", error);
        // Remove corrupted user data if parsing fails
        localStorage.removeItem('user');
      }
    }
  }, []);

  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage setUser={setUser} />} />
          <Route path="/signup" element={<SignUpForm />} />
          <Route path="/success" element={<SuccessPage />} />
          
          {/* Pass user as a prop to HomePage */}
          <Route path="/home" element={<HomePage user={user} />} />

          <Route path="/program" element={<ProgramPage />} />
          <Route path="/routine" element={<RoutinePage />} />
          <Route path="/WorkoutPage" element={<WorkoutPage />} />
          <Route path="/curl-exercise" element={<CurlExercisePage />} />
          <Route path="/high-knees-exercise" element={<HighKneesPage />} />
          <Route path="/jumping-exercise" element={<JumpingJacksPage />} />
          <Route path="/lunges-exercise" element={<LungesExercisePage />} />
          <Route path="/push-ups" element={<PushUpsExercisePage />} />
          <Route path="/shoulder-press" element={<ShoulderPressExercisePage />} />
          <Route path="/workout-complete" element={<WorkoutsPage />} />

          {/* Profile page with logout option, pass user and setUser */}
          <Route path="/profile" element={<ProfilePage user={user} setUser={setUser} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
