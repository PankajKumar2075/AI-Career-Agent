
from agents.resume_agent.resume_tools import (
    extract_skills,
    extract_projects,
    get_resume_statistics
)


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


print("===== RESUME TOOL TESTING =====")

skills = extract_skills(sample_resume)
projects = extract_projects(sample_resume)
statistics = get_resume_statistics(sample_resume)

print("\nExtracted Skills:")
print(skills)

print("\nExtracted Projects:")
print(projects)

print("\nResume Statistics:")
print(statistics)
