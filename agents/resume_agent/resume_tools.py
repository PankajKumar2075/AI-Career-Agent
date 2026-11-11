
import re


# ---------------------------------------------------------
# 1. Resume section detection
# ---------------------------------------------------------

SECTION_HEADINGS = {
    "skills": [
        "skills", "technical skills", "core skills",
        "technical competencies", "core competencies",
        "technologies", "tech stack"
    ],
    "projects": [
        "projects", "personal projects",
        "academic projects", "key projects"
    ],
    "education": [
        "education", "educational background",
        "academic background", "qualifications"
    ],
    "experience": [
        "experience", "work experience",
        "professional experience", "employment",
        "internships", "internship"
    ],
    "certifications": [
        "certifications", "certificates",
        "professional certifications"
    ],
    "achievements": [
        "achievements", "awards", "honors",
        "honours", "accomplishments"
    ]
}


def parse_resume_sections(resume_text):
    """
    Detect common resume sections.
    Returns section names mapped to their original text lines.
    """

    sections = {name: [] for name in SECTION_HEADINGS}
    current_section = None

    heading_lookup = {}

    for section, headings in SECTION_HEADINGS.items():
        for heading in headings:
            heading_lookup[heading] = section

    for line in resume_text.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        # Normalize headings such as TECHNICAL SKILLS:
        normalized = re.sub(r"[:\s]+$", "", clean_line.lower())
        normalized = re.sub(r"\s+", " ", normalized)

        if normalized in heading_lookup:
            current_section = heading_lookup[normalized]
            continue

        if current_section:
            sections[current_section].append(clean_line)

    return sections


# ---------------------------------------------------------
# 2. Technical skill extraction
# ---------------------------------------------------------

SKILL_LIST = [
    "Python", "C", "C++", "C#", "Java", "JavaScript",
    "TypeScript", "PHP", "Ruby", "Go", "Rust",
    "React", "Next.js", "Node.js","MERN", "MERN Stack", "Express.js",
    "Spring Boot", "FastAPI", "Flask", "Django",
    "HTML", "CSS", "Bootstrap", "Tailwind CSS",
    "MongoDB", "MySQL", "PostgreSQL", "SQLite",
    "SQL", "Redis", "Firebase",
    "Machine Learning", "Deep Learning",
    "Generative AI", "Artificial Intelligence",
    "Natural Language Processing", "Computer Vision",
    "Large Language Models", "LLM",
    "Pandas", "NumPy", "Scikit-learn",
    "TensorFlow", "PyTorch", "OpenCV",
    "Data Structures", "Data Structures and Algorithms",
    "Object Oriented Programming", "OOP",
    "Git", "GitHub", "Docker", "Kubernetes",
    "AWS", "Azure", "Google Cloud",
    "REST API", "REST APIs", "GraphQL",
    "Socket.IO", "R", "Excel",
    "Power BI", "Tableau", "Linux",
    "Postman", "Cloudinary", "JWT"
]



def extract_skills(resume_text):
    """
    Backward-compatible skill extraction.
    Removes URLs before matching so profile links do not count as skills.
    """

    text_without_urls = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        resume_text,
        flags=re.IGNORECASE
    )

    found_skills = []

    for skill in SKILL_LIST:

        if skill == "C":
            # Prevent C from matching inside C++ or C#
            pattern = r"(?<![\w+#])C(?![\w+#])"
        else:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text_without_urls, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills



def extract_skill_proficiency(resume_text):
    """
    Detect proficiency only when the resume explicitly states it.
    Never assumes that mentioning a skill means proficiency.
    """

    results = []

    levels = [
        "beginner", "novice", "intermediate",
        "advanced", "expert", "proficient"
    ]

    for skill in extract_skills(resume_text):
        proficiency = "Not specified"

        for level in levels:
            pattern = (
                r"\b" + re.escape(skill) +
                r"\b\s*[-:–]?\s*\b" + level + r"\b"
            )

            reverse_pattern = (
                r"\b" + level +
                r"\b\s+(?:in|with)\s+\b" +
                re.escape(skill) + r"\b"
            )

            if (
                re.search(pattern, resume_text, re.IGNORECASE)
                or re.search(reverse_pattern, resume_text, re.IGNORECASE)
            ):
                proficiency = level.title()
                break

        results.append({
            "name": skill,
            "proficiency": proficiency
        })

    return results



def extract_structured_skills(resume_text):
    """
    Prefer the dedicated skills section.
    If no skills section exists, fall back to the full resume.
    """

    sections = parse_resume_sections(resume_text)

    skills_text = "\n".join(sections["skills"])

    if not skills_text.strip():
        skills_text = resume_text

    return extract_skill_proficiency(skills_text)


# ---------------------------------------------------------
# 3. Project extraction
# ---------------------------------------------------------

def extract_projects(resume_text):
    """
    Backward-compatible function.
    Returns the original project-section lines as a list.
    """

    sections = parse_resume_sections(resume_text)
    return sections["projects"]



def extract_structured_projects(resume_text):
    """
    Groups numbered or pipe-separated project headings
    with their following descriptions.
    """

    lines = extract_projects(resume_text)
    projects = []
    current_project = None

    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        # Detect common project heading formats:
        # 1. Project Name | Technologies
        # • Project Name | Technologies
        # Project Name | Technologies
        numbered_heading = bool(
            re.match(r"^\s*\d+[\.)]\s*", line)
        )

        pipe_heading = "|" in clean_line

        is_heading = numbered_heading or pipe_heading

        if is_heading:

            if current_project:
                projects.append(current_project)

            title = re.sub(
                r"^\s*(?:\d+[\.)]\s*|[•*\-]\s*)",
                "",
                clean_line
            ).strip()

            current_project = {
                "name": title,
                "description": [],
                "technologies": extract_skills(title),
                "evidence": [line]
            }

        elif current_project:

            current_project["description"].append(clean_line)
            current_project["evidence"].append(line)

            for skill in extract_skills(clean_line):
                if skill not in current_project["technologies"]:
                    current_project["technologies"].append(skill)

        else:
            # Preserve text even if no recognizable project heading exists.
            current_project = {
                "name": None,
                "description": [clean_line],
                "technologies": extract_skills(clean_line),
                "evidence": [line]
            }

    if current_project:
        projects.append(current_project)

    return projects


# ---------------------------------------------------------
# 4. Contact information extraction
# ---------------------------------------------------------

def extract_contact_details(resume_text):
    emails = re.findall(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        resume_text
    )

    phones = re.findall(
        r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?"
        r"(?:\d[-.\s]?){9,12}\d(?!\w)",
        resume_text
    )

    linkedin = re.findall(
        r"(?:https?://)?(?:www\.)?linkedin\.com/in/[^\s,]+",
        resume_text,
        re.IGNORECASE
    )

    github = re.findall(
        r"(?:https?://)?(?:www\.)?github\.com/[^\s,]+",
        resume_text,
        re.IGNORECASE
    )

    # A name candidate is only a heuristic, not a guarantee.
    name = None
    for line in resume_text.splitlines()[:6]:
        candidate = line.strip()

        if not candidate:
            continue

        if (
            "@" in candidate
            or re.search(r"\d", candidate)
            or "linkedin.com" in candidate.lower()
            or "github.com" in candidate.lower()
        ):
            continue

        words = candidate.split()

        if (
            2 <= len(words) <= 4
            and all(re.fullmatch(r"[A-Za-z][A-Za-z'.-]*", word) for word in words)
        ):
            name = candidate
            break

    return {
        "name_candidate": name,
        "emails": list(dict.fromkeys(emails)),
        "phone_numbers": list(dict.fromkeys(phones)),
        "linkedin_urls": list(dict.fromkeys(linkedin)),
        "github_urls": list(dict.fromkeys(github))
    }


# ---------------------------------------------------------
# 5. Education extraction
# ---------------------------------------------------------

def extract_education(resume_text):
    sections = parse_resume_sections(resume_text)
    lines = sections["education"]

    cgpa_or_percentage = []

    for line in lines:
        if re.search(
            r"\b(CGPA|GPA|percentage|percent|aggregate)\b",
            line,
            re.IGNORECASE
        ):
            cgpa_or_percentage.append(line)

    return {
        "entries": lines,
        "cgpa_or_percentage_evidence": cgpa_or_percentage
    }


# ---------------------------------------------------------
# 6. Experience extraction
# ---------------------------------------------------------

def extract_experience(resume_text):
    sections = parse_resume_sections(resume_text)

    # Preserve original lines instead of guessing job titles,
    # organizations, dates, or responsibilities.
    return {
        "entries": sections["experience"]
    }


# ---------------------------------------------------------
# 7. Certifications and achievements
# ---------------------------------------------------------

def extract_certifications(resume_text):
    sections = parse_resume_sections(resume_text)

    return {
        "entries": sections["certifications"]
    }


def extract_achievements(resume_text):
    sections = parse_resume_sections(resume_text)

    return {
        "entries": sections["achievements"]
    }


# ---------------------------------------------------------
# 8. Resume statistics
# ---------------------------------------------------------

def get_resume_statistics(resume_text):
    """
    Backward-compatible statistics function.
    """

    words = resume_text.split()

    return {
        "total_words": len(words),
        "total_characters": len(resume_text),
        "total_lines": len(resume_text.splitlines())
    }


# ---------------------------------------------------------
# 9. Complete structured resume extraction
# ---------------------------------------------------------

def extract_structured_resume(resume_text):
    """
    Main deterministic extraction function.

    Extracted values are based on resume text.
    Missing information remains empty or unspecified.
    """

    if not resume_text or not resume_text.strip():
        return {
            "contact": {},
            "skills": [],
            "projects": [],
            "education": {},
            "experience": {},
            "certifications": {},
            "achievements": {},
            "statistics": {}
        }

    return {
        "contact": extract_contact_details(resume_text),
        "skills": extract_structured_skills(resume_text),
        "projects": extract_structured_projects(resume_text),
        "education": extract_education(resume_text),
        "experience": extract_experience(resume_text),
        "certifications": extract_certifications(resume_text),
        "achievements": extract_achievements(resume_text),
        "statistics": get_resume_statistics(resume_text)
    }
