
from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
from backend.app.services.roadmap_service import generate_learning_roadmap
from backend.app.services.progress_service import (
    save_learning_progress,
    get_learning_progress
)
from generative_ai.ollama_service import (
    generate_ai_response,
    generate_chat_response
)
from generative_ai.rag.rag_pipeline import generate_rag_result
from backend.app.services.resume_parser import parse_resume_file



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


class InterviewQuestionRequest(BaseModel):
    target_career: str
    skills: list[str] = []
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    num_questions: int = Field(default=5, ge=1, le=10)



class InterviewAnswerRequest(BaseModel):
    question: str
    answer: str
    target_career: str



class FollowUpRequest(BaseModel):
    question: str
    answer: str
    evaluation: str
    target_career: str



class MockInterviewRequest(BaseModel):
    questions: list[str]
    answers: list[str]
    target_career: str



class LearningProgressRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=100)
    target_career: Literal[
        "ML Engineer",
        "Data Analyst",
        "Full Stack Developer"
    ]
    completed_weeks: list[int] = Field(default_factory=list)

class AIAdviceRequest(BaseModel):
    question: str = Field(min_length=5, max_length=2000)


class PersonalizedAIRequest(StudentSkills):
    question: str = Field(min_length=5, max_length=2000)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)


class CareerChatRequest(StudentSkills):
    messages: list[ChatMessage] = Field(
        min_length=1,
        max_length=10
    )

class RAGQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

    category: str | None = None


# Initial illustrative skill benchmarks for each career

CAREER_REQUIREMENTS = {

    "ML Engineer": {
        "Python": 9,
        "Machine_Learning": 9,
        "SQL": 7
    },

    "Data Analyst": {
        "Python": 7,
        "SQL": 9,
        "Excel": 9,
        "Machine_Learning": 5
    },

    "Full Stack Developer": {
        "React": 9,
        "Node": 9,
        "MongoDB": 8,
        "SQL": 6
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


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Read at most 10 MB + 1 byte to enforce the file-size limit.
        contents = await file.read(10 * 1024 * 1024 + 1)

        # Extract and validate resume content.
        result = parse_resume_file(file.filename, contents)

        return {
            "message": "Resume uploaded and text extracted successfully.",
            **result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the uploaded resume."
        )

    finally:
        await file.close()

        
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



@app.post("/agentic-learning-plan")
def agentic_learning_plan(student: SkillGapRequest):

    # Import here to avoid circular imports
    from agents.learning_agent.learning_agent import create_learning_plan

    # Step 1: Calculate actual skill gaps
    gap_result = analyze_skill_gap(student)

    # Step 2: Generate the personalized learning plan
    learning_result = create_learning_plan(
        skill_gaps=gap_result["skill_gaps"],
        target_career=gap_result["target_career"]
    )

    # Step 3: Return complete results
    return {
        "target_career": gap_result["target_career"],
        "coverage_score": gap_result["coverage_score"],
        "skill_gaps": gap_result["skill_gaps"],
        "learning_plan": learning_result
    }




@app.post("/learning-roadmap")
def create_learning_roadmap(student: SkillGapRequest):

    # First, calculate the student's skill gaps
    gap_result = analyze_skill_gap(student)

    # Generate a roadmap using the calculated skill gaps
    roadmap_result = generate_learning_roadmap(
        gap_result["skill_gaps"]
    )

    return {
        "target_career": student.target_career,
        "coverage_score": gap_result["coverage_score"],
        "total_weeks": roadmap_result["total_weeks"],
        "roadmap": roadmap_result["roadmap"]
    }



@app.post("/save-progress")
def save_progress(request: LearningProgressRequest):

    result = save_learning_progress(
        request.student_id,
        request.target_career,
        request.completed_weeks
    )

    return result



@app.get("/get-progress/{student_id}/{target_career}")
def retrieve_progress(student_id: str, target_career: str):

    if target_career not in CAREER_REQUIREMENTS:
        return {
            "error": "Invalid target career"
        }

    result = get_learning_progress(
        student_id,
        target_career
    )

    return result


@app.post("/ai-career-advice")
def ai_career_advice(request: AIAdviceRequest):

    prompt = f"""
    You are an expert AI career mentor.

    Give clear, practical and beginner-friendly
    career guidance to students.

    Student's question:
    {request.question}

    Provide a structured and useful answer.
    """

    try:
        answer = generate_ai_response(prompt)

        return {
            "question": request.question,
            "ai_response": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"AI service unavailable: {str(e)}"
        )

@app.post("/personalized-ai-advice")
def personalized_ai_advice(request: PersonalizedAIRequest):

    # Get student skills
    student_data = pd.DataFrame([
        request.model_dump(exclude={"question"})
    ])

    # Predict career using our trained ML model
    prediction = model.predict(student_data)[0]

    # Calculate skill gaps
    required_skills = CAREER_REQUIREMENTS[str(prediction)]

    current_skills = request.model_dump(
        exclude={"question"}
    )

    skill_gaps = {}

    for skill, required in required_skills.items():

        current = current_skills[skill]
        gap = max(0, required - current)

        if gap > 0:
            skill_gaps[skill] = {
                "current": current,
                "required": required,
                "gap": gap
            }

    # Prepare personalized prompt
    prompt = f"""
    You are an expert AI career mentor.

    STUDENT SKILLS:
    {current_skills}

    ML MODEL PREDICTED CAREER:
    {prediction}

    IDENTIFIED SKILL GAPS:
    {skill_gaps}

    STUDENT QUESTION:
    {request.question}

    Instructions:
    1. Give advice based on the actual student skills.
    2. Explain which skills need improvement.
    3. Prioritize the most important skill gaps.
    4. Suggest practical projects where relevant.
    5. Give beginner-friendly explanations.
    6. Do not invent student experience or achievements.
    """

    try:
        answer = generate_ai_response(prompt)

        return {
            "recommended_career": str(prediction),
            "student_skills": current_skills,
            "skill_gaps": skill_gaps,
            "question": request.question,
            "ai_response": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"AI service unavailable: {str(e)}"
        )


@app.post("/personalized-ai-chat")
def personalized_ai_chat(request: CareerChatRequest):

    # Get student skills
    current_skills = request.model_dump(
        exclude={"messages"}
    )

    # Predict career
    student_data = pd.DataFrame([current_skills])
    prediction = str(model.predict(student_data)[0])

    # Calculate skill gaps
    required_skills = CAREER_REQUIREMENTS[prediction]

    skill_gaps = {}

    for skill, required in required_skills.items():

        current = current_skills[skill]
        gap = max(0, required - current)

        if gap > 0:
            skill_gaps[skill] = {
                "current": current,
                "required": required,
                "gap": gap
            }

    # Create system instructions
    system_prompt = f"""
    You are an expert AI career mentor.

    STUDENT SKILLS:
    {current_skills}

    PREDICTED CAREER:
    {prediction}

    STUDENT SKILL GAPS:
    {skill_gaps}

    Instructions:
    1. Remember the conversation history.
    2. Give personalized career guidance.
    3. Use the student's actual skill levels.
    4. Explain concepts in beginner-friendly language.
    5. Suggest practical projects when relevant.
    6. Do not invent student achievements.
    """

    # Prepare conversation
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for message in request.messages:
        messages.append({
            "role": message.role,
            "content": message.content
        })

    try:
        answer = generate_chat_response(messages)

        return {
            "recommended_career": prediction,
            "skill_gaps": skill_gaps,
            "ai_response": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"AI service unavailable: {str(e)}"
        )


@app.post("/rag-career-advice")
def rag_career_advice(request: RAGQuestion):

    result = generate_rag_result(
        request.question,
        category=request.category
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "total_chunks_used": result["total_chunks_used"]
    }



# ==============================
# INTERVIEW AGENT APIs
# ==============================

@app.post("/interview/questions")
def generate_interview_questions_api(request: InterviewQuestionRequest):

    from agents.interview_agent.interview_agent import generate_interview_questions

    result = generate_interview_questions(
        target_career=request.target_career,
        skills=request.skills,
        difficulty=request.difficulty,
        num_questions=request.num_questions
    )

    return result


@app.post("/interview/evaluate")
def evaluate_interview_answer_api(request: InterviewAnswerRequest):

    from agents.interview_agent.interview_agent import evaluate_interview_answer

    result = evaluate_interview_answer(
        question=request.question,
        answer=request.answer,
        target_career=request.target_career
    )

    return result


@app.post("/interview/follow-up")
def generate_follow_up_api(request: FollowUpRequest):

    from agents.interview_agent.interview_agent import generate_follow_up_question

    result = generate_follow_up_question(
        question=request.question,
        answer=request.answer,
        evaluation=request.evaluation,
        target_career=request.target_career
    )

    return result


@app.post("/interview/mock")
def run_mock_interview_api(request: MockInterviewRequest):

    from agents.interview_agent.interview_agent import run_mock_interview

    result = run_mock_interview(
        questions=request.questions,
        answers=request.answers,
        target_career=request.target_career
    )

    return result




# ==============================
# MULTI-AGENT ORCHESTRATOR API
# ==============================

class FullCareerWorkflowRequest(BaseModel):

    resume_text: str = Field(min_length=50)

    mode: Literal["discover", "goal"] = "discover"

    target_career: Literal[
        "ML Engineer",
        "Data Analyst",
        "Full Stack Developer"
    ] | None = None

    difficulty: Literal["easy", "medium", "hard"] = "medium"

    num_questions: int = Field(default=5, ge=1, le=10)


class ContinueCareerWorkflowRequest(BaseModel):

    resume_text: str = Field(min_length=50)

    target_career: Literal[
        "ML Engineer",
        "Data Analyst",
        "Full Stack Developer"
    ]

    difficulty: Literal["easy", "medium", "hard"] = "medium"

    num_questions: int = Field(default=5, ge=1, le=10)


@app.post("/agents/full-career-workflow")
def run_full_career_workflow_api(
    request: FullCareerWorkflowRequest
):

    from agents.orchestrator.orchestrator import (
        run_full_career_workflow
    )

    if request.mode == "goal" and not request.target_career:
        raise HTTPException(
            status_code=400,
            detail="Please select a target career for goal mode."
        )

    try:
        result = run_full_career_workflow(
            resume_text=request.resume_text,
            mode=request.mode,
            target_career=request.target_career,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Multi-agent workflow failed: {str(e)}"
        )


@app.post("/agents/continue-career-workflow")
def continue_career_workflow_api(
    request: ContinueCareerWorkflowRequest
):

    from agents.orchestrator.orchestrator import (
        continue_career_workflow
    )

    try:
        result = continue_career_workflow(
            resume_text=request.resume_text,
            target_career=request.target_career,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Career workflow continuation failed: {str(e)}"
        )