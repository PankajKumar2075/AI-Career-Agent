SKILL_ROADMAP = {

    "Python": {
        "topics": [
            "Python fundamentals, data types, and control flow",
            "Functions, OOP, error handling, and data structures",
            "NumPy, Pandas, and data manipulation",
            "Working with real-world datasets"
        ],
        "weekly_tasks": [
            "Solve Python programming problems using functions and data structures",
            "Clean and analyze a dataset using Pandas and NumPy",
            "Practice data manipulation and write reusable Python code"
        ],
        "project": "Build a complete exploratory data analysis project using Python"
    },

    "SQL": {
        "topics": [
            "SQL fundamentals, SELECT, WHERE, and sorting",
            "Joins, grouping, and aggregate functions",
            "Subqueries, CTEs, and window functions",
            "Query optimization and practical database analysis"
        ],
        "weekly_tasks": [
            "Write SQL queries to filter and retrieve data",
            "Solve practical problems using joins and aggregate functions",
            "Practice complex SQL queries on a sample database"
        ],
        "project": "Build a database analysis project using SQL"
    },

    "Machine_Learning": {
        "topics": [
            "Python for Machine Learning, NumPy, and Pandas",
            "Statistics, probability, and linear algebra fundamentals",
            "Supervised learning: regression and classification",
            "Decision Trees, Random Forest, and Support Vector Machines",
            "Unsupervised learning: K-Means and clustering",
            "Model evaluation, cross-validation, and hyperparameter tuning",
            "Feature engineering and model optimization",
            "Deploying and using machine learning models through APIs"
        ],
        "weekly_tasks": [
            "Implement basic ML algorithms using scikit-learn",
            "Train and compare classification and regression models",
            "Evaluate models using cross-validation and appropriate metrics"
        ],
        "project": "Build and deploy an end-to-end machine learning project"
    },

    "React": {
        "topics": [
            "React components, JSX, and props",
            "State, events, and React hooks",
            "API integration and routing",
            "Reusable components and frontend architecture"
        ],
        "weekly_tasks": [
            "Build reusable React components",
            "Create interactive pages using hooks and state",
            "Connect a React application to backend APIs"
        ],
        "project": "Build a responsive React application with API integration"
    },

    "Node": {
        "topics": [
            "Node.js fundamentals and asynchronous JavaScript",
            "Express.js and REST API development",
            "Middleware, authentication, and authorization",
            "API validation, error handling, and backend architecture"
        ],
        "weekly_tasks": [
            "Build basic backend services using Node.js",
            "Create REST APIs using Express.js",
            "Implement authentication and API validation"
        ],
        "project": "Build a secure REST API using Node.js and Express"
    },

    "MongoDB": {
        "topics": [
            "MongoDB fundamentals and document structure",
            "CRUD operations and query operators",
            "Schema design and data relationships",
            "Aggregation pipeline and indexing"
        ],
        "weekly_tasks": [
            "Practice MongoDB CRUD operations",
            "Design collections for a practical application",
            "Use aggregation and indexing to query data efficiently"
        ],
        "project": "Design and implement a MongoDB database for a full-stack application"
    },

    "Excel": {
        "topics": [
            "Excel formulas and functions",
            "Sorting, filtering, and data cleaning",
            "Pivot tables and charts",
            "Dashboard creation and data visualization"
        ],
        "weekly_tasks": [
            "Practice formulas and spreadsheet functions",
            "Clean and summarize a dataset",
            "Create charts and an interactive dashboard"
        ],
        "project": "Build a data analysis dashboard using Excel"
    }
}


def generate_learning_roadmap(skill_gaps):

    roadmap = []

    # Keep only skills that need improvement.
    missing_skills = []

    for skill, details in skill_gaps.items():

        gap = details["gap"]

        if gap > 0 and skill in SKILL_ROADMAP:
            missing_skills.append({
                "skill": skill,
                "gap": gap
            })

    # Prioritize skills with the largest gaps.
    missing_skills.sort(
        key=lambda item: item["gap"],
        reverse=True
    )

    current_week = 1

    for item in missing_skills:

        skill = item["skill"]
        gap = item["gap"]

        skill_data = SKILL_ROADMAP[skill]

        topics = skill_data["topics"]
        weekly_tasks = skill_data["weekly_tasks"]

        # Larger gaps receive more learning time.
        if gap >= 5:
            duration = 3
        elif gap >= 3:
            duration = 2
        else:
            duration = 1

        # Divide topics across the allocated weeks.
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

            task = weekly_tasks[
                min(week, len(weekly_tasks) - 1)
            ]

            roadmap.append({
                "week": current_week,
                "skill": skill,
                "gap": gap,
                "topics": weekly_topics,
                "task": task
            })

            current_week += 1

        # Add a practical project after completing the skill.
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