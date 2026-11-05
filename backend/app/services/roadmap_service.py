
SKILL_ROADMAP = {
    "Python": {
        "topics": [
            "Python fundamentals and data types",
            "Functions, loops, and data structures",
            "NumPy and Pandas",
            "Data analysis mini-project"
        ],
        "project": "Build a student performance analysis project"
    },
    "SQL": {
        "topics": [
            "SQL fundamentals and queries",
            "Filtering, sorting, and joins",
            "Group By and aggregate functions",
            "Subqueries and window functions"
        ],
        "project": "Build a student database analysis project"
    },
    "Machine_Learning": {
        "topics": [
            "Introduction to Machine Learning",
            "Linear and Logistic Regression",
            "Decision Trees, Random Forest, and SVM",
            "Model evaluation and cross-validation",
            "Feature engineering and model tuning",
            "End-to-end ML project"
        ],
        "project": "Build an ML model to predict student career suitability"
    },
    "React": {
        "topics": [
            "React components and JSX",
            "Props, state, and events",
            "Hooks and API integration",
            "Routing and reusable components"
        ],
        "project": "Build a React career dashboard"
    },
    "Node": {
        "topics": [
            "Node.js fundamentals",
            "Express.js and REST APIs",
            "Middleware and authentication",
            "API error handling and validation"
        ],
        "project": "Build a REST API using Node.js and Express"
    },
    "MongoDB": {
        "topics": [
            "MongoDB fundamentals",
            "CRUD operations",
            "Schema design and relationships",
            "Aggregation pipeline"
        ],
        "project": "Build a student career profile database"
    },
    "Excel": {
        "topics": [
            "Excel formulas and functions",
            "Sorting, filtering, and data cleaning",
            "Pivot tables and charts",
            "Dashboard creation"
        ],
        "project": "Build a student performance dashboard"
    }
}


def generate_learning_roadmap(skill_gaps):

    roadmap = []

    # Keep only skills that need improvement
    missing_skills = []

    for skill, details in skill_gaps.items():

        gap = details["gap"]

        if gap > 0:
            missing_skills.append({
                "skill": skill,
                "gap": gap
            })

    # Prioritize the skills with the largest gaps
    missing_skills.sort(
        key=lambda item: item["gap"],
        reverse=True
    )

    current_week = 1

    for item in missing_skills:

        skill = item["skill"]
        gap = item["gap"]

        if skill not in SKILL_ROADMAP:
            continue

        skill_data = SKILL_ROADMAP[skill]
        topics = skill_data["topics"]

        # Larger gaps receive more learning time
        if gap >= 5:
            duration = 3
        elif gap >= 3:
            duration = 2
        else:
            duration = 1

        # Divide topics across the allocated weeks
        topics_per_week = len(topics) // duration
        extra_topics = len(topics) % duration

        topic_index = 0

        for week in range(duration):

            count = topics_per_week

            if week < extra_topics:
                count += 1

            weekly_topics = topics[
                topic_index:topic_index + count
            ]

            topic_index += count

            roadmap.append({
                "week": current_week,
                "skill": skill,
                "gap": gap,
                "topics": weekly_topics,
                "task": f"Practice {skill} concepts covered this week"
            })

            current_week += 1

        # Add a project after completing this skill
        roadmap.append({
            "week": current_week,
            "skill": skill,
            "gap": gap,
            "topics": ["Practical project"],
            "task": skill_data["project"]
        })

        current_week += 1

    return {
        "total_weeks": current_week - 1,
        "roadmap": roadmap
    }
