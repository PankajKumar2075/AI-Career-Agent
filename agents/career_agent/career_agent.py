
from pathlib import Path
import joblib
import pandas as pd

from agents.resume_agent.resume_tools import extract_skills


# Locate the trained ML model
ROOT_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    ROOT_DIR
    / "machine_learning"
    / "saved_models"
    / "career_model.joblib"
)


# Feature order must match the model's training data
FEATURES = [
    "Python",
    "SQL",
    "Machine_Learning",
    "React",
    "Node",
    "MongoDB",
    "Excel"
]


# Convert extracted skills into model inputs
def prepare_skill_data(resume_text):

    extracted_skills = extract_skills(resume_text)

    skills_lower = [skill.lower() for skill in extracted_skills]

    skill_mapping = {
        "Python": ["python"],
        "SQL": ["sql", "mysql"],
        "Machine_Learning": ["machine learning", "deep learning"],
        "React": ["react"],
        "Node": ["node.js", "node"],
        "MongoDB": ["mongodb"],
        "Excel": ["excel"]
    }

    skill_scores = {}

    for feature, keywords in skill_mapping.items():

        if any(skill in skills_lower for skill in keywords):
            skill_scores[feature] = 5
        else:
            skill_scores[feature] = 1

    return extracted_skills, skill_scores


# Career prediction
def recommend_career(resume_text):

    if not resume_text.strip():
        return "Please provide resume text."

    if not MODEL_PATH.exists():
        return f"ML model not found: {MODEL_PATH}"

    # Step 1: Extract skills
    extracted_skills, skill_scores = prepare_skill_data(resume_text)

    # Step 2: Load trained model
    model = joblib.load(MODEL_PATH)

    # Step 3: Prepare model input
    input_data = pd.DataFrame(
        [skill_scores],
        columns=FEATURES
    )

    # Step 4: Predict career
    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    # Step 5: Display results
    results = sorted(
        zip(model.classes_, probabilities),
        key=lambda item: item[1],
        reverse=True
    )

    print("\n===== CAREER AGENT =====")

    print("\nExtracted Skills:")
    print(extracted_skills)

    print("\nPredicted Career:")
    print(prediction)

    print("\nCareer Prediction Probabilities:")

    for career, probability in results:
        print(f"{career}: {probability * 100:.2f}%")

    print("\nTemporary Input Scores:")
    print(skill_scores)

    return {
        "predicted_career": prediction,
        "skills": extracted_skills,
        "skill_scores": skill_scores,
        "probabilities": {
            career: round(float(probability) * 100, 2)
            for career, probability in results
        }
    }


if __name__ == "__main__":

    sample_resume = """
    Candidate: Software Developer

    Skills:
    Python, C++, JavaScript, React, Node.js,
    MongoDB, SQL, Machine Learning.

    Projects:
    1. AI Career Agent using Python and Machine Learning.
    2. Learning Management System using MERN Stack.

    Education:
    B.Tech Computer Science Engineering.
    """

    recommend_career(sample_resume)



def recommend_career_options(resume_text):
    """
    Recommend multiple career directions.
    The ML model ranks options; it does not choose the user's career.
    """

    result = recommend_career(resume_text)

    if not isinstance(result, dict):
        raise ValueError(result)

    probabilities = result.get("probabilities", {})

    recommended_careers = [
        {
            "career": career,
            "ranking_score": score
        }
        for career, score in sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ]

    return {
        "recommended_careers": recommended_careers,
        "skills": result.get("skills", []),
        "skill_scores": result.get("skill_scores", {}),
        "note": (
            "These are experimental model rankings based on a synthetic "
            "training dataset. They are suggestions, not calibrated job "
            "readiness scores or predictions of career success."
        )
    }
