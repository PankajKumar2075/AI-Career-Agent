
from backend.app.services.roadmap_service import generate_learning_roadmap

skill_gaps = {
    "Python": {
        "current_level": 6,
        "required_level": 9,
        "gap": 3
    },
    "SQL": {
        "current_level": 7,
        "required_level": 7,
        "gap": 0
    },
    "Machine_Learning": {
        "current_level": 4,
        "required_level": 9,
        "gap": 5
    }
}

result = generate_learning_roadmap(skill_gaps)

print("Total Weeks:", result["total_weeks"])

for item in result["roadmap"]:
    print("\nWeek:", item["week"])
    print("Skill:", item["skill"])
    print("Topics:", item["topics"])
    print("Task:", item["task"])
