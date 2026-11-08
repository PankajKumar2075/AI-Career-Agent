
from agents.learning_agent.learning_agent import create_learning_plan


# Sample skill gaps for testing only
skill_gaps = {
    "Python": {"gap": 4},
    "SQL": {"gap": 2},
    "Machine_Learning": {"gap": 5},
    "React": {"gap": 0},
    "Node": {"gap": 3},
    "MongoDB": {"gap": 2},
    "Excel": {"gap": 1}
}


print("===== LEARNING AGENT TEST =====")

result = create_learning_plan(
    skill_gaps,
    target_career="ML Engineer"
)

print("\n===== LEARNING ROADMAP =====")

print("Target Career:", result["target_career"])
print("Total Weeks:", result["total_weeks"])

for item in result["roadmap"]:

    print(f"\nWeek {item['week']}")
    print("Skill:", item["skill"])
    print("Skill Gap:", item["gap"])
    print("Topics:", item["topics"])
    print("Task:", item["task"])


print("\n===== AI LEARNING GUIDANCE =====")
print(result["explanation"])
