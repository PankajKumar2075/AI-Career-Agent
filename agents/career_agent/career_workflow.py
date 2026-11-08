
from agents.resume_agent.resume_agent import analyze_resume
from agents.career_agent.career_agent import recommend_career


def run_career_workflow(resume_text):

    print("\n===== AI CAREER AGENT WORKFLOW =====")

    # Step 1: Resume Agent
    print("\n1. Running Resume Agent...")

    resume_analysis = analyze_resume(
        resume_text,
        "Analyze my complete resume."
    )

    print("\nResume Analysis Completed!")

    # Step 2: Career Agent
    print("\n2. Running Career Agent...")

    career_result = recommend_career(resume_text)

    print("\nCareer Prediction Completed!")

    # Step 3: Combined output
    print("\n===== FINAL CAREER REPORT =====")

    print("\nRESUME ANALYSIS:")
    print(resume_analysis)

    print("\nRECOMMENDED CAREER:")
    print(career_result["predicted_career"])

    print("\nCAREER PROBABILITIES:")

    for career, probability in career_result["probabilities"].items():
        print(f"{career}: {probability}%")

    print("\nEXTRACTED SKILLS:")
    print(career_result["skills"])

    return {
        "resume_analysis": resume_analysis,
        "career_result": career_result
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

    run_career_workflow(sample_resume)
