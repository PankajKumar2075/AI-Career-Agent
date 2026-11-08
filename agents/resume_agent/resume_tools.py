
import re


# Tool 1: Extract technical skills
def extract_skills(resume_text):

    skill_list = [
        "Python", "C++", "Java", "JavaScript",
        "React", "Node.js", "Express.js",
        "MongoDB", "MySQL", "SQL",
        "Machine Learning", "Deep Learning",
        "HTML", "CSS", "Bootstrap",
        "FastAPI", "Flask", "Django",
        "Pandas", "NumPy", "TensorFlow",
        "PyTorch", "Git", "GitHub",
        "Data Structures", "OOP", "Excel"
    ]

    found_skills = []

    for skill in skill_list:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, resume_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# Tool 2: Extract projects
def extract_projects(resume_text):

    lines = resume_text.splitlines()
    projects = []

    inside_projects = False

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        if re.search(r"projects|personal projects", clean_line, re.IGNORECASE):
            inside_projects = True
            continue

        if inside_projects and re.search(
            r"^(education|experience|skills|certifications)\b",
            clean_line,
            re.IGNORECASE
        ):
            inside_projects = False

        if inside_projects:
            projects.append(clean_line)

    return projects


# Tool 3: Generate resume statistics
def get_resume_statistics(resume_text):

    words = resume_text.split()

    return {
        "total_words": len(words),
        "total_characters": len(resume_text),
        "total_lines": len(resume_text.splitlines())
    }
