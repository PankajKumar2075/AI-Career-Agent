
from backend.app.main import analyze_skill_gap, SkillGapRequest
from agents.learning_agent.learning_agent import create_learning_plan


def run_learning_workflow(student_data):
    """
    Complete workflow:
    Student Skills -> Skill Gap Analysis -> Learning Agent
    """

    # Step 1: Validate incoming student data
    student = SkillGapRequest(**student_data)

    # Step 2: Calculate actual skill gaps
    gap_result = analyze_skill_gap(student)

    skill_gaps = gap_result["skill_gaps"]
    target_career = gap_result["target_career"]

    # Step 3: Generate personalized learning plan
    learning_result = create_learning_plan(
        skill_gaps=skill_gaps,
        target_career=target_career
    )

    # Step 4: Return the combined result
    return {
        "target_career": target_career,
        "coverage_score": gap_result["coverage_score"],
        "skill_gaps": skill_gaps,
        "learning_plan": learning_result
    }


if __name__ == "__main__":

    # Sample student data for testing
    student_data = {
        "Python": 5,
        "SQL": 6,
        "Machine_Learning": 4,
        "React": 3,
        "Node": 2,
        "MongoDB": 4,
        "Excel": 5,
        "target_career": "ML Engineer"
    }

    result = run_learning_workflow(student_data)

    print("\n===== CAREER TO LEARNING WORKFLOW =====")
    print("Target Career:", result["target_career"])
    print("Coverage Score:", result["coverage_score"], "%")

    print("\n===== SKILL GAP ANALYSIS =====")

    for skill, details in result["skill_gaps"].items():
        print(
            f"{skill}: Current={details['current_level']}, "
            f"Required={details['required_level']}, "
            f"Gap={details['gap']}"
        )

    print("\n===== PERSONALIZED LEARNING PLAN =====")
    print("Total Weeks:", result["learning_plan"]["total_weeks"])

    for week in result["learning_plan"]["roadmap"]:
        print(f"\nWeek {week['week']} - {week['skill']}")
        print("Topics:", week["topics"])
        print("Task:", week["task"])

    print("\n===== AI LEARNING GUIDANCE =====")
    print(result["learning_plan"]["explanation"])
