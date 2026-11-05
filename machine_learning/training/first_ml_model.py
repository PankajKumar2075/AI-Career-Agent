
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

from sklearn.tree import plot_tree

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# STEP 1: Generate sample student data

np.random.seed(42)

n = 600

data = pd.DataFrame({
    "Python": np.random.randint(1, 11, n),
    "SQL": np.random.randint(1, 11, n),
    "Machine_Learning": np.random.randint(1, 11, n),
    "React": np.random.randint(1, 11, n),
    "Node": np.random.randint(1, 11, n),
    "MongoDB": np.random.randint(1, 11, n),
    "Excel": np.random.randint(1, 11, n)
})


# STEP 2: Calculate career scores

ml_score = (
    0.45 * data["Python"]
    + 0.40 * data["Machine_Learning"]
    + 0.15 * data["SQL"]
)

analyst_score = (
    0.25 * data["Python"]
    + 0.50 * data["SQL"]
    + 0.25 * data["Excel"]
)

fullstack_score = (
    0.45 * data["React"]
    + 0.40 * data["Node"]
    + 0.15 * data["MongoDB"]
)


# STEP 3: Assign career categories

scores = np.column_stack([
    ml_score,
    analyst_score,
    fullstack_score
])

roles = [
    "ML Engineer",
    "Data Analyst",
    "Full Stack Developer"
]

data["Career"] = np.array(roles)[np.argmax(scores, axis=1)]


# STEP 4: Save dataset

data.to_csv(
    "machine_learning/datasets/student_skills_demo.csv",
    index=False
)


# STEP 5: Separate features and target

X = data.drop("Career", axis=1)
y = data["Career"]


# STEP 6: Split training and testing data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# STEP 7: Create and train model

model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)


# STEP 8: Make predictions

y_pred = model.predict(X_test)


# STEP 9: Evaluate model

accuracy = accuracy_score(y_test, y_pred)

print("Dataset shape:", data.shape)
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# STEP 10: Predict for a new student

new_student = pd.DataFrame([{
    "Python": 9,
    "SQL": 8,
    "Machine_Learning": 10,
    "React": 2,
    "Node": 3,
    "MongoDB": 4,
    "Excel": 7
}])

prediction = model.predict(new_student)

print("\nRecommended Career:", prediction[0])

plt.figure(figsize=(22, 12))

plot_tree(
    model,
    feature_names=X.columns,
    class_names=model.classes_,
    filled=True,
    rounded=True,
    fontsize=9
)

plt.title("Decision Tree - Career Recommendation")
plt.show()

# Feature Importance

importance = model.feature_importances_

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(feature_importance)

# Visualization

plt.figure(figsize=(10, 6))

plt.barh(
    feature_importance["Feature"],
    feature_importance["Importance"]
)

plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.title("Feature Importance - Career Recommendation")

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Save trained model

model_path = "machine_learning/saved_models/career_model.joblib"

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Model location:", model_path)