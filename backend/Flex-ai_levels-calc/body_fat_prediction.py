import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv('/Users/saumyapandey/Desktop/Documents/FLEX-AI/bodyPerformance.csv')


# Basic preprocessing
def preprocess_data(data):
    data = data.drop(columns=['diastolic', 'systolic', 'gripForce', 'sit and bend forward_cm', 'sit-ups counts'])
    le = LabelEncoder()
    data['gender'] = le.fit_transform(data['gender'])
    data = data.dropna()
    return data


# Preprocess the data
data = preprocess_data(data)

# Split the data into features and target variable
X = data[['age', 'gender', 'height_cm', 'weight_kg']]
y = data['body fat_%']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define and train the model
model = LinearRegression()
model.fit(X_train, y_train)


# Function to calculate BMI
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100  # Convert height from cm to meters
    return weight_kg / (height_m ** 2)


# Function to predict body fat percentage and calculate BMI
def predict_body_fat_and_bmi(age, gender, height_cm, weight_kg):
    gender_encoded = 1 if gender.lower() == 'm' else 0
    input_data = pd.DataFrame([[age, gender_encoded, height_cm, weight_kg]],
                              columns=['age', 'gender', 'height_cm', 'weight_kg'])

    # Predict the body fat percentage
    predicted_body_fat = model.predict(input_data)[0]

    # Calculate the BMI
    bmi = calculate_bmi(weight_kg, height_cm)

    return predicted_body_fat, bmi


# Fitness level classification function
def classify_fitness_level(bmi, body_fat, gender):
    if bmi < 18.5:
        bmi_category = 'Underweight'
    elif 18.5 <= bmi < 25:
        bmi_category = 'Normal'
    elif 25 <= bmi < 30:
        bmi_category = 'Overweight'
    else:
        bmi_category = 'Obese'

    if gender.lower() == 'm':
        if body_fat <= 5:
            body_fat_category = 'Essential'
        elif 6 <= body_fat <= 13:
            body_fat_category = 'Athlete'
        elif 14 <= body_fat <= 17:
            body_fat_category = 'Fitness'
        elif 18 <= body_fat <= 24:
            body_fat_category = 'Acceptable'
        else:
            body_fat_category = 'Obese'
    else:
        if body_fat <= 13:
            body_fat_category = 'Essential'
        elif 14 <= body_fat <= 20:
            body_fat_category = 'Athlete'
        elif 21 <= body_fat <= 24:
            body_fat_category = 'Fitness'
        elif 25 <= body_fat <= 31:
            body_fat_category = 'Acceptable'
        else:
            body_fat_category = 'Obese'

    if bmi_category == 'Normal' and body_fat_category in ['Athlete', 'Fitness']:
        fitness_level = 'Advanced'
    elif bmi_category in ['Normal', 'Overweight'] and body_fat_category in ['Fitness', 'Acceptable']:
        fitness_level = 'Intermediate'
    else:
        fitness_level = 'Beginner'

    return fitness_level


if __name__ == "__main__":
    age = int(sys.argv[1])
    gender = sys.argv[2]
    height_cm = float(sys.argv[3])
    weight_kg = float(sys.argv[4])

    # Make predictions for body fat and BMI
    predicted_body_fat, bmi = predict_body_fat_and_bmi(age, gender, height_cm, weight_kg)

    # Classify fitness level
    fitness_level = classify_fitness_level(bmi, predicted_body_fat, gender)

    # Output the results
    print(f"{predicted_body_fat},{bmi},{fitness_level}")
