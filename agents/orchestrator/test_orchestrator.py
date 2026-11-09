
from agents.orchestrator.orchestrator import run_full_career_workflow


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


result = run_full_career_workflow(
    resume_text=sample_resume,
    difficulty="medium",
    num_questions=3
)

print("\n========== FINAL REPORT ==========")

print("\nRecommended Career:")
print(result["career_result"]["predicted_career"])

print("\nCareer Probabilities:")
print(result["career_result"]["probabilities"])

print("\nSkill Gap Coverage:")
print(result["learning_result"]["coverage_score"], "%")

print("\nTotal Learning Weeks:")
print(result["learning_result"]["learning_plan"]["total_weeks"])

print("\nInterview Questions:")
print(result["interview_result"]["questions"])
