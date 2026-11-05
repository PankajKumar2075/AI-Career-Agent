import joblib
import pandas as pd

# Load saved model

model_path = "machine_learning/saved_models/career_model.joblib"

model = joblib.load(model_path)

print("Model loaded successfully!")

# Create a new student's profile

new_student = pd.DataFrame([{
    "Python": 9,
    "SQL": 8,
    "Machine_Learning": 10,
    "React": 2,
    "Node": 3,
    "MongoDB": 4,
    "Excel": 7
}])

# Predict career

prediction = model.predict(new_student)

print("\nStudent Skills:")
print(new_student)

print("\nRecommended Career:", prediction[0])