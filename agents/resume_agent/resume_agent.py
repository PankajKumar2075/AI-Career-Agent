
import json

from generative_ai.ollama_service import generate_ai_response

from agents.resume_agent.resume_tools import (
    extract_skills,
    extract_projects,
    get_resume_statistics
)


# Available tools
AVAILABLE_TOOLS = {
    "extract_skills": extract_skills,
    "extract_projects": extract_projects,
    "get_resume_statistics": get_resume_statistics
}


# Step 1: Let the LLM decide which tools are required
def select_tools(user_request):

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

Return ONLY valid JSON in this format:
{{"tools": ["extract_skills"]}}

User request:
{user_request}
"""

    response = generate_ai_response(prompt)

    try:
        # Extract JSON if the model adds extra text
        start = response.find("{")
        end = response.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("Invalid planner response")

        data = json.loads(response[start:end])

        selected_tools = data.get("tools", [])

        # Validate tool names
        selected_tools = [
            tool for tool in selected_tools
            if tool in AVAILABLE_TOOLS
        ]

        if not selected_tools:
            raise ValueError("No valid tools selected")

        return selected_tools

    except (ValueError, json.JSONDecodeError, TypeError):
        print("Planner fallback: selecting all tools.")
        return list(AVAILABLE_TOOLS.keys())


# Step 2: Execute selected tools
def execute_tools(resume_text, selected_tools):

    results = {}

    for tool_name in selected_tools:

        tool_function = AVAILABLE_TOOLS[tool_name]

        results[tool_name] = tool_function(resume_text)

    return results


# Step 3: Main Resume Agent
def analyze_resume(resume_text, user_request):

    if not resume_text.strip():
        return "Please provide resume text."

    print("\nUser Request:", user_request)

    # Planning
    selected_tools = select_tools(user_request)

    print("\nSelected Tools:", selected_tools)

    # Tool execution
    tool_results = execute_tools(resume_text, selected_tools)

    print("\nTool Execution Completed!")

    # Final analysis
    prompt = f"""
You are an evidence-based Resume Analysis Agent.

User request:
{user_request}

Information extracted by your tools:
{json.dumps(tool_results, indent=2)}

Original resume:
{resume_text}

Instructions:
- Answer the user's request directly.
- Use only information supported by the resume.
- Do not invent qualifications or experience.
- Distinguish missing information from missing skills.
- Preserve the exact education wording from the resume.
- If information is unavailable, say so clearly.

Provide a clear and structured response.
"""

    return generate_ai_response(prompt)


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

    request = "Count the words and lines in my resume."

    print("\n===== AI CAREER AGENT: RESUME AGENT =====")

    result = analyze_resume(sample_resume, request)

    print("\n===== FINAL RESULT =====")
    print(result)
