
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal


# 1. Create FastAPI application

app = FastAPI(
    title="AI Career Recommendation API",
    description="Predict career categories using Machine Learning",
    version="1.0.0"
)


# Allow React frontend to communicate with FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Locate and load the trained ML model

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "machine_learning"
    / "saved_models"
    / "career_model.joblib"
)

model = joblib.load(MODEL_PATH)

print("Career prediction model loaded successfully!")


# 3. Define input data structure

class StudentSkills(BaseModel):

    Python: int = Field(ge=1, le=10)
    SQL: int = Field(ge=1, le=10)
    Machine_Learning: int = Field(ge=1, le=10)
    React: int = Field(ge=1, le=10)
    Node: int = Field(ge=1, le=10)
    MongoDB: int = Field(ge=1, le=10)
    Excel: int = Field(ge=1, le=10)



class SkillGapRequest(StudentSkills):

    target_career: Literal[
        "ML Engineer",
        "Data Analyst",
        "Full Stack Developer"
    ]



# Initial illustrative skill benchmarks for each career

CAREER_REQUIREMENTS = {

    "ML Engineer": {
        "Python": 9,
        "SQL": 7,
        "Machine_Learning": 9,
        "React": 2,
        "Node": 2,
        "MongoDB": 3,
        "Excel": 4
    },

    "Data Analyst": {
        "Python": 7,
        "SQL": 9,
        "Machine_Learning": 5,
        "React": 1,
        "Node": 1,
        "MongoDB": 4,
        "Excel": 9
    },

    "Full Stack Developer": {
        "Python": 4,
        "SQL": 6,
        "Machine_Learning": 2,
        "React": 9,
        "Node": 9,
        "MongoDB": 8,
        "Excel": 2
    }
}



# 4. Home endpoint

@app.get("/")
def home():

    return {
        "message": "Welcome to AI Career Recommendation API"
    }


# 5. Health endpoint

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "model_loaded": True
    }


# 6. Career prediction endpoint


@app.post("/predict-career")
def predict_career(student: StudentSkills):

    # Convert input into a DataFrame
    student_data = pd.DataFrame(
        [student.model_dump()]
    )

    # Keep the same feature order used during training
    feature_order = [
        "Python",
        "SQL",
        "Machine_Learning",
        "React",
        "Node",
        "MongoDB",
        "Excel"
    ]

    student_data = student_data[feature_order]

    # Predict the best career
    prediction = model.predict(student_data)

    # Calculate estimated scores for all career categories
    probabilities = model.predict_proba(student_data)[0]

    career_scores = {
        str(career): round(float(score) * 100, 2)
        for career, score in zip(model.classes_, probabilities)
    }

    # Return prediction and scores
    return {
        "recommended_career": str(prediction[0]),
        "career_scores": career_scores,
        "student_skills": student_data.to_dict(orient="records")[0]
    }


# skill gap analysis

@app.post("/skill-gap")
def analyze_skill_gap(student: SkillGapRequest):

    # Get the selected career
    target_career = student.target_career

    # Get required skills for that career
    required_skills = CAREER_REQUIREMENTS[target_career]

    # Get student's current skills
    current_skills = student.model_dump(
        exclude={"target_career"}
    )

    skill_gaps = {}
    total_required = 0
    total_covered = 0

    # Compare current and required skill levels
    for skill, required in required_skills.items():

        current = current_skills[skill]

        gap = max(0, required - current)

        skill_gaps[skill] = {
            "current_level": current,
            "required_level": required,
            "gap": gap,
            "status": "Needs Improvement" if gap > 0 else "Requirement Met"
        }

        total_required += required
        total_covered += min(current, required)

    # Calculate requirement coverage
    coverage = (
        total_covered / total_required
    ) * 100

    return {
        "target_career": target_career,
        "skill_gaps": skill_gaps,
        "coverage_score": round(coverage, 2)
    }
