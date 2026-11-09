from agents.resume_agent.resume_agent import analyze_resume
from agents.career_agent.career_agent import recommend_career_options
from agents.learning_agent.learning_workflow import run_learning_workflow
from agents.interview_agent.interview_agent import generate_interview_questions


SUPPORTED_CAREERS = [
    "ML Engineer",
    "Data Analyst",
    "Full Stack Developer"
]


def continue_career_workflow(
    resume_text,
    target_career,
    difficulty="medium",
    num_questions=5
):
    """
    Continue the workflow after the user selects a career.
    The selected career always comes from the user, not the ML model.
    """

    if target_career not in SUPPORTED_CAREERS:
        raise ValueError(
            f"Unsupported career. Choose one of: {SUPPORTED_CAREERS}"
        )

    print("\n========== CONTINUING CAREER WORKFLOW ==========")

    # Extract skills and get career suggestions from the resume.
    career_result = recommend_career_options(resume_text)

    extracted_skills = career_result["skills"]
    skill_scores = career_result["skill_scores"]

    # Learning Agent
    print("\n[1/2] Running Learning Agent...")

    student_data = {
        **skill_scores,
        "target_career": target_career
    }

    learning_result = run_learning_workflow(student_data)

    print("Personalized learning roadmap completed.")

    # Interview Agent
    print("\n[2/2] Running Interview Agent...")

    interview_result = generate_interview_questions(
        target_career=target_career,
        skills=extracted_skills,
        difficulty=difficulty,
        num_questions=num_questions
    )

    print("Interview questions generated.")

    return {
        "selected_career": target_career,
        "learning_result": learning_result,
        "interview_result": interview_result
    }


def run_full_career_workflow(
    resume_text,
    mode="discover",
    target_career=None,
    difficulty="medium",
    num_questions=5
):
    """
    Mode 1: discover
        Analyze resume and recommend multiple career options.

    Mode 2: goal
        Use the career explicitly selected by the user and run
        the complete workflow.
    """

    print("\n========== MULTI-AGENT WORKFLOW ==========")

    # Resume Agent
    print("\n[1/2] Running Resume Agent...")

    resume_result = analyze_resume(
        resume_text,
        "Analyze my complete resume. Identify my skills, education, "
        "projects, experience, and areas for improvement."
    )

    print("Resume analysis completed.")

    # Career Agent
    print("\n[2/2] Running Career Agent...")

    career_result = recommend_career_options(resume_text)

    print("Career recommendations generated.")

    # Discovery mode: wait for the user's career choice.
    if mode == "discover":

        return {
            "workflow_mode": "discover",
            "workflow_stage": "career_selection_required",
            "resume_analysis": resume_result,
            "career_result": career_result,
            "message": (
                "Choose a career from the recommendations to generate "
                "your personalized learning roadmap and interview preparation."
            )
        }

    # Goal mode: the user must explicitly provide a career.
    if mode == "goal":

        if not target_career:
            raise ValueError(
                "Please select a target career before starting goal mode."
            )

        selected_results = continue_career_workflow(
            resume_text=resume_text,
            target_career=target_career,
            difficulty=difficulty,
            num_questions=num_questions
        )

        return {
            "workflow_mode": "goal",
            "workflow_stage": "completed",
            "resume_analysis": resume_result,
            "career_result": career_result,
            "selected_career": target_career,
            "learning_result": selected_results["learning_result"],
            "interview_result": selected_results["interview_result"]
        }

    raise ValueError("Mode must be either 'discover' or 'goal'.")