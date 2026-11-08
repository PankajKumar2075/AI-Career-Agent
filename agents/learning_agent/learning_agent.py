
from backend.app.services.roadmap_service import generate_learning_roadmap
from generative_ai.ollama_service import generate_ai_response

import json


def create_learning_plan(skill_gaps, target_career=None):

    if not skill_gaps:
        return {
            "message": "No skill gap information provided.",
            "learning_plan": None
        }

    # Step 1: Generate the structured roadmap
    learning_plan = generate_learning_roadmap(skill_gaps)

    if not learning_plan["roadmap"]:
        return {
            "message": "No learning gaps found. Your skills meet the specified requirements.",
            "learning_plan": learning_plan
        }

    roadmap = learning_plan["roadmap"]
    total_weeks = learning_plan["total_weeks"]

    # Step 2: Extract skills in roadmap priority order
    skills = list(dict.fromkeys(
        week["skill"] for week in roadmap
    ))

    # Step 3: Ask AI for learning priorities and final advice only
    prompt = f"""
You are an expert AI Learning Mentor.

Target Career: {target_career}

Skills to learn, in priority order:
{json.dumps(skills)}

Generate two sections:

LEARNING PRIORITIES:
- Explain why each listed skill matters for the target career.
- Keep each explanation short.
- Do not introduce any additional skills.

FINAL ADVICE:
- Give exactly 3 practical tips for completing the learning roadmap.

Rules:
- Use only the skills provided.
- Do not invent projects, topics, or week numbers.
- Use simple and clear language.
- Keep the response under 150 words.
"""

    ai_guidance = generate_ai_response(prompt)

    # Step 4: Generate weekly study strategy using Python
    weekly_strategy = []

    for week in roadmap:

        week_number = week["week"]
        skill = week["skill"]
        topics = week["topics"]
        task = week["task"]

        week_text = f"Week {week_number} - {skill}\n"

        week_text += "Topics:\n"

        for topic in topics:
            week_text += f"- {topic}\n"

        week_text += f"Weekly Task: {task}\n"

        weekly_strategy.append(week_text)

    # Step 5: Extract projects directly from the roadmap
    projects = []

    for week in roadmap:

        task = week["task"]

        if task.lower().startswith("build"):
            projects.append(
                f"Week {week['week']} - {week['skill']}: {task}"
            )

    # Step 6: Assemble the final explanation
    explanation = f"""
LEARNING PRIORITIES AND FINAL ADVICE
{ai_guidance}

WEEKLY STUDY STRATEGY
Total Duration: {total_weeks} Weeks

{"".join(weekly_strategy)}

PROJECT GUIDANCE

"""

    if projects:
        for project in projects:
            explanation += f"- {project}\n"
    else:
        explanation += "No separate projects are included in this roadmap.\n"

    # Step 7: Return structured roadmap and explanation
    return {
        "target_career": target_career,
        "total_weeks": total_weeks,
        "roadmap": roadmap,
        "explanation": explanation.strip()
    }


if __name__ == "__main__":

    sample_gaps = {
        "Machine_Learning": {"gap": 5},
        "Python": {"gap": 4},
        "Node": {"gap": 3},
        "SQL": {"gap": 2},
        "MongoDB": {"gap": 2},
        "Excel": {"gap": 1},
        "React": {"gap": 0}
    }

    result = create_learning_plan(
        skill_gaps=sample_gaps,
        target_career="ML Engineer"
    )

    print("\n===== LEARNING AGENT TEST =====")

    print("\n===== AI LEARNING GUIDANCE =====")
    print(result["explanation"])

    print("\n===== TOTAL DURATION =====")
    print(result["total_weeks"], "weeks")
