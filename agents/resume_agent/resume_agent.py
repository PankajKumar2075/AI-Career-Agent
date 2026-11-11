
import json

from generative_ai.ollama_service import generate_ai_response

from agents.resume_agent.resume_tools import (
    extract_skills,
    extract_projects,
    get_resume_statistics,
    extract_structured_resume
)


# ---------------------------------------------------------
# 1. Available tools
# ---------------------------------------------------------

AVAILABLE_TOOLS = {
    "extract_skills": extract_skills,
    "extract_projects": extract_projects,
    "get_resume_statistics": get_resume_statistics
}


# ---------------------------------------------------------
# 2. Tool selection
# ---------------------------------------------------------

def select_tools(user_request):
    """
    Uses the LLM to select the tools required for a request.

    If the LLM returns invalid JSON or an invalid tool name,
    the function safely falls back to all available tools.
    """

    prompt = f"""
You are a tool selection planner for a Resume Agent.

Available tools:
1. extract_skills
2. extract_projects
3. get_resume_statistics

Choose only the tools needed for the user's request.

Rules:
- Skills questions: extract_skills
- Project questions: extract_projects
- Resume statistics questions: get_resume_statistics
- Full resume analysis: select all three tools
- Never select tools outside the available list.

Return ONLY valid JSON:
{{"tools": ["extract_skills"]}}

User request:
{user_request}
"""

    try:
        response = generate_ai_response(prompt)

        if not response or not isinstance(response, str):
            raise ValueError("Empty or invalid planner response")

        # Find the JSON object in the response.
        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end <= start:
            raise ValueError("Invalid planner JSON")

        data = json.loads(response[start:end])

        if not isinstance(data, dict):
            raise ValueError("Planner response must be a JSON object")

        tools = data.get("tools", [])

        if not isinstance(tools, list):
            raise ValueError("Tools must be returned as a list")

        selected_tools = [
            tool
            for tool in tools
            if isinstance(tool, str) and tool in AVAILABLE_TOOLS
        ]

        if not selected_tools:
            raise ValueError("No valid tools selected")

        return selected_tools

    except Exception as error:
        print(f"Planner fallback: {error}")
        print("Selecting all available tools.")

        return list(AVAILABLE_TOOLS.keys())


# ---------------------------------------------------------
# 3. Tool execution
# ---------------------------------------------------------

def execute_tools(resume_text, selected_tools):
    """
    Executes the tools selected by the planner.
    """

    results = {}

    for tool_name in selected_tools:

        if tool_name not in AVAILABLE_TOOLS:
            continue

        tool_function = AVAILABLE_TOOLS[tool_name]

        try:
            results[tool_name] = tool_function(resume_text)

        except Exception as error:
            print(f"Tool execution error ({tool_name}): {error}")
            results[tool_name] = None

    return results


# ---------------------------------------------------------
# 4. Report formatting helpers
# ---------------------------------------------------------

def format_list(items, empty_message="Not mentioned in resume."):
    """
    Converts extracted information into readable bullet points.
    """

    if items is None:
        return f"- {empty_message}"

    if isinstance(items, str):
        items = [items]

    if not isinstance(items, (list, tuple)):
        return f"- {empty_message}"

    valid_items = [
        str(item).strip()
        for item in items
        if item is not None and str(item).strip()
    ]

    if not valid_items:
        return f"- {empty_message}"

    return "\n".join(f"- {item}" for item in valid_items)


def safe_get(data, key, default=None):
    """
    Safely retrieves a value from a dictionary.
    """

    if isinstance(data, dict):
        return data.get(key, default)

    return default


# ---------------------------------------------------------
# 5. Deterministic factual report
# ---------------------------------------------------------

def build_factual_report(data):
    """
    Creates the factual resume report using Python.

    The report uses extracted resume information.
    It does not ask the LLM to invent candidate details.
    """

    if not isinstance(data, dict):
        data = {}

    contact = safe_get(data, "contact", {})
    skills = safe_get(data, "skills", [])
    projects = safe_get(data, "projects", [])
    education = safe_get(data, "education", {})
    experience = safe_get(data, "experience", {})
    certifications = safe_get(data, "certifications", {})
    achievements = safe_get(data, "achievements", {})
    statistics = safe_get(data, "statistics", {})

    report = []

    report.append("# Resume Analysis")
    report.append("")

    report.append(
        "The following information was extracted from the "
        "provided resume. It has not been supplemented with "
        "assumed qualifications, experience, or achievements."
    )

    # -----------------------------------------------------
    # Contact Information
    # -----------------------------------------------------

    report.append("\n## 1. Contact Information")

    name = safe_get(contact, "name_candidate")

    if name:
        report.append(
            f"- **Possible name (heuristic):** {name}"
        )
    else:
        report.append("- **Name:** Not mentioned in resume.")

    report.append("\n**Email addresses:**")
    report.append(
        format_list(safe_get(contact, "emails", []))
    )

    report.append("\n**Phone numbers:**")
    report.append(
        format_list(safe_get(contact, "phone_numbers", []))
    )

    report.append("\n**LinkedIn profiles:**")
    report.append(
        format_list(safe_get(contact, "linkedin_urls", []))
    )

    report.append("\n**GitHub profiles:**")
    report.append(
        format_list(safe_get(contact, "github_urls", []))
    )

    # -----------------------------------------------------
    # Technical Skills
    # -----------------------------------------------------

    report.append("\n## 2. Technical Skills")

    if isinstance(skills, list) and skills:

        for skill in skills:

            if isinstance(skill, dict):

                skill_name = skill.get("name", "Unknown skill")

                proficiency = skill.get(
                    "proficiency",
                    "Not specified"
                )

                report.append(
                    f"- **{skill_name}** — {proficiency}"
                )

            else:
                report.append(f"- {skill}")

    else:
        report.append("- Not mentioned in resume.")

    report.append(
        "\n*Proficiency is shown only when explicitly identified "
        "in the resume. An unspecified level does not mean "
        "the candidate is a beginner.*"
    )

    # -----------------------------------------------------
    # Projects
    # -----------------------------------------------------

    report.append("\n## 3. Projects")

    if isinstance(projects, list) and projects:

        for index, project in enumerate(projects, start=1):

            if not isinstance(project, dict):
                report.append(f"\n### {index}. {project}")
                continue

            project_name = (
                project.get("name")
                or "Project name not identified"
            )

            report.append(
                f"\n### {index}. {project_name}"
            )

            descriptions = project.get("description", [])

            # Important correction:
            # Some resumes contain the complete project statement
            # in the project heading itself.
            # Do not incorrectly report that its description is missing.

            if not descriptions and project.get("name"):
                descriptions = [
                    project.get("name")
                ]

            report.append("**Description / Project statement:**")
            report.append(format_list(descriptions))

            technologies = project.get("technologies", [])

            report.append("\n**Technologies identified:**")
            report.append(format_list(technologies))

    else:
        report.append("- Not mentioned in resume.")

    # -----------------------------------------------------
    # Education
    # -----------------------------------------------------

    report.append("\n## 4. Education")

    education_entries = safe_get(
        education,
        "entries",
        []
    )

    report.append(
        format_list(education_entries)
    )

    score_evidence = safe_get(
        education,
        "cgpa_or_percentage_evidence",
        []
    )

    report.append("\n**CGPA / Percentage evidence:**")
    report.append(
        format_list(score_evidence)
    )

    # -----------------------------------------------------
    # Work Experience
    # -----------------------------------------------------

    report.append("\n## 5. Work Experience / Internships")

    experience_entries = safe_get(
        experience,
        "entries",
        []
    )

    report.append(
        format_list(experience_entries)
    )

    # -----------------------------------------------------
    # Certifications
    # -----------------------------------------------------

    report.append("\n## 6. Certifications")

    certification_entries = safe_get(
        certifications,
        "entries",
        []
    )

    report.append(
        format_list(certification_entries)
    )

    # -----------------------------------------------------
    # Achievements
    # -----------------------------------------------------

    report.append("\n## 7. Achievements and Awards")

    achievement_entries = safe_get(
        achievements,
        "entries",
        []
    )

    report.append(
        format_list(achievement_entries)
    )

    # -----------------------------------------------------
    # Resume Statistics
    # -----------------------------------------------------

    report.append("\n## 8. Resume Statistics")

    if isinstance(statistics, dict) and statistics:

        report.append(
            f"- **Total Words:** "
            f"{statistics.get('total_words', 0)}"
        )

        report.append(
            f"- **Total Characters:** "
            f"{statistics.get('total_characters', 0)}"
        )

        report.append(
            f"- **Total Lines:** "
            f"{statistics.get('total_lines', 0)}"
        )

    else:
        report.append("- Statistics are unavailable.")

    return "\n".join(report)


# ---------------------------------------------------------
# 6. AI Resume Improvement Suggestions
# ---------------------------------------------------------


def generate_resume_suggestions(resume_text, structured_resume):
    """
    Generates grounded resume improvement suggestions.

    Suggestions are created using extracted resume data
    instead of relying on unrestricted LLM-generated claims.

    This prevents fabricated metrics, achievements,
    project features, and qualifications.
    """

    if not isinstance(structured_resume, dict):
        structured_resume = {}

    contact = structured_resume.get("contact", {})
    skills = structured_resume.get("skills", [])
    projects = structured_resume.get("projects", [])
    education = structured_resume.get("education", {})
    experience = structured_resume.get("experience", {})
    certifications = structured_resume.get("certifications", {})
    achievements = structured_resume.get("achievements", {})

    suggestions = []

    # -----------------------------------------------------
    # Contact information
    # -----------------------------------------------------

    if not contact.get("emails"):
        suggestions.append(
            "Add a professional email address to your resume."
        )

    if not contact.get("phone_numbers"):
        suggestions.append(
            "Add a contact phone number if appropriate."
        )

    if not contact.get("linkedin_urls"):
        suggestions.append(
            "Consider adding your LinkedIn profile URL."
        )

    if not contact.get("github_urls"):
        suggestions.append(
            "If you have a GitHub profile containing relevant "
            "work, consider adding its URL."
        )

    # -----------------------------------------------------
    # Skills
    # -----------------------------------------------------

    if skills:

        unspecified = [
            skill.get("name")
            for skill in skills
            if isinstance(skill, dict)
            and skill.get("proficiency", "Not specified")
            == "Not specified"
        ]

        if unspecified:
            suggestions.append(
                "Where useful, specify your proficiency for "
                "relevant skills, but only if you can accurately "
                "justify the stated level."
            )

    else:
        suggestions.append(
            "Add a Technical Skills section listing your "
            "actual programming languages, tools, and technologies."
        )

    # -----------------------------------------------------
    # Projects
    # -----------------------------------------------------

    if not projects:
        suggestions.append(
            "Consider adding relevant academic or personal "
            "projects that you have actually completed."
        )

    else:
        for project in projects:

            if not isinstance(project, dict):
                continue

            description = project.get("description", [])

            project_name = (
                project.get("name")
                or "your project"
            )

            # A heading alone may not explain implementation details.
            if not description or len(description) <= 1:
                suggestions.append(
                    f"For '{project_name}', consider adding "
                    "genuine implementation details, your specific "
                    "contribution, and important features."
                )

            # Suggest genuine outcomes without inventing numbers.
            suggestions.append(
                f"For '{project_name}', include actual results "
                "or measurable outcomes if you have reliable "
                "evidence for them."
            )

    # -----------------------------------------------------
    # Education
    # -----------------------------------------------------

    education_entries = education.get("entries", [])

    score_evidence = education.get(
        "cgpa_or_percentage_evidence",
        []
    )

    if education_entries and not score_evidence:
        suggestions.append(
            "Consider including your CGPA or percentage "
            "if it is relevant and you want to disclose it."
        )

    if not education_entries:
        suggestions.append(
            "Add your educational qualifications, institution, "
            "degree, and study dates."
        )

    # -----------------------------------------------------
    # Work experience
    # -----------------------------------------------------

    experience_entries = experience.get("entries", [])

    if not experience_entries:
        suggestions.append(
            "If you have completed internships, employment, "
            "or relevant practical experience, consider adding "
            "those details. Do not add experience you do not have."
        )
    else:
        suggestions.append(
            "For each experience entry, clearly describe your "
            "actual responsibilities and contributions."
        )

    # -----------------------------------------------------
    # Certifications
    # -----------------------------------------------------

    certification_entries = certifications.get("entries", [])

    if not certification_entries:
        suggestions.append(
            "If you have earned relevant certifications, "
            "consider listing their names and issuing providers."
        )

    # -----------------------------------------------------
    # Achievements
    # -----------------------------------------------------

    achievement_entries = achievements.get("entries", [])

    if not achievement_entries:
        suggestions.append(
            "If applicable, include genuine awards, coding "
            "achievements, competition results, or other "
            "recognition."
        )

    # -----------------------------------------------------
    # Final output
    # -----------------------------------------------------

    if not suggestions:
        suggestions.append(
            "Your extracted resume sections contain useful "
            "information. Review formatting, consistency, "
            "and relevance to your target role."
        )

    report = ["### Improvement Suggestions", ""]

    for suggestion in suggestions:
        report.append(f"- {suggestion}")

    return "\n".join(report)



# ---------------------------------------------------------
# 7. Main Resume Agent
# ---------------------------------------------------------

def analyze_resume(resume_text, user_request):
    """
    Main entry point for the Resume Agent.

    Workflow:
    1. Validate resume input.
    2. Handle exact statistics questions using Python.
    3. Select and execute existing tools.
    4. Extract structured resume information.
    5. Generate a factual report using Python.
    6. Generate separate AI improvement suggestions.
    """

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if not resume_text or not resume_text.strip():
        return "Please provide resume text."

    if not user_request:
        user_request = "Analyze my complete resume."

    request = user_request.lower()

    print("\nUser Request:", user_request)

    # -----------------------------------------------------
    # Exact numerical statistics using Python
    # -----------------------------------------------------

    asks_for_count = any(
        phrase in request
        for phrase in [
            "count",
            "how many",
            "number of",
            "total"
        ]
    )

    asks_for_statistics = any(
        word in request
        for word in [
            "word",
            "line",
            "character",
            "statistic"
        ]
    )

    if asks_for_count and asks_for_statistics:

        stats = get_resume_statistics(resume_text)

        return (
            "### Resume Statistics\n\n"
            f"- **Total Words:** {stats['total_words']}\n"
            f"- **Total Characters:** "
            f"{stats['total_characters']}\n"
            f"- **Total Lines:** {stats['total_lines']}"
        )

    # -----------------------------------------------------
    # Select tools
    # -----------------------------------------------------

    selected_tools = select_tools(user_request)

    print("\nSelected Tools:", selected_tools)

    # -----------------------------------------------------
    # Execute selected tools
    # -----------------------------------------------------

    execute_tools(
        resume_text,
        selected_tools
    )

    print("\nExisting Tool Execution Completed!")

    # -----------------------------------------------------
    # Structured resume extraction
    # -----------------------------------------------------

    try:

        structured_resume = extract_structured_resume(
            resume_text
        )

        if not isinstance(structured_resume, dict):
            raise ValueError(
                "Structured extraction returned invalid data."
            )

    except Exception as error:

        print(f"\nStructured extraction error: {error}")

        return (
            "Resume analysis could not be completed because "
            "the resume extraction process failed. "
            "Please check the resume text and try again."
        )

    print("\nStructured Resume Extraction Completed!")

    # -----------------------------------------------------
    # Generate factual report
    # -----------------------------------------------------

    factual_report = build_factual_report(
        structured_resume
    )

    print("\nFactual Resume Report Generated!")

    # -----------------------------------------------------
    # Generate AI suggestions separately
    # -----------------------------------------------------

    print("\nGenerating AI Improvement Suggestions...")

    suggestions = generate_resume_suggestions(
        resume_text,
        structured_resume
    )

    print("\nResume Analysis Completed!")

    # -----------------------------------------------------
    # Final output
    # -----------------------------------------------------

    return (
        factual_report
        + "\n\n---\n\n"
        + suggestions
    )


# ---------------------------------------------------------
# 8. Testing
# ---------------------------------------------------------

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

    request = "Analyze my complete resume."

    print("\n===== AI CAREER AGENT: RESUME AGENT =====")

    result = analyze_resume(
        sample_resume,
        request
    )

    print("\n===== FINAL RESULT =====")
    print(result)
