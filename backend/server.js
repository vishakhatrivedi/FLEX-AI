const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const { spawn } = require('child_process');
const WebSocket = require('ws');
const jwt = require('jsonwebtoken');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/flexai')
  .then(() => console.log("Connected to MongoDB"))
  .catch(err => console.error("MongoDB connection error:", err));

const secretKey = 'your_secret_key';
// JWT verification middleware
const verifyToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Extract the token after "Bearer"

  if (!token) {
    return res.status(403).json({ error: 'Access denied. No token provided.' });
  }

  try {
    const decoded = jwt.verify(token, secretKey);
    req.user = decoded; // Attach user info (userId and username) to the request
    next(); // Proceed to the next middleware or route handler
  } catch (error) {
    res.status(401).json({ error: 'Invalid or expired token.' });
  }
};

//get username
app.get('/api/getUsername', (req, res) => {
  const token = req.headers['authorization'];

  // Check if the token is provided
  if (!token) {
    return res.status(403).json({ error: 'No token provided' });
  }

  try {
    // Decode the token to retrieve user information
    const decoded = jwt.verify(token.split(' ')[1], secretKey); // Assuming "Bearer <token>" format
    res.status(200).json({ username: decoded.username }); // Send username in the response
  } catch (err) {
    console.error('Error verifying token:', err);
    res.status(401).json({ error: 'Invalid or expired token' });
  }
});


// Path and port for the squat exercise script
const squatScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/squat.py';
const squatPort = 5001;

let currentPythonProcess = null;

// Helper function to stop the current Python process if one is running
function stopCurrentProcess() {
  if (currentPythonProcess) {
    currentPythonProcess.kill();
    currentPythonProcess = null;
  }
}

// Function to start the squat exercise
function startSquatExercise(res) {
  stopCurrentProcess();
  currentPythonProcess = spawn('python3', [squatScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: squatPort });
      }
      hasSentResponse = true;
    }
  });
}

// API endpoint to start the squat exercise
app.post('/api/runSquatExercise', verifyToken, (req, res) => {
  startSquatExercise(res);
});

// Function to start the curl exercise
function startCurlExercise(res) {
  stopCurrentProcess();
  const curlScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/curl.py'; // Replace with actual path
  const curlPort = 5003; // Define the port for curl exercise if different

  currentPythonProcess = spawn('python3', [curlScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: curlPort });
      }
      hasSentResponse = true;
    }
  });
}

// API endpoint to start the curl exercise
app.post('/api/runCurlExercise', verifyToken, (req, res) => {
  startCurlExercise(res);
});

// Function to start the high_knees exercise
function startHighKneesExercise(res) {
  stopCurrentProcess();
  const highKneesScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/high_knees.py';
  const highKneesPort = 5005;

  currentPythonProcess = spawn('python3', [highKneesScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: highKneesPort });
      }
      hasSentResponse = true;
    }
  });
}

// API endpoint to start the high_knees exercise
app.post('/api/runHighKnees', verifyToken, (req, res) => {
  startHighKneesExercise(res);
});

function startJumpingJacksExercise(res) {
  stopCurrentProcess();
  const jumpingJacksScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/jumping_jacks.py';
  const jumpingJacksPort = 5009;

  currentPythonProcess = spawn('python3', [jumpingJacksScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: jumpingJacksPort });
      }
      hasSentResponse = true;
    }
  });
}
// API endpoint to stop the current exercise
app.post('/api/stopExercise', verifyToken, (req, res) => {
  stopCurrentProcess();
  res.status(200).json({ message: 'Exercise stopped successfully.' });
});


// API endpoint to start the jumping jacks exercise
app.post('/api/runJumpingJacks', (req, res) => {
  startJumpingJacksExercise(res);
});

//lunges
function startLungesExercise(res) {
  stopCurrentProcess();
  const lungesScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/lunges.py';
  const lungesPort = 5006;

  currentPythonProcess = spawn('python3', [lungesScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: lungesPort });
      }
      hasSentResponse = true;
    }
  });
}

// API endpoint to start the lunges exercise
app.post('/api/runLunges', verifyToken, (req, res) => {
  startLungesExercise(res);
});

//pushups
function startPushUpsExercise(res) {
  stopCurrentProcess();
  const pushUpsScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/push_ups.py';
  const pushUpsPort = 5004;

  currentPythonProcess = spawn('python3', [pushUpsScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: pushUpsPort });
      }
      hasSentResponse = true;
    }
  });
}

// API endpoint to start the push-ups exercise
app.post('/api/runPushUps',verifyToken, (req, res) => {
  startPushUpsExercise(res);
});

function startShoulderPressExercise(res) {
  stopCurrentProcess();
  const shoulderPressScriptPath = '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/modules/shoulder_press.py';
  const shoulderPressPort = 5008;

  currentPythonProcess = spawn('python3', [shoulderPressScriptPath]);

  let hasSentResponse = false;

  currentPythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`);
  });

  currentPythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
    if (!hasSentResponse) {
      res.status(500).send({ error: `Python script error: ${data.toString()}` });
      hasSentResponse = true;
    }
  });

  currentPythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    if (!hasSentResponse) {
      if (code !== 0) {
        res.status(500).send({ error: "Python script failed to execute" });
      } else {
        res.send({ message: "Python script executed successfully", videoFeedPort: shoulderPressPort });
      }
      hasSentResponse = true;
    }
  });
}

// API endpoint to start the shoulder press exercise
app.post('/api/runShoulderPress', verifyToken, (req, res) => {
  startShoulderPressExercise(res);
});



// MongoDB Schemas and Models
const userSchema = new mongoose.Schema({
  firstName: String,
  lastName: String,
  username: { type: String, unique: true },
  password: String,
});

const User = mongoose.model('User', userSchema);


const resultSchema = new mongoose.Schema({
  username: String,
  height_cm: Number,
  weight_kg: Number,
  age: Number,
  gender: String,
  body_fat: Number,
  bmi: Number,
  fitness_level: String,
  date: { type: Date, default: Date.now },
});

const Result = mongoose.model('Result', resultSchema);

// WebSocket setup
const wss = new WebSocket.Server({ port: 3001 });
wss.on('connection', ws => {
  console.log('Client connected to WebSocket');
  ws.on('message', message => {
    console.log('Received:', message);
  });
});

// User Registration
app.post('/api/register', async (req, res) => {
  const { firstName, lastName, username, password } = req.body;
  const newUser = new User({ firstName, lastName, username, password });

  try {
    await newUser.save();
    res.status(201).json({ message: 'User registered successfully!' });
  } catch (err) {
    console.error('Error saving user:', err);
    if (err.code === 11000) {
      res.status(400).json({ error: 'Username already exists. Please choose another one.' });
    } else {
      res.status(500).json({ error: 'Failed to register user.' });
    }
  }
});


// User Login JWT
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    const user = await User.findOne({ username });
    if (user && user.password === password) {
      // Generate a JWT token
      const token = jwt.sign(
        { userId: user._id, username: user.username },
        secretKey,
        { expiresIn: '1h' } // Token expires in 1 hour
      );

      // Send the token along with user information
      res.status(200).json({ 
        message: 'Login successful!', 
        token, 
        user: { 
          username: user.username, 
          firstName: user.firstName 
        } 
      });
      
    } else {
      res.status(401).json({ error: 'Invalid username or password.' });
    }
  } catch (err) {
    console.error('Error during login:', err);
    res.status(500).json({ error: 'Server error during login.' });
  }
});


// Calculate Body Metrics
app.post('/calculate', (req, res) => {
  const { height_cm, weight_kg, age, gender } = req.body;
  const pythonProcess = spawn('/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/Flex-ai_levels-calc/.venv/bin/python3', [
    '/Users/saumyapandey/Desktop/Documents/FLEX-AI/backend/Flex-ai_levels-calc/body_fat_prediction.py',
    age,
    gender,
    height_cm,
    weight_kg,
  ]);

  let scriptOutput = '';

  pythonProcess.stdout.on('data', (data) => {
    scriptOutput += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Error from Python script: ${data}`);
    res.status(500).json({ error: 'Error calculating BMI and body fat.' });
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      const [bodyFat, bmi, fitnessLevel] = scriptOutput.split(',');
      res.json({ body_fat: parseFloat(bodyFat), bmi: parseFloat(bmi), fitness_level: fitnessLevel.trim() });
    } else {
      res.status(500).json({ error: 'Failed to calculate BMI and body fat.' });
    }
  });
});

// Save Workout Results JWT
app.post('/api/saveResult', async (req, res) => {
  const { username, height_cm, weight_kg, age, gender, body_fat, bmi, fitness_level } = req.body;

  try {
    const newResult = new Result({ username, height_cm, weight_kg, age, gender, body_fat, bmi, fitness_level });
    await newResult.save();
    res.status(201).json({ message: 'Result saved successfully!' });
  } catch (error) {
    console.error('Error saving result:', error);
    res.status(500).json({ error: 'Failed to save result.' });
  }
});

app.post('/api/getUserData', verifyToken, async (req, res) => {
  try {
    // Retrieve user information from the JWT token payload
    const { username } = req.user;

    // Find the latest fitness level entry for the user
    const latestResult = await Result.findOne({ username }).sort({ date: -1 });
    if (!latestResult) {
      return res.status(404).json({ error: 'No fitness level found for this user.' });
    }

    // Send the username and fitness level in the response
    res.status(200).json({
      first_name: req.user.username,
      fitness_level: latestResult.fitness_level
    });
  } catch (error) {
    console.error('Error retrieving user data:', error);
    res.status(500).json({ error: 'Failed to retrieve user data' });
  }
});

const workoutSchema = new mongoose.Schema({
  workoutName: String,
  repsDone: { type: Number, default: 8 },
  date: { type: Date, default: Date.now } // Automatically set the date to the current time
});


app.post('/saveworkout', verifyToken, async (req, res) => {
  const { workoutName } = req.body;

  if (!workoutName) {
    return res.status(400).json({ error: "Workout name is required" });
  }

  try {
    const workout = new Workout({
      workoutName,
      date: new Date() // Explicitly set the date here
    });
    await workout.save();
    res.status(200).json({ message: 'Workout saved successfully!' });
  } catch (error) {
    console.error("Error saving workout data:", error); // Log any errors
    res.status(500).json({ error: 'Error saving workout data' });
  }
});

// Protected API endpoint to get today's workouts
app.get('/api/todaysWorkouts', verifyToken, async (req, res) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  try {
    const todaysWorkouts = await Workout.find({ date: { $gte: today } });
    console.log("Retrieved today's workouts:", todaysWorkouts); // Log retrieved data
    res.status(200).json(todaysWorkouts);
  } catch (error) {
    console.error("Error retrieving workouts:", error); // Log the error details
    res.status(500).json({ error: 'Failed to retrieve workouts' });
  }
});



const PORT = 2000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
